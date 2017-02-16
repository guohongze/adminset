#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.forms.widgets import *

from .models import Host, Idc, HostGroup


class AssetForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(AssetForm, self).clean()
        value = cleaned_data.get('hostname')
        try:
            Host.objects.get(hostname=value)
            self._errors['hostname']=self.error_class(["%s的信息已经存在" % value])
        except Host.DoesNotExist:
            pass
        return cleaned_data

    class Meta:
        model = Host
        exclude = ("id",)
        widgets = {
            'hostname': TextInput(attrs={'class': 'form-control', 'style': 'width:250px;'}),
            'ip': TextInput(attrs={'class': 'form-control', 'style': 'width:250px;'}),
            'group': TextInput(attrs={'class': 'form-control', 'style': 'width:250px;'}),
            'os': TextInput(attrs={'class': 'form-control', 'style': 'width:250px;'}),
            'vendor': TextInput(attrs={'class': 'form-control', 'style': 'width:250px;'}),
            'cpu_model': TextInput(attrs={'class': 'form-control', 'style': 'width:250px;'}),
            'cpu_num': TextInput(attrs={'class': 'form-control', 'style': 'width:250px;'}),
            'memory': TextInput(attrs={'class': 'form-control', 'style': 'width:250px;'}),
            'disk': TextInput(attrs={'class': 'form-control', 'style': 'width:250px;'}),
            'sn': TextInput(attrs={'class': 'form-control', 'style': 'width:250px;'}),
            'idc': Select(attrs={'class': 'form-control', 'style': 'width:250px;'}),
        }


class IdcForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(IdcForm, self).clean()
        value = cleaned_data.get('name')
        try:
            HostGroup.objects.get(name=value)
            self._errors['name']=self.error_class(["%s的信息已经存在" % value])
        except HostGroup.DoesNotExist:
            pass
        return cleaned_data

    class Meta:
        model = Idc
        exclude = ("id",)

        widgets = {
            'name': TextInput(attrs={'style': 'width:250px;'}),
            'address': TextInput(attrs={'style': 'width:250px;'}),
            'tel': TextInput(attrs={'style': 'width:250px;'}),
            'contact': TextInput(attrs={'style': 'width:250px;'}),
            'contact_phone': TextInput(attrs={'style': 'width:250px;'}),
            'jigui': TextInput(attrs={'style': 'width:250px;'}),
            'bandwidth': TextInput(attrs={'style': 'width:250px;'}),
        }
