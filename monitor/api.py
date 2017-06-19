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
@token_verify()
def received_sys_info(request):
    if request.method == 'POST':
        mongodb_ip = get_dir("mongodb_ip")
        mongodb_port = get_dir("mongodb_port")
        received_json_data = json.loads(request.body)
        hostname = received_json_data["hostname"]
        received_json_data['timestamp'] = int(time.time())
        client = MongoClient(mongodb_ip, int(mongodb_port))
        db = client.sys_info
        collection = db[hostname]
        collection.insert_one(received_json_data)
        return HttpResponse("Post the system Monitor Data successfully!")
    else:
        return HttpResponse("Your push have errors, Please Check your data!")
