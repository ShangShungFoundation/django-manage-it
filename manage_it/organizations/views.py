from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from user_access import staff_required
from forms import GroupForm, OrganizationForm, UserForm, EditUserForm
from models import Organization, OrganizationGroup

from django.conf import settings


@login_required
@staff_required
def new_user(request, org_url):
    organization = request.organization
    form = UserForm(request.POST or None)
    #import ipdb; ipdb.set_trace()
    form.fields["groups"].queryset = organization.get_groups()
    if form.is_valid():
        new_user = form.save()
        # add to the staff group
        staff_group = organization.staff_group
        staff_group.user_set.add(new_user)
        return redirect(
            "set_organization_group", [org_url, "staff_group"]
        )
    return render(
        request,
        "organizations/user_new.html",
        dict(
            form=form,
            org=organization,
            org_url=org_url,
        )
    )


@login_required
@staff_required
def edit_user(request, org_url, user_id):
    organization = request.organization
    user = settings.AUTH_USER_MODEL.objects.get(id=user_id)
    form = EditUserForm(request.POST or None, instance=user)

    if form.is_valid():
        form.save()
        return redirect(
            "set_organization_group", [org_url, "staff_group"]
        )

    return render(
        request,
        "organizations/user_new.html",
        dict(
            form=form,
            org=organization,
            org_url=org_url,
        )
    )


@login_required
@staff_required
def view_user(request, org_url, user_id):
    organization = request.organization
    user = settings.AUTH_USER_MODEL.objects.get(id=user_id)
    return render(
        request,
        "organizations/user_view.html",
        dict(
            org=organization,
            org_url=org_url,
            usr=user,
        )
    )


def list_organizations(request):
    organizations = Organization.objects.filter(parent__isnull=True)
    return render(
        request,
        "organizations/list.html",
        dict(orgs=organizations),
    )


@login_required
@staff_required
def view_organization(request, org_url):

    organization = request.organization
    sub_organizations = Organization.objects.filter(parent__exact=organization)

    return render(
        request,
        "organizations/view.html",
        dict(
            org=organization,
            suborgs=sub_organizations,
            org_url=org_url)
    )


@login_required
@staff_required
def new_organization(request, org_url):

    organization = request.organization
    form = OrganizationForm(request.POST or None)
    # get only organizations
    form.fields["parent"].queryset = form.fields["parent"].queryset.filter(
        url__startswith=organization.head.url)

    if form.is_valid():
        new_organization = form.save(commit=False)
        # get or create staff group
        staff_group_name = u"%s staff" % organization.name
        staff_group = Group.objects.get_or_create(name=staff_group_name)
        #associate group with organization
        new_organization.staff_group = staff_group
        new_organization.save()
        #associate group with organization groups
        organization_group_staff = OrganizationGroup.objects.create(
            org=organization,
            group=staff_group,
            role=1)
        organization_group_staff.save()

        return redirect(
            "set_organization_group" [new_organization.url, "staff_group"]
        )

    return render(
        request,
        "organizations/new.html",
        dict(
            form=form,
            org=organization,
            org_url=org_url
        ),
    )


@login_required
@staff_required
def set_organization_group(request, org_url, group_role=""):
    organization = request.organization
    #get or create revelant organization group
    try:
        organizationgroup = OrganizationGroup.objects.filter(
            role__exact=group_role,
            org=organization)[0]
    except IndexError:
        organizationgroup = None

    if not organizationgroup:
        role_name = dict(OrganizationGroup.GROUP_ROLES)[group_role]
        group_name = u"%s %s" % (organization.name, role_name)
        group = Group.objects.get_or_create(name=group_name)
        organizationgroup = OrganizationGroup.objects.create(
            role=group_role,
            group=group[0],
            org=organization)

    form = GroupForm(
        request.POST or None,
        instance=organizationgroup.group)
    form.fields["users"].queryset = organization.staff_group.user_set.all()

    if form.is_valid():
        group = form.save()
        # store reference to group in organization
        setattr(organization, group_role, group)
        organization.save()
        return redirect("organization", (org_url,))

    return render(
        request,
        "organizations/edit_group.html",
        dict(
            form=form,
            org=organization,
            group=organizationgroup.group,
            group_types=organizationgroup.GROUP_ROLES,
            org_url=org_url
        ),
    )
