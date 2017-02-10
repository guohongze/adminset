from django.shortcuts import render
from .models import navi
from django.http import HttpResponse
from django.shortcuts import render_to_response,redirect
# Create your views here.

def index(request):
    allnavi = navi.objects.all()
    return render_to_response("navi/index.html",locals())

