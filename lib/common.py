#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from config.views import get_dir


def token_verify():

    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            iToken = get_dir('token')
            if request.POST:
                pToken = request.POST.get('token')
                if iToken == pToken:
                    return view_func(request, *args, **kwargs)
                else:
                    message = "forbidden your token error!!"
                    print message
                    return HttpResponse(status=403)
            if request.GET:
                pToken = request.GET['token']
                if iToken == pToken:
                    return view_func(request, *args, **kwargs)
                else:
                    message = "forbidden your token error!!"
                    print message
                    return HttpResponse(status=403)
            return HttpResponse(status=403)

        return _wrapped_view

    return decorator
