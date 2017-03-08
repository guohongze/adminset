from django.shortcuts import render

# Create your views here.

from django.shortcuts import render_to_response, redirect, HttpResponse, HttpResponseRedirect, RequestContext
from django.contrib.auth.decorators import login_required
from hashlib import sha1
from django.contrib import auth
from forms import LoginUserForm


@login_required()
def index(request):
    return HttpResponse("ok")


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')

    if request.method == 'GET' and request.GET.has_key('next'):
        next = request.GET['next']
    else:
        next = '/'

    if request.method == "POST":
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():
            auth.login(request, form.get_user())
            return HttpResponseRedirect(request.POST['next'])
    else:
        form = LoginUserForm(request)

    kwvars = {
        'request': request,
        'form':  form,
        'next': next,
    }

    return render_to_response('accounts/login.html', kwvars, RequestContext(request))


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))