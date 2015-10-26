# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notebooks', '0003_note_source_page_ref'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='height_on_sourcepage',
            field=models.PositiveSmallIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='note',
            name='width_on_sourcepage',
            field=models.PositiveSmallIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='note',
            name='x_on_sourcepage',
            field=models.PositiveSmallIntegerField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='note',
            name='y_on_sourcepage',
            field=models.PositiveSmallIntegerField(null=True, blank=True),
        ),
    ]
