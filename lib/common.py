#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from config.views import get_dir
import json


def token_verify():

    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            iToken = get_dir('token')
            error_info = "Post forbidden, your token error!!"
            if request.method == 'POST':
                # pToken = request.POST.get('token')
                pToken = json.loads(request.body)
                if iToken == pToken["token"]:
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponse(error_info, status=403)
            if request.GET:
                pToken = request.GET['token']
                if iToken == pToken:
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponse(error_info, status=403)
            return HttpResponse(error_info, status=403)

        return _wrapped_view

    return decorator
