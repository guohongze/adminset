#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from config.views import get_dir
import json


def token_verify():

    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            set_token = get_dir('token')
            error_info = "Post forbidden, your token error!!"
            if request.method == 'POST':
                post_token = json.loads(request.body)
                if set_token == post_token["token"]:
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponse(error_info, status=403)
            if request.GET:
                post_token = request.GET['token']
                if set_token == post_token:
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponse(error_info, status=403)
            return HttpResponse(error_info, status=403)

        return _wrapped_view

    return decorator
