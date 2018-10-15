from django.views.generic.base import View
from django.shortcuts import render_to_response
from django.contrib.auth.mixins import LoginRequiredMixin


class finder(LoginRequiredMixin,View):
    def get(self,request):
        temp_name = "mfile/mfile-header.html"
        return render_to_response('mfile/finder.html', locals())