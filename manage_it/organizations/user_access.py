import logging
from functools import wraps

from django.shortcuts import redirect
from django.utils.decorators import available_attrs

from models import Organization, OrganizationGroup

logger = logging.getLogger('django.request')

from settings import REDIRECT_URL, SUPERIOR_GROUPS


#https://github.com/django/django/blob/master/django/views/decorators/http.py#L31

def get_user_groups(org, usr):
    user_groups = OrganizationGroup.objects.filter(
        org=org,
        group__user=usr)
    return user_groups


def get_user_groups_in_org(org, usr):
    """get all user groups in organization herarchy"""
    user_groups = OrganizationGroup.objects.filter(
        org__url__startswith=org.get_head_url(org.url),
        group__user=usr)
    return user_groups


def get_user_manager_roles_in_org(org, usr):
    """get all user groups in organization herarchy"""
    user_groups = get_user_groups_in_org(org, usr)
    user_manager_roles = user_groups.filer(role="admin_group")
    return user_manager_roles


def get_superior_groups(organization_groups, org):
    superior_groups = dict([g, []] for g in SUPERIOR_GROUPS)
    for org_group in organization_groups:
        if not org_group.org.url.startswith(org.url) and org_group.role in SUPERIOR_GROUPS:
            superior_groups[org_group.role].append(org_group.org)
    return superior_groups


def get_user_roles(org, usr):
    user_groups = get_user_groups_in_org(org, usr)
    user_roles_in_org = user_groups.filter(
        org__exact=org).values_list("role", flat=True)
    superior_user_groups = get_superior_groups(
        user_groups, org)
    return user_roles_in_org, superior_user_groups


def required_member(parameter=None):
    """
    Possible paramenters are defined by roles groups slugs \
    in OrganizationGroup.
    """

    def decorator(view_func):

        @wraps(view_func, assigned=available_attrs(view_func))
        def inner(request, *args, **kwargs):
            if 'org_url' in kwargs:
                org_url = kwargs["org_url"]
            else:
                org_url = request.path.split("/")[1]
            try:
                request.organization = Organization.objects.get(url=org_url)
            except:
                return redirect(REDIRECT_URL)

            request.user.roles, superior_groups = get_user_roles(
                request.organization,
                request.user)
            #assing superior groups to user
            for group in SUPERIOR_GROUPS:
                setattr(
                    request.user,
                    "super_%s" % group,
                    superior_groups.get(group, []))

            # free ride for superuser
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            # let pass user belonging to any group in org
            if request.user.roles and not parameter:
                return view_func(request, *args, **kwargs)
            # let go user belonging to particular group
            if request.user.roles and parameter in request.user.roles:
                return view_func(request, *args, **kwargs)
            return redirect(REDIRECT_URL)
        return inner
    return decorator

manager_required = required_member("admin_group")
manager_required.__doc__ = """Decorator to require that a view \
only accept members belonging to organization maneger group"""

staff_required = required_member("staff_group")
staff_required.__doc__ = "Decorator to require that a view only \
accept members belonging to organization"

acountant_required = required_member("accounting_group")
acountant_required.__doc__ = "Decorator to require that a view \
only accept members belonging to organization acounting group"
