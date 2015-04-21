from django_apogee.utils import make_etudiant_password
from duck_utils.utils import email_ied

__author__ = 'paulguichon'
# -*- coding: utf-8 -*-
from django.conf import settings
from django_apogee.models import AnneeUni, VersionEtape as VersionEtapeApogee, EtpGererCge, Etape, InsAdmEtp
from duck_inscription.models import SettingAnneeUni, SettingsEtape, Wish, InscriptionUser, Individu
from django.core.management.base import BaseCommand
APOGEE_CONNECTION = getattr(settings, 'APOGEE_CONNECTION', 'oracle')


class Command(BaseCommand):
    def handle(self, *args, **options):
        for ins in InsAdmEtp.inscrits.all():
            ind = ins.cod_ind
            cod_etu = ind.cod_etu
            i, create = InscriptionUser.objects.get_or_create(username=cod_etu, email=email_ied(ind))

            i.set_password(make_etudiant_password(cod_etu))
            i.save()
            individu = Individu.objects.get_or_create(user=i, personal_email=i.email)[0]
            individu.last_name = ind.lib_nom_pat_ind
            individu.common_name = ind.lib_nom_usu_ind
            individu.first_name1 = ind.lib_pr1_ind
            individu.first_name2 = ind.lib_pr2_ind
            individu.first_name3 = ind.lib_pr3_ind
            individu.student_code = ind.cod_etu
            individu.sex = ind.cod_sex_etu
            individu.birthday = ind.date_nai_ind
            individu.save()
        print InscriptionUser.objects.count()