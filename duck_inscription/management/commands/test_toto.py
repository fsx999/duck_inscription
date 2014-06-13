# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import IntegrityError
from django.db.models import Count
from django_xworkflows.xworkflow_log.models import TransitionLog
from django_apogee.models import AnneeUni, VersionEtape as VersionEtapeApogee, EtpGererCge, Etape
from duck_inscription.models import SettingAnneeUni, SettingsEtape, Wish, WishTransitionLog, WishParcourTransitionLog, \
    IndividuTransitionLog

__author__ = 'paul'
from django.core.management.base import BaseCommand
APOGEE_CONNECTION = getattr(settings, 'APOGEE_CONNECTION', 'oracle')


class Command(BaseCommand):
    def handle(self, *args, **options):
        # on récupére les personnes du jour (soit la date de création, de modif plus grand que la veille
        for a in SettingsEtape.objects.filter(annee__cod_anu=2014):
            print a.stat_parcours_dossier()
            print a.stat_suivi_dossier()

        # print type(a.modified_object)
        # wishes = Wish.objects.filter(pk__in=pks, etape__cod_etp__in=['L1NPSY', 'L2NPSY', 'L3NPSY'])
        # print wishes

