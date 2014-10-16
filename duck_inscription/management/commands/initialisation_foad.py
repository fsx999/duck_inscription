# -*- coding: utf-8 -*-
from django.conf import settings
from django_apogee.models import AnneeUni, VersionEtape as VersionEtapeApogee, EtpGererCge, Etape
from duck_inscription.models import SettingAnneeUni, SettingsEtape, Wish
from foad.models import SettingsEtapeFoad, EtapeMpttModel

__author__ = 'paul'
from django.core.management.base import BaseCommand
APOGEE_CONNECTION = getattr(settings, 'APOGEE_CONNECTION', 'oracle')


class Command(BaseCommand):
    def handle(self, *args, **options):
        # on récupére les personnes du jour (soit la date de création, de modif plus grand que la veille
        print u"debut d'initialisation"
        for etape in Etape.objects.filter(etpgerercge__cod_cmp='034'):
            e = SettingsEtapeFoad.objects.get_or_create(cod_etp=etape.cod_etp, etape_ptr=etape)[0]
            e.lib_etp = etape.settingsetape.label
            e.save()
            i = EtapeMpttModel.objects.get_or_create(etape=e)[0]
            i.lib_etp = e.lib_etp
            i.save()
        print "fin initialisation"






