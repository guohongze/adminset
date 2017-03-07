from django.shortcuts import render

# Create your views here.

from django.shortcuts import render_to_response, redirect, HttpResponse
from models import SysUser
from django.contrib.auth.decorators import login_required
from hashlib import sha1


def login(request):
    ret = {}
    if request.method == 'POST':
        user = request.POST.get('username', None)
        pwd = request.POST.get('password', None)
        is_auth = SysUser.objects.filter(username=user, password=pwd).count()
        if is_auth == 1:
            request.session['is_login'] = {'user': user}
            return redirect('/auser/')
        else:
            ret['status'] = 'user or password error!'
    return render_to_response('auser/login2.html', locals())


def index(request):
    is_login = request.session.get('is_login', None)
    if is_login:
        user_name = is_login['user']
        return render_to_response('auser/index.html', locals())
    else:
        return redirect('/auser/login')


def login_out(request):
    if request.user.is_authenticated():
        print "yes"
    del request.session['is_login']
    print request.user
    return HttpResponse('ok')

