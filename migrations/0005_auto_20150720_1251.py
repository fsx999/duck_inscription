# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('duck_inscription', '0004_auto_20150702_1748'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoriePieceModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='PieceDossierModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.TextField()),
                ('category', models.ForeignKey(to='duck_inscription.CategoriePieceModel')),
            ],
        ),
        migrations.CreateModel(
            name='PiecesManquantesDossierWishModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('pieces', models.ManyToManyField(to='duck_inscription.PieceDossierModel')),
                ('wish', models.ForeignKey(to='duck_inscription.Wish')),
            ],
        ),
        migrations.AlterField(
            model_name='dossierinscription',
            name='centre_payeur',
            field=models.CharField(blank=True, max_length=6, null=True, choices=[(b'', b'------'), (b'SMEREP', b'SMEREP'), (b'LMDE', b'LMDE')]),
        ),
    ]
