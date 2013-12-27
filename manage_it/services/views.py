# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

from dataforms.forms import create_form, get_answers
from dataforms.models import DataForm
from models import Service, SLA

from organizations.user_access import staff_required, manager_required

from forms import SLAForm, DocumentFormSet

DATA_FORM_KEY = u"%s_%s"


@login_required
@staff_required
def list_services(request, *args, **kwargs):
    org = request.organization
    slas = SLA.objects.in_organization(org.slug)
    vars = dict(
        org=org,
        slas=slas,
    )

    return render(
        request,
        "services/list_services.html",
        vars)


@login_required
@staff_required
def view_service(request, object_id, *args, **kwargs):
    org = request.organization

    service = Service.objects.get(pk=object_id)
    #user_service = service.is_used_by(request.user)

    vars = dict(
        org=org,
        service=service,
    )

    return render(
        request,
        "services/view_service.html",
        vars)


def _create_properties_form(request, service_id, data_form_id):
    item_class = DataForm.objects.get(id=data_form_id)
    new_sku = DATA_FORM_KEY % (service_id, data_form_id)
    form = create_form(request, form=item_class.slug, submission=new_sku)
    vars = dict(
        form=form,
        id=service_id,
        item_class=item_class)
    return vars


@login_required
@manager_required
def sla_detail_form(request, service_id, data_form_id, *args, **kwargs):
    return render(
        request,
        "services/_sku_properties_form.html",
        _create_properties_form(request, service_id, data_form_id),
    )


@login_required
@manager_required
def add_sla(request, service_id, *args, **kwargs):
    property_forms = {}
    org = request.organization
    service = get_object_or_404(Service, pk=service_id)
    sla_form = SLAForm(request.POST or None)
    document_form = DocumentFormSet(
        request.POST or None,
        request.FILES or None,)

    if request.method == "POST":
        sla_poroperties_ids = sla_form.data.getlist('service_classes')

        property_forms_valid = []

        for sla_poroperty_id in sla_poroperties_ids:
            property_form = _create_properties_form(
                request, service_id, int(sla_poroperty_id))
            property_forms_valid.append(property_form["form"].is_valid())
            property_forms["form_%s" % sla_poroperty_id] = property_form

        if all(property_forms_valid) and sla_form.is_valid() and document_form.is_valid():
            # we save SLA properties
            for form_id in property_forms:
                property_forms[form_id]["form"].save()
            # we save SLA
            sla = sla_form.save(commit=False)
            sla.service_id = service_id
            sla.created_by = request.user
            sla.save()
            # we must save m2m too
            sla_form.save_m2m()
            #save documents
            documents = document_form.save(commit=False)
            for doc in documents:
                doc.SLA = sla
                doc.created_by = request.user
                doc.save()

            return redirect(sla)
    vars = dict(
        org=org,
        service=service,
        sla_form=sla_form,
        property_forms=property_forms,
        document_form=document_form,
    )
    return render(
        request,
        "services/new_sla.html",
        vars)


@login_required
@manager_required
def edit_sla(request, service_id, sla_id, *args, **kwargs):
    property_forms = {}
    org = request.organization
    service = get_object_or_404(Service, pk=service_id)
    sla = get_object_or_404(SLA, pk=sla_id)

    sla_form = SLAForm(request.POST or None, instance=sla)
    #import ipdb; ipdb.set_trace()

    if request.method == "POST":
        sla_poroperties_ids = sla_form.data.getlist('service_classes')
        document_form = DocumentFormSet(
            request.POST,
            request.FILES,
            instance=sla)

        property_forms_valid = []

        for sla_poroperty_id in sla_poroperties_ids:
            property_form = _create_properties_form(
                request, service_id, int(sla_poroperty_id))
            property_forms_valid.append(property_form["form"].is_valid())
            property_forms["form_%s" % sla_poroperty_id] = property_form

        if all(property_forms_valid) and sla_form.is_valid() and document_form.is_valid():
            # we save SLA properties
            for form_id in property_forms:
                property_forms[form_id]["form"].save()
            # we save SLA
            sla = sla_form.save(commit=False)
            #sla.modyfied_by = request.user
            sla.save()
            # we must save m2m too
            sla_form.save_m2m()
            #save documents
            documents = document_form.save(commit=False)
            for doc in documents:
                doc.SLA = sla
                doc.created_by = request.user
                doc.save()

            return redirect(sla)
    else:
        document_form = DocumentFormSet(instance=sla)
    vars = dict(
        org=org,
        service=service,
        sla_form=sla_form,
        property_forms=property_forms,
        document_form=document_form,
    )

    return render(
        request,
        "services/new_sla.html",
        vars)


@login_required
@staff_required
def sla_view(request, service_id, object_id, *args, **kwargs):

    service = get_object_or_404(Service, id=service_id)
    sku = get_object_or_404(SLA, id=object_id)
    org = request.organization

    sku_properties = []
    #import ipdb; ipdb.set_trace()
    for sku_prop in list(sku.service_classes.all()):
        properties = get_answers(DATA_FORM_KEY % (service_id, sku_prop.id))
        sku_properties.append(properties)

    vars = dict(
        org=org,
        service=service,
        sku=sku,
        sku_properties=sku_properties,
    )

    return render(
        request,
        "services/view_sla.html",
        vars)
