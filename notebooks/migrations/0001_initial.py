# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import notebooks.models


class Migration(migrations.Migration):

    dependencies = [
        ('manuscripts', '0001_initial'),
        ('library', '0001_initial'),
        ('texts', '0001_initial'),
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
                ('source', models.TextField(blank=True)),
                ('textref', models.CharField(max_length=50, blank=True)),
                ('libraryexcerpt', models.ManyToManyField(related_name='note_set', to='library.LibraryExcerpt', blank=True)),
                ('manuscriptexcerpt', models.ForeignKey(related_name='note_set', blank=True, to='manuscripts.ManuscriptExcerpt', null=True)),
                ('note', models.ForeignKey(related_name='note_set', blank=True, to='notebooks.Note', null=True)),
            ],
            options={
                'ordering': ['notejj'],
            },
        ),
        migrations.CreateModel(
            name='Notebook',
            fields=[
                ('slug', models.SlugField(unique=True, max_length=255, blank=True)),
                ('name', models.CharField(max_length=80, serialize=False, verbose_name=b'title', primary_key=True)),
                ('item_type', models.CharField(max_length=100, blank=True)),
                ('link', models.CharField(max_length=255, blank=True)),
                ('info', models.TextField(blank=True)),
                ('draft_period', models.CharField(max_length=255, blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NotebookCollection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=300)),
                ('info', models.TextField(blank=True)),
                ('slug', models.SlugField(unique=True, max_length=255, blank=True)),
                ('collection', models.ForeignKey(related_name='collection_set', blank=True, to='notebooks.NotebookCollection', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='NotebookPage',
            fields=[
                ('page_number', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('slug', models.SlugField(max_length=255, blank=True)),
                ('image', models.ImageField(upload_to=notebooks.models.upload_to_file, blank=True)),
                ('notebook', models.ForeignKey(related_name='page_set', to='notebooks.Notebook', max_length=50)),
            ],
            options={
                'ordering': ['notebook'],
            },
        ),
        migrations.AddField(
            model_name='notebook',
            name='collection',
            field=models.ForeignKey(related_name='item_set', default=b'', blank=True, to='notebooks.NotebookCollection'),
        ),
        migrations.AddField(
            model_name='notebook',
            name='libraryitem',
            field=models.ManyToManyField(related_name='notebook_set', to='library.LibraryItem', blank=True),
        ),
        migrations.AddField(
            model_name='notebook',
            name='text',
            field=models.ForeignKey(related_name='notebook_set', default=b'', blank=True, to='texts.Text'),
        ),
        migrations.AddField(
            model_name='note',
            name='noteb',
            field=models.ForeignKey(related_name='note_set', blank=True, to='notebooks.Notebook', max_length=80, null=True),
        ),
        migrations.AddField(
            model_name='note',
            name='page',
            field=models.ForeignKey(related_name='note_set', verbose_name=b'page', blank=True, to='notebooks.NotebookPage', max_length=100),
        ),
        migrations.AddField(
            model_name='note',
            name='textline',
            field=models.ForeignKey(related_name='note_set', blank=True, to='texts.Line', max_length=255, null=True),
        ),
    ]
