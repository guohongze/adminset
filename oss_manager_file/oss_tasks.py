# -*- coding: utf-8 -*-
from __future__ import absolute_import
#from celery import Celery
from celery import shared_task
import oss2, traceback
import os
try:
    import configparser
except:
    import ConfigParser
    configparser = ConfigParser


dirs = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config = configparser.ConfigParser()
with open(dirs + '/adminset.conf', 'r') as cfgfile:
    config.readfp(cfgfile)
    access_key_id = config.get("oss_info", "access_key_id")
    access_key_secret = config.get("oss_info", "access_key_secret")
    bucket_name = config.get("oss_info", "bucket_name")
    endpoint = config.get("oss_info", "endpoint")


@shared_task
def oss_update(oss_info,oss_file_dir):
    try:
        bucket = oss2.Bucket(oss2.Auth(access_key_id,access_key_secret),endpoint,bucket_name)
        if isinstance(oss_info,list):
            new_file_name = oss_info
        else:
            new_file_name = [oss_info]
        file_obj_out = []
        for bucket_file in new_file_name:
            with open("%s/%s" % (oss_file_dir,bucket_file)) as file_obj:
                out_obj = bucket.put_object(bucket_file,file_obj)
            file_obj_out.append({bucket_file:out_obj.status})
        return file_obj_out
    except:
        return traceback.print_exc()



@shared_task
def oss_dir_upload(oss_info):
    try:
        auth = oss2.Auth(access_key_id, access_key_secret)
        bucket = oss2.Bucket(auth,endpoint, bucket_name)
        oss_out = bucket.put_object(oss_info, "")
        return oss_out.status
    except:
        print traceback.print_exc()
        return traceback.print_exc()


def oss_log(oss_out_info):
    if not os.path.isfile("/var/log/oss_upload_file.log"):
        with open("/var/log/oss_upload_file.log", "wb") as f:
            f.write("")
        f.close()
    if isinstance(oss_out_info,list):
        with open("/var/log/oss_upload_file.log", "ab+") as f:
            f.writelines(oss_out_info)
        f.close()
    else:
        with open("/var/log/oss_upload_file.log", "ab+") as f:
            f.write(str(oss_out_info))
        f.close()

if __name__ == "__main__":
    ooo = oss_dir_upload("dsasduu/")
    print ooo.status