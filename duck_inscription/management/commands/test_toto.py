# -*- coding: utf-8 -*-
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.db import IntegrityError
from django_xworkflows.xworkflow_log.models import TransitionLog
from django_apogee.models import AnneeUni, VersionEtape as VersionEtapeApogee, EtpGererCge, Etape
from duck_inscription.models import SettingAnneeUni, SettingsEtape, Wish, WishTransitionLog, WishParcourTransitionLog


__author__ = 'paul'
from django.core.management.base import BaseCommand
APOGEE_CONNECTION = getattr(settings, 'APOGEE_CONNECTION', 'oracle')


class Command(BaseCommand):
    def handle(self, *args, **options):
        # on récupére les personnes du jour (soit la date de création, de modif plus grand que la veille
        text = u"""
Madame, Monsieur

Suite à une erreur de notre part, le montant des droits universitaires qu'il vous a été demandé d'acquitter est erroné ; il manque 5,10€ (pour la visite médicale). Or la validation de votre inscription est subordonnée au paiement de la totalité des droits.

1. Vous n'avez pas encore effectué de paiement

Il vous suffit de vous connecter sur votre compte IED et de télécharger à nouveau le dossier déjà rempli. Vous joindrez les pièces au dossier en suivant les consignes indiquées dans les nouveaux formulaires de paiement, avant de l'envoyer.

2. Vous avez déjà effectué un virement

Vous devrez effectuer un virement de 5,10 €, exactement dans les mêmes conditions que pour le premier virement (bénéficiaire et motif, très important pour identifier le paiement et valider l'inscription). Pour retrouver le bénéficiaire et le motif, il vous suffit de vous connecter sur votre compte IED et de télécharger à nouveau le dossier.

3. Vous avez déjà envoyé votre paiement par chèque

Il vous suffit de vous connecter sur votre compte IED et de télécharger à nouveau votre dossier. Il ne faudra pas nous envoyer de chèque complémentaire, mais un chèque pour le total des droits, destiné à remplacer l'ancien, que nous détruirons à réception du nouveau.

Vous devrez nous envoyer le chèque au montant total indiqué dans le nouveau dossier, avec au dos le motif indiqué dans le dossier (le même que la première fois), et avec le même bénéficiaire (IED Université Paris 8). Collez sur l'enveloppe l'adresse telle qu'elle figure dans le dossier téléchargé.



Attention : cette erreur concerne exclusivement le paiement des droits universitaires, il n'est pas nécessaire de changer quoi que ce soit au paiement des frais d'enseignement à distance.

Nous vous prions de bien vouloir accepter nos excuses pour les désagréments causés.

La direction de l'IED

        """
        for x in Wish.objects.filter(annee__cod_anu=2014, state='inscription'):
            send_mail(u'[IED] Important erreur de montant pour l\'inscription', text, 'nepasrepondre@iedparis8.net', [x.individu.user.email])

        print "fini"
