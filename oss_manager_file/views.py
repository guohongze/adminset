# -*- coding: utf-8 -*-
from django.shortcuts import render, HttpResponseRedirect
from .public_module_oss import oss_local_file
import json,re, os
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from accounts.permission import permission_verify
import traceback
from .oss_tasks import oss_update, oss_dir_upload
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

def gjzjianche(name):
    name = name.lstrip("/")
    if re.search(r"/$", name):
        pass
    elif name == "":
        pass
    else:
        name = name + "/"
    return name

def path_file(path_d):
    if path_d != "":
        url_list = path_d.split('/')
    else:
        return ""
    if len(url_list) > 2:
        return "/".join(url_list[0:-2])
    else:
        return ""

@login_required()
@permission_verify()
def index(request):
    temp_name = "delivery/delivery-header.html"
    return render(request, "oss_manager_file/index.html", locals())

@login_required()
@permission_verify()
def get_file(request):
    if request.method == 'GET':
        ssgjz = request.GET.get("ssgjz","")
        os_show = oss_local_file()
        oss_file,oss_d = [],[]
        if ssgjz == "":
            ssgjz = "/"
        else:
            ssgjz = gjzjianche(ssgjz)
        for lie in os_show.get_obj(ssgjz):
            if lie.endswith("/"):
                oss_d.append({"file_name":lie})
            else:
                oss_file.append({"file_url":lie,"file_name":lie.split("/")[-1]})

        if len(oss_file) > 1:
            if re.search(r'/$',oss_file[0]["file_name"]):
                oss_d_d = path_file(re.sub("http://{0}.{1}/".format(bucket_name,endpoint),"",oss_file[0]["file_name"]))
                #print "http://{0}.{1}/".format(bucket_name,endpoint)
                del oss_file[0]
            else:
                oss_d_d=path_file(ssgjz)
        elif len(oss_file) == 1:
            if re.search(r'/$',oss_file[0]["file_name"]):
                oss_d_d=path_file(oss_file[0]["file_name"])
                del oss_file[0]
            else:
                oss_d_d = path_file(ssgjz)
        else:
            oss_d_d = path_file(ssgjz)
        if ssgjz != "":
            path_danqian = ssgjz
        else:
            path_danqian = "/"
        oss_all = {"code":0, "msg":"", "count":1000, "dir":oss_d_d, "path_danqian":path_danqian, "xia_dir":oss_d, "data":oss_file}
        # print(oss_all)
        oss_file_json = json.dumps(oss_all)
        return HttpResponse(oss_file_json,content_type="application/json")
    else:
        return HttpResponse('{"status":"error","errcode":"4001"}',content_type="application/json")

@login_required()
@permission_verify()
def path_create(request):
    if request.method == "POST":
        try:
            path_name = json.loads(request.body.decode())
        except:
            return HttpResponse('{"error":u"数据格式异常！"}',content_type="application/json")
        ssgjz = gjzjianche(path_name["create_oss_path"])
        oss_create = oss_local_file()
        try:
            if oss_create.create_path_obj(ssgjz) == "1":
                oss_create_status = u"创建失败,目录已存在!"
            else:
                oss_cr_id = oss_dir_upload.delay(str(ssgjz))
                oss_create_status = u"成功提交至后端队列，请稍后! 队列ID %s" % oss_cr_id
        except:
            oss_create_status = u"创建失败!"
        status_jg = json.dumps(({'creste_status': oss_create_status}))
        return HttpResponse(status_jg, content_type="application/json")
    else:
        return HttpResponse("{'status':u'提交方式异常'}", content_type="application/json")

# @csrf_exempt
@login_required()
@permission_verify()
def upload_file(request):
    if request.method == "POST":
        try:
            file_data = request.FILES.get('file', None)
        except:
            pass
        file_data_path_s = request.POST.get("path_name", None)
        if not file_data:
            return HttpResponse('{"upload_status":u"没有文件！"}',None)
        if not file_data_path_s:
            return HttpResponse('{"upload_status":u"存储路径未获取到"}')
        print(file_data_path_s)
        file_data_path_d = gjzjianche(file_data_path_s)
        file_name = file_data_path_d + file_data.name
        print(file_name)
        if file_data.size < 1048576:
            oss_upload = oss_local_file()
            try:
                oss_upload_file = oss_upload.updata_file(file_name,file_data.read())
                #print oss_upload_file
                file_up_id = oss_update.delay(file_name,"{0}/{1}".format(oss_upload_file.split(bucket_name)[0],bucket_name))
                return JsonResponse({"upload_status":u"文件上传完成,已提交至队列,id %s！" % file_up_id})
            except:
                traceback.print_exc()
                return JsonResponse({"upload_status":u"文件上传失败！"})

        else:
            return HttpResponse('{"status":u"上传文件超过限制！"}',content_type="application/json")
    else:
        return  HttpResponse('{"status":u"请求格式异常！"}')
