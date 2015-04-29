# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_xworkflows.models


class Migration(migrations.Migration):

    dependencies = [
        ('duck_inscription', '0006_statmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='individu',
            name='student_code',
            field=models.IntegerField(default=None, null=True, verbose_name='Code \xe9tudiant', blank=True),
        ),
        migrations.AlterField(
            model_name='settingsuser',
            name='property',
            field=models.ManyToManyField(to='duck_utils.Property', blank=True),
        ),
        migrations.AlterField(
            model_name='wish',
            name='state',
            field=django_xworkflows.models.StateField(max_length=25, workflow=django_xworkflows.models._SerializedWorkflow(states=[b'creation', b'ouverture_equivalence', b'liste_diplome', b'demande_equivalence', b'equivalence', b'liste_attente_equivalence', b'mis_liste_attente_equi', b'ouverture_candidature', b'note_master', b'candidature', b'liste_attente_candidature', b'mis_liste_attente_candi', b'ouverture_inscription', b'dossier_inscription', b'choix_ied_fp', b'droit_univ', b'inscription', b'liste_attente_inscription', b'auditeur', b'auditeur_traite'], initial_state=b'creation', name=b'WishWorkflow')),
        ),
    ]
