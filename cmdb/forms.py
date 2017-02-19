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
            'hostname': TextInput(attrs={'class': 'form-control', 'style': 'width:350px;', 'placeholder': u'必填项'}),
            'ip': TextInput(attrs={'class': 'form-control', 'style': 'width:350px;', 'placeholder': u'必填项'}),
            'other_ip': TextInput(attrs={'class': 'form-control', 'style': 'width:350px;'}),
            'host_type': TextInput(attrs={'class': 'form-control', 'style': 'width:350px;', 'placeholder': u'物理机/虚机/容器'}),
            'group': TextInput(attrs={'class': 'form-control', 'style': 'width:350px;', 'placeholder': u'备注'}),
            'os': TextInput(attrs={'class': 'form-control', 'style': 'width:350px;'}),
            'vendor': TextInput(attrs={'class': 'form-control', 'style': 'width:350px;'}),
            'cpu_model': TextInput(attrs={'class': 'form-control', 'style': 'width:350px;'}),
            'cpu_num': TextInput(attrs={'class': 'form-control', 'style': 'width:350px;'}),
            'memory': TextInput(attrs={'class': 'form-control', 'style': 'width:350px;'}),
            'disk': TextInput(attrs={'class': 'form-control', 'style': 'width:350px;'}),
            'sn': TextInput(attrs={'class': 'form-control', 'style': 'width:350px;'}),
            'idc': Select(attrs={'class': 'form-control', 'style': 'width:350px;'}),
            'position': TextInput(attrs={'class': 'form-control', 'style': 'width:350px;', 'placeholder': u'物理机写位置，虚机写宿主'}),
            'memo': TextInput(attrs={'class': 'form-control', 'style': 'width:350px;'}),
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
            'name': TextInput(attrs={'style': 'width:350px;'}),
            'address': TextInput(attrs={'style': 'width:350px;'}),
            'tel': TextInput(attrs={'style': 'width:350px;'}),
            'contact': TextInput(attrs={'style': 'width:350px;'}),
            'contact_phone': TextInput(attrs={'style': 'width:350px;'}),
            'jigui': TextInput(attrs={'style': 'width:350px;'}),
            'bandwidth': TextInput(attrs={'style': 'width:350px;'}),
        }
