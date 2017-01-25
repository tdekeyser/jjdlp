# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import library.models


class Migration(migrations.Migration):

    dependencies = [
        ('gentext', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibraryCollection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=300)),
                ('info', models.TextField(blank=True)),
                ('slug', models.SlugField(unique=True, max_length=255, blank=True)),
                ('collection_type', models.CharField(max_length=50, blank=True)),
                ('publication_period', models.CharField(max_length=100, blank=True)),
                ('image', models.ImageField(upload_to=library.models.upload_to_collection, blank=True)),
                ('collection', models.ForeignKey(related_name='collection_set', blank=True, to='library.LibraryCollection', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LibraryExcerpt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
            ],
            options={
                'ordering': ['page'],
            },
        ),
        migrations.CreateModel(
            name='LibraryItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=300)),
                ('item_type', models.CharField(max_length=10, blank=True)),
                ('date', models.PositiveIntegerField(null=True, blank=True)),
                ('bib', models.TextField(blank=True)),
                ('slug', models.SlugField(unique=True, max_length=255, blank=True)),
                ('discovered_by', models.CharField(max_length=300, blank=True)),
                ('info', models.TextField(blank=True)),
                ('side_note', models.TextField(blank=True)),
                ('link', models.CharField(max_length=255, blank=True)),
                ('notebooks', models.CharField(max_length=300, blank=True)),
                ('author', models.ManyToManyField(to='gentext.Author', blank=True)),
                ('collection', models.ForeignKey(related_name='item_set', blank=True, to='library.LibraryCollection', null=True)),
                ('publisher', models.ForeignKey(default=b'', blank=True, to='gentext.Publisher', null=True)),
            ],
            options={
                'ordering': ['date'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LibraryPage',
            fields=[
                ('page_number', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('slug', models.SlugField(max_length=255, blank=True)),
                ('image', models.ImageField(upload_to=library.models.upload_to_item, blank=True)),
                ('actual_pagenumber', models.CharField(max_length=50, blank=True)),
                ('item', models.ForeignKey(related_name='page_set', blank=True, to='library.LibraryItem', max_length=255, null=True)),
            ],
            options={
                'ordering': ['actual_pagenumber'],
            },
        ),
        migrations.AddField(
            model_name='libraryexcerpt',
            name='item',
            field=models.ForeignKey(related_name='excerpt_set', to='library.LibraryItem'),
        ),
        migrations.AddField(
            model_name='libraryexcerpt',
            name='page',
            field=models.ForeignKey(related_name='excerpt_set', to='library.LibraryPage'),
        ),
    ]
