# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notebooks', '0005_auto_20151005_0821'),
    ]

    operations = [
        migrations.RenameField(
            model_name='note',
            old_name='novel_page',
            new_name='novelpage',
        ),
        migrations.RenameField(
            model_name='note',
            old_name='novel_ref',
            new_name='novelpage_ref',
        ),
    ]
