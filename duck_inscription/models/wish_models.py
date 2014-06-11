# -*- coding: utf-8 -*-
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
from duck_inscription.models import SettingAnneeUni, Individu, SettingsEtape
from django_xworkflows import models as xwf_models
from django.utils.timezone import now
from django.conf import settings
from xhtml2pdf import pdf as pisapdf
from xhtml2pdf import pisa
__author__ = 'paul'


class WishWorkflow(xwf_models.Workflow):
    log_model = 'duck_inscription.WishParcourTransitionLog'
    states = (
        ('creation', 'Création'),
        ('ouverture_equivalence', 'Ouverture equivalence'),
        ('liste_diplome', 'Liste Diplome équivalent'),
        ('demande_equivalence', 'Demande desir équivalence'),
        ('equivalence', 'Dossier équivalence'),
        ('liste_attente_equivalence', 'Dossier en liste attente équivalence'),
        ('ouverture_candidature', 'Ouverture candidature'),
        ('note_master', 'Note master'),
        ('candidature', 'Candidature'),
        ('liste_attente_candidature', 'Dossier en liste attente candidature'),
        ('ouverture_inscription', 'Ouverture inscription')
    )

    transitions = (
        ('ouverture_equivalence', 'creation', 'ouverture_equivalence'),
        ('liste_diplome', 'ouverture_equivalence', 'liste_diplome'),
        ('demande_equivalence', ('creation', 'liste_diplome'), 'demande_equivalence'),
        ('equivalence', ('creation', 'liste_diplome', 'demande_equivalence'), 'equivalence'),
        ('liste_attente_equivalence', ('ouverture_equivalence', 'demande_equivalence'), 'liste_attente_equivalence'),
        ('ouverture_candidature', ('creation', 'ouverture_equivalence', 'equivalence', 'demande_equivalence'),
         'ouverture_candidature'),
        ('note_master', 'ouverture_candidature', 'note_master'),
        ('candidature', ('note_master', 'ouverture_candidature'), 'candidature'),
        ('ouverture_inscription', ('creation', 'ouverture_equivalence', 'ouverture_candidature'),
         'ouverture_inscription'),
    )

    initial_state = 'creation'


class SuiviDossierWorkflow(xwf_models.Workflow):
    log_model = 'duck_inscription.WishTransitionLog'

    states = (
        ('inactif', 'Inactif'),
        ('equivalence_reception', 'Dossier Equivalence receptionné'),
        ('equivalence_complet', 'Dossier Equivalence complet'),
        ('equivalence_incomplet', 'Dossier Equivalence incomplet'),
        ('equivalence_traite', 'Dossier Equivalence traite'),
        ('candidature_reception', 'Dossier Candidature receptionné'),
        ('candidature_complet', 'Dossier Candidature complet'),
        ('candidature_incomplet', 'Dossier Candidature incomplet'),
        ('candidature_traite', 'Dossier Candidature traite'),
        ('inscription_reception', 'Dossier inscription receptionné'),
        ('inscription_complet', 'Dossier inscription complet'),
        ('inscription_incomplet', 'Dossier inscription incomplet'),
        ('inscription_traite', 'Dossier inscription traite'),
    )

    initial_state = 'inactif'
    transitions = (
        ('equivalence_receptionner', ('inactif', 'equivalence_incomplet'), 'equivalence_reception'),
        ('equivalence_incomplet', 'equivalence_reception', 'equivalence_incomplet'),
        ('equivalence_complet', ('equivalence_reception', 'equivalence_incomplet'), 'equivalence_complet'),
        ('equivalence_traite', 'equivalence_complet', 'equivalence_traite'),
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
#     """
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
#     def has_diplome(self):
#         if self.diplome_step.count() == 0:
#             return False
#         else:
#             return True
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
#     def stat_pal(self):
#         resultat = {}
#         annee = AnneeEnCour.objects.get(ouverte_inscription=True)
#         wishes = self.wish_set.filter(annee=annee)
#         if not self.no_equivalence:
#             resultat['nb_equivalence'] = wishes.filter(etape='equivalence').count()
#             resultat['nb_equivalence_reception'] = wishes.filter(
#                 etapedossier__etape__name='equivalence_reception').count()
#             resultat['nb_equivalence_traite'] = wishes.filter(etapedossier__etape__name='equivalence_traite').count()
#             resultat['nb_equivalence_en_cours'] = resultat['nb_equivalence_reception'] - resultat['nb_equivalence_traite']
#         if self.candidature:
#             resultat['nb_candidature'] = wishes.filter(etape='candidature').count()
#             resultat['nb_candidature_reception'] = wishes.filter(etapedossier__etape__name='candidature_reception').count()
#             nb_candidature_refuse = wishes.filter(etapedossier__etape__name='candidature_refuse').count()
#             nb_candidature_accepte = wishes.filter(etapedossier__etape__name='candidature_traite').count()
#             resultat['nb_candidature_accepte'] = nb_candidature_accepte
#             resultat['nb_candidature_traite'] = nb_candidature_refuse + nb_candidature_accepte
#             resultat['nb_candidature_en_cours'] = resultat['nb_candidature_reception'] - resultat['nb_candidature_traite']
#         return resultat
#
#     def stat(self):
#         resultat = {}
#         #        wish = self.wish_set.all()
#         annee = AnneeEnCour.objects.get(ouverte_inscription='O')
#         etapes = self.wish_set.filter(annee=annee).values_list('etape', 'is_reins')
#         d = {}
#         a = {}
#         [d.__setitem__(item[0], 1 + d.get(item[0], 0)) for item in etapes]
#         [a.__setitem__(item[0], 1 + a.get(item[0], 0)) for item in etapes if item[1] is True]
#         #        etape = Etape.objects.get(name="inscription_reception")
#         resultat['nb_voeu'] = self.wish_set.filter(annee=annee).count()
#         resultat['nb_reins'] = a.get('inscription', 0)
#         resultat['nb_inscription'] = d.get('inscription', 0)
#         resultat['nb_primo_inscription'] = resultat['nb_inscription'] - resultat['nb_reins']
#
#         resultat['nb_dossier_inscription_reception'] = EtapeDossier.objects.filter(etape__name="inscription_reception",
#                                                                                    wish__step=self,
#                                                                                    wish__annee=annee).count()
#         resultat['nb_dossier_reins_reception'] = EtapeDossier.objects.filter(etape__name="inscription_reception",
#                                                                              wish__step=self,
#                                                                              wish__is_reins=True,
#                                                                              wish__annee=annee).count()
#         resultat['nb_dossier_primo_reception'] = resultat['nb_dossier_inscription_reception'] - resultat[
#             'nb_dossier_reins_reception']
#         resultat['nb_dossier_complet'] = EtapeDossier.objects.filter(etape__name="inscription_complet",
#                                                                      wish__step=self,
#                                                                      wish__annee=annee).count()
#         resultat['nb_dossier_reins_complet'] = EtapeDossier.objects.filter(etape__name="inscription_complet",
#                                                                            wish__step=self, wish__is_reins=True,
#                                                                            wish__annee=annee
#                                                                            ).count()
#         resultat['nb_dossier_primo_complet'] = resultat['nb_dossier_complet'] - resultat['nb_dossier_reins_complet']
#         resultat['nb_inscription_incomplet'] = EtapeDossier.objects.filter(etape__name="inscription_incomplet",
#                                                                            wish__step=self,
#                                                                            wish__annee=annee).count()
#         resultat['nb_liste_attente'] = self.wish_set.filter(etape="liste_attente_inscription",
#                                                             annee=annee).count()
#         resultat['nb_inscription_fp'] = self.wish_set.filter(etape="inscription",
#                                                              centre_gestion__centre_gestion='fp',
#                                                              annee=annee).count()
#
#         return resultat
#
#     def stat_apogee(self):
#         resultat = {}
#         #        wish = self.wish_set.all()
#
#         try:
#             resultat['nb_dossier_apogee'] = INS_ADM_ETP.inscrits.filter(COD_ETP=self.name).count()
#             resultat['nb_dossier_fp'] = INS_ADM_ETP.inscrits.filter(COD_ETP=self.name, COD_CGE='FPE').count()
#             resultat['nb_dossier_ied'] = INS_ADM_ETP.inscrits.filter(COD_ETP=self.name, COD_CGE='IED').count()
#
#         except DatabaseError:
#             resultat['nb_dossier_apogee'] = u"Apogée indisponible"
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
    centre_gestion = models.ForeignKey(CentreGestion, null=True, blank=True)
    is_reins = models.NullBooleanField(default=None, blank=True)

    date_validation = models.DateTimeField(null=True, blank=True)
    state = xwf_models.StateField(WishWorkflow)
    suivi_dossier = xwf_models.StateField(SuiviDossierWorkflow)

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
        elif self.etape.date_fermeture_equivalence <= now():  # équi ferme
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

    def is_reins_formation(self):
        if self.is_reins is None:
            diplomes = self.etape.diplome.settingsetape_set.all().values_list('pk', flat=True)
            if self.individu.student_code:
                self.is_reins = InsAdmEtp.objects.filter(cod_ind__cod_etu=self.individu.student_code, cod_etp__in=diplomes).count() != 0
            else:
                self.is_reins = False
            self.save()
        return self.is_reins

    def envoi_email_reception(self):
        if self.state.name == "equivalence":
            etape = u"d'équivalence"

        elif self.state.name == "candidature":
            etape = u"de candidature"
        elif self.etape == u"inscription":
            etape = u"d'inscripiton"
        else:
            raise Exception(u"Etape inconnu")
        site = settings.INSCRIPTION_URL
        template = Mail.objects.get(name='email_reception')
        if settings.DEBUG:
            email_destination = ("paul.guichon@iedparis8.net",)
        else:
            email_destination = (self.individu.personal_email,)

        mail = template.make_message(
            context={'site': site, 'etape': etape},
            recipients=email_destination
        )
        mail.send()

    @property
    def transitions_logs(self):
        return TransitionLog.objects.filter(content_id=self.code_dossier).order_by('timestamp')
    # def not_place(self):
    #     if self.step.limite_etu and not self.is_ok and not self.place_dispo():
    #         return True
    #     return False
    #
    # def place_dispo(self):
    #     if self.step.limite_etu:
    #         nb = self.step.limite_etu-self.step.wish_set.filter(date_validation__isnull=False, annee=self.annee).count()
    #         if nb < 0:
    #             nb = 0
    #     else:
    #         nb = 0
    #     return nb
    #
    # def rang(self):
    #     rang = self.step.wish_set.filter(date_validation__lt=self.date_validation,
    #                               etape='liste_attente_inscription',
    #                               annee=self.annee).count() - self.place_dispo()
    #
    #     if rang < 0:
    #         rang = 0
    #     return rang
    #
    # def valide_liste(self):
    #     self.date_validation = datetime.datetime.today()
    #     if self.place_dispo() or not self.step.limite_etu or self.is_reins_formation() or self.is_ok:
    #         self.is_ok = True
    #         self.valide = True
    #     self.save()
    #
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
            pdf.addDocument(pisa.CreatePDF(render_to_string(template, context, context_instance=RequestContext(
                request))))  # on construit le pdf
            #il faut fusionner la suite

        pdf.addFromFile(self.do_pdf(context['url_doc']))
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
            #on verifie si il y a un template pour le model d'equivalence
            # template = "duck_inscription/wish/{}".format(etape.path_template_equivalence)
            template = "duck_inscription/wish/{}".format(self.etape.path_template_equivalence)
            pdf.addFromString(PDFTemplateResponse(request=request,
                                                  context=context,
                                                  template=[template, ]).rendered_content)
            pdf.addFromFile(self.etape.grille_de_equivalence)

    def do_pdf_candi(self, flux, templates, request, context):
        pdf = pisapdf.pisaPDF()
        for template in templates:
            pdf.addDocument(pisa.CreatePDF(render_to_string(template, context, context_instance=RequestContext(
                request))))  # on construit le pdf
            #il faut fusionner la suite

        pdf.addFromFile(self.do_pdf(context['url_doc']))
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
    # def droit_univ(self):
    #     if self.individu.droit_univ():
    #         return self.step.droit
    #     else:
    #         return import_settting.TARIF_MEDICAL
    #
    # def tarif_secu(self):
    #     if self.individu.need_secu():
    #         return import_settting.TARIF_SECU
    #     else:
    #         return 0
    #
    # def date_limite_envoi(self):
    #     if self.is_reins_formation():
    #         return self.step.fin_reins
    #
    #     elif self.step.limite_etu:
    #         date = (self.date_validation or datetime.date.today()) + datetime.timedelta(21)
    #         return date
    #     else:
    #         return self.step.fin_inscription
    #
    # def droit_total(self):
    #     return float(self.droit_univ() + self.tarif_secu())
    #
    # def frais_peda(self):
    #     return self.step.get_tarif_paiement(self.is_reins_formation(), self.demi_annee)
    #
    # def can_demi_annee(self):
    #     return self.step.can_demi_annee(self.is_reins_formation())
    #

    def name_url(self):
        name_url = unicode(self.etape.label)
        return name_url
    #
    @models.permalink
    def get_absolute_url(self):
        return self.state.name, [str(self.pk)]
    #
    # def is_reins_formation(self):
    #     if self.is_reins is None:
    #         self.is_reins = not StudentApogeeValid.objects.filter(student_code=self.individu.student_code,
    #                                                               step__formation=self.step.formation).count() == 0
    #         self.is_ok = True
    #         self.save()
    #     return self.is_reins
    #
    # def dispatch(self):
    #     """
    #     ===========
    #     Le principe
    #     ===========
    #     la méthode appelle la méthode du même nom. C'est le dispacher du systeme.
    #     Pour chaque étape d'un voeu, doit correspondre une fonction ici
    #
    #     """
    #     return getattr(self, self.dispatch_etape)()
    #
    # def orientation_liste_diplome(self):
    #     if self.is_reins_formation():  # il se réinscrit dans le diplôme on pass
    #         self.etape = self.dispatch_etape = "ouverture_paiement"
    #
    #     elif self.step.no_equivalence:  # il n'y a pas d'équivalence
    #         self.etape = self.dispatch_etape = "ouverture_candidature"
    #
    #     elif self.step.has_diplome():  # il y a des diplômes à l'étape
    #         self.etape = "liste_diplome"
    #         self.dispatch_etape = "orientation_demande_equivalence"
    #
    #     else:
    #         self.save()
    #         return self.orientation_demande_equivalence()
    #         #sinon on va en équi
    #     self.save()
    #     return True
    #
    # def orientation_demande_equivalence(self):
    #     #date ouverte
    #     if datetime.date.today() <= self.step.fin_equivalence:
    #         if self.diplome_acces or not self.step.equivalence_obligatoire:
    #             self.etape = self.dispatch_etape = "demande_equivalence_etape"
    #         else:
    #             self.etape = self.dispatch_etape = "ouverture_equivalence"
    #     #date fermé:
    #     elif datetime.date.today() > self.step.fin_equivalence:
    #         if self.diplome_acces or not self.step.equivalence_obligatoire:
    #             self.etape = self.dispatch_etape = "ouverture_candidature"
    #
    #         else:  # il n'a pas de diplome:
    #             self.etape = self.dispatch_etape = "liste_attente_equivalence"
    #
    #     self.save()
    #     return True
    #
    # def demande_equivalence_etape(self):
    #     if self.demande_equivalence:
    #         self.etape = self.dispatch_etape = "ouverture_equivalence"
    #     else:
    #         self.etape = self.dispatch_etape = "ouverture_candidature"
    #     self.save()
    #     return True
    #
    # def ouverture_equivalence(self):
    #     today = datetime.date.today()
    #     if today < self.step.debut_equivalence:  # c'est pas ouvert
    #         return False
    #     if self.step.debut_equivalence <= today < self.step.fin_equivalence:
    #         self.etape = self.dispatch_etape = "equivalence"
    #     elif today > self.step.fin_equivalence and self.step.equivalence_obligatoire and not self.diplome_acces:
    #         self.etape = self.dispatch_etape = "liste_attente_equivalence"
    #     else:
    #         self.etape = self.dispatch_etape = "ouverture_candidature"
    #     self.save()
    #     return True
    #
    # def equivalence(self):
    #     if self.step.candidature:
    #         self.etape = self.dispatch_etape = "candidature"
    #     else:
    #         self.etape = self.dispatch_etape = 'ouverture_paiement'
    #     self.save()
    #     return True
    #
    # def liste_attente_equivalence(self):
    #     if self.step.candidature:
    #         self.etape = self.dispatch_etape = 'candidature'
    #     else:
    #         self.etape = self.dispatch_etape = 'ouverture_paiement'
    #     self.save()
    #     return True
    #
    # def ouverture_candidature(self):
    #     today = datetime.date.today()
    #
    #     if not self.step.candidature:
    #         self.etape = self.dispatch_etape = 'ouverture_paiement'
    #     elif today < self.step.debut_candidature:
    #
    #         return False
    #     elif self.step.debut_candidature <= today < self.step.fin_candidature:
    #         if self.step.note:
    #             self.etape = self.dispatch_etape = "note_master"
    #         else:
    #             self.etape = self.dispatch_etape = 'candidature'
    #
    #     elif today >= self.step.fin_candidature:
    #         self.etape = self.dispatch_etape = "liste_attente_candidature"
    #     else:
    #         return False
    #     self.save()
    #     return True
    #
    # def note_master(self):
    #     self.etape = self.dispatch_etape = "candidature"
    #     self.save()
    #     return True
    #
    # def candidature(self):
    #     self.etape = self.dispatch_etape = "ouverture_paiement"
    #     self.save()
    #     return True
    #
    # def liste_attente_candidature(self):
    #     self.etape = self.dispatch_etape = 'ouverture_paiement'
    #     self.save()
    #     return True
    #
    # def ouverture_paiement(self):
    #     self.dispatch_etape = 'ouverture_paiement'
    #     self.save()
    #     if datetime.date.today() < self.step.debut_inscription:
    #         return False
    #     try:
    #         self.individu.dossier_inscription
    #         if self.individu.dossier_inscription.etape != 'recapitulatif' or\
    #           self.individu.dossier_inscription.dernier_etablissement == None or self.individu.dossier_inscription.etablissement_bac == None:
    #             self.etape = self.dispatch_etape = "dossier_inscription"
    #             self.save()
    #             self.individu.dossier_inscription.etape == 'scolarite'
    #             self.individu.dossier_inscription.save()
    #             return True
    #     except DossierInscription.DoesNotExist:
    #         self.etape = self.dispatch_etape = "dossier_inscription"
    #         self.save()
    #         return True
    #
    #     if self.step.debut_inscription <= datetime.date.today() <= self.step \
    #         .fin_inscription or self.etapes.filter(name="equivalence_traite") or self.etapes \
    #         .filter(
    #             name='candidature_traite') or self.is_reins_formation() or self.is_ok:
    #         self.etape = self.dispatch_etape = "choix_ied_fp"
    #         self.save()
    #         return True
    #     elif self.is_reins_formation() and datetime.date.today() > self.step.fin_reins:
    #         self.etape = self.dispatch_etape = "liste_attente_inscription"
    #         self.save()
    #         return True
    #     elif datetime.date.today() > self.step.fin_inscription:
    #         self.etape = self.dispatch_etape = "liste_attente_inscription"
    #         self.save()
    #         return True
    #
    #     return False
    #
    # def dossier_inscription(self):
    #     self.etape = self.dispatch_etape = "ouverture_paiement"
    #     self.save()
    #     return True
    #
    # def situation_sociale(self):
    #     self.etape = self.dispatch_etape = "ouverture_paiement"
    #     self.save()
    #     return True
    #
    # def choix_ied_fp(self):
    #     if self.centre_gestion:
    #         if self.centre_gestion.centre_gestion == 'ied':
    #             self.etape = self.dispatch_etape = 'droit_universitaire'
    #         else:
    #             self.etape = self.dispatch_etape = 'inscription'
    #         self.save()
    #     return True
    #
    # def droit_universitaire(self):
    #     try:
    #
    #         self.etape = self.dispatch_etape = 'inscription'
    #         self.save()
    #         return True
    #     except AttributeError:
    #         self.etape = self.dispatch_etape = "choix_ied_fp"
    #         self.save()
    #
    #
    # def paiement(self):
    #     pass
    #
    # def orientation_inscription(self):
    #     pass
    #
    # def inscription(self):
    #     pass
    #
    # def liste_attente_inscription(self):
    #     pass

    def __unicode__(self):
        return u"%s %s %s" % (self.individu, self.code_dossier, self.etape)

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


# class EtapeDossier(models.Model):
#     wish = models.ForeignKey(Wish)
#     etape = models.ForeignKey(Etape)
#     date = models.DateField(auto_now_add=True)
#
#     class Meta:
#         db_table = u"pal_wishes_etapes"
#         app_label = "inscription"
#         ordering = ['date']
#
#     def __unicode__(self):
#         return u"%s le %s" % (self.etape, self.date)
#
#
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
# class MoyenPaiementModel(models.Model):
#     """
#     chéque virement etc
#     """
#     type = models.CharField('type paiement', primary_key=True, max_length=3)
#     label = models.CharField('label', max_length=60)
#
#     class Meta:
#         db_table = u'pal_moyen_paiement'
#         verbose_name = u'Moyen de paiement'
#         verbose_name_plural = u'Moyens de paiement'
#         app_label = "inscription"
#
#     def __unicode__(self):
#         return unicode(self.label)
#
#
# class TypePaiementModel(models.Model):
#     """
#     Droit univ ou frais péda
#     """
#     type = models.CharField('type de frais', primary_key=True, max_length=5)
#     label = models.CharField('label', max_length=40)
#
#     class Meta:
#         db_table = u"pal_type_paiement"
#         verbose_name = u"Type de paiement"
#         verbose_name_plural = u"Types de paiement"
#         app_label = "inscription"
#
#     def __unicode__(self):
#         return unicode(self.label)
#
# PRECEDENT = 0
# TITLE = 1
# NEXT = 2
#
#
# class PaiementAllModel(models.Model):
#     moment_paiement = [
#         u"Au moment de l'inscription",
#         u'02/01/14',
#         u'15/02/14'
#     ]
#     liste_etapes = {
#         'droit_univ': [None, u'Droit universitaire', 'choix_demi_annee'],
#         'choix_demi_annee': ['droit_univ', u'Inscription aux semestres', 'nb_paiement'],
#         'nb_paiement': ['choix_demi_annee', u"Choisir le nombre de paiements", 'recapitulatif'],
#         'recapitulatif': ['nb_paiement', u"Récapitulatif", None],
#     }
#     wish = models.OneToOneField(Wish)
#     moyen_paiement = models.ForeignKey(MoyenPaiementModel, verbose_name=u'Votre moyen de paiement :',
#                                        help_text=u"Veuillez choisir un moyen de paiement", null=True)
#     nb_paiement_frais = models.IntegerField(verbose_name=u"Nombre de paiements pour les frais pédagogiques", default=1)
#     etape = models.CharField(max_length=20, default="droit_univ")
#     demi_annee = models.BooleanField(default=False)
#
#     def liste_motif(self):
#         a = []
#         for x in range(self.nb_paiement_frais):
#             chaine = u'IED  %s %s %s %s' % (self.wish.step.name,
#                                                     self.wish.individu.code_opi,
#                                                     self.wish.individu.last_name,
#                                                     str(x+1))
#             a.append(chaine)
#         return a
#
#
#     def range(self):
#         a = []
#         for x in  range(self.nb_paiement_frais):
#             a.append((x, self.moment_paiement[x]))
#         return a
#
#     class Meta:
#         app_label = "inscription"
#
#     def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
#         if self.demi_annee and not self.wish.demi_annee:
#             self.wish.demi_annee = True
#             self.wish.save()
#         super(PaiementAllModel, self).save(force_insert, force_update, using, update_fields)
#
#     def precedente_etape(self):
#         if self.liste_etapes[self.etape][PRECEDENT]:
#             if self.etape == 'nb_paiement' and not self.wish.can_demi_annee():
#                 self.etape = 'droit_univ'
#             else:
#                 self.etape = self.liste_etapes[self.etape][PRECEDENT]
#             self.save()
#             return True
#         return False
#
#     def recap(self):
#         return not self.liste_etapes[self.etape][NEXT]
#
#     def prev(self):
#         return self.liste_etapes[self.etape][PRECEDENT]
#
#     def template_name(self):
#         return 'inscription/wish/%s.html' % self.etape
#
#     def title(self):
#         return self.liste_etapes[self.etape][TITLE]
#
#     def next_etape(self):
#         if self.liste_etapes[self.etape][NEXT]:
#             if self.etape == 'droit_univ' and not self.wish.can_demi_annee():
#                 self.etape = 'nb_paiement'
#             else:
#                 self.etape = self.liste_etapes[self.etape][NEXT]
#             self.save()
#             return True
#         return False
#
#
# class PaiementModel(models.Model):
#     moment_paiement = [
#         u"Au moment de l'inscription",
#         u'01/01/13',
#         u'15/02/13'
#     ]
#     wish = models.ForeignKey(Wish)
#     type = models.ForeignKey(TypePaiementModel)  # droit univ ou frais péda
#
#     moyen_paiement = models.ForeignKey(MoyenPaiementModel, verbose_name=u'Votre moyen de paiement :',
#                                        help_text=u"Veuillez choisir un moyen de paiement")  # chéque ou virement
#     num_paiement = models.IntegerField(default=1)
#
#     etudiant_payeur = models.NullBooleanField(null=True, default=None)
#     autre_payeur = models.TextField(null=True, default=None, blank=True)
#     banque = models.CharField(u'Etablissement bancaire du titulaire du compte', max_length=100, default='')
#
#     # virement
#     etablissement = models.CharField(max_length=100, null=True, default=None, blank=True)
#     guichet = models.CharField(max_length=20, null=True, default=None, blank=True)
#     num_compte = models.CharField(max_length=20, null=True, default=None, blank=True)
#     cle = models.CharField(max_length=4, null=True, default=None, blank=True)
#     #cheque
#     num_cheque = models.CharField(max_length=20, null=True, blank=True)
#
#     def date_paiement(self):
#         return self.moment_paiement[self.num_paiement - 1]
#
#     class Meta:
#         db_table = u'pal_paiement_droit_univ_ied'
#         ordering = ['wish', 'type']
#         verbose_name = u"Paiement"
#         verbose_name_plural = u"Paiments"
#         app_label = "inscription"
#
#     def __unicode__(self):
#         return u"%s %s %s" % (self.wish, self.type, self.num_paiement)  # index humain
#
#     def date_limite_paiement(self):
#         return self.date_paiement()
#
#     def motif(self):
#         code_diplome = self.wish.step.name
#
#         if self.autre_payeur:
#             nom_payeur = self.autre_payeur
#         else:
#             nom_payeur = self.wish.individu.last_name
#         code_opi = self.wish.individu.code_opi
#
#         if self.type.type == 'droit':
#             code_paiement = 0
#         else:
#             code_paiement = self.num_paiement
#
#         chaine = u'IED Etudiant %s %s %s %s' % (code_diplome, code_opi, nom_payeur, code_paiement)
#         return chaine
