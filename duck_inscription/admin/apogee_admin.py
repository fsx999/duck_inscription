# coding=utf-8
from __future__ import unicode_literals
from django.contrib import admin
from django_xworkflows.xworkflow_log.models import TransitionLog
from duck_inscription.models import SettingAnneeUni, SettingsEtape, DiplomeEtape, ListeDiplomeAces, Wish


admin.site.register(SettingAnneeUni)
admin.site.register(SettingsEtape)
admin.site.register(DiplomeEtape)
admin.site.register(ListeDiplomeAces)
admin.site.register(Wish)
