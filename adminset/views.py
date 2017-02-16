#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response,redirect

def index(request):
    temp_name = "main-header.html"
    return render_to_response("index.html", locals())