# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notebooks', '0006_auto_20151005_0834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='source_page_ref',
            field=models.ForeignKey(related_name='note_on_sourcepage', blank=True, to='library.SourcePage', null=True),
        ),
    ]
