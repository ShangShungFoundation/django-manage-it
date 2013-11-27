# -*- coding: utf-8 -*-
import time

from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.utils import simplejson
from django.core import serializers

from dataforms.forms import create_form, get_answers
from dataforms.models import DataForm, Submission

from models import Connection


def get(request):

    conections = list(Connection.objects.select_related("device_1", "device_2").all())
    return render(request,
            "network/view.html",
            {"conections": conections},
    )

def connections(request):
    
    conections = list(Connection.objects.select_related("device_1", "device_2").all())
    data = serializers.serialize("json", conections)
    out = "var connections=%s;" % data
    return HttpResponse(out, mimetype='application/json')

