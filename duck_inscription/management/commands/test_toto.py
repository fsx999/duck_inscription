# -*- coding: utf-8 -*-
from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.db import IntegrityError
from django_xworkflows.xworkflow_log.models import TransitionLog
from mailrobot.models import Mail
from django_apogee.models import AnneeUni, VersionEtape as VersionEtapeApogee, EtpGererCge, Etape
from duck_inscription.models import SettingAnneeUni, SettingsEtape, Wish, WishTransitionLog, WishParcourTransitionLog



class Command(BaseCommand):
    def handle(self, *args, **options):
        # on récupére les personnes du jour (soit la date de création, de modif plus grand que la veille
        mail = Mail.objects.get(name='email_inscription_ouverte')
        site = Site.objects.get(domain='preins.iedparis8.net')
        print WishTransitionLog.objects.filter(wish__etape__cod_etp='L3NEDU',
                                               to_state='inscription_reception').count()
        print Wish.objects.filter(etape__cod_etp='L3NEDU', etape_dossier__to_state='inscription_reception').count()

