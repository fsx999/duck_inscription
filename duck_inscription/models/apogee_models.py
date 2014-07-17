# coding=utf-8
from __future__ import unicode_literals
from django.db.models import Count
from django.utils.encoding import python_2_unicode_compatible
from django_apogee.models import AnneeUni, Etape

from django.db import models
from duck_inscription.managers import SettingAnneeUniManager



@python_2_unicode_compatible
class SettingAnneeUni(AnneeUni):
    inscription = models.BooleanField(default=False)
    objects = SettingAnneeUniManager()
    transfert_pdf = models.FileField(upload_to='document_inscription', null=True, blank=True)
    bourse_pdf = models.FileField(upload_to='document_inscription', null=True, blank=True)
    pieces_pdf = models.FileField(upload_to='document_inscription', null=True, blank=True)

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
    cursus = models.ForeignKey('CursusEtape', null=True, blank=True)
    required_equivalence = models.BooleanField('Equivalence obligatoire', default=True)
    is_inscription_ouverte = models.BooleanField('ouverture campagne inscription', default=True)
    date_ouverture_equivalence = models.DateTimeField(null=True, blank=True)
    date_fermeture_equivalence = models.DateTimeField(null=True, blank=True)
    date_ouverture_candidature = models.DateTimeField(null=True, blank=True)
    date_fermeture_candidature = models.DateTimeField(null=True, blank=True)
    date_ouverture_inscription = models.DateTimeField(null=True, blank=True)
    date_fermeture_inscription = models.DateTimeField(null=True, blank=True)
    date_fermeture_reinscription = models.DateTimeField(null=True, blank=True)

    label_formation = models.CharField(max_length=120, null=True, blank=True)
    annee = models.ForeignKey(SettingAnneeUni, default=2014)
    document_equivalence = models.FileField(upload_to='document_equivalence',
                                            verbose_name=u"Document d'équivalence", null=True, blank=True)
    document_candidature = models.FileField(upload_to='document_candidature',
                                            verbose_name=u"Document de candidature", null=True, blank=True)
    note_maste = models.BooleanField(default=False)
    path_template_equivalence = models.CharField('Path Template Equivalence', max_length=1000, null=True, blank=True)
    grille_de_equivalence = models.FileField(upload_to='grilles_evaluations', null=True, blank=True,
                                             verbose_name="Grille evaluations")

    droit = models.FloatField(u"Droit", default=186)
    frais = models.FloatField(u"Frais", default=1596)
    nb_paiement = models.IntegerField(u"Nombre paiement", default=3)
    demi_tarif = models.BooleanField(u"Demi tarif en cas de réins", default=False)
    semestre = models.BooleanField(u"Demie année", default=False)

    limite_etu = models.IntegerField(u"Capacité d'accueil", null=True, blank=True)

    class Meta:
        app_label = 'duck_inscription'
        verbose_name = 'Settings Etape'
        verbose_name_plural = 'Settings Etapes'

    def can_demi_annee(self, reins):
        if self.semestre and not reins:
            return True
        return False

    def get_tarif_paiement(self, reins=False, semestre=False):
        tarif = self.frais
        if self.demi_tarif and (reins or semestre):
            tarif /= 2
        return tarif

    def __str__(self):
        result = self.label or ""
        return result

    def stat_parcours_dossier(self):
        from duck_inscription.models import WishParcourTransitionLog
        return dict(WishParcourTransitionLog.objects.filter(wish__etape=self, to_state__in=[
            'ouverture_equivalence',
            'equivalence',
            'candidature'
        ]).values_list('to_state').annotate(Count('to_state')))

    def stat_suivi_dossier(self):
        from duck_inscription.models import WishTransitionLog
        return dict(WishTransitionLog.objects.filter(
            wish__etape=self).values_list('to_state').annotate(Count('to_state')))


@python_2_unicode_compatible
class DiplomeEtape(models.Model):
    label = models.CharField('Label web', max_length=120, null=True)
    is_inscription_ouverte = models.BooleanField('ouverture campagne inscription', default=True)

    class Meta:
        app_label = 'duck_inscription'
        verbose_name_plural = 'Diplomes'
        verbose_name = 'Diplômes'

    def __str__(self):
        return self.label or ''


@python_2_unicode_compatible
class CursusEtape(models.Model):
    label = models.CharField('Label web', max_length=200, null=True)

    class Meta:
        app_label = 'duck_inscription'
        verbose_name_plural = 'Cursus'
        verbose_name = 'Cursus'

    def __str__(self):
        return self.label or ''


@python_2_unicode_compatible
class CentreGestionModel(models.Model):
    centre_gestion = models.CharField('', max_length=3)
    label = models.CharField(max_length=100)

    class Meta:
        verbose_name = u"Centre de gestion"
        verbose_name_plural = u"Centres de gestion"
        app_label = "duck_inscription"

    def __str__(self):
        return unicode(self.label)
