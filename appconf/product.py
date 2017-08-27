#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from models import Product
from forms import ProductForm
from accounts.permission import permission_verify


@login_required()
@permission_verify()
def product_list(request):
    temp_name = "appconf/appconf-header.html"
    all_product = Product.objects.all()
    results = {
        'temp_name': temp_name,
        'all_product':  all_product,
    }
    return render(request, 'appconf/product_list.html', results)


@login_required
@permission_verify()
def product_del(request):
    product_id = request.GET.get('id', '')
    if product_id:
        Product.objects.filter(id=product_id).delete()

    product_id_all = str(request.POST.get('product_id_all', ''))
    if product_id_all:
        for product_id in product_id_all.split(','):
            Product.objects.filter(id=product_id).delete()

    return HttpResponseRedirect(reverse('product_list'))


@login_required
@permission_verify()
def product_add(request):
    temp_name = "appconf/appconf-header.html"
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('product_list'))
    else:
        form = ProductForm()

    results = {
        'form': form,
        'request': request,
        'temp_name': temp_name,
    }
    return render(request, 'appconf/product_base.html', results)


@login_required
@permission_verify()
def product_edit(request, product_id):
    product = Product.objects.get(id=product_id)
    temp_name = "appconf/appconf-header.html"
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('product_list'))
    else:
        form = ProductForm(instance=product)

    results = {
        'form': form,
        'product_id': product_id,
        'request': request,
        'temp_name': temp_name,
    }
    return render(request, 'appconf/product_base.html', results)


@login_required
@permission_verify()
def project_list(request, product_id):
    temp_name = "appconf/appconf-header.html"
    product = Product.objects.get(id=product_id)
    projects = product.project_set.all()
    results = {
        'temp_name': temp_name,
        'project_list':  projects,
    }
    return render(request, 'appconf/product_project_list.html', results)



