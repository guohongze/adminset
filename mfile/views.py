from django.views.generic.base import View
from django.shortcuts import render_to_response
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import  method_decorator
from accounts.permission import permission_verify


class finder(LoginRequiredMixin,View):
    @method_decorator(permission_verify())
    def get(self,request):
        temp_name = "mfile/mfile-header.html"
        return render_to_response('mfile/finder.html', locals())