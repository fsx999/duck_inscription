# coding=utf-8
from __future__ import unicode_literals
from datetime import date
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
import unicodedata
from django_xworkflows.xworkflow_log.models import TransitionLog
from django_apogee.models import Departement, Pays, SitFam, SitMil, TypHandicap, TypHebergement, BacOuxEqu, AnneeUni, \
    ComBdi
from django_xworkflows import models as xwf_models
from duck_inscription.models.workflows_models import IndividuWorkflow


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
