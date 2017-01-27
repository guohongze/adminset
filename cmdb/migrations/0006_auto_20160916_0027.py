# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0005_host_idc'),
    ]

    operations = [
        migrations.AddField(
            model_name='interface',
            name='price',
            field=models.IntegerField(default=0, verbose_name='\u4ef7\u683c'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='host',
            name='hostname',
            field=models.CharField(max_length=30, verbose_name='\u4e3b\u673a\u540d'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='host',
            name='idc',
            field=models.ForeignKey(verbose_name='\u6240\u5728\u673a\u623f', to='cmdb.Idc'),
            preserve_default=True,
        ),
    ]
