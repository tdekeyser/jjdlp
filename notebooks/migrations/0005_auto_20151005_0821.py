# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0003_auto_20150929_0849'),
        ('notebooks', '0004_auto_20150924_1925'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='novel_page',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='note',
            name='novel_ref',
            field=models.ForeignKey(related_name='note_of_novel', blank=True, to='novels.Page', max_length=15, null=True),
        ),
    ]
