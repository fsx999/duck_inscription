# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from StringIO import StringIO
from PyPDF2 import PdfFileWriter, PdfFileReader
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models
from django.template import RequestContext
from django.template.loader import render_to_string
import django_xworkflows
from django_xworkflows.xworkflow_log.models import TransitionLog
from mailrobot.models import Mail
from wkhtmltopdf.views import PDFTemplateResponse
from xworkflows import transition, after_transition, before_transition, on_enter_state, transition_check
from django_apogee.models import CentreGestion, Diplome, InsAdmEtp
from duck_inscription.models import SettingAnneeUni, Individu, SettingsEtape, CentreGestionModel
from django_xworkflows import models as xwf_models
from django.utils.timezone import now
from django.conf import settings
from xhtml2pdf import pdf as pisapdf
from xhtml2pdf import pisa

__author__ = 'paul'


class WishWorkflow(xwf_models.Workflow):
    log_model = 'duck_inscription.WishParcourTransitionLog'
    states = (
        ('creation', 'Création'), ('ouverture_equivalence', 'Ouverture equivalence'),
        ('liste_diplome', 'Liste Diplome équivalent'), ('demande_equivalence', 'Demande desir équivalence'),
        ('equivalence', 'Dossier en équivalence'),
        ('liste_attente_equivalence', 'Dossier en liste attente équivalence'),
        ('ouverture_candidature', 'Ouverture candidature'), ('note_master', 'Note master'),
        ('candidature', 'Dossier en candidature'),
        ('liste_attente_candidature', 'Dossier en liste attente candidature'),
        ('ouverture_inscription', 'Ouverture inscription'), ('dossier_inscription', 'Dossier inscription'),
        ('choix_ied_fp', 'Choix centre gestion'), ('droit_univ', 'Droit universitaire'),
        ('inscription', 'Dossier en inscription'), ('liste_attente_inscription', 'Liste attente inscription'),
        ('auditeur', 'Dossier Auditeur'),
        ('auditeur_traite', 'Dossier Auditeur Traité')
    )

    transitions = (
        ('ouverture_equivalence', 'creation', 'ouverture_equivalence'),
        ('liste_diplome', 'ouverture_equivalence', 'liste_diplome'),
        ('demande_equivalence', ('creation', 'liste_diplome'), 'demande_equivalence'),
        ('equivalence', ('creation', 'liste_diplome', 'demande_equivalence'), 'equivalence'),
        ('equivalence_from_attente', 'liste_attente_equivalence', "equivalence"),
        ('liste_attente_equivalence', ('ouverture_equivalence', 'demande_equivalence', 'liste_diplome'),
         'liste_attente_equivalence'),
        ('ouverture_candidature', ('creation', 'ouverture_equivalence', 'equivalence', 'demande_equivalence'),
         'ouverture_candidature'),
        ('note_master', 'ouverture_candidature', 'note_master'),
        ('candidature', ('note_master', 'ouverture_candidature', 'liste_attente_candidature'), 'candidature'),
        ('liste_attente_candidature', ('ouverture_candidature',), 'liste_attente_candidature'),
        ('ouverture_inscription_from_equi', ('equivalence', 'liste_attente_equivalence'), 'ouverture_inscription'),
        ('ouverture_inscription', ('creation', 'ouverture_equivalence', 'ouverture_candidature', 'equivalence',
                                   'candidature', 'dossier_inscription'), 'ouverture_inscription'),
        ('dossier_inscription', ('ouverture_inscription',), 'dossier_inscription'),
        ('choix_ied_fp', 'dossier_inscription', 'choix_ied_fp'), ('droit_universitaire', 'choix_ied_fp', 'droit_univ'),
        ('inscription', ('droit_univ', 'choix_ied_fp', 'liste_attente_inscription'), 'inscription'),
        ('liste_attente_inscription', 'inscription', 'liste_attente_inscription'),
        ('auditeur', 'creation', 'auditeur'),
        ('auditeur_traite', 'auditeur', 'auditeur_traite')
    )

    initial_state = 'creation'


class SuiviDossierWorkflow(xwf_models.Workflow):
    log_model = 'duck_inscription.WishTransitionLog'

    states = (
        ('inactif', 'Inactif'), ('equivalence_reception', 'Dossier Equivalence receptionné'),
        ('equivalence_complet', 'Dossier Equivalence complet'),
        ('equivalence_incomplet', 'Dossier Equivalence incomplet'),
        ('equivalence_traite', 'Dossier Equivalence traite'), ('equivalence_refuse', 'Dossier Equivalence refuse'),
        ('candidature_reception', 'Dossier Candidature receptionné'),
        ('candidature_complet', 'Dossier Candidature complet'),
        ('candidature_incomplet', 'Dossier Candidature incomplet'),
        ('candidature_traite', 'Dossier Candidature traite'),
        ('candidature_refuse', 'Dossier Candidature refuse'),
        ('inscription_reception', 'Dossier inscription receptionné'),
        ('inscription_complet', 'Dossier inscription complet'),
        ('inscription_incomplet', 'Dossier inscription incomplet'),
        ('inscription_incom_r', 'Dossier inscription incomplet avec renvoi'),
        ('inscription_traite', 'Remontée OPI effectué'),
        ('inscription_refuse', 'Dossier inscription refusé'),
        ('inscription_annule', 'Dossier inscription annulé'),
    )

    initial_state = 'inactif'
    transitions = (
        ('equivalence_receptionner', ('inactif', 'equivalence_incomplet'), 'equivalence_reception'),
        ('equivalence_incomplet', 'equivalence_reception', 'equivalence_incomplet'),
        ('equivalence_complet', ('equivalence_reception', 'equivalence_incomplet'), 'equivalence_complet'),
        ('equivalence_traite', 'equivalence_complet', 'equivalence_traite'),
        ('equivalece_refuse', ('equivalence_reception', 'equivalence_incomplet', 'equivalence_complet'),
         'equivalence_refuse'),
        ('candidature_reception', ('inactif', 'equivalence_traite', 'candidature_incomplet'), 'candidature_reception'),
        ('candidature_complet', ('candidature_reception', 'candidature_incomplet'), 'candidature_complet'),
        ('candidature_incomplet', 'candidature_reception', 'candidature_incomplet'),
        ('candidature_traite', ('candidature_complet', 'candidature_refuse'), 'candidature_traite'),
        ('candidature_refuse', ('candidature_reception', 'candidature_incomplet', 'candidature_complet'),
         'candidature_refuse'),

        ('inscription_reception',
         ('inactif', 'equivalence_traite', 'candidature_complet', 'candidature_traite', 'inscription_incomplet',
          'inscription_incom_r'),
         'inscription_reception'),
        ('inscription_incomplet', ('inscription_reception', 'inscription_complet',
                                   'inscription_traite'), 'inscription_incomplet'),
        ('inscription_incomplet_renvoi', ('inscription_reception', 'inscription_complet','inscription_traite'),
         'inscription_incom_r'),
        ('inscription_complet', ('inscription_reception', 'inscription_incomplet'), 'inscription_complet'),
        ('inscription_traite', ('inscription_reception', 'inscription_complet', 'inscription_incomplet',
                                'inscription_refuse'), 'inscription_traite',),
        ('inscription_refuse', ('inscription_reception', 'inscription_complet', 'inscription_incomplet', 'inactif'),
         'inscription_refuse',),
        ('inscription_annule', ('inscription_annule', 'inscription_refuse', 'inscription_reception',
                                'inscription_complet',
                                'inscription_incomplet', 'inactif', 'inscription_incom_r'),
         'inscription_annule')
    )


class WishTransitionLog(django_xworkflows.models.BaseTransitionLog):
    wish = models.ForeignKey('Wish', related_name='etape_dossier')
    MODIFIED_OBJECT_FIELD = 'wish'

    class Meta:
        app_label = 'duck_inscription'


class WishParcourTransitionLog(django_xworkflows.models.BaseTransitionLog):
    wish = models.ForeignKey('Wish', related_name='parcours_dossier')
    MODIFIED_OBJECT_FIELD = 'wish'

    class Meta:
        app_label = 'duck_inscription'


# class Step(models.Model):
# """
#     le modéle des étapes
#     """
#     name = models.CharField(u"Code de l'étape", max_length=15, help_text="le code de l'étape", unique=True)
#
#     label = models.CharField(u"Label long", max_length=200, help_text="le nom de l'étape", default="", blank=True)
#     grade = models.ForeignKey(Grade, verbose_name='Diplome', db_column='grade_id', db_index=True,
#                               help_text="le diplome de l'étape")
#     vdi = models.IntegerField(verbose_name="vdi", default='910', blank=True)
#     vet = models.IntegerField(verbose_name="vet", default='910', blank=True)
#     formation = models.CharField(max_length=15)
#     label_formation = models.CharField(verbose_name=u"label formation", max_length=200, default="", blank=True)
#
#     debut_equivalence = models.DateField(u"Date du début de l'équivalence", null=True, blank=True)
#     fin_equivalence = models.DateField(null=True, blank=True)
#     fin_attente_equivalence = models.DateField(null=True, blank=True, default=datetime.date(2012, 06, 30))
#
#     equivalence_obligatoire = models.BooleanField(u"Equivalence obligatoire",
#                                                   help_text=u"Cochez si l'équivalence ne peut pas être facultative",
#                                                   default=False)
#     no_equivalence = models.BooleanField(u"Absence d'équivalence", default=True,
#                                          help_text=u"Cochez s'il n'y a pas d'équivalence pour l'étape")
#     candidature = models.BooleanField(default=False)
#     debut_candidature = models.DateField(u"Date du début de la candidature", null=True, blank=True)
#     fin_candidature = models.DateField(u"Date de fin de la candidature", null=True, blank=True)
#     fin_attente_candidature = models.DateField(null=True, blank=True, default=datetime.date(2012, 10, 30))
#
#     debut_inscription = models.DateField(u"Date du début de l'inscription", default=datetime.date(2012, 07, 06))
#     fin_inscription = models.DateField(u"Date de fin de l'inscription", default=datetime.date(2012, 07, 06))
#     fin_reins = models.DateField(u"Date de fin de réinscription", default=datetime.date(2012, 9, 30))
#     droit = models.FloatField(u"Droit de l'ied", default=186)
#     tarif = models.FloatField(u"Tarif de l'ied", default=1596)
#     nb_paiement = models.IntegerField(u"Nombre paiement", default=3)
#     demi_tarif = models.BooleanField(u"Demi tarif en cas de réins", default=False)
#     semestre = models.BooleanField(u"Demie année", default=False)

#     note = models.BooleanField('Note Master', default=False)
#
#     limite_etu = models.IntegerField(u"Capacité d'accueil", null=True, blank=True)
#
#     def get_tarif_paiement(self, reins=False, semestre=False):
#         tarif = self.tarif
#         if self.demi_tarif and (reins or semestre):
#             tarif /= 2
#         return tarif
#
#     def can_demi_annee(self, reins):
#         if self.semestre and not reins:
#             return True
#         return False
#
#     def __unicode__(self):
#         return self.label
#
#
#     def stat_tarif(self):
#         # resultat = {}
#         resultat = dict(reins=Wish.objects.filter(step=self, is_reins=True,
#                                                   etapes__name='inscription_reception').count())
#         if self.demi_tarif:
#             resultat['reins_tarif'] = resultat['reins'] * self.tarif / 2
#         else:
#             resultat['reins_tarif'] = resultat['reins'] * self.tarif
#         resultat['plein'] = Wish.objects.filter(step=self, is_reins=False, demi_annee=False,
#                                                 etapes__name='inscription_reception').count()
#         resultat['tarif_plein'] = resultat['plein'] * self.tarif
#         resultat['demi_annee'] = Wish.objects.filter(step=self, is_reins=False, demi_annee=True,
#                                                      etapes__name='inscription_reception').count()
#         if self.semestre:
#
#             resultat['tarif_demi_annee'] = resultat['demi_annee'] * self.tarif / 2
#         else:
#             resultat['tarif_demi_annee'] = resultat['demi_annee'] * self.tarif
#         return resultat
#
#     def stat_tarif_previsionnel(self):
#         # resultat = {}
#         resultat = {'nb_reins': INS_ADM_ETP_IED.inscrits.filter(COD_CGE='IED',
#                                                                 COD_ETP=self.name).exclude(NBR_INS_ETP=1).count()}
#         # les reins : les IED qui sont à plus de 1
#
#         if self.demi_tarif:
#             resultat['tarif_reins'] = resultat['nb_reins'] * self.tarif / 2
#         else:
#             resultat['tarif_reins'] = resultat['nb_reins'] * self.tarif
#
#         resultat['nb_primo'] = INS_ADM_ETP_IED.inscrits.filter(COD_CGE='IED',
#                                                                COD_ETP=self.name, NBR_INS_ETP=1).count()
#         resultat['tarif_primo'] = resultat['nb_primo'] * self.tarif
#         resultat['total'] = resultat['tarif_reins'] + resultat['tarif_primo']
#
#         return resultat
#


class Wish(xwf_models.WorkflowEnabled, models.Model):
    code_dossier = models.AutoField('code dossier', primary_key=True)
    individu = models.ForeignKey(Individu, related_name='wishes', null=True)
    etape = models.ForeignKey(SettingsEtape, verbose_name='Etape', null=True)
    date = models.DateField("La date du vœux", auto_now_add=True)
    valide = models.BooleanField(default=False, blank=True)
    diplome_acces = models.ForeignKey('ListeDiplomeAces', default=None, blank=True, null=True,
                                      related_name="diplome_acces")
    annee = models.ForeignKey(SettingAnneeUni, default=2014, db_column='annee')
    centre_gestion = models.ForeignKey(CentreGestionModel, null=True, blank=True)
    is_reins = models.NullBooleanField(default=None, blank=True)
    is_auditeur = models.BooleanField(default=False)

    date_validation = models.DateTimeField(null=True, blank=True)
    state = xwf_models.StateField(WishWorkflow)
    suivi_dossier = xwf_models.StateField(SuiviDossierWorkflow)
    demi_annee = models.BooleanField(default=False, choices=((True, '1'), (False, '0')))

    is_ok = models.BooleanField(default=False)
    date_liste_inscription = models.DateTimeField(null=True, blank=True)

    @on_enter_state('ouverture_equivalence')
    def on_enter_state_ouverture_equivalence(self, res, *args, **kwargs):
        if self.is_reins_formation():
            self.ouverture_inscription()
            return
        if not self.etape.date_ouverture_equivalence:  # il n'y a pas d'équivalence on va en candidature
            self.ouverture_candidature()
        elif self.etape.date_ouverture_equivalence <= now() <= self.etape.date_fermeture_equivalence:  # l'équi est ouverte
            self.liste_diplome()
        elif self.etape.date_fermeture_equivalence <= now() and not self.etape.required_equivalence:
            self.ouverture_candidature()
        elif self.etape.date_fermeture_equivalence <= now():  # équi ferme
            self.liste_diplome()

    @on_enter_state('liste_diplome')
    def on_enter_liste_diplome(self, *args, **kwargs):

        if self.etape.date_ouverture_equivalence:  # ouverture equivalence
            if not self.etape.diplome_aces.count():
                if now() <= self.etape.date_fermeture_equivalence:  # pas de diplome
                    self.demande_equivalence()
                else:
                    self.liste_attente_equivalence()

    @transition_check('liste_diplome')
    def check_liste_diplome(self):
        if self.etape.date_ouverture_equivalence <= now():
            return True
        return False

    @on_enter_state('demande_equivalence')
    def on_enter_state_demande_equivalence(self, res, *args, **kwargs):
        if self.etape.required_equivalence and not self.diplome_acces:  # l'équivalence est obligatoire et il n'y pas de diplome
            if self.etape.date_ouverture_equivalence <= now() <= self.etape.date_fermeture_equivalence:
                self.equivalence()
            else:
                self.liste_attente_equivalence()
        elif self.diplome_acces and now() >= self.etape.date_fermeture_equivalence:
            self.ouverture_candidature()

    @on_enter_state('ouverture_candidature')
    def on_enter_state_ouverture_candidature(self, res, *args, **kwargs):
        if not self.etape.date_ouverture_candidature:  # il n'y a pas de candidature
            self.ouverture_inscription()
        elif self.etape.date_ouverture_candidature <= now() <= self.etape.date_fermeture_candidature:  # l'équi est ouverte
            self.note_master()
        elif self.etape.date_fermeture_candidature <= now():  # équi ferme
            self.liste_attente_candidature()

    @on_enter_state('note_master')
    def on_enter_state_note_master(self, res, *arg, **kwargs):
        if not self.etape.note_maste:
            self.candidature()

    @transition_check('note_master')
    def check_note_master(self):
        if self.etape.date_ouverture_candidature <= now():
            return True
        return False

    @transition_check('dossier_inscription')
    def check_dossier_inscription(self):
        if self.etape.date_ouverture_inscription <= now():
            return True
        return False

    def is_reins_formation(self):
        # if self.is_reins is None:
        diplomes = self.etape.cursus.settingsetape_set.all().values_list('pk', flat=True)
        if self.individu.student_code:
            self.is_reins = InsAdmEtp.objects.filter(cod_ind__cod_etu=self.individu.student_code,
                                                     cod_etp__in=diplomes).count() != 0
        else:
            self.is_reins = False
        self.save()
        return self.is_reins

    def envoi_email_reception(self):
        if self.state.name == "equivalence":
            etape = u"d'équivalence"

        elif self.state.name == "candidature":
            etape = u"de candidature"
        elif self.state.name == u"inscription":
            etape = u"d'inscripiton"
        elif self.state.name == u"auditeur":
            etape = u"d'auditeur"
        else:
            raise Exception(u"Etape inconnu")
        site = settings.INSCRIPTION_URL
        template = Mail.objects.get(name='email_reception')
        if settings.DEBUG:
            email_destination = ("paul.guichon@iedparis8.net", "stefan.ciobotaru@iedparis8.net")
        else:
            email_destination = (self.individu.personal_email,)

        mail = template.make_message(context={'site': site, 'etape': etape}, recipients=email_destination)
        mail.send()

    @property
    def transitions_logs(self):
        return TransitionLog.objects.filter(content_id=self.code_dossier).order_by('timestamp')

    def valide_liste(self):
        self.date_validation = datetime.datetime.today()
        if self.place_dispo() or not self.etape.limite_etu or self.is_reins_formation() or self.is_ok or self.centre_gestion.centre_gestion == 'fp':
            self.is_ok = True
            self.valide = True
        self.save()

    def not_place(self):
        if self.etape.limite_etu and not self.is_ok and not self.place_dispo():
            return True
        return False

    def place_dispo(self):
        if self.etape.limite_etu:
            nb = self.etape.limite_etu - self.etape.wish_set.filter(date_validation__isnull=False,
                                                                    annee=self.annee).count()
            if nb < 0:
                nb = 0
        else:
            nb = 0
        return nb

    # def rang(self):
    #     rang = self.etape.wish_set.filter(date_validation__lt=self.date_validation,
    #                               etape='liste_attente_inscription',
    #                               annee=self.annee).count() - self.place_dispo()
    #
    #     if rang < 0:
    #         rang = 0
    #     return rang

    def save(self, force_insert=False, force_update=False, using=None):
        if not self.code_dossier:
            nb = Wish.objects.count()
            if nb != 0:
                self.code_dossier = Wish.objects.all().order_by('-code_dossier')[0].code_dossier + 1
            else:
                self.code_dossier = 10000000
        if not self.is_reins:
            self.is_reins_formation
        super(Wish, self).save(force_insert, force_update, using)

    def do_pdf_equi(self, flux, templates, request, context):
        pdf = pisapdf.pisaPDF()
        for template in templates:
            pdf.addDocument(pisa.CreatePDF(
                render_to_string(template, context, context_instance=RequestContext(request))))  # on construit le pdf
            #il faut fusionner la suite

        pdf.addFromString(self.do_pdf(context['url_doc']).getvalue())
        self.add_decision_equi_pdf(pdf, request, context)
        pdf.join(flux)
        return flux

    def do_pdf_decision_equi_pdf(self, flux, request, context):
        pdf = pisapdf.pisaPDF()
        self.add_decision_equi_pdf(pdf, request, context)
        pdf.join(flux)
        return flux

    def add_decision_equi_pdf(self, pdf, request, context):
        if self.etape.path_template_equivalence and self.etape.grille_de_equivalence:
            template = "duck_inscription/wish/{}".format(self.etape.path_template_equivalence)
            pdf.addFromString(
                PDFTemplateResponse(request=request, context=context, template=[template, ]).rendered_content)
            pdf.addFromFileName(self.etape.grille_de_equivalence.file.file.name)

    def do_pdf_candi(self, flux, templates, request, context):
        pdf = pisapdf.pisaPDF()
        for template in templates:
            pdf.addDocument(pisa.CreatePDF(
                render_to_string(template, context, context_instance=RequestContext(request))))  # on construit le pdf
            #il faut fusionner la suite

        pdf.addFromString(self.do_pdf(context['url_doc']).getvalue())
        pdf.join(flux)
        return flux

    def do_pdf(self, file):
        """
        retourne un pdf sans la première page
        """
        result = StringIO()
        output = PdfFileWriter()
        input1 = PdfFileReader(file)
        for x in range(1, input1.getNumPages()):
            output.addPage(input1.getPage(x))
        output.write(result)

        return result

    #
    # def save_auditeur(self):
    #     if self.is_auditeur:
    #         pass
    #

    def droit_univ(self):
        if self.individu.droit_univ():
            return self.etape.droit
        else:
            return self.annee.tarif_medical

    def tarif_secu(self):
        if self.individu.need_secu():
            return self.annee.tarif_secu
        else:
            return 0

    def date_limite_envoi(self):
        # if self.is_reins_formation():
        return self.etape.date_fermeture_reinscription
        #
        # elif self.etape.limite_etu:
        #     date = (self.date_validation or datetime.date.today()) + datetime.timedelta(21)
        #     return date
        # else:
        #     return self.etape.date_fermeture_inscription

    def droit_total(self):
        return float(self.droit_univ() + self.tarif_secu())

    def frais_peda(self):
        return self.etape.get_tarif_paiement(self.is_reins_formation(), self.demi_annee)

    def can_demi_annee(self):
        return self.etape.can_demi_annee(self.is_reins_formation())

    def name_url(self):
        if self.is_auditeur:
            name_url = u"{} Auditeur libre".format(self.code_dossier)
        else:
            name_url = u"{}  Code dossier : {}".format(self.etape.label, self.code_dossier)
        return name_url

    @models.permalink
    def get_absolute_url(self):
        return self.state.name, [str(self.pk)]

    def __unicode__(self):
        if self.is_auditeur:
            return u"%s %s" % (self.code_dossier, 'auditeur libre')
        return u"%s %s %s" % (self.individu, self.code_dossier, self.etape)

    def save_opi(self):
        self.individu.save_opi()

    class Meta:
        verbose_name = "Voeu"
        verbose_name_plural = "Voeux"
        app_label = "duck_inscription"

        # def get_etapes_dossier(self):
        #     response = '<div class="well">'
        #     for etape in self.etapedossier_set.all():
        #         response += etape.__unicode__() + '<br/>'
        #     response += '</div>'
        #     return '%s' % (response,)

        # get_etapes_dossier.short_description = 'Etapes du dossier'
        # get_etapes_dossier.allow_tags = True

        # def get_pdf(self):
        #     response = ''
        #     if not self.is_reins_formation() and not self.step.no_equivalence:
        #         url = reverse('impression_equivalence', kwargs={'pk': self.id})
        #         response += '<p><a href="' + url + '" class="btn btn-primary">Imprimer le dossier d\'equivalence</a></p>'
        #     if not self.is_reins_formation() and self.step.candidature:
        #         url = reverse('impression_candidature', kwargs={'pk': self.id})
        #         response += '<p><a href="' + url + '" class="btn btn-primary">Imprimer le dossier de candidature</a></p>'
        #     try:
        #         if self.paiementallmodel:
        #
        #             url = reverse('impression_inscription', kwargs={'pk': self.id})
        #             response += '<p><a href="' + url + '" class="btn btn-primary">Imprimer le dossier d\'inscription</a></p>'
        #     except PaiementAllModel.DoesNotExist:
        #         pass
        #     return response

        # get_pdf.short_description = u'Impression des dossiers'
        # get_pdf.allow_tags = True


class NoteMasterModel(models.Model):
    moyenne_general = models.FloatField(null=True, blank=True)
    note_memoire = models.FloatField(null=True, blank=True)
    note_stage = models.FloatField(null=True, blank=True)
    wish = models.OneToOneField(Wish)

    class Meta:
        app_label = "duck_inscription"


class ListeDiplomeAces(models.Model):
    label = models.CharField("nom du diplome d'acces", max_length=100)
    etape = models.ForeignKey(SettingsEtape, related_name="diplome_aces", null=True)

    def __unicode__(self):
        return self.label

    class Meta:
        db_table = u'pal_liste_diplome_aces'
        verbose_name = u"Liste des diplômes d'accès direct"
        verbose_name_plural = u"Liste des diplômes d'accès direct"
        app_label = "duck_inscription"


#
#
# class StudentApogeeValid(models.Model):
#     step = models.ForeignKey(Step)
#     student_code = models.CharField(max_length=8)
#     cod_cge = models.CharField(max_length=3, default=3)
#
#     class Meta:
#         db_table = u'pal_student_apogee_valid'
#         app_label = "inscription"
#
#
class MoyenPaiementModel(models.Model):
    """
    chéque virement etc
    """
    type = models.CharField('type paiement', primary_key=True, max_length=3)
    label = models.CharField('label', max_length=60)

    class Meta:
        db_table = u'pal_moyen_paiement'
        verbose_name = u'Moyen de paiement'
        verbose_name_plural = u'Moyens de paiement'
        app_label = "duck_inscription"

    def __unicode__(self):
        return unicode(self.label)


class TypePaiementModel(models.Model):
    """
    Droit univ ou frais péda
    """
    type = models.CharField('type de frais', primary_key=True, max_length=5)
    label = models.CharField('label', max_length=40)

    class Meta:
        db_table = u"pal_type_paiement"
        verbose_name = u"Type de paiement"
        verbose_name_plural = u"Types de paiement"
        app_label = "duck_inscription"

    def __unicode__(self):
        return unicode(self.label)


PRECEDENT = 0
TITLE = 1
NEXT = 2


class PaiementAllModel(models.Model):
    moment_paiement = [u"Au moment de l'inscription", u'01/01/15', u'15/02/15']
    liste_etapes = {'droit_univ': [None, u'Droit universitaire', 'choix_demi_annee'],
                    'choix_demi_annee': ['droit_univ', u'Inscription aux semestres', 'nb_paiement'],
                    'nb_paiement': ['choix_demi_annee', u"Choisir le nombre de paiements", 'recapitulatif'],
                    'recapitulatif': ['nb_paiement', u"Récapitulatif", None], }
    wish = models.OneToOneField(Wish)
    moyen_paiement = models.ForeignKey(MoyenPaiementModel, verbose_name=u'Votre moyen de paiement :',
                                       help_text=u"Veuillez choisir un moyen de paiement", null=True)
    nb_paiement_frais = models.IntegerField(verbose_name=u"Nombre de paiements pour les frais pédagogiques", default=1)
    etape = models.CharField(max_length=20, default="droit_univ")
    demi_annee = models.BooleanField(default=False)

    def liste_motif(self):
        a = []
        for x in range(self.nb_paiement_frais):
            chaine = u'IED  %s %s %s %s' % (
            self.wish.etape.cod_etp, self.wish.individu.code_opi, self.wish.individu.last_name, str(x + 1))
            a.append(chaine)
        return a

    def range(self):
        a = []
        for x in range(self.nb_paiement_frais):
            a.append((x, self.moment_paiement[x]))
        return a

    class Meta:
        app_label = "duck_inscription"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.demi_annee and not self.wish.demi_annee:
            self.wish.demi_annee = True
            self.wish.save()
        super(PaiementAllModel, self).save(force_insert, force_update, using, update_fields)

    def precedente_etape(self):
        if self.liste_etapes[self.etape][PRECEDENT]:
            if self.etape == 'nb_paiement' and not self.wish.can_demi_annee():
                self.etape = 'droit_univ'
            else:
                self.etape = self.liste_etapes[self.etape][PRECEDENT]
            self.save()
            return True
        return False

    def recap(self):
        return not self.liste_etapes[self.etape][NEXT]

    def prev(self):
        return self.liste_etapes[self.etape][PRECEDENT]

    def template_name(self):
        return 'duck_inscription/wish/%s.html' % self.etape

    def title(self):
        return self.liste_etapes[self.etape][TITLE]

    def next_etape(self):
        if self.liste_etapes[self.etape][NEXT]:
            if self.etape == 'droit_univ' and not self.wish.can_demi_annee():
                self.etape = 'nb_paiement'
            else:
                self.etape = self.liste_etapes[self.etape][NEXT]
            self.save()
            return True
        return False
