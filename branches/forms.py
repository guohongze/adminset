#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.forms.widgets import *
from branches.models import Branch, Region, Resource
from django.contrib.admin import widgets


class RegionForm(forms.ModelForm):

    class Meta:
        model = Region
        exclude = ("id",)
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'address': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'telephone': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'owner': Select(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'description': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
        }


class BranchForm(forms.ModelForm):

    class Meta:
        model = Branch
        exclude = ("id",)
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'address': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'telephone': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'owner': Select(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'region': Select(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'description': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),

        }


class ResourceForm(forms.ModelForm):

    class Meta:
        model = Resource
        exclude = ("id",)
        widgets = {
            'sn': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'name': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'spec': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'budget': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'paid': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'contract': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'contract_start': DateInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'contract_end': DateInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'supplier': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'service_phone': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'branch': Select(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'owner': Select(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'description': Textarea(attrs={'class': 'form-control', 'style': 'width:450px;'}),

        }
