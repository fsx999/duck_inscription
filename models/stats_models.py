# coding=utf-8
from __future__ import unicode_literals
from django_apogee.models import Etape
from duck_inscription.models import SettingAnneeUni
from django.db import models
__author__ = 'paulguichon'


class StatModel(models.Model):
    etape = models.ForeignKey(Etape)
    cod_anu = models.ForeignKey(SettingAnneeUni)
    equi_effectue = models.IntegerField(null=True)
    equi_reception = models.IntegerField(null=True)
    equi_refuse = models.IntegerField(null=True)
    equi_traite = models.IntegerField(null=True)
    candidature_effectue = models.IntegerField(null=True)
    candidature_reception = models.IntegerField(null=True)
    candidature_refuse = models.IntegerField(null=True)
    candidature_accepte = models.IntegerField(null=True)
    inscription_effectue = models.IntegerField(null=True)
    inscription_reception = models.IntegerField(null=True)
    inscription_incomplet = models.IntegerField(null=True)
    inscription_complet = models.IntegerField(null=True)
    inscription_opi = models.IntegerField(null=True)
    inscription_attente = models.IntegerField(null=True)

    class Meta:
        verbose_name_plural = 'statistiques'
        verbose_name = 'statistique'


class StatModelManager(models.Manager):

    def create_stat(self, etape, cod_anu):
        stat = self.get_or_create(etape=etape, cod_anu=cod_anu)[0]
        stat_parcours = etape.stat_parcours_dossier()
        # stat_suivi = etape.
        stat.equi_effectue = etape