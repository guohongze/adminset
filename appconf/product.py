#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from appconf.models import Product
from appconf.forms import ProductForm
from accounts.permission import permission_verify


@login_required()
@permission_verify()
def product_list(request):
    all_product = Product.objects.all()
    results = {
        'all_product':  all_product,
    }
    return render(request, 'appconf/product_list.html', results)


@login_required
@permission_verify()
def product_del(request):
    product_id = request.GET.get('id', '')
    if product_id:
        Product.objects.filter(id=product_id).delete()

    if request.method == 'POST':
        product_items = request.POST.getlist('g_check', [])
        if product_items:
            for n in product_items:
                Product.objects.filter(id=n).delete()
    all_product = Product.objects.all()
    return render(request, "appconf/product_list.html", locals())


@login_required
@permission_verify()
def product_add(request):
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
    }
    return render(request, 'appconf/product_base.html', results)


@login_required
@permission_verify()
def product_edit(request, product_id):
    product = Product.objects.get(id=product_id)
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
    }
    return render(request, 'appconf/product_base.html', results)


@login_required
@permission_verify()
def project_list(request, product_id):
    product = Product.objects.get(id=product_id)
    projects = product.project_set.all()
    results = {
        'project_list':  projects,
    }
    return render(request, 'appconf/product_project_list.html', results)



