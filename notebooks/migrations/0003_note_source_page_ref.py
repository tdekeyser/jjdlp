# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
        ('notebooks', '0002_note_noteb'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='source_page_ref',
            field=models.ForeignKey(related_name='sourcepage_of_note', blank=True, to='library.SourcePage', null=True),
        ),
    ]
