# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_auto_20150924_1925'),
    ]

    operations = [
        migrations.RenameField(
            model_name='source',
            old_name='note',
            new_name='info',
        ),
    ]
