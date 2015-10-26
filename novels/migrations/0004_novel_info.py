# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0003_auto_20150929_0849'),
    ]

    operations = [
        migrations.AddField(
            model_name='novel',
            name='info',
            field=models.TextField(max_length=1000, null=True, blank=True),
        ),
    ]
