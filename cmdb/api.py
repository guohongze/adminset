#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse
from models import Host, HostGroup, ASSET_TYPE, ASSET_STATUS
from django.core.paginator import Paginator, EmptyPage, InvalidPage
import xlsxwriter
import datetime

try:
    import json
except ImportError,e:
    import simplejson as json


def str2gb(args):
    ret = str(args).encode('gb2312')
    return ret


def get_object(model, **kwargs):
    """
    use this function for query
    使用改封装函数查询数据库
    """
    for value in kwargs.values():
        if not value:
            return None

    the_object = model.objects.filter(**kwargs)
    if len(the_object) == 1:
        the_object = the_object[0]
    else:
        the_object = None
    return the_object


def page_list_return(total, current=1):
    """
    page
    分页，返回本次分页的最小页数到最大页数列表
    """
    min_page = current - 2 if current - 4 > 0 else 1
    max_page = min_page + 4 if min_page + 4 < total else total

    return range(min_page, max_page + 1)


def pages(post_objects, request):
    """
    page public function , return page's object tuple
    分页公用函数，返回分页的对象元组
    """
    paginator = Paginator(post_objects, 20)
    try:
        current_page = int(request.GET.get('page', '1'))
    except ValueError:
        current_page = 1

    page_range = page_list_return(len(paginator.page_range), current_page)

    try:
        page_objects = paginator.page(current_page)
    except (EmptyPage, InvalidPage):
        page_objects = paginator.page(paginator.num_pages)

    if current_page >= 5:
        show_first = 1
    else:
        show_first = 0

    if current_page <= (len(paginator.page_range) - 3):
        show_end = 1
    else:
        show_end = 0

    # 所有对象， 分页器， 本页对象， 所有页码， 本页页码，是否显示第一页，是否显示最后一页
    return post_objects, paginator, page_objects, page_range, current_page, show_first, show_end


def write_excel(asset_all):
    data = []
    now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')
    file_name = 'cmdb_excel_' + now + '.xlsx'
    workbook = xlsxwriter.Workbook('static/files/excels/%s' % file_name)
    worksheet = workbook.add_worksheet(u'CMDB数据')
    worksheet.set_first_sheet()
    worksheet.set_column('A:E', 15)
    worksheet.set_column('F:F', 40)
    worksheet.set_column('G:Z', 15)
    title = [u'主机名', u'IP', u'IDC', u'所属主机组', u'操作系统', u'CPU', u'内存(G)', u'硬盘(G)',
             u'机柜位置', u'MAC', u'远控IP', u'机器状态', u'备注']
    for asset in asset_all:
        group_list = []
        for p in asset.group.all():
            group_list.append(p.name)

        disk = asset.disk
        group_all = '/'.join(group_list)
        status = asset.get_status_display()
        idc_name = asset.idc.name if asset.idc else u''
        system_version = asset.os if asset.system_version else u''
        system_os = unicode(system_version)

        alter_dic = [asset.hostname, asset.ip, idc_name, group_all, system_os, asset.cpu, asset.memory,
                     disk, asset.cabinet, asset.mac, asset.remote_ip, status, asset.comment]
        data.append(alter_dic)
    format = workbook.add_format()
    format.set_border(1)
    format.set_align('center')
    format.set_align('vcenter')
    format.set_text_wrap()

    format_title = workbook.add_format()
    format_title.set_border(1)
    format_title.set_bg_color('#cccccc')
    format_title.set_align('center')
    format_title.set_bold()

    format_ave = workbook.add_format()
    format_ave.set_border(1)
    format_ave.set_num_format('0.00')

    worksheet.write_row('A1', title, format_title)
    i = 2
    for alter_dic in data:
        location = 'A' + str(i)
        worksheet.write_row(location, alter_dic, format)
        i += 1

    workbook.close()
    ret = (True, file_name)
    return ret


def collect(request):
    req = request
    if req.POST:
        vendor = req.POST.get('vendor')
        group = req.POST.get('group')
        disk = req.POST.get('disk')
        cpu_model = req.POST.get('cpu_model')
        cpu_num = req.POST.get('cpu_num')
        memory = req.POST.get('memory')
        sn = req.POST.get('sn')
        osver = req.POST.get('osver')
        hostname = req.POST.get('hostname')
        ip = req.POST.get('ip')
        asset_type = ""
        status = ""
        try:
            host = Host.objects.get(hostname=hostname)
        except:
            host = Host()
        # if req.POST.get('identity'):
        #     identity = req.POST.get('identity')
        #     try:
        #         host = Host.objects.get(identity=identity)
        #     except:
        #         host = Host()
        host.hostname = hostname
        #host.group = group
        host.cpu_num = int(cpu_num)
        host.cpu_model = cpu_model
        host.memory = int(memory)
        host.sn = sn
        host.disk = disk
        host.os = osver
        host.vendor = vendor
        host.ip = ip
        host.asset_type = asset_type
        host.status = status
        host.save()
        return HttpResponse("post data successfully!")
    else:
        return HttpResponse("no any post data!")


def get_group(request):
    if request.GET:
        d = []
        try:
            name = request.GET['name']
        except:
            return HttpResponse('you have no data')
        host_groups = HostGroup.objects.get(name=name)
        ret_hg = {'host_group': host_groups.name, 'members': []}
        members = host_groups.members.all()
        for h in members:
            ret_h = {'hostname': h.hostname, 'ipaddr': h.ip}
            ret_hg['members'].append(ret_h)
        d.append(ret_hg)
        return HttpResponse(json.dumps(d))
    else:
        d = []
        host_groups = HostGroup.objects.all()
        for hg in host_groups:
            ret_hg = {'host_group': hg.name, 'members': []}
            members = hg.members.all()
            for h in members:
                ret_h = {'hostname': h.hostname, 'ipaddr': h.ip}
                ret_hg['members'].append(ret_h)
            d.append(ret_hg)
        return HttpResponse(json.dumps(d))


def get_host(request):
    try:
        hostname = request.GET['hostname']
    except:
        return HttpResponse('you have no data')
    try:
        host = Host.objects.get(hostname=hostname)
    except:
        return HttpResponse('no data,please check your hostname')
    data = {'hostname': host.hostname, 'ip': host.ip}
    return HttpResponse(json.dumps({'status': 0, 'message': 'ok', 'data': data}))

