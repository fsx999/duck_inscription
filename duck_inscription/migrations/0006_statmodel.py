# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('django_apogee', '0001_initial'),
        ('duck_inscription', '0005_auto_20150417_1047'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('equi_effectue', models.IntegerField(null=True)),
                ('equi_reception', models.IntegerField(null=True)),
                ('equi_refuse', models.IntegerField(null=True)),
                ('equi_traite', models.IntegerField(null=True)),
                ('candidature_effectue', models.IntegerField(null=True)),
                ('candidature_reception', models.IntegerField(null=True)),
                ('candidature_refuse', models.IntegerField(null=True)),
                ('candidature_accepte', models.IntegerField(null=True)),
                ('inscription_effectue', models.IntegerField(null=True)),
                ('inscription_reception', models.IntegerField(null=True)),
                ('inscription_incomplet', models.IntegerField(null=True)),
                ('inscription_complet', models.IntegerField(null=True)),
                ('inscription_opi', models.IntegerField(null=True)),
                ('inscription_attente', models.IntegerField(null=True)),
                ('cod_anu', models.ForeignKey(to='duck_inscription.SettingAnneeUni')),
                ('etape', models.ForeignKey(to='django_apogee.Etape')),
            ],
            options={
                'verbose_name': 'statistique',
                'verbose_name_plural': 'statistiques',
            },
        ),
    ]
