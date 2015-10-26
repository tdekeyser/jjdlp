# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import notebooks.models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notejj', models.CharField(max_length=250)),
                ('msinfo', models.TextField(max_length=500, blank=True)),
                ('annotation', models.TextField(max_length=2000, blank=True)),
                ('ctransfer', models.CharField(max_length=30, blank=True)),
                ('source_info', models.TextField(max_length=2000, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Notebook',
            fields=[
                ('name', models.CharField(max_length=80, serialize=False, primary_key=True)),
                ('info', models.TextField(max_length=1000, blank=True)),
                ('further_usage', models.CharField(max_length=100, blank=True)),
                ('used_source', models.ManyToManyField(to='library.Source', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='NotebookPage',
            fields=[
                ('page_number', models.CharField(max_length=15, serialize=False, primary_key=True)),
                ('image', models.ImageField(upload_to=notebooks.models.upload_to_file, blank=True)),
                ('image_caption', models.CharField(max_length=200, blank=True)),
                ('notebook_ref', models.ForeignKey(related_name='notebook_page', to='notebooks.Notebook', max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='note',
            name='notepage',
            field=models.ForeignKey(related_name='note_of_page', blank=True, to='notebooks.NotebookPage', max_length=50),
        ),
        migrations.AddField(
            model_name='note',
            name='source',
            field=models.ForeignKey(related_name='source_of_note', blank=True, to='library.Source', null=True),
        ),
    ]
