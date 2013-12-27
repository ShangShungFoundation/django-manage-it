# -*- coding: utf-8 -*-
from django.shortcuts import render

from assets.models import Item, AssetRequest
from incidents.models import Incident, IncidentFollowup


def dashboard(request):

    #import ipdb; ipdb.set_trace()
    vars = dict(
        asset_watched=Item.objects.filter(state__gt=1)[:10],
        asset_requested=AssetRequest.objects.filter(status__lt=3)[:10],
        incidents_watched=Incident.objects.filter(status__lt=3)[:10],
        incidents_followups=IncidentFollowup.objects.all()[:10]
    )

    return render(
        request,
        "index.html",
        vars)
