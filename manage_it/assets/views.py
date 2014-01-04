# -*- coding: utf-8 -*-
import time
from markdown import markdown

import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse

from dataforms.forms import create_form, get_answers
from dataforms.models import DataForm, Submission

from assets.models import Item, AssetRequest
from assets.forms import ItemForm, ResourcesSet, AssetRequestForm

from incidents.forms import NewIncidentForm
from organizations.user_access import staff_required


def _out_dict(it):
    return dict(
        pk=it.pk,
        sku=it.property_number,
        function=markdown(it.function),
        description=markdown(it.description or ""),
        active=it.active,
        state=it.state_id,
        state_name=it.state.name,
        item_template=it.item_template.description,
        item_class=it.item_class_id,
        item_class__description=markdown(it.item_class.description),
        item_class__title=it.item_class.title,
        item_class__slug=it.item_class.slug,
        location=it.location_id,
        location__name=it.location.name,
        owner=it.owner_id,
        owner__last_name=it.owner.last_name,
        owner__first_name=it.owner.first_name,
        users=[[u.id, u.first_name, u.last_name] for u in it.users.all()],
    )


def categories(request, org_url):

    categories = list(DataForm.objects.all().select_related("location"))
    return render(
        request,
        "assets/categories.html",
        dict(
            categories=categories,
            org_url=org_url,
            org=request.organization,
        ),
    )


@login_required
@staff_required
def get(request, org_url,  slug):
    vars = dict(
        item=Item.objects.get(property_number=slug),
        data=get_answers(slug),
        new_incident_form=NewIncidentForm(),
        org_url=org_url,
        org=request.organization,
    )
    return render(
        request,
        "assets/asset.html",
        vars,
    )


@login_required
@staff_required
def get_json(request, org_url, slug):

    it = Item.objects.select_related(
        "item_template", "item_class", "users",
        "owner", "state").get(property_number=slug)

    data = _out_dict(it)
    data["properties"] = get_answers(slug)
    out = json.dumps([data])
    return HttpResponse(out, mimetype='application/json')


@login_required
@staff_required
def add(request, org_url, slug):

    # generqating SKU
    timestamp = int(time.time())
    item_class = DataForm.objects.get(id=slug)
    new_sku = u"%s%s" % (item_class.slug, timestamp)

    # initialize forms
    detail_form = create_form(request, form=item_class.slug, submission=new_sku)
    form = ItemForm(request.POST or None)
    # limit invetories to the organization
    form.fields["inventory"].queryset = form.fields["inventory"].queryset.filter(organization__url__exact=org_url)
    #form.fields["users"].queryset= form.fields["users"].queryset.filter(group__url__exact=org_url)

    resource_form = ResourcesSet(request.POST or None, request.FILES or None)
    #initalize variables
    vars = {"item_class": item_class}
    msgs = []

    # handle forms
    if request.method == "POST":
        if form.is_valid() and detail_form.is_valid():
            detail_saved = detail_form.save()
            form_saved = form.save(commit=False)
            form_saved.item_class = item_class
            form_saved.property_number = new_sku
            form_saved.save()
            msgs.append("item saved id: %s" % detail_saved.slug)
            #return redirect(...)

    # preprae vars for render
    vars["resource_form"] = resource_form
    vars["detail_form"] = detail_form
    vars["form"] = form
    vars["msgs"] = msgs
    vars["org_url"] = org_url
    vars["org"] = request.organization
    return render(
        request,
        "assets/asset_form.html",
        vars,
    )


@login_required
@staff_required
def edit(request, org_url, slug):
    instance = get_object_or_404(Item, property_number=slug)
    submission = Submission.objects.get(slug=slug)

    form = ItemForm(request.POST or None, instance=instance)
    detail_form = create_form(
        request,
        form=instance.item_class,
        submission=submission)
    resource_form = ResourcesSet(request.POST or None, request.FILES or None)

    msgs = []
    if request.method == "POST" and form.is_valid() and detail_form.is_valid() and resource_form.is_valid():
        form.save()
        detail_saved = detail_form.save()
        # TODO save resources
        #resource_form.save(commit=False)
        #resource.item_id = instance.id
        msg = "item SKU: %s updated" % detail_saved.slug
        messages.success(request, msg)
        #msgs.append()

    vars = dict(
        item=instance,
        detail_form=detail_form,
        resource_form=resource_form,
        form=form,
        msgs=msgs,
        org=request.organization,
        org_url=org_url,
    )
    return render(
        request,
        "assets/asset_edit_form.html",
        vars,
    )


@login_required
@staff_required
def delete(request, org_url, slug):
    instance = get_object_or_404(Item, property_number=slug)
    instance.delete()
    msg = "asset %s has been deleted" % instance.property_number
    messages.success(request, msg)
    return redirect('catalog')


@login_required
@staff_required
def new_asset_request(request, org_url,):
    asset_request_form = AssetRequestForm(request.POST or None)
    if request.method == "POST" and asset_request_form.is_valid():
        asset_request = asset_request_form.save(commit=False)
        asset_request.created_by = request.user
        asset_request.status = 1  # open
        asset_request.save()
        msg = "asset request #%s has been submited sucesfully" % asset_request.pk
        messages.success(request, msg)
        return redirect('catalog')

    return render(
        request,
        "assets/asset_request_form.html",
        dict(
            asset_request_form=asset_request_form,
            org=request.organization,
            org_url=org_url,
        ),
    )


@login_required
@staff_required
def asset_request(request, org_url, object_id):
    asset_request = get_object_or_404(AssetRequest, id=object_id)
    return render(
        request,
        "assets/asset_request.html",
        dict(
            asset_request=asset_request,
            org=request.organization,
            org_url=org_url,
        ),
    )
