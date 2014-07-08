# -*- coding: utf-8 -*-

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
        Bonjour,

        Suite à des retards techniques, nous ne sommes pas en mesure d'ouvrir les inscriptions à la date du 8 juillet.

        Nous remettons cette ouverture au 17 juillet en fin de matinée.

        Veuillez nous excuser pour la gêne occasionnée.

        L'équipe informatique de l'IED.
        """
        for user in User.objects.filter(is_staff=False):
            send_mail(u"[IED]Inscription retardée", text, 'nepasrepondre@iedparis8.net', [user.email])



