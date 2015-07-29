# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.db import models
from mailrobot.models import Mail
from wkhtmltopdf.views import PDFTemplateResponse
from xworkflows import transition, after_transition, before_transition, on_enter_state, transition_check
from django_apogee.models import  InsAdmEtp
from duck_inscription.models import SettingAnneeUni, Individu, SettingsEtape, CentreGestionModel
from django_xworkflows import models as xwf_models
from django.utils.timezone import now
from django.conf import settings
from xhtml2pdf import pdf as pisapdf
from duck_utils.utils import make_multi_pdf, num_page, remove_page_pdf, get_email_envoi

__author__ = 'paul'


class WishWorkflow(xwf_models.Workflow):
    log_model = 'duck_inscription.WishParcourTransitionLog'
    states = (
        ('creation', 'Création'),
        ('ouverture_equivalence', 'Ouverture equivalence'),
        ('liste_diplome', 'Liste diplome équivalent'),
        ('demande_equivalence', 'Demande équivalence'),
        ('equivalence', 'Dossier en équivalence'),
        ('liste_attente_equivalence', 'Dossier en demande liste attente équivalence'),
        ('mis_liste_attente_equi', 'Dossier en liste attente équivalence'),
        ('ouverture_candidature', 'Ouverture candidature'),
        ('note_master', 'Note master'),
        ('candidature', 'Dossier en candidature'),
        ('liste_attente_candidature', 'Dossier en demande liste attente candidature'),
        ('mis_liste_attente_candi', 'Dossier en liste attente candidature'),
        ('ouverture_inscription', 'Ouverture inscription'),
        ('dossier_inscription', 'Dossier inscription'),
        ('dispatch', 'Orientation vers les paiements'),
        ('inscription', 'Dossier en inscription'),
        ('liste_attente_inscription', 'Liste attente inscription'),
        ('auditeur', 'Dossier Auditeur'),
        ('auditeur_traite', 'Dossier Auditeur Traité')
    )

    transitions = (
        ('ouverture_equivalence', 'creation', 'ouverture_equivalence'),
        ('liste_diplome', 'ouverture_equivalence', 'liste_diplome'),
        ('demande_equivalence', ('creation', 'liste_diplome'), 'demande_equivalence'),
        ('equivalence', ('creation', 'liste_diplome', 'demande_equivalence', 'mis_liste_attente_equi'), 'equivalence'),
        ('equivalence_from_attente', 'liste_attente_equivalence', "equivalence"),
        ('liste_attente_equivalence', ('ouverture_equivalence', 'demande_equivalence', 'liste_diplome'),
         'liste_attente_equivalence'),
        ('mis_liste_attente_equi', ('liste_attente_equivalence', 'mis_liste_attente_equi'), 'mis_liste_attente_equi'),
        ('ouverture_candidature', ('creation', 'ouverture_equivalence', 'equivalence', 'demande_equivalence'),
         'ouverture_candidature'),
        ('note_master', 'ouverture_candidature', 'note_master'),
        ('candidature', ('note_master', 'ouverture_candidature', 'liste_attente_candidature', 'mis_liste_attente_candi'), 'candidature'),
        ('liste_attente_candidature', ('ouverture_candidature',), 'liste_attente_candidature'),
        ('mis_liste_attente_candi', ('liste_attente_candidature', 'mis_liste_attente_candi'), 'mis_liste_attente_candi'),
        ('ouverture_inscription_from_equi', ('equivalence', 'liste_attente_equivalence'), 'ouverture_inscription'),
        ('ouverture_inscription', ('creation', 'ouverture_equivalence', 'ouverture_candidature', 'equivalence',
                                   'candidature', 'dossier_inscription'), 'ouverture_inscription'),
        ('dossier_inscription', ('ouverture_inscription',), 'dossier_inscription'),
        ('dispatch', ('dossier_inscription', 'liste_attente_inscription', 'inscription'), 'dispatch'),
        ('inscription', ('dispatch', 'liste_attente_inscription'), 'inscription'),
        ('liste_attente_inscription', ('dispatch', 'inscription'), 'liste_attente_inscription'),
        ('auditeur', 'creation', 'auditeur'),
        ('auditeur_traite', 'auditeur', 'auditeur_traite')
    )

    initial_state = 'creation'


class SuiviDossierWorkflow(xwf_models.Workflow):
    log_model = 'duck_inscription.WishTransitionLog'

    states = (
        ('inactif', 'En attente de reception'),
        ('equivalence_reception', 'Dossier Equivalence receptionné'),
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
        ('candidature_incomplet', ('candidature_reception', 'candidature_complet'), 'candidature_incomplet'),
        ('candidature_traite', ('candidature_complet', 'candidature_refuse'), 'candidature_traite'),
        ('candidature_refuse', ('candidature_reception', 'candidature_incomplet', 'candidature_complet'),
         'candidature_refuse'),

        ('inscription_reception', ('inactif',
                                   'equivalence_traite',
                                   'candidature_complet',
                                   'candidature_traite', 'inscription_incomplet', 'equivalence_reception'
                                   'inscription_incom_r'), 'inscription_reception'),
        ('inscription_incomplet', ('inscription_reception', 'inscription_complet',
                                   'inscription_traite'), 'inscription_incomplet'),
        ('inscription_incomplet_renvoi', ('inscription_reception',
                                          'inscription_complet',
                                          'inscription_traite',),
         'inscription_incom_r'),
        ('inscription_complet', ('inscription_reception', 'inscription_incomplet', ), 'inscription_complet'),
        ('inscription_traite', ('inscription_reception', 'inscription_complet', 'inscription_incomplet',
                                'inscription_refuse', 'inscription_traite'), 'inscription_traite',),
        ('inscription_refuse', ('inscription_reception', 'inscription_complet', 'inscription_incomplet', 'inactif'),
         'inscription_refuse',),
        ('inscription_annule', ('inscription_annule', 'inscription_refuse', 'inscription_reception',
                                'inscription_complet',
                                'inscription_incomplet', 'inactif', 'inscription_incom_r'),
         'inscription_annule')
    )


class WishTransitionLog(xwf_models.BaseTransitionLog):
    wish = models.ForeignKey('Wish', related_name='etape_dossier')
    MODIFIED_OBJECT_FIELD = 'wish'

    class Meta:
        app_label = 'duck_inscription'


class WishParcourTransitionLog(xwf_models.BaseTransitionLog):
    wish = models.ForeignKey('Wish', related_name='parcours_dossier')
    MODIFIED_OBJECT_FIELD = 'wish'

    class Meta:
        app_label = 'duck_inscription'


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
                                                     cod_etp__in=diplomes, cod_anu=2014).count() != 0
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
            raise NameError(u"Etape inconnu")
        site = settings.INSCRIPTION_URL
        template = Mail.objects.get(name='email_reception')
        email = [get_email_envoi(self.individu.user.email)]

        mail = template.make_message(context={'site': site, 'etape': etape}, recipients=email)
        mail.send()

    @property
    def transitions_logs(self):
        reponse = []
        for transition in self.etape_dossier.all().order_by('timestamp'):
            print type(transition.timestamp)
            reponse.append('{} {}'.format(SuiviDossierWorkflow.states[transition.to_state].title,
                           transition.timestamp.strftime('le %d-%m-%Y à %H:%M ')))
        return reponse

    @property
    def transition_etat_dossier(self):
        reponse = []
        for transition in self.parcours_dossier.all().order_by('timestamp'):
            reponse.append('{}'.format(WishWorkflow.states[transition.to_state].title))
        return reponse

    def valide_liste(self):
        self.date_validation = datetime.datetime.today()
        if self.place_dispo() or self.etape.limite_etu is None or self.is_reins_formation() or self.is_ok or self.centre_gestion.centre_gestion == 'fp':
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

    def save(self, force_insert=False, force_update=False, using=None, **kwargs):
        if not self.code_dossier:
            nb = Wish.objects.count()
            if nb != 0:
                self.code_dossier = Wish.objects.all().order_by('-code_dossier')[0].code_dossier + 1
            else:
                self.code_dossier = 10000000

        super(Wish, self).save(force_insert, force_update, using)
        if self.is_reins is None:
            self.is_reins_formation()


    def do_pdf_equi(self, request, context):
        templates = [{'name': "duck_inscription/wish/etiquette.html"},
                    {'name': 'duck_inscription/wish/equivalence_pdf.html',
                     'footer': 'duck_inscription/wish/footer.html'}]

        context['voeu'] = self
        doc_equi = self.etape.document_equivalence.file
        context['num_page'] = num_page(doc_equi)

        return make_multi_pdf(context=context, templates=templates, files=[remove_page_pdf(doc_equi)])

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

    def do_pdf_candi(self, request, context):
        templates = [{'name': "duck_inscription/wish/etiquette.html"},
                {'name': 'duck_inscription/wish/candidature_pdf.html',
                 'footer': 'duck_inscription/wish/footer.html'}]

        context['voeu'] = self
        doc_candi = self.etape.document_candidature.file
        context['num_page'] = num_page(doc_candi)

        return make_multi_pdf(context=context, templates=templates, files=[remove_page_pdf(doc_candi)])

    def do_pdf_pieces_manquantes(self, request, context={}):
        context = context.copy()
        templates = [
            {'name': "duck_inscription/wish/etiquette.html"},
            {'name': "duck_inscription/wish/pieces_manquantes.html"}
        ]
        context['voeu'] = self
        context['is_pieces_manquantes'] = True
        context['pieces_manquantes'] = self.dossier_pieces_manquantes
        return make_multi_pdf(context=context, templates=templates)

    def do_pdf_inscription(self, request, context):
        cmd_option={
            'margin_bottom': '20',

        }
        if self.centre_gestion.centre_gestion != 'fp':
            templates = [
                {'name': "duck_inscription/wish/etiquette.html"},
             {'name': 'duck_inscription/wish/dossier_inscription_pdf.html',
                          'footer': 'duck_inscription/wish/footer.html'},
              ]
        else:
            templates = [
             {'name': 'duck_inscription/wish/dossier_inscription_pdf.html',
                          'footer': 'duck_inscription/wish/footer.html'},
              ]
        try:
            templates.extend(self.paiementallmodel.get_templates())
        except AttributeError:
            pass
        templates.extend([ {'name': 'duck_inscription/wish/autorisation_photo.html'}])

        context['voeu'] = self
        context['wish'] = self
        context['individu'] = self.individu
        try:
            context.update(self.paiementallmodel.get_context())
        except AttributeError:
            pass
        files = []
        try:
            files.append(self.etape.autres.file.file.name,)
        except ValueError:
            pass
        try:
            files.append(self.annee.transfert_pdf.file.file.name)
        except ValueError:
            pass
        try:
            files.append(self.annee.bourse_pdf.file.file.name)
        except ValueError:
            pass
        try:
            files.append(self.annee.pieces_pdf.file.file.name)
        except ValueError:
            pass

        return make_multi_pdf(context=context, templates=templates, files=files, cmd_options=cmd_option)

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
        return self.etape.date_fermeture_inscription

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



