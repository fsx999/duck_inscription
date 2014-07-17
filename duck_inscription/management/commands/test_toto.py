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
        pass
        # print Wish.objects.filter(state='equivalence', suivi_dossier='inactif', etape__cod_etp__in=['L1NPSY', 'L2NPSY', 'L3NPSY']).delete()
