# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.core.mail import send_mail
from django_apogee.models import AnneeUni, VersionEtape as VersionEtapeApogee, EtpGererCge, Etape, Individu
from duck_inscription.models import SettingAnneeUni, SettingsEtape, Wish

__author__ = 'paul'
from django.core.management.base import BaseCommand
APOGEE_CONNECTION = getattr(settings, 'APOGEE_CONNECTION', 'oracle')


class Command(BaseCommand):
    def handle(self, *args, **options):
        text = """
Bonjour,

Les cours de la Licence de droit commenceront le lundi 26 octobre.
Vous recevrez vos codes d'accès à la plateforme à la date retenue.

Cordialement.



Merci
"""
        queryset = Wish.objects.filter(etape__cod_etp__in=['L1NDRO', 'L2NDRO', 'L3NDRO'], state='inscription', etape_dossier__to_state='inscription_complet')
        print queryset.count()

        for x in queryset:
            send_mail('[IED] information inscription', text, 'nepasrepondre@iedparis8.net', [x.individu.personal_email])
        #on récupére les personnes du jour (soit la date de création, de modif plus grand que la veille
        # print "debut test"
        # print Individu.objects.using(APOGEE_CONNECTION).count()
        # print "ca marche"






