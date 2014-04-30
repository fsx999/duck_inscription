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


class SuiviDossierWorkflow(xwf_models.Workflow):
    states = (
        ('inactif', 'Inactif'),
        ('equivalence_reception', 'Dossier Equivalence receptionné'),
        ('equivalence_complet', 'Dossier Equivalence complet'),
        ('equivalence_incomplet', 'Dossier Equivalence incomplet'),
        ('equivalence_traite', 'Dossier Equivalence traite'),
        ('candidature_reception', 'Dossier Candidature receptionné'),
        ('candidature_complet', 'Dossier Candidature complet'),
        ('candidature_incomplet', 'Dossier Candidature incomplet'),
        ('candidature_traite', 'Dossier Candidature traite'),
        ('inscription_reception', 'Dossier inscription receptionné'),
        ('inscription_complet', 'Dossier inscription complet'),
        ('inscription_incomplet', 'Dossier inscription incomplet'),
        ('inscription_traite', 'Dossier inscription traite'),
    )

    initial_state = 'inactif'
    transitions = (
        ('equivalence_receptionner', ('inactif', 'equivalence_incomplet'), 'equivalence_reception'),
        ('equivalence_incomplet', 'equivalence_reception', 'equivalence_incomplet'),
        ('equivalence_complet', ('equivalence_reception', 'equivalence_incomplet'), 'equivalence_complet'),
        ('equivalence_traite', 'equivalence_complet', 'equivalence_traite'),
    )
