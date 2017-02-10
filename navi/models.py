from __future__ import unicode_literals
from django.db import models


class navi(models.Model):
    name = models.CharField(max_length=50,null=True)
    description = models.CharField(max_length=50,null=True)
    url = models.URLField()

    def __unicode__(self):
        return self.name