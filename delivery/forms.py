#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from django import forms
from django.forms import widgets
from delivery.models import Delivery


class DeliveryFrom(forms.ModelForm):

    class Meta:
        model = Delivery
        exclude = ("id", "bar_data", "status")

        widgets = {
            'job_name': widgets.Select(attrs={'class': 'form-control','style': 'width:450px;'}),
            'deploy_num': widgets.TextInput(attrs={'class': 'form-control', 'style': 'width:450px;', "readonly": "readonly"}),
            'version': widgets.TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'description': widgets.Textarea(attrs={'class': 'form-control', 'style': 'width:450px; height:100px'}),
            'deploy_policy': widgets.Select(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'shell': widgets.Textarea(attrs={'class': 'form-control', 'style': 'width:450px; height:100px'}),
            'auth': widgets.Select(attrs={'class': 'form-control','style': 'width:450px;'}),

        }
