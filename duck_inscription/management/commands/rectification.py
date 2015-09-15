# coding=utf-8
from django.core.mail import send_mail
from django_apogee.utils import make_etudiant_password
from duck_utils.utils import email_ied, get_recipients, get_email_envoi

__author__ = 'paulguichon'
# -*- coding: utf-8 -*-
from django.conf import settings
from django_apogee.models import AnneeUni, VersionEtape as VersionEtapeApogee, EtpGererCge, Etape, InsAdmEtp
from duck_inscription.models import SettingAnneeUni, SettingsEtape, Wish, InscriptionUser, Individu
from django.core.management.base import BaseCommand
APOGEE_CONNECTION = getattr(settings, 'APOGEE_CONNECTION', 'oracle')


class Command(BaseCommand):
    def handle(self, *args, **options):
        text = """
Le problème technique empêchant la visualisation des formulaires de paiement a été corrigé.
Pour effectuer votre inscription en Licence 1 psychologie, vous devez aller sur votre espace d'inscription et compléter les formulaires de paiement.
Si vous aviez déjà envoyé un dossier accompagné des bons chèques ou des preuves des virements, vous n'avez rien d'autre à faire.
Dans tous les autres cas, vous devez renvoyer le dossier complet.

Cordialement.

La scolarité de l'IED.
        """
        obj = "[IED] Inscription L1 psychologie, formulaire de paiement manquant"
        for wish in Wish.objects.filter(annee__cod_anu=2015,
                                        state='inscription',
                                        etape__cod_etp='L1NPSY', paiementallmodel__moyen_paiement__isnull=True):
            send_mail(obj, text, 'nepasrepondre@iedparis8.net', [get_email_envoi(wish.individu.personal_email)])
            wish.dispatch()
        print "fini"