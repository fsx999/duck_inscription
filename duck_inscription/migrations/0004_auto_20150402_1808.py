# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('duck_inscription', '0003_auto_20150402_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='inscriptionuser',
            name='last_login',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='inscriptionuser',
            name='password',
            field=models.CharField(default=' ', max_length=128, verbose_name='password'),
            preserve_default=False,
        ),
    ]
