#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import HttpResponseRedirect, reverse


def index(request):
    return HttpResponseRedirect(reverse('navi'))
