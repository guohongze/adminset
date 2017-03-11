#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response,redirect
from accounts.permission import permission_verify
from django.contrib.auth.decorators import login_required


def index(request):
    return redirect('/navi/')