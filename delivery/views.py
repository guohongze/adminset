#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.views.generic.base import TemplateView
from django.shortcuts import render
from .models import Delivery


def index(request):
    temp_name = "delivery/delivery-header.html"
    projects = Delivery.objects.all()
    return render(request, "delivery/index.html", locals())
