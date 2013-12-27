# -*- coding: utf-8 -*-
import datetime
import xlwt

from django.shortcuts import render
from django.http import HttpResponse
from django.utils import simplejson

from dataforms.forms import get_answers

from assets.models import Item
from assets.forms import ItemSearchFormSet
from assets.views import _out_dict

from lib.search_form import search as search_form
from organizations.models import Organization

from models import Inventory


def get(request, org_url, inventory_id):

    vars = search_form(
        request,
        ItemSearchFormSet,
        Item.objects.select_related(
            "item_template", "location").filter(inventory_id=inventory_id)
    )
    vars["org_url"] = org_url

    return render(
        request,
        "catalog/get.html",
        vars,
    )


def list(request, org_url):
    organization = Organization.objects.get(url=org_url)
    inventories = Inventory.objects.filter(organization__url__exact=org_url)

    return render(
        request,
        "catalog/list.html",
        dict(
            inventories=inventories,
            org_url=org_url,
            organization=organization,
        ),
    )


def export_xsl(request, org_url):
    results = search_form(
        request,
        ItemSearchFormSet,
        Item.objects.select_related("item_template")
    )

    font0 = xlwt.Font()
    font0.name = 'Arial'
    font0.bold = True

    style0 = xlwt.XFStyle()
    style0.font = font0

    font1 = xlwt.Font()
    font1.name = 'Arial'

    style1 = xlwt.XFStyle()
    style1.font = font1

    style1 = xlwt.XFStyle()
    style1.num_format_str = 'D-MMM-YY'

    wb = xlwt.Workbook()
    ws = wb.add_sheet('0')

    items = results["queryset"]

    # making headers
    column_names = [
        "SKU", "serial number", "location",
        "owner", "active", "state", "function",
        "description", "brand", "model", "notes"]

    if results["query"] and items:
        # import ipdb; ipdb.set_trace()
        # get properties from the last item
        extra_column_names = get_answers(
            items.reverse()[0].property_number).keys()

    for i, name in enumerate(column_names):
        ws.write(0, i, name, style1)

    # writing values 
    for j, item in enumerate(items):
        i = j + 1
        #import ipdb; ipdb.set_trace()
        values = [
            item.property_number,
            item.serial_number,
            item.location.name,
            item.owner.__unicode__(),
            item.active,
            item.state.__unicode__(),
            item.function,
            item.description,
            item.item_template.brand,
            item.item_template.model,
            item.item_template.notes,
        ]

        if results["query"]:
            extra_values = []
            extra_properties = get_answers(item.property_number)
            for name in extra_column_names:
                value = extra_properties.get(name, "")
                extra_values.append(value)
            values = values + extra_values

        for z, val in enumerate(values):
            ws.write(i, z, val, style1)

    date = datetime.datetime.now()

    query_to_remove = [
        u"item_set-TOTAL_FORMS", u"item_set-MAX_NUM_FORMS",
        u"item_set-INITIAL_FORMS"]
    query_str = "_".join(
        ["%s-%s" % (prop[0], prop[1])
        for prop in request.GET.items()
        if prop[1] != "0" or  prop[0] not in query_to_remove]
        )

    name = "inventory_%s%s.xls" % (date.strftime("%d-%m-%Y"), query_str)
    wb.save(name)
    return xls_to_response(wb, name)


def xls_to_response(xls, fname):
    response = HttpResponse(mimetype="application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=%s' % fname
    xls.save(response)
    return response


def list_json(request):

    items = Item.objects.select_related(
        "item_template", "item_class", "users", "owner", "state").all()

    out = []
    for it in items:
        out.append(_out_dict(it))

    #items = (Item.objects.values("id", "notes", "active", "state", "property_number", "item_template_id", "item_template__description", "item_class__title", "item_class__slug", "item_class_id", "location__name", "owner__last_name", "owner__first_name")[5:7])

    #data = serializers.serialize("json", items)

    out = "var nodes=%s;" % simplejson.dumps(out)
    return HttpResponse(out, mimetype='application/json')
