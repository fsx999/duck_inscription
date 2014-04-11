# coding=utf-8
from __future__ import unicode_literals
from django.contrib import admin
from django.contrib.contenttypes.generic import GenericTabularInline
from django.contrib.sites.models import Site
from django_xworkflows.xworkflow_log.models import TransitionLog
from duck_inscription.models import SettingAnneeUni, SettingsEtape, DiplomeEtape, ListeDiplomeAces, Wish


class WorkFlowWish(GenericTabularInline):
    model = TransitionLog
    ct_fk_field = 'content_id'
    extra = 0

class WishAdmin(admin.ModelAdmin):
    inlines = [WorkFlowWish]


class ListeDiplomeAcesInline(admin.TabularInline):
    model = ListeDiplomeAces
    extra = 1


class EtapeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'diplome')
    inlines = [ListeDiplomeAcesInline]
    fieldsets = (
        ("Description", {
            'fields': ('cod_etp', 'label', 'diplome', 'label_formation')

        }),
        ("Equivalence", {
            'classes': ('collapse',),
            'fields': ('required_equivalence', 'date_ouverture_equivalence', 'date_fermeture_equivalence',
                       'document_equivalence')
        }),
        ("Candidature", {
            'classes': ('collapse',),
            'fields': ('date_ouverture_candidature', 'date_fermeture_candidature', 'document_candidature')
        }),

    )

admin.site.register(SettingAnneeUni)
admin.site.register(SettingsEtape, EtapeAdmin)
admin.site.register(DiplomeEtape)
admin.site.register(Site)
# admin.site.register(ListeDiplomeAces)
admin.site.register(Wish, WishAdmin)
