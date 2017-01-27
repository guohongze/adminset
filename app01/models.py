from __future__ import unicode_literals
from django.db import models


class test(models.Model):
    username = models.CharField(max_length=30, null=True)
    password = models.CharField(max_length=30, null=True)
