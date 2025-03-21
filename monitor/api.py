import json
from lib.common import token_verify
from pymongo import MongoClient
from config.views import get_dir
from django.shortcuts import HttpResponse
import time
from django.views.decorators.csrf import csrf_exempt


class GetSysData(object):
    db = get_dir("mongodb_collection")

    def __init__(self, hostname, monitor_item, timing, no=0):
        self.hostname = hostname
        self.monitor_item = monitor_item
        self.timing = timing
        self.no = no

    @classmethod
    def connect_db(cls):
        mongodb_ip = get_dir("mongodb_ip")
        mongodb_port = get_dir("mongodb_port")
        mongodb_user = get_dir("mongodb_user")
        mongodb_pwd = get_dir("mongodb_pwd")
        if mongodb_user:
            uri = 'mongodb://'+mongodb_user+':'+mongodb_pwd+'@'+mongodb_ip+':'+mongodb_port+'/'+cls.db
            client = MongoClient(uri)
        else:
            client = MongoClient(mongodb_ip, int(mongodb_port))
        return client

    def get_data(self):
        client = self.connect_db()
        db = client[self.db]
        collection = db[self.hostname]
        now_time = int(time.time())
        find_time = now_time-self.timing
        cursor = collection.find({'timestamp': {'$gte': find_time}}, {self.monitor_item: 1, "timestamp": 1}).limit(self.no)
        return cursor


@csrf_exempt
@token_verify()
def received_sys_info(request):
    if request.method == 'POST':
        try:
            # 在 Python 3 中，request.body 是字节类型，需要先解码
            received_json_data = json.loads(request.body.decode('utf-8'))
            hostname = received_json_data["hostname"]
            received_json_data['timestamp'] = int(time.time())
            client = GetSysData.connect_db()
            db = client[GetSysData.db]
            collection = db[hostname]
            collection.insert_one(received_json_data)
            return HttpResponse("Post the system Monitor Data successfully!")
        except (ValueError, json.JSONDecodeError) as e:
            return HttpResponse(f"Error processing data: {str(e)}", status=400)
    else:
        return HttpResponse("Your push have errors, Please Check your data!")

