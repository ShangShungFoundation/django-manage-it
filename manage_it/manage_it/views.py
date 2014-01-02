# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from assets.models import Item, AssetRequest
from incidents.models import Incident, IncidentFollowup
from organizations.user_access import manager_required


@login_required
@manager_required
def dashboard(request, org_url):
    vars = dict(
        org_url=org_url,
        org=request.organization,
        asset_watched=Item.objects.filter(
            state__gt=1,
            inventory__organization__url__exact=org_url)[:10],
        asset_requested=AssetRequest.objects.filter(
            status__lt=3,
            organization__url__exact=org_url)[:10],
        incidents_watched=Incident.objects.filter(
            status__lt=3,
            organization__url__exact=org_url)[:10],
        incidents_followups=IncidentFollowup.objects.filter(
            incident__organization__url__exact=org_url)[:10]
    )

    return render(
        request,
        "dashboard.html",
        vars)
