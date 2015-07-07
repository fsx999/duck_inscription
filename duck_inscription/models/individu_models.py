# coding=utf-8
from __future__ import unicode_literals
from datetime import date, datetime
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.db import models, IntegrityError
import unicodedata
import django_xworkflows
from django_xworkflows.xworkflow_log.models import TransitionLog
from django_apogee.models import Departement, Pays, SitFam, SitMil, TypHandicap, TypHebergement, BacOuxEqu, AnneeUni, \
    ComBdi, Etablissement, MentionBac, CatSocPfl, TypeDiplomeExt, SituationSise, QuotiteTra, DomaineActPfl, SitSociale, \
    RegimeParent, MtfNonAflSso, IndOpi, OpiBac, Individu as IndividuApogee, AdresseOpi, IndBac, InsAdmAnu
from django_xworkflows import models as xwf_models
from django.conf import settings
from duck_inscription.models import SettingAnneeUni
from duck_inscription.models.auth_models import InscriptionUser


class IndividuWorkflow(xwf_models.Workflow):
    log_model = 'duck_inscription.IndividuTransitionLog'
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


class IndividuTransitionLog(django_xworkflows.models.BaseTransitionLog):
    individu = models.ForeignKey('Individu', related_name='etape_dossier')
    MODIFIED_OBJECT_FIELD = 'individu'

    class Meta:
        app_label = 'duck_inscription'


@python_2_unicode_compatible
class Individu(xwf_models.WorkflowEnabled, models.Model):
    """
    Gére les informations factuelles d'un individu
    """
    state = xwf_models.StateField(IndividuWorkflow)
    code_opi = models.IntegerField(unique=True, null=True)
    """
    C'est la classe qui gère l'entité individu de base
    """

    GENDER_CHOICES = (
        ('M', 'Homme'),
        ('F', 'Femme'),
    )
    user = models.OneToOneField(InscriptionUser, null=True)
    last_name = models.CharField("Nom patronymique", max_length=30, null=True)
    common_name = models.CharField("Nom d'époux", max_length=30, null=True,
                                   blank=True)
    first_name1 = models.CharField("Prénom", max_length=30)
    first_name2 = models.CharField("Deuxième prénom", max_length=30, null=True,
                                   blank=True)
    first_name3 = models.CharField("Troisième prénom", max_length=30, null=True,
                                   blank=True)
    student_code = models.IntegerField("Code étudiant", null=True,
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

    annee_obtention = models.CharField(u"Année d'obtention",
                                       choices=[(unicode(i), i) for i in range(1900, date.today().year+1)],
                                       max_length=4, null=True,
                                       blank=True,
                                       help_text=u"Année d'obtention du baccalauréat ou équivalent")
    diplome_acces = models.ForeignKey(BacOuxEqu, null=True, blank=True, )
    opi_save = models.IntegerField(null=True, blank=True)
    year = models.ForeignKey(AnneeUni, null=True, blank=True)

    class Meta:
        ordering = ['pk']
        app_label = 'duck_inscription'

    def __str__(self):
        return u"%s %s %s %s" % (self.last_name, self.common_name, self.first_name1, self.first_name2)

    def numeros_telephones(self):
        """
        :return un paragraphe html avec les numéros de téléphones
        """
        html_reponse = "<p>"
        for adresse in self.adresses.all():
            html_reponse += "{}<br>".format(adresse.listed_number)
        return html_reponse+"</p>"

    numeros_telephones.short_description = "Tel:"
    numeros_telephones.allow_tags = True

    def p28(self):
        """
        test l'age de l'individu
        :return True si individu > 28 ans sinon False
        """
        e = (date.today() - self.birthday)
        if e.days / 365 > 28:
            return True
        return False

    def save(self, force_insert=False, force_update=False, using=None, **kwargs):
        if not self.code_opi:
            individus = Individu.objects.filter(code_opi__isnull=False).order_by('-code_opi')
            if len(individus) > 0:
                self.code_opi = individus[0].code_opi + 1
            else:
                self.code_opi = 7700000
        return super(Individu, self).save(force_insert, force_update, using, **kwargs)

    def get_absolute_url(self):
        return reverse(self.state.name, kwargs={'pk': self.pk})

    @property
    def transitions_logs(self):
        """
        :return les transistions de l'individu
        """
        return TransitionLog.objects.filter(content_id=self.id).order_by('timestamp')

    def droit_univ(self):
        """
        test si l'individu est exonéré ou pas
        :return True si l'individu doit payer sinon False
        """
        if self.dossier_inscription.situation_sociale.pk != 'NO':
            return False
        return True

    def need_secu(self):
        """
        Test si l'individu doit payer la sécu
        :return True si oui False sinon
        """
        if self.p28() or self.dossier_inscription.affiliation_parent or\
                self.dossier_inscription.non_affiliation or self.dossier_inscription.situation_sociale.pk != 'NO':
            return False
        else:
            return True

    def is_ancien_p8(self):
        """
        Test si l'individu posséde un numéro étudiant
        """
        if self.student_code:
            return u'Oui'
        return u'Non'

    def lieu_naissance(self):
        """
        :return le lieu de naissance formaté
        """
        chaine = u''
        if self.code_departement_birth:
            chaine += u'Département : %s, ' % self.code_departement_birth
        chaine += u'Pays : %s' % self.code_pays_birth
        if self.town_birth:
            chaine += u', Ville : %s' % self.town_birth
        return chaine

    def sex_display(self):
        """
        :return le label du sexe
        """
        if self.sex == 'M':
            return unicode('Homme')
        else:
            return unicode('Femme')

    def dep_or_pays(self):
        """
        :return: le code à utiliser pour le champs opi dep ou pays
        """
        if self.code_pays_birth_id in ['100', 100, u"100"]:
            return self.code_departement_birth_id, 'D'
        else:
            return self.code_pays_birth_id, 'P'

    def get_tel(self):
        """
        :return :type String le téléphone pour l'appel téléphonique
        """
        w = self.adresses.filter(type='1')
        if len(w):
            return unicode(w[0].listed_number)
        else:
            return u'Aucun téléphone'

    def save_opi(self):
        """
        effectue la remontee opi
        TODO à refactoriser
        """
        db = 'oracle_test' if settings.DEBUG else 'oracle'
        premier_universite_fr_id = self.dossier_inscription.premier_universite_fr_id
        ine = self.ine[:-1] if self.ine else ""
        cle = self.ine[-1] if self.ine else ""
        annee_premiere_inscription_universite_fr = self.dossier_inscription.annee_premiere_inscription_universite_fr
        lieu_naiss = self.dep_or_pays()
        etablissement_autre = Etablissement.objects.get(cod_etb=15)
        if not self.dossier_inscription.dernier_etablissement:
            self.dossier_inscription.dernier_etablissement = etablissement_autre
        if not self.dossier_inscription.etablissement_annee_precedente:
            self.dossier_inscription.etablissement_annee_precedente = etablissement_autre
        if not self.dossier_inscription.etablissement_bac:
            self.dossier_inscription.etablissement_bac = etablissement_autre

        if not self.student_code:
            if self.ine == u"000000000000" or u"00000000000":
                ine = ""
                cle = ""
            individu = IndOpi.objects.using(db).get_or_create(
                cod_ind_opi=self.code_opi,
                date_nai_ind_opi=self.birthday,
                lib_pr1_ind_opi=self.first_name1,
                lib_nom_pat_ind_opi=self.last_name,
                cod_opi_int_epo=self.code_opi,)[0]

            individu.cod_ind_opi = self.code_opi
            individu.cod_sim = self.situation_militaire_id or 8
            individu.cod_pay_nat = self.code_pays_nationality_id
            individu.cod_etb = premier_universite_fr_id
            individu.cod_nne_ind_opi = ine
            individu.cod_cle_nne_ind_opi = cle
            individu.daa_ent_etb_opi = annee_premiere_inscription_universite_fr
            individu.lib_nom_pat_ind_opi = self.last_name.upper()
            individu.lib_nom_usu_ind_opi = self.common_name.upper()
            individu.lib_pr1_ind_opi = self.first_name1.upper()
            individu.lib_pr2_ind_opi = self.first_name2.upper()
            individu.lib_pr3_ind_opi = self.first_name3.upper()
            individu.num_tel_ind_opi = self.get_tel()
            individu.cod_etu_opi = self.student_code
            individu.lib_vil_nai_etu_opi = self.town_birth
            individu.cod_opi_int_epo = self.code_opi

            individu.cod_fam = self.family_status_id
            individu.cod_pcs = self.dossier_inscription.cat_soc_etu_id
            individu.cod_dep_pay_nai = lieu_naiss[0]
            individu.cod_typ_dep_pay_nai = lieu_naiss[1]
            individu.daa_ens_sup_opi = self.dossier_inscription.annee_premiere_inscription_enseignement_sup_fr
            individu.daa_etb_opi = self.dossier_inscription.annee_premiere_inscription_p8 if\
                self.dossier_inscription.annee_premiere_inscription_p8 != '2013' else '2014'
            individu.cod_sex_etu_opi = self.sex
            individu.cod_thp_opi = self.type_handicap_id
            individu.cod_thb_opi = self.type_hebergement_annuel_id
            individu.adr_mail_opi = self.personal_email
            individu.num_tel_por_opi = self.get_tel()
            individu.cod_tpe_ant_iaa = self.dossier_inscription.dernier_etablissement.cod_tpe_id
            individu.cod_etb_ant_iaa = None
            individu.cod_dep_pay_ant_iaa_opi = self.dossier_inscription.dernier_etablissement.get_pays_dep()
            individu.cod_typ_dep_pay_ant_iaa_opi = self.dossier_inscription.dernier_etablissement.get_type()
            individu.daa_etb_ant_iaa_opi = self.dossier_inscription.annee_dernier_etablissement
            individu.cod_sis_ann_pre_opi = self.dossier_inscription.sise_annee_precedente_id
            individu.cod_dep_pay_ann_pre_opi = self.dossier_inscription.etablissement_annee_precedente.get_pays_dep()
            individu.cod_typ_dep_pay_ann_pre_opi = self.dossier_inscription.etablissement_annee_precedente.get_type()
            individu.cod_etb_ann_pre_opi = None
            individu.cod_tds_opi = self.dossier_inscription.sise_annee_precedente_id
            # COD_TYP_DEP_PAY_DER_DIP=self.dossier_inscription.etablissement_dernier_diplome.get_type(),
            # COD_ETB_DER_DIP=self.dossier_inscription.etablissement_dernier_diplome_id,
            individu.daa_etb_der_dip = self.dossier_inscription.annee_dernier_diplome
            # individu.cod_etb_ann_crt = self.dossier_inscription.autre_etablissement_id
            individu.cod_etb_ann_crt = None
            individu.daa_etb_der_dip = self.dossier_inscription.annee_dernier_diplome
            individu.daa_etb_der_dip = self.dossier_inscription.annee_dernier_diplome
            # COD_TDE_DER_DIP=self.dossier_inscription.type_dernier_diplome_id,
            individu.cod_pcs_ap = self.dossier_inscription.cat_soc_autre_parent_id
            individu.cod_dep_pay_der_dip = self.dossier_inscription.etablissement_dernier_diplome.get_pays_dep()
            individu.cod_rgi = '1'
            individu.cod_stu = '01'
            individu.save(using=db)
            opi_bac = OpiBac.objects.using(db).get_or_create(cod_ind_opi=self.code_opi,
                                                             cod_bac=self.dossier_inscription.bac.cod_bac)[0]

            opi_bac.cod_etb = self.dossier_inscription.etablissement_bac_id
            opi_bac.cod_dep = self.dossier_inscription.etablissement_bac.cod_dep.cod_dep
            opi_bac.cod_mnb = self.dossier_inscription.mention_bac_id
            opi_bac.daa_obt_bac_oba = self.dossier_inscription.annee_bac
            opi_bac.save(using=db)

        elif self.student_code:
            individu_apogee = IndividuApogee.objects.using(db).get(cod_etu=self.student_code)
            # ins_adm_anu = InsAdmAnu.objects.using(db).filter(cod_ind=individu_apogee).order_by('cod_anu').last()

            individu = IndOpi.objects.using(db).get_or_create(
                cod_ind_opi=self.code_opi,
                date_nai_ind_opi=self.birthday,
                lib_pr1_ind_opi=self.first_name1.upper(),
                lib_nom_pat_ind_opi=self.last_name.upper(),
                cod_opi_int_epo=self.code_opi,)[0]
            individu.cod_ind_opi = self.code_opi
            individu.cod_sim = individu_apogee.cod_sim
            individu.cod_pay_nat = individu_apogee.cod_pay_nat
            individu.cod_etb = individu_apogee.cod_etb
            individu.cod_ind = individu_apogee.cod_ind
            individu.date_nai_ind_opi = self.birthday
            individu.daa_ens_sup_opi = individu_apogee.daa_ens_sup
            individu.daa_etb_opi = individu_apogee.daa_etb
            individu.daa_ent_etb_opi = individu_apogee.daa_ent_etb
            individu.lib_nom_pat_ind_opi = self.last_name
            individu.lib_nom_usu_ind_opi = self.common_name
            individu.lib_pr1_ind_opi = self.first_name1
            individu.lib_pr2_ind_opi = self.first_name2
            individu.lib_pr3_ind_opi = self.first_name3
            individu.num_tel_ind_opi = self.get_tel()
            individu.cod_etu_opi = self.student_code
            individu.cod_opi_int_epo = self.code_opi
            individu.cod_pcs = self.dossier_inscription.cat_soc_etu_id
            individu.cod_thb_opi = self.type_hebergement_annuel_id
            individu.adr_mail_opi = self.personal_email
            individu.num_tel_por_opi = self.get_tel()
            individu.cod_pcs_ap = self.dossier_inscription.cat_soc_autre_parent_id
            individu.cod_rgi = '1'
            individu.cod_stu = '01'
            individu.save(using=db)
            # copie du bac d'apogee

            bac_apogee = IndBac.objects.using(db).filter(cod_ind=individu.cod_ind).first()

            if bac_apogee:
                opi_bac = OpiBac.objects.using(db).get_or_create(cod_ind_opi=self.code_opi,
                                                                 cod_bac=bac_apogee.cod_bac)[0]
                opi_bac.cod_etb = bac_apogee.cod_etb
                opi_bac.cod_dep = bac_apogee.cod_dep
                opi_bac.cod_mnb = bac_apogee.cod_mnb
                opi_bac.daa_obt_bac_oba = bac_apogee.daa_obt_bac_iba
                opi_bac.save(using=db)

        if self.adresses.count() != 2:
            adresse = self.adresses.all()[0]
            self._save(adresse, 1, db)
            self._save(adresse, 2, db)
        else:

            for adresse in self.adresses.all():
                type = 2 if adresse.type == 1 else 1
                self._save(adresse, type, db)

    def get_adresse_annuelle_simple(self):
        try:
            a = self.adresses.get(type='1')
            return a.get_full_adresse_simple()
        except AdresseIndividu.DoesNotExist:
            return "Aucune"

    def _save(self, adresse, type, db):
        cod_bdi = None
        cod_com = None
        if adresse.com_bdi:
            cod_bdi = adresse.com_bdi.cod_bdi
            cod_com = adresse.com_bdi.cod_com
        res = AdresseOpi.objects.using(db).filter(cod_ind_opi=self.code_opi, cod_typ_adr_opi=type)
        if len(res):
            ad = res.first()
        else:
            ad = AdresseOpi.objects.using(db).create(
                cod_ind_opi=self.code_opi,
                cod_typ_adr_opi=str(type),
                cod_pay=adresse.code_pays.cod_pay,
                cod_bdi=cod_bdi,
                cod_com=cod_com,
                lib_ad1=adresse.label_adr_1,
                lib_ad2=adresse.label_adr_2,
                lib_ad3=adresse.label_adr_3,
                lib_ade=adresse.label_adr_etr)


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
    centre_payeur = models.CharField(max_length=6, choices=settings.CENTRE_SECU, null=True,
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
