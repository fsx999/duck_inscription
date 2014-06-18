# coding=utf-8
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from duck_inscription.models import SettingsEtape


class SettingsUser(models.Model):
    user = models.OneToOneField(User, related_name='setting_user')
    etapes = models.ManyToManyField(SettingsEtape, related_name='etapes')

    class Meta:
        app_label = 'duck_inscription'
