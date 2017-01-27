from django.views import generic
from .models import Host
from django.http import HttpResponse
from django.shortcuts import render_to_response,redirect
import csv
import models


def index1(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def index2(request):
    hosts = Host.objects.all()
    return render_to_response('cmdb/index.html', {'host_list':hosts})


def index3(request):
    host_list = Host.objects.all()
    return render_to_response('cmdb/index.html',locals())


class IndexView(generic.ListView):
    template_name = 'cmdb/index.html'
    context_object_name = 'host_list'

    def get_queryset(self):
        return Host.objects.order_by('hostname')


def execl(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'
    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])
    return response


def login(request):
    ret = {}
    if request.method == 'POST':
        user = request.POST.get('username',None)
        pwd = request.POST.get('password',None)
        is_auth = models.UserInfo.objects.filter(username=user,password=pwd).count()
        if is_auth == 1:
            return redirect('/cmdb')
        else:
            ret['status'] = 'user or password error'
            return render_to_response('cmdb/login.html', locals())
    else:
        return render_to_response('cmdb/login.html', locals())