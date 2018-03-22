# -*- coding: utf-8 -*-
import redis, os
import traceback
try:
    import configparser
except:
    import ConfigParser
    configparser = ConfigParser

dirs = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = configparser.ConfigParser()
with open(dirs + '/adminset.conf', 'r') as cfgfile:
    config.readfp(cfgfile)
    redis_host = config.get("redis","redis_host")
    redis_port = config.get("redis","redis_port")
    redis_passwd = config.get("redis","redis_password")
    redis_db = config.get("redis","redis_db")
    redis_dir_key_name = "oss_create_info"

redis_serv = redis.Redis(host=redis_host,port=redis_port,db=redis_db,password=redis_passwd)

def redis_put(put_info):
    try:
        if not redis_serv.exists(redis_dir_key_name):
            redis_serv.lpush(redis_dir_key_name,put_info)
        else:
            redis_serv.rpush(redis_dir_key_name,put_info)
        return "ok"
    except:
        redis_put_err = traceback.print_exc()
        return redis_put_err
