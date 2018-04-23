#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.forms.widgets import *
from .models import Product, Project, AppOwner, AuthInfo


class AuthInfoForm(forms.ModelForm):

    class Meta:
        model = AuthInfo
        exclude = ("id",)
        widgets = {
            'dis_name': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'username': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'password': TextInput(attrs={'class': 'form-control', 'type': 'password', 'style': 'width:450px'}),
            'private_key': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'memo': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
        }


class AppOwnerForm(forms.ModelForm):

    class Meta:
        model = AppOwner
        exclude = ("id",)
        widgets = {
            'name': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'phone': TextInput(attrs={'class': 'form-control','style': 'width:450px'}),
            'qq': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'weChat': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
        }


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        exclude = ("id",)
        widgets = {
            'name': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'description': Textarea(attrs={'class': 'form-control','style': 'width:450px; height:100px'}),
            'owner': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
        }


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project
        exclude = ("id",)

        widgets = {
            'name': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'description': Textarea(attrs={'class': 'form-control','style': 'width:450px; height:100px'}),
            'language_type': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
            'app_type': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
            'server_type': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
            'app_arch': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
            'appPath': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'source_type': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
            'source_address': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'configPath': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'product': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
            'owner': Select(attrs={'class': 'form-control','style': 'width:450px;'}),
            'serverList': forms.SelectMultiple(attrs={'class': 'form-control', 'size':'10', 'multiple': 'multiple'}),
        }
