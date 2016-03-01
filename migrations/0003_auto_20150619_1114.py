# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('duck_inscription', '0002_auto_20150603_1252'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paiementallmodel',
            name='moyen_paiement',
        ),
        migrations.RemoveField(
            model_name='paiementallmodel',
            name='wish',
        ),
        migrations.DeleteModel(
            name='TypePaiementModel',
        ),
        # migrations.AlterModelManagers(
        #     name='inscriptionuser',
        #     managers=[
        #         (b'objects', django.contrib.auth.models.UserManager()),
        #     ],
        # ),
        migrations.DeleteModel(
            name='MoyenPaiementModel',
        ),
        migrations.DeleteModel(
            name='PaiementAllModel',
        ),
    ]
