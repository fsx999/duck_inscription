# coding=utf-8
from __future__ import unicode_literals
from django.db import models


class SettingAnneeUniManager(models.Manager):
    @property
    def annee_inscription_en_cours(self):
        """
        :return: annee inscription ouverte ou bien None
        """
        result = self.filter(inscription=True).order_by('-cod_anu')
        if result:
            return result.first()
        else:
            return None
