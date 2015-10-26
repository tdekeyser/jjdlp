# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='line',
            name='content',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
