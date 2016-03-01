# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('duck_inscription', '0006_auto_20150723_1117'),
    ]

    operations = [
        migrations.AddField(
            model_name='settinganneeuni',
            name='debut_pause',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='settinganneeuni',
            name='fin_pause',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='piecesmanquantesdossierwishmodel',
            name='wish',
            field=models.OneToOneField(related_name='dossier_pieces_manquantes', to='duck_inscription.Wish'),
        ),
    ]
