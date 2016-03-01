# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('duck_inscription', '0005_auto_20150720_1251'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='categoriepiecemodel',
            options={'verbose_name': 'Cat\xe9gorie pi\xe8ces', 'verbose_name_plural': 'Cat\xe9gories pi\xe8ces'},
        ),
        migrations.AlterModelOptions(
            name='piecedossiermodel',
            options={'verbose_name': 'Pi\xe8ce dossier', 'verbose_name_plural': 'Pi\xe8ces dossier'},
        ),
        migrations.AlterField(
            model_name='piecesmanquantesdossierwishmodel',
            name='wish',
            field=models.OneToOneField(related_name='dossier_pieces_manquante', to='duck_inscription.Wish'),
        ),
    ]
