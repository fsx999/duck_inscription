# coding=utf-8
from __future__ import unicode_literals
from django_xworkflows import models as xwf_models


class IndividuWorkflow(xwf_models.Workflow):
    log_model = ''
    states = (
        ('first_connection', 'Première connexion'),
        ('individu', 'Individu'),
        ('adresse', 'Adresse'),
        ('recap', 'Recapitulatif'),
        ('accueil', 'Accueil')
    )

    transitions = (
        ('valid_fisrt_connection', 'first_connection', 'individu'),
        ('valid_individu', 'individu', 'adresse'),
        ('valid_adresse', 'adresse', 'recap'),
        ('valid_recap', 'recap', 'accueil')
    )
    initial_state = 'individu'

