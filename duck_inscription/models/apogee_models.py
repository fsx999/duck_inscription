# coding=utf-8
# 3611 2821
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django_apogee.models.models_apogee import AnneeUni
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
