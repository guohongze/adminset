#! /usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.forms.widgets import *
from branches.models import Branch


class BranchForm(forms.ModelForm):

    class Meta:
        model = Branch
        exclude = ("id",)
        widgets = {
        }


class SubranchForm(forms.ModelForm):

    class Meta:
        model = Branch
        exclude = ("id",)
        widgets = {
        }


class ResourceForm(forms.ModelForm):

    class Meta:
        model = Branch
        exclude = ("id",)
        widgets = {
        }