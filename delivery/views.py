from django.views.generic.base import TemplateView
from django.shortcuts import render
from delivery.models import Delivery


def index(request):
    projects = Delivery.objects.all()
    return render(request, "delivery/delivery_list.html", locals())
