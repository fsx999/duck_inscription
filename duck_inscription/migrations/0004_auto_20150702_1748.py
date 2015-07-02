# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_xworkflows.models
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('duck_inscription', '0003_auto_20150619_1114'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='inscriptionuser',
            managers=[
                (b'objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='settingsetape',
            name='autres',
            field=models.FileField(null=True, upload_to='document_autre', blank=True),
        ),
        migrations.AlterField(
            model_name='wish',
            name='state',
            field=django_xworkflows.models.StateField(max_length=25, workflow=django_xworkflows.models._SerializedWorkflow(states=[b'creation', b'ouverture_equivalence', b'liste_diplome', b'demande_equivalence', b'equivalence', b'liste_attente_equivalence', b'mis_liste_attente_equi', b'ouverture_candidature', b'note_master', b'candidature', b'liste_attente_candidature', b'mis_liste_attente_candi', b'ouverture_inscription', b'dossier_inscription', b'dispatch', b'inscription', b'liste_attente_inscription', b'auditeur', b'auditeur_traite'], initial_state=b'creation', name=b'WishWorkflow')),
        ),
    ]
