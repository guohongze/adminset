#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.forms.widgets import *

from .models import Host, Idc, HostGroup, Cabinet


class AssetForm(forms.ModelForm):

    class Meta:
        model = Host
        exclude = ("id",)
        widgets = {
            'hostname': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'必填项'}),
            'ip': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'必填项'}),
            'account': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'other_ip': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'group': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'asset_no': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'asset_type': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'status': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'os': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'vendor': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'up_time': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'cpu_model': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'cpu_num': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'memory': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'disk': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'sn': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'idc': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'position': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'物理机写位置，虚机写宿主'}),
            'memo': Textarea(attrs={'rows': 4, 'cols': 15, 'class': 'form-control', 'style': 'width:530px;'}),
        }


class IdcForm(forms.ModelForm):

    # def clean(self):
    #     cleaned_data = super(IdcForm, self).clean()
    #     value = cleaned_data.get('ids')
    #     try:
    #         Idc.objects.get(name=value)
    #         self._errors['ids'] = self.error_class(["%s的信息已经存在" % value])
    #     except Idc.DoesNotExist:
    #         pass
    #     return cleaned_data

    class Meta:
        model = Idc
        exclude = ("id",)

        widgets = {
            'ids': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'name': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'address': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'tel': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'contact': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'contact_phone': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'ip_range': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'jigui': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
            'bandwidth': TextInput(attrs={'class': 'form-control','style': 'width:450px;'}),
        }


class GroupForm(forms.ModelForm):

    def clean(self):
        cleaned_data = super(GroupForm, self).clean()
        value = cleaned_data.get('name')
        try:
            Cabinet.objects.get(name=value)
            self._errors['name'] = self.error_class(["%s的信息已经存在" % value])
        except Cabinet.DoesNotExist:
            pass
        return cleaned_data

    class Meta:
        model = HostGroup
        exclude = ("id", )

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'desc': Textarea(attrs={'rows': 4, 'cols': 15, 'class': 'form-control', 'style': 'width:450px;'}),

        }


class CabinetForm(forms.ModelForm):

    # def clean(self):
    #     cleaned_data = super(CabinetForm, self).clean()
    #     value = cleaned_data.get('name')
    #     try:
    #         Cabinet.objects.get(name=value)
    #         self._errors['name'] = self.error_class(["%s的信息已经存在" % value])
    #     except Cabinet.DoesNotExist:
    #         pass
    #     return cleaned_data

    class Meta:
        model = Cabinet
        exclude = ("id", )

        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'idc': Select(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'desc': Textarea(attrs={'rows': 4, 'cols': 15, 'class': 'form-control', 'style': 'width:450px;'}),

        }
