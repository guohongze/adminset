# -*- coding: utf-8 -*-
import oss2,logging, os, re
#from .redis_input import redis_put
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
    bucket_name = config.get("oss_info", "bucket_name")
    endpoint = config.get("oss_info", "endpoint")
    access_key_id = config.get("oss_info", "access_key_id")
    access_key_secret = config.get("oss_info", "access_key_secret")

class OS_file_operation(object):
    """oss 文件操作对象"""

    def __init__(self,bucket_name):
        self.access_key_id = access_key_id
        self.access_key_secret = access_key_secret
        self.bucket_name = bucket_name
        self.endpoint = endpoint


    def oss_upload(self,oss_file_name,oss_file_path):
        try:
            bucket = oss2.Bucket(oss2.Auth(self.access_key_id,self.access_key_secret),self.endpoint,self.bucket_name)
            if isinstance(oss_file_name,list):
                new_file_name = oss_file_name
            else:
                new_file_name = [oss_file_name]
            file_obj_out = []
            for bucket_file in new_file_name:
                with open("%s/%s" % (oss_file_path,bucket_file)) as file_obj:
                    out_obj = bucket.put_object(bucket_file,file_obj)
                file_obj_out.append({bucket_file:out_obj})

            return file_obj_out
        except:
            return traceback.print_exc()

    def oss_del_path(self,del_path):
        pass

    def oss_def_file(self,def_path,def_file_name):
        pass

    def oss_create_path(self,directory_name):
        try:
            if isinstance(directory_name, str):
                if not directory_name.endswith("/"):
                    directory_name = "%s/" % directory_name
            bucket = oss2.Bucket(oss2.Auth(self.access_key_id,self.access_key_secret),
                                 self.endpoint, self.bucket_name)
            bucket.put_object(directory_name,"")
            return 200
        except:
            print traceback.print_exc()
            return traceback.print_exc()

    def oss_get_to_file(self,oss_tmp):
        auth = oss2.Auth(self.access_key_id,self.access_key_secret)
        bucket = oss2.Bucket(auth,self.endpoint,self.bucket_name)
        oss_tmp_new = ""

        for i in oss2.ObjectIterator(bucket):
            oss_tmp_new += i.key + "\n"
        with open(oss_tmp,"w") as f:
            f.write(oss_tmp_new)
        return 0

def oss_tmp_file(bucket_name):
    dirs = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config = configparser.ConfigParser()
    with open(dirs + '/adminset.conf', 'r') as cfgfile:
        config.readfp(cfgfile)
        oss_tmp = config.get("oss_tmp_file","file_name")
    if not os.path.isfile(oss_tmp):
        oss_get = OS_file_operation(bucket_name)
        oss_get.oss_get_to_file(oss_tmp)
    return oss_tmp

def oss_updata_path(new_bucket_name):
    dirs = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config = configparser.ConfigParser()
    with open(dirs + '/adminset.conf', 'r') as cfgfile:
        config.readfp(cfgfile)
        oss_updata_dir = config.get("oss_updata_file_path","updata_file_dir")
    if not os.path.isdir("%s/%s" % (oss_updata_dir,new_bucket_name)):
        os.makedirs("%s/%s" % (oss_updata_dir,new_bucket_name))
    return "%s/%s" % (oss_updata_dir,new_bucket_name)

class oss_local_file(object):
    """oss 缓存文件处理"""
    def __init__(self):
        self.endpoint = endpoint
        self.bucket_name = bucket_name
        self.oss_tmp = oss_tmp_file(self.bucket_name)
    def get_obj(self,prefix="/"):
        oss_out_1 = []
        with open(self.oss_tmp, "r") as f:
            if prefix == "/":
                for i in f.readlines():
                    oss_obj = i.replace("\n", "").split("/")
                    if len(oss_obj) == 1:
                        oss_out_1.append("http://%s.%s/%s" % (self.bucket_name, self.endpoint, "/".join(oss_obj)))
                    if len(oss_obj) > 1:
                        oss_out_1.append(oss_obj[0]+ "/")
                oss_out= list(set(oss_out_1))

            else:
                lin_j = 0
                for lin in f.readlines():
                    if prefix in lin:
                        lin_j += 1
                        if lin_j != 1:
                            oss_obj = lin.replace("\n", "").replace(prefix, "", 1).split("/")
                            if len(oss_obj) == 1:
                                oss_out_1.append(
                                    "http://%s.%s/%s%s" % (self.bucket_name, self.endpoint, prefix, "/".join(oss_obj)))
                            if len(oss_obj) > 1:
                                oss_out_1.append(prefix + oss_obj[0] + "/")
                oss_out = list(set(oss_out_1))

        return oss_out

    def create_path_obj(self,obj_name):
        with open(self.oss_tmp, "r") as f:
            for lin in f:
                if obj_name in lin:
                    return "1"
        with open(self.oss_tmp, "ab+") as f:
            f.writelines("%s\n" % obj_name)
            f.read()
        return 0

    def updata_file(self,file_name, file_file):
        file_name_dir = "/".join(file_name.split("/")[:-1])
        file_name_name = file_name.split("/")[-1]
        if file_name_dir != "" or file_name_dir != None:
            file_dir = "%s/%s" % (self.bucket_name,file_name_dir)
            oss_path = oss_updata_path(file_dir)
        else:
            oss_path = oss_updata_path(self.bucket_name)
        file_path = "%s/%s" % (oss_path,file_name_name)
        with open(self.oss_tmp, "r") as f:
            oss_tmp_info = f.readline()
        f.close()
        kk = 0
        for lne in oss_tmp_info:
            if file_name == lne.replace("\n",""):
                kk = 1
                break
        if  kk == 0:
            try:
                with open(file_path, "wb") as file_open:
                    file_open.write(file_file)
                file_open.close()
                with open(self.oss_tmp, "ab+") as f:
                    f.writelines("%s\n" % file_name)
                    f.read()
                return file_path
            except:
                return traceback.print_exc()
        else:
            try:
                with open(file_path, "wb") as file_open:
                    file_open.write(file_file)
                file_open.close()
                return file_path
            except:
                return traceback.print_exc()
