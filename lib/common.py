from django.http import HttpResponse
from config.views import get_dir
import json
import redis

def token_verify():

    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            set_token = get_dir('token')
            error_info = "Post forbidden, your token error!!"
            if request.method == 'POST':
                try:
                    # 在Python 3中，request.body是字节类型，需要先解码
                    post_data = json.loads(request.body.decode('utf-8'))
                    if set_token == post_data["token"]:
                        return view_func(request, *args, **kwargs)
                    else:
                        return HttpResponse(error_info, status=403)
                except (ValueError, json.JSONDecodeError, KeyError):
                    return HttpResponse("Invalid JSON data or missing token", status=400)
            if request.GET:
                post_token = request.GET.get('token', '')
                if set_token == post_token:
                    return view_func(request, *args, **kwargs)
                else:
                    return HttpResponse(error_info, status=403)
            return HttpResponse(error_info, status=403)

        return _wrapped_view

    return decorator


class GetRedis(object):
    host = get_dir("redis_host")
    port = get_dir("redis_port")
    db = get_dir("redis_db")
    password = get_dir("redis_password")

    @classmethod
    def connect(cls):
        # 使用通用的参数格式，适用于新旧版本的redis-py
        conn_params = {
            'host': cls.host,
            'port': cls.port,
            'db': cls.db
        }
        if cls.password:
            conn_params['password'] = cls.password
            
        conn = redis.StrictRedis(**conn_params)
        return conn