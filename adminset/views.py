#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import redirect


def index(request):
    return redirect('/navi/')