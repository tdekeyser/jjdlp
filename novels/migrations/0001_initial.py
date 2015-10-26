# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BookSection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.PositiveSmallIntegerField()),
                ('title', models.CharField(max_length=255, blank=True)),
                ('booksection_ref', models.ForeignKey(related_name='chapter_in_section', blank=True, to='novels.BookSection', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Line',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('linenumber', models.FloatField()),
                ('booksection_ref', models.ForeignKey(related_name='line_of_section', blank=True, to='novels.BookSection', null=True)),
                ('chapter_ref', models.ForeignKey(related_name='line_of_chapter', blank=True, to='novels.Chapter', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Novel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
                ('publisher', models.CharField(max_length=255, blank=True)),
                ('publication_date', models.PositiveSmallIntegerField(blank=True)),
                ('slug', models.SlugField(unique=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pagenumber', models.PositiveSmallIntegerField()),
                ('booksection_ref', models.ForeignKey(related_name='page_of_section', blank=True, to='novels.BookSection', null=True)),
                ('chapter_ref', models.ForeignKey(related_name='page_of_chapter', blank=True, to='novels.Chapter', null=True)),
                ('novel_ref', models.ForeignKey(related_name='page_of_novel', blank=True, to='novels.Novel', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='line',
            name='novel_ref',
            field=models.ForeignKey(related_name='line_of_novel', blank=True, to='novels.Novel', null=True),
        ),
        migrations.AddField(
            model_name='line',
            name='page_ref',
            field=models.ForeignKey(related_name='line_of_page', blank=True, to='novels.Page', null=True),
        ),
        migrations.AddField(
            model_name='chapter',
            name='novel_ref',
            field=models.ForeignKey(related_name='chapter_in_novel', blank=True, to='novels.Novel', null=True),
        ),
        migrations.AddField(
            model_name='booksection',
            name='novel_ref',
            field=models.ForeignKey(related_name='section_in_novel', blank=True, to='novels.Novel', null=True),
        ),
    ]
