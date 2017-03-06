from __future__ import unicode_literals

from django.db import models

# Create your models here.


class SysUser(models.Model):
    username = models.CharField(max_length=30, null=True)
    password = models.CharField(max_length=30, null=True)

    def __unicode__(self):
        return self.username