# coding=utf-8
from __future__ import unicode_literals
from datetime import date, datetime
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
import unicodedata
from django_xworkflows.xworkflow_log.models import TransitionLog
from django_apogee.models import Departement, Pays, SitFam, SitMil, TypHandicap, TypHebergement, BacOuxEqu, AnneeUni, \
    ComBdi, Etablissement, MentionBac, CatSocPfl, TypeDiplomeExt, SituationSise, QuotiteTra, DomaineActPfl, SitSociale, \
    RegimeParent, MtfNonAflSso
from django_xworkflows import models as xwf_models

class IndividuWorkflow(xwf_models.Workflow):
    states = (
        ('first_connection', 'Première connexion'),
        ('code_etu_manquant', 'Code etudiant manquant'),
        ('individu', 'Individu'),
        ('adresse', 'Adresse'),
        ('recap', 'Recapitulatif'),
        ('accueil', 'Accueil'),
    )

    transitions = (
        ('modif_individu', ('first_connection', 'code_etu_manquant', 'recap'), 'individu'),
        ('first_connection', 'individu', 'first_connection'),
        ('modif_adresse', ('individu', 'recap'), 'adresse'),
        ('recap', 'adresse', 'recap'),
        ('accueil', 'recap', 'accueil'),
        ('code_etud_manquant', 'individu', 'code_etu_manquant'),
    )
    initial_state = 'first_connection'

@python_2_unicode_compatible
class Individu(xwf_models.WorkflowEnabled, models.Model):
    state = xwf_models.StateField(IndividuWorkflow)
    code_opi = models.IntegerField(unique=True, null=True)
    """
    C'est la classe qui gère l'entité individu de base
    """

    GENDER_CHOICES = (
        ('M', 'Homme'),
        ('F', 'Femme'),
    )
    user = models.OneToOneField(User, null=True)
    last_name = models.CharField("Nom patronymique", max_length=30, null=True)
    common_name = models.CharField("Nom d'époux", max_length=30, null=True,
                                   blank=True)
    first_name1 = models.CharField("Prénom", max_length=30)
    first_name2 = models.CharField("Deuxième prénom", max_length=30, null=True,
                                   blank=True)
    first_name3 = models.CharField("Troisième prénom", max_length=30, null=True,
                                   blank=True)
    student_code = models.IntegerField("Code étudiant", max_length=8, null=True,
                                       blank=True, default=None)
    personal_email = models.EmailField("Email", unique=True, null=True)
    personal_email_save = models.EmailField("Email", null=True, blank=True)
    date_registration_current_year = models.DateTimeField(auto_now_add=True)
    sex = models.CharField(u'sexe', max_length=1, choices=GENDER_CHOICES, null=True)
    birthday = models.DateField('date de naissance', null=True)
    code_pays_birth = models.ForeignKey(
        to=Pays,
        verbose_name=u"Pays de naissance",
        related_name=u"pays_naissance",
        default=None,
        null=True
    )
    code_departement_birth = models.ForeignKey(
        verbose_name=u"Département de naissance",
        to=Departement,
        null=True,
        blank=True,
    )
    town_birth = models.CharField(
        verbose_name=u'Ville naissance',
        max_length=30,
        null=True,
        blank=True,
    )
    code_pays_nationality = models.ForeignKey(
        verbose_name=u"Nationnalité",
        to=Pays,
        related_name=u"nationnalite",
        null=True
    )
    valid_ine = models.CharField(
        verbose_name=u"Avez vous un numéro INE",
        max_length=1,
        null=None,
        blank=False,
        default='O',
        choices=(
            ('O', u'J\'ai un numéro INE'),
            ('N', u"Je n'ai pas de numéro INE")
        )
    )
    ine = models.CharField(
        verbose_name=u"INE/BEA",
        max_length=12,
        null=True,
        blank=True,
        help_text=u"Obligatoire si vous en avez un",
    )

    family_status = models.ForeignKey(
        verbose_name=u"Status familial",
        to=SitFam,
        blank=False,
        null=True
    )
    situation_militaire = models.ForeignKey(
        verbose_name=u"Situation militaire",
        to=SitMil,
        blank=True,
        null=True
    )
    type_handicap = models.ForeignKey(
        verbose_name=u"Handicap",
        to=TypHandicap,
        null=True,
        blank=True
    )

    type_hebergement_annuel = models.ForeignKey(TypHebergement, null=True, blank=True, )
    diplome_acces = models.ForeignKey(BacOuxEqu, null=True, blank=True, )
    annee_obtention = models.CharField(u"Année d'obtention",
                                       choices=[(unicode(i), i) for i in range(1900, date.today().year+1)],
                                       max_length=4, null=True,
                                       blank=True,
                                       help_text=u"Année d'obtention du baccalauréat ou équivalent")
    opi_save = models.IntegerField(null=True, blank=True)
    year = models.ForeignKey(AnneeUni, null=True, blank=True)

    class Meta:
        ordering = ['pk']
        app_label = 'duck_inscription'

    def __str__(self):
        return u"%s %s" % (self.last_name, self.first_name1)

    def p28(self):
        e = (date.today() - self.birthday)
        if e.days / 365 > 28:
            return True
        return False

    def save(self, force_insert=False, force_update=False, using=None):
        if not self.code_opi:
            individus = Individu.objects.filter(code_opi__isnull=False).order_by('-code_opi')
            if len(individus) > 0:
                self.code_opi = individus[0].code_opi + 1
            else:
                self.code_opi = 7700000
        return super(Individu, self).save(force_insert, force_update, using)

    @models.permalink
    def get_absolute_url(self):
        return self.state.name,

    @property
    def transitions_logs(self):
        return TransitionLog.objects.filter(content_id=self.id).order_by('timestamp')

    def droit_univ(self):
        if self.dossier_inscription.situation_sociale.pk != 'NO':
            return False
        return True

    def need_secu(self):
        if self.p28() or self.dossier_inscription.affiliation_parent or\
                self.dossier_inscription.non_affiliation or self.dossier_inscription.situation_sociale.pk != 'NO':
            return False
        else:
            return True


class AdresseIndividu(models.Model):
    """c'est l'addresse de l'étudiant
    aussi bien l'adresse étrangère que française
    """
    CHOICES = (
        ('1', 'OPI'),
        ('2', 'Fixe'),
    )
    listed_number = models.CharField(u'Numero de teléphone :', max_length=15)
    #obligatoire
    individu = models.ForeignKey(u'Individu', related_name='adresses')
    code_pays = models.ForeignKey(Pays, verbose_name='Pays :')
    label_adr_1 = models.CharField(u'Adresse :', max_length=32, null=False)
    label_adr_2 = models.CharField(u"Suite de l'adresse :", max_length=32,
                                   null=True, blank=True)
    label_adr_3 = models.CharField(u"Suite de l'adresse :", max_length=32,
                                   null=True, blank=True)
    com_bdi = models.ForeignKey(ComBdi, null=True, blank=True)
    label_adr_etr = models.CharField(u"Code postal et ville étrangère :",
                                     #                                     help_text=u"Complément adresse",
                                     max_length=32, null=True, blank=True)
    type = models.CharField(max_length=1, choices=CHOICES)

    def __unicode__(self):
        if self.type == '1':
            return 'Annuelle'
        else:
            return 'Fixe'

    def get_full_adresse(self):
        response = '<ul style="list-style-type: none;"><li>'
        line = "<li>%s</li>"
        if self.label_adr_1:
            response += self.label_adr_1
        if self.label_adr_2:
            response += " " + self.label_adr_2
        if self.label_adr_3:
            response += " " + self.label_adr_3 + '</li>'
        if self.com_bdi:
            response += "<li>" + self.com_bdi.cod_bdi + " " + self.com_bdi.lib_ach + '</li>'
        if self.label_adr_etr:
            response += "<li>" + self.label_adr_etr + '</li>'
        response += line % (self.code_pays.lib_pay,)
        response += "</ul>"
        return response

    def get_full_adresse_simple(self):
        response = ''

        if self.label_adr_1:
            response += self.label_adr_1
        if self.label_adr_2:
            response += " " + self.label_adr_2
        if self.label_adr_3:
            response += " " + self.label_adr_3
        if self.com_bdi:
            response += " " + self.com_bdi.cod_bdi + " " + self.com_bdi.lib_ach
        if self.label_adr_etr:
            response += " " + self.label_adr_etr
        response += " " + self.code_pays.lib_pay
        return response

    def save(self, *args, **kwargs):
        if self.label_adr_1:
            self.label_adr_1 = unicodedata.normalize('NFKD', self.label_adr_1.strip()).encode('ascii', 'ignore')
        if self.label_adr_2:
            self.label_adr_2 = unicodedata.normalize('NFKD', self.label_adr_2.strip()).encode('ascii', 'ignore')
        if self.label_adr_3:
            self.label_adr_3 = unicodedata.normalize('NFKD', self.label_adr_3.strip()).encode('ascii', 'ignore')
        if self.label_adr_etr:
            self.label_adr_etr = unicodedata.normalize('NFKD', self.label_adr_etr.strip()).encode('ascii', 'ignore')
        if self.listed_number:
            self.listed_number = self.listed_number.strip()

        super(AdresseIndividu, self).save(*args, **kwargs)

    class Meta:
        app_label = 'duck_inscription'

ANNEE = (('', '------'),) + tuple([(x, x) for x in range(1920, datetime.today().year)])
ANNEE_P8 = (('', 'Jamais'),) + tuple([(x, x) for x in range(2000,
                                                            datetime.today().year)])
ANNEE_INSCRIPTION = (('', 'Jamais'),) + tuple([(x, x) for x in range(1920, datetime.today().year)])

PRECEDENT = 0
TITLE = 1
NEXT = 2


class DossierInscription(models.Model):
    class Meta:
        verbose_name = "Dossier d'inscription"
        verbose_name_plural = "Dossiers d'inscription"
        app_label = 'duck_inscription'

    liste_etapes = {
        'scolarite': [None,
                      u"Votre scolarité dans l’enseignement supérieur FRANÇAIS ", 'info_bac'],
        'info_bac': ['scolarite',
                     u"Baccalauréat ou équivalence", 'cat_soc'],
        'cat_soc': ['scolarite',  u"Catégorie socio professionnelle", 'dernier_eta'],
        'dernier_eta': ['cat_soc', u"Dernier établissement fréquenté", 'situation_sise'],
        'situation_sise': ["dernier_eta", "Situation durant l'année %i-%i" % (date.today().year - 1, date.today().year),
                           'etablissement_sise'],
        'etablissement_sise': ["situation_sise", u"Etablissement de l'année précédente", 'eta_dernier_dip'],
        'eta_dernier_dip': ["etablissement_sise",  u"Dernier diplôme obtenu", 'test_autre_eta'],
        'test_autre_eta': ['eta_dernier_dip', u"Autre établissement d'enseignement pour l'année en cours", 'autre_eta'],
        'autre_eta': ['test_autre_eta', u"Autre établissement d'enseignement pour l'année en cours",
                                        'situation_sociale'],
        'situation_sociale': ['autre_eta', u"Situation sociale", 'securite_sociale'],
        'securite_sociale': ['situation_sociale', u"Affiliation à la sécurité sociale",  'num_secu'],
        'num_secu': ['securite_sociale', u"Numéro securité sociale", 'recapitulatif'],
        'recapitulatif': ['num_secu', u"Récapitulatif", None]

    }

    individu = models.OneToOneField(Individu, related_name="dossier_inscription")

    annee_premiere_inscription_p8 = models.CharField(null=True, max_length=4, blank=True)
    annee_premiere_inscription_enseignement_sup_fr = models.CharField(null=True, max_length=4)
    annee_premiere_inscription_universite_fr = models.CharField(null=True, max_length=4, blank=True)
    premier_universite_fr = models.ForeignKey(Etablissement, null=True, default=None,
                                              related_name="premiere_universite_fr", blank=True)
    bac = models.ForeignKey(BacOuxEqu, null=True, blank=True)
    annee_bac = models.CharField(u"Année d'obtention",
                                 choices=[(unicode(i), i) for i in range(1900, date.today().year+1)],
                                 max_length=4, null=True,
                                 blank=True,
                                 help_text=u"Année d'obtention du baccalauréat ou équivalent")
    mention_bac = models.ForeignKey(MentionBac, null=True)
    etablissement_bac = models.ForeignKey(Etablissement, related_name="etablissement_bac", null=True)

    annee_dernier_etablissement = models.CharField(null=True, max_length=4, blank=True)
    annee_derniere_inscription_universite_hors_p8 = models.CharField(null=True, max_length=4, blank=True)
    dernier_etablissement = models.ForeignKey(Etablissement, related_name="dernier_etablissement", null=True)

    sise_annee_precedente = models.ForeignKey(SituationSise, verbose_name="size_annee_precedente", null=True)
    etablissement_annee_precedente = models.ForeignKey(Etablissement,
                                                       related_name="etablissement_annee_precedente", null=True)

    type_dernier_diplome = models.ForeignKey(TypeDiplomeExt, null=True)
    annee_dernier_diplome = models.CharField(null=True, max_length=4)
    etablissement_dernier_diplome = models.ForeignKey(Etablissement, related_name="etablissement_dernier_diplome",
                                                      null=True)

    autre_eta = models.NullBooleanField(null=True)
    autre_etablissement = models.ForeignKey(Etablissement, related_name="autre_etablissement", null=True,
                                            blank=True)

    cat_soc_etu = models.ForeignKey(CatSocPfl, related_name="cat_soc_etu", null=True)
    cat_soc_chef_famille = models.ForeignKey(CatSocPfl, related_name="cat_soc_chef_famille", null=True)
    cat_soc_autre_parent = models.ForeignKey(CatSocPfl, related_name="cat_soc_autre_parent", null=True,
                                             blank=True)
    sportif_haut_niveau = models.BooleanField("sportif haut niveau", default=False)
    quotite_travail = models.ForeignKey(QuotiteTra, null=True, blank=True)
    cat_travail = models.ForeignKey(DomaineActPfl, null=True, blank=True)
    etape = models.CharField(max_length=20, default="scolarite")

    situation_sociale = models.ForeignKey(SitSociale, default='NO', null=True, blank=True,
                                          related_name="situation_sociale_dossier")
    echelon = models.CharField("Echelon", max_length=2, null=True, blank=True)
    num_boursier = models.CharField("N° de boursier", max_length=13, null=True, blank=True)
    boursier_crous = models.NullBooleanField("Bousier du Crous de l'année précédente", null=True, default=None)
    affiliation_parent = models.ForeignKey(RegimeParent, related_name="affiliation_parent_dossier",
                                           null=True,
                                           blank=True)
    non_affiliation = models.ForeignKey(MtfNonAflSso, related_name="non_affiliation_dossier", null=True,
                                        blank=True)
    centre_payeur = models.CharField(max_length=6, choices=(('LMDE', 'LMDE'), ('SMEREP', 'SMEREP')), null=True,
                                     blank=True)
    num_secu = models.CharField(max_length=15, null=True, blank=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.autre_eta:
            self.autre_etablissement = None
        if self.sise_annee_precedente_id in [u'T', u"U"]:
            self.etablissement_annee_precedente = None
        super(DossierInscription, self).save(force_insert, force_update, using, update_fields)

    def precedente_etape(self):
        if self.liste_etapes[self.etape][PRECEDENT]:
            if self.etape == 'eta_dernier_dip' and self.sise_annee_precedente.cod_sis in [u'T', u"U"]:
                self.etape = 'situation_sise'
            elif self.etape == 'situation_sociale' and not self.autre_eta:
                self.etape = 'test_autre_eta'
            elif self.etape == 'recapitulatif' and self.individu.p28():
                self.etape = 'situation_sociale'
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
        return 'duck_inscription/individu/dossier_inscription/%s.html' % self.etape

    def title(self):
        return self.liste_etapes[self.etape][TITLE]

    def next_etape(self):
        if self.liste_etapes[self.etape][NEXT]:
            if self.etape == 'situation_sise' and self.sise_annee_precedente.cod_sis in [u'T', u"U"]:
                self.etape = "eta_dernier_dip"
            elif self.etape == 'test_autre_eta' and not self.autre_eta:
                self.etape = 'situation_sociale'
            elif self.etape == 'situation_sociale' and self.individu.p28():
                self.etape = 'recapitulatif'
            else:
                self.etape = self.liste_etapes[self.etape][NEXT]

            self.save()
            return True
        return False

    def __unicode__(self):
        return u"%s %s %s" % (self.individu.code_opi, self.individu.last_name, self.individu.first_name1)
