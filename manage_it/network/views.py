# -*- coding: utf-8 -*-
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers

from models import Connection
from scan import scan

NMAP_RAPORT_PATH = "/home/kamil/nmap/"


def get(request):

    conections = list(
        Connection.objects.select_related("device_1", "device_2").all())
    return render(
        request,
        "network/view.html",
        {"conections": conections})


def connections(request):

    connections = list(
        Connection.objects.select_related("device_1", "device_2").all())

    #devices_ips = Answer.objects.filter(field=1).values_list("submission__slug", "value")

    #import ipdb; ipdb.set_trace()

    connections_json = serializers.serialize("json", connections)
    #devices_ips_json = simplejson.dumps(dict(devices_ips))

    out = """var connections=%s;""" % connections_json
    return HttpResponse(out, mimetype='application/json')


def scan_network(request, network_id):
    #network = Network.objects.get(id=network_id)
    file_path = '%s/last.xml' % NMAP_RAPORT_PATH
    raport = scan(file_path)
    #connections = list(
        #Connection.objects.select_related("device_1", "device_2").all())
    data = json.dumps(raport)
    out = "var nmap_raport=%s;" % data
    return HttpResponse(out, mimetype='application/json')
