#! /usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms

from .models import Host


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

