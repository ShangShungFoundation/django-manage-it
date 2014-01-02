# -*- coding: utf-8 -*-
from django.utils import simplejson
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from organizations.models import Organization
from organizations.user_access import staff_required

from models import Incident, IncidentFollowup
from forms import (
    NewIncidentForm,
    IncidentFollowupFormAdmin,
    IncidentFollowupForm)


@login_required
@staff_required
def get(request, org_url, object_id):

    incident = get_object_or_404(Incident, id=object_id)
    #organization = get_object_or_404(Organization, url=org_url)

    if request.user.is_staff:
        incident_followup_form = IncidentFollowupFormAdmin(
            request.POST or None,
            instance=incident)
    else:
        incident_followup_form = IncidentFollowupForm(
            request.POST or None,
            initial={"incident": incident})

    if request.method == "POST" and incident_followup_form.is_valid():
        incident = incident_followup_form.save(commit=True)
        #incident.incident_id = object_id
        incident.save()

        followup = IncidentFollowup(
            incident=incident,
            observations=incident_followup_form.cleaned_data["observations"],
            created_by=request.user,
            status_change=simplejson.dumps(incident.diff))
        followup.save()
        messages.success(request, "follow up has been sumited")

    return render(
        request,
        "incidents/get.html",
        dict(
            incident=incident,
            new_incident_followup_form=incident_followup_form,
            org_url=org_url,
            org=request.organization,
        ),
    )


@login_required
@staff_required
def list(request, org_url):
    new_incident_form = NewIncidentForm(request.POST or None, )
    organization = get_object_or_404(Organization, url=org_url)
    vars = dict(
        incidents=Incident.objects.all(),
        new_incident_form=new_incident_form,
        org_url=org_url,
        org=organization,
    )

    return render(
        request,
        "incidents/list.html",
        vars)


@login_required
@staff_required
def new(request, org_url):
    msgs = []

    organization = request.organization
    new_incident_form = NewIncidentForm(request.POST or None)

    if new_incident_form.is_valid():
        incident = new_incident_form.save(commit=False)
        incident.submited_by = request.user
        incident.organization = organization
        incident.save()

        messages.success(request, "incident has been sumited")
        return redirect('incidents', organization.url)

    vars = {
        "msgs": msgs,
        "new_incident_form": new_incident_form,
        "org_url": org_url,
        "org": organization,
    }

    return render(request, "incidents/new.html", vars)


@login_required
@staff_required
def new_followup(request, org_url, object_id):

    vars = {}
    incident = get_object_or_404(Incident, id=object_id)

    if request.user.is_staff:
        incident_followup_form = IncidentFollowupFormAdmin(
            request.POST or None, incident)
    else:
        incident_followup_form = IncidentFollowupForm(request.POST or None)
    if incident_followup_form.is_valid():
        followup = incident_followup_form.save(commit=False)
        #followup.incident_id = int(object_id)
        #followup.created_by = request.user
        followup.save()

        messages.success(request, "followup has been sumited")
        return redirect('incident', object_id)

    vars["new_incident_followup_form"] = incident_followup_form
    return render(request, "incidents/get.html", vars)
