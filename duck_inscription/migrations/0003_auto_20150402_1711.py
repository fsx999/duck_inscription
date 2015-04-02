# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('duck_inscription', '0002_inscriptionuser'),
    ]

    operations = [
        migrations.RemoveField(model_name='individu', name='user'),
        migrations.AddField(
            model_name='individu',
            name='user',
            field=models.OneToOneField(null=True, to='duck_inscription.InscriptionUser'),
            preserve_default=True,
        ),
    ]
