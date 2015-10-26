# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notebooks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='noteb',
            field=models.ForeignKey(related_name='note_of_book', blank=True, to='notebooks.Notebook', max_length=80, null=True),
        ),
    ]
