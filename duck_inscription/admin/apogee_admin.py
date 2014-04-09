# coding=utf-8
from __future__ import unicode_literals
from django.contrib import admin
from duck_inscription.models import SettingAnneeUni, SettingsEtape, DiplomeEtape


admin.site.register(SettingAnneeUni)
admin.site.register(SettingsEtape)
admin.site.register(DiplomeEtape)
