# coding=utf-8
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django_apogee.models import AnneeUni, Etape

from django.db import models
from duck_inscription.managers import SettingAnneeUniManager


@python_2_unicode_compatible
class SettingAnneeUni(AnneeUni):
    inscription = models.BooleanField(default=False)
    objects = SettingAnneeUniManager()

    class Meta:
        app_label = 'duck_inscription'
        verbose_name = 'Setting année universitaire'
        verbose_name_plural = u'Settings année universitaire'

    def __str__(self):
        if self.inscription:
            inscription = 'inscription ouverte'
        else:
            inscription = 'inscription fermée'
        return '{} {}'.format(self.cod_anu, inscription)


@python_2_unicode_compatible
class SettingsEtape(Etape):
    label = models.CharField('Label', max_length=120, null=True)
    diplome = models.ForeignKey('DiplomeEtape', null=True, blank=True)

    class Meta:
        app_label = 'duck_inscription'
        verbose_name = 'Settings Etape'
        verbose_name_plural = 'Settings Etapes'

    def __str__(self):
        return self.label or ""


@python_2_unicode_compatible
class DiplomeEtape(models.Model):
    label = models.CharField('Label web', max_length=120, null=True)

    class Meta:
        app_label = 'duck_inscription'
        verbose_name_plural = 'Diplomes'
        verbose_name = 'Diplômes'

    def __str__(self):
        return self.label or ''
