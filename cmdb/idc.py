#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from forms import IdcForm
from .models import Idc


def idc(request):
    temp_name = "cmdb/cmdb-header.html"
    idc_info = Idc.objects.all()
    return render_to_response('cmdb/idc.html', locals())


def idc_add(request):
    temp_name = "cmdb/cmdb-header.html"
    if request.method == "POST":
        idc_form = IdcForm(request.POST)
        if idc_form.is_valid():
            idc_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render_to_response("cmdb/idc_add.html", locals())
    else:
        display_control = "none"
        idc_form = IdcForm()
        return render_to_response("cmdb/idc_add.html", locals())


def idc_add_mini(request):
    temp_name = "cmdb/cmdb-header.html"
    if request.method == "POST":
        idc_form = IdcForm(request.POST)
        if idc_form.is_valid():
            idc_form.save()
            tips = u"增加成功！"
            display_control = ""
        else:
            tips = u"增加失败！"
            display_control = ""
        return render_to_response("cmdb/idc_add_mini.html", locals())
    else:
        display_control = "none"
        idc_form = IdcForm()
        return render_to_response("cmdb/idc_add_mini.html", locals())


def idc_del(request):
    temp_name = "cmdb/cmdb-header.html"
    if request.method == 'POST':
        idc_items = request.POST.getlist('idc_check', [])
        if idc_items:
            for n in idc_items:
                Idc.objects.filter(id=n).delete()
    idc_info = Idc.objects.all()
    return render_to_response("cmdb/idc.html", locals())


def idc_edit(request):
    temp_name = "cmdb/cmdb-header.html"
    if request.method == 'GET':
        idcid = request.GET.get("idcid")
        obj = Idc.objects.get(id=idcid)
        allidc = Idc.objects.all()
    return render_to_response("cmdb/idc_edit.html", locals())


def idc_save(request):
    temp_name = "cmdb/cmdb-header.html"
    if request.method == 'POST':
        id = request.POST.get('id')
        name = request.POST.get('name')
        address = request.POST.get('address')
        tel = request.POST.get('tel')
        contact = request.POST.get('contact')
        contact_phone = request.POST.get('contact_phone')
        jigui = request.POST.get('jigui')
        bandwidth = request.POST.get('bandwidth')
        idc_item = Idc.objects.get(id=id)
        idc_item.name = name
        idc_item.address = address
        idc_item.tel = tel
        idc_item.contact = contact
        idc_item.contact_phone = contact_phone
        idc_item.jigui = jigui
        idc_item.bandwidth = bandwidth
        idc_item.save()
        obj = idc_item
    return render_to_response("cmdb/idc_edit.html",locals())