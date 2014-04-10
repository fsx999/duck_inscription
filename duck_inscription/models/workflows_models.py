# coding=utf-8
from __future__ import unicode_literals
from django_xworkflows import models as xwf_models


class IndividuWorkflow(xwf_models.Workflow):
    states = (
        ('first_connection', 'Première connexion'),
        ('code_etu_manquant', 'Code etudiant manquant'),
        ('individu', 'Individu'),
        ('adresse', 'Adresse'),
        ('recap', 'Recapitulatif'),
        ('accueil', 'Accueil'),
    )

    transitions = (
        ('modif_individu', ('first_connection', 'code_etu_manquant', 'recap'), 'individu'),
        ('first_connection', 'individu', 'first_connection'),
        ('modif_adresse', ('individu', 'recap'), 'adresse'),
        ('recap', 'adresse', 'recap'),
        ('accueil', 'recap', 'accueil'),
        ('code_etud_manquant', 'individu', 'code_etu_manquant'),
    )
    initial_state = 'first_connection'


class WishWorkflow(xwf_models.Workflow):
    states = (
        ('creation', 'Création'),
        ('ouverture_equivalence', 'Ouverture equivalence'),
        ('liste_diplome', 'Liste Diplome équivalent'),
        ('demande_equivalence', 'Demande desir équivalence'),
        ('equivalence', 'Dossier équivalence'),
        ('ouverture_candidature', 'Ouverture candidature'),
        ('ouverture_inscription', 'Ouverture inscription')
    )

    transitions = (
        ('ouverture_equivalence', 'creation', 'ouverture_equivalence'),
        ('liste_diplome', 'ouverture_equivalence', 'liste_diplome'),
        ('demande_equivalence', ('creation', 'liste_diplome'), 'demande_equivalence'),
        ('equivalence', ('creation', 'liste_diplome', 'demande_equivalence'), 'equivalence'),
        ('ouverture_candidature', ('creation', 'ouverture_equivalence', 'equivalence', 'demande_equivalence'),
         'ouverture_candidature'),
        ('ouverture_inscription', ('creation', 'ouverture_equivalence', 'ouverture_candidature'), 'ouverture_inscription'),
    )

    initial_state = 'creation'
