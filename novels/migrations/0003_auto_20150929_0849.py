# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('novels', '0002_line_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='line',
            name='linenumber',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
