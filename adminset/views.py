
from django.shortcuts import HttpResponseRedirect, reverse, render


def index(request):
    return HttpResponseRedirect(reverse('navi'))