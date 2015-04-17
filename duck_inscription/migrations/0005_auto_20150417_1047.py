# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('duck_inscription', '0004_auto_20150402_1808'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='inscriptionuser',
            managers=[
                (b'objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='individu',
            name='personal_email',
            field=models.EmailField(max_length=254, unique=True, null=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='individu',
            name='personal_email_save',
            field=models.EmailField(max_length=254, null=True, verbose_name='Email', blank=True),
        ),
        migrations.AlterField(
            model_name='inscriptionuser',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='email address', blank=True),
        ),
        migrations.AlterField(
            model_name='inscriptionuser',
            name='groups',
            field=models.ManyToManyField(related_query_name='user_inscription', related_name='user_inscription_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups'),
        ),
        migrations.AlterField(
            model_name='inscriptionuser',
            name='user_permissions',
            field=models.ManyToManyField(related_query_name='user_inscription', related_name='user_inscription_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions'),
        ),
    ]
