#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json
from lib.common import token_verify
from pymongo import MongoClient
from config.views import get_dir
from django.shortcuts import HttpResponse
import time
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def received_sys_info(request):
    iToken = get_dir("token")
    if request.method == 'POST':
        mongodb_ip = get_dir("mongodb_ip")
        mongodb_port = get_dir("mongodb_port")
        received_json_data = json.loads(request.body)
        # 验证token
        if received_json_data["token"] != iToken:
            print "forbidden your token error!!"
            return HttpResponse(status=403)
        hostname = received_json_data["hostname"]
        received_json_data['timestamp'] = int(time.time())
        client = MongoClient(mongodb_ip, int(mongodb_port))
        db = client.sys_info
        collection = db[hostname]
        collection.insert_one(received_json_data)
        return HttpResponse("Post the system Monitor Data to Server successfully!")
    else:
        return HttpResponse("Your push hava errors, Please Check your data!")
