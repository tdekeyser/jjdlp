# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import library.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=30, blank=True)),
                ('last_name', models.CharField(max_length=50, blank=True)),
            ],
            options={
                'ordering': ['last_name'],
            },
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('publisher_name', models.CharField(max_length=100, blank=True)),
                ('city', models.CharField(max_length=50, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source_type', models.CharField(max_length=10, blank=True)),
                ('title', models.CharField(max_length=300)),
                ('publication_date', models.PositiveSmallIntegerField()),
                ('lib_type', models.CharField(max_length=10, blank=True)),
                ('note', models.TextField(max_length=1000, blank=True)),
                ('source_link', models.CharField(max_length=255, blank=True)),
                ('certainty_info', models.TextField(max_length=500, blank=True)),
                ('slug', models.SlugField(unique=True, max_length=255, blank=True)),
                ('author', models.ManyToManyField(to='library.Author', blank=True)),
                ('publisher', models.ForeignKey(blank=True, to='library.Publisher', null=True)),
            ],
            options={
                'ordering': ['title'],
            },
        ),
        migrations.CreateModel(
            name='SourcePage',
            fields=[
                ('page_number', models.CharField(max_length=20, serialize=False, primary_key=True)),
                ('image', models.ImageField(upload_to=library.models.upload_to_item, blank=True)),
                ('image_caption', models.CharField(max_length=200)),
                ('actual_pagenumber', models.CharField(max_length=10, blank=True)),
                ('source_ref', models.ForeignKey(related_name='page_of_source', blank=True, to='library.Source', max_length=255, null=True)),
            ],
            options={
                'ordering': ['source_ref'],
                'verbose_name': 'Source page',
                'verbose_name_plural': 'Source pages',
            },
        ),
        migrations.CreateModel(
            name='Usage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('used_book', models.CharField(max_length=100)),
                ('used_book_chapter', models.CharField(max_length=15, blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='source',
            name='usage',
            field=models.ManyToManyField(to='library.Usage', blank=True),
        ),
    ]
