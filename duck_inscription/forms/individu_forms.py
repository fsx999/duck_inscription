# -*- coding: utf-8 -*-
from __future__ import unicode_literals
# import autocomplete_light
import autocomplete_light
import django
from django.conf import settings
from django.utils import formats, six
import re
from django_apogee.models import Individu, Departement, Pays, SitFam, SitMil, TypHandicap, BacOuxEqu, TypHebergement, \
    ComBdi, MentionBac, CatSocPfl, DomaineActPfl, QuotiteTra, SituationSise, MtfNonAflSso, RegimeParent, TypeDiplomeExt, \
    SitSociale
from duck_inscription.models import AdresseIndividu, DossierInscription
from django_apogee.models import Etablissement, TypEtb, BacOuxEqu

RE_DATE = re.compile(r'(\d{4})-(\d\d?)-(\d\d?)$')
import floppyforms as forms

from django.forms.models import modelformset_factory, BaseInlineFormSet
from django.template import loader

__author__ = 'paul'
from django.utils.dates import MONTHS
from datetime import datetime, date, timedelta, tzinfo


ANNEE = (('', '------'),) + tuple([(x, str(x) + '/' + str(x + 1)) for x in range(1920, datetime.today().year + 1)])
ANNEE_INSCRIPTION = (('', 'Jamais'),) + tuple(
    [(x, str(x) + '/' + str(x + 1)) for x in range(1950, datetime.today().year + 1)])
ANNEE_P8 = ((u'', u'Jamais'),) + tuple([(x, str(x) + '/' + str(x + 1)) for x in range(2000, datetime.today().year + 1)])
FRANCE = '100'


class GMT0(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=0, minutes=0)

    def tzname(self, dt):
        return "GMT +5"

    def dst(self, dt):
        return timedelta(0)


class NationalityModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.lib_nat


class LabelModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        if hasattr(obj, 'title'):
            return "%s" % obj.title
        if hasattr(obj, 'lib_thp'):
            return "%s" % obj.lib_thp
        if hasattr(obj, 'lib_sim'):
            return "%s" % obj.lib_sim
        if hasattr(obj, 'lib_ach'):
            return "%s" % obj.lib_ach
        if hasattr(obj, 'lib_thb'):
            return "%s" % obj.lib_thb
        if hasattr(obj, 'lib_fam'):
            return "%s" % obj.lib_fam


class EtablissementWidget(forms.Select):
    def get_context(self, name, value, attrs, choices=()):
        ctx = super(EtablissementWidget, self).get_context(name, value, attrs, choices)
        ctx['name'] = "etablissement"
        return ctx


class SelectDateWidget(forms.SelectDateWidget):
    """
    A Widget that splits date input into three <select> boxes.

    This also serves as an example of a Widget that has more than one HTML
    element and hence implements value_from_datadict.
    """
    none_value = ('', '---')
    month_field = '%s_month'
    day_field = '%s_day'
    year_field = '%s_year'
    template_name = 'floppyforms/select_date.html'

    def render(self, name, value, attrs=None, extra_context={}):
        try:
            year_val, month_val, day_val = value.year, value.month, value.day
        except AttributeError:
            year_val = month_val = day_val = None
            if isinstance(value, six.text_type):
                if settings.USE_L10N:
                    try:
                        input_format = formats.get_format('DATE_INPUT_FORMATS')[0]
                        v = datetime.strptime(value, input_format)
                        year_val, month_val, day_val = v.year, v.month, v.day
                    except ValueError:
                        pass
                else:
                    match = RE_DATE.match(value)
                    if match:
                        year_val, month_val, day_val = map(int, match.groups())

        context = self.get_context(name, value, attrs=attrs, extra_context=extra_context)

        context['year_choices'] = [(i, i) for i in self.years]
        context['year_val'] = year_val

        context['month_choices'] = list(MONTHS.items())
        context['month_val'] = month_val

        context['day_choices'] = [(i, i) for i in range(1, 32)]
        context['day_val'] = day_val

        context['year_choices'].insert(0, self.none_value)
        context['month_choices'].insert(0, self.none_value)
        context['day_choices'].insert(0, self.none_value)

        return loader.render_to_string(self.template_name, context)

    def value_from_datadict(self, data, files, name):
        y = data.get(self.year_field % name)
        m = data.get(self.month_field % name)
        d = data.get(self.day_field % name)
        if y == m == d == "0":
            return None
        if y and m and d:
            return '%s/%s/%s' % (d, m, y)
        return data.get(name, None)


class CodeEtudiantForm(forms.Form):
    """
    Ce formulaire permet de vérifier si un code étudiant existe
    et si le mot de passe fournit est corect.
    Cette classe dépend du contenu de IndividuApogee
    """
    code_etu = forms.CharField(label="Numero étudiant :", max_length=8, required=True,
                               help_text=u"(Votre numéro d'étudiant figure sur votre carte d'étudiant)"

    )
    date_naissance = django.forms.DateField(label=u"Date de naissance ", required=True,
                                            widget=SelectDateWidget(  # years = ['-----']+[x for x in range(1900,2001)]
                                                                      years=range(datetime.today().year - 15 - 80,
                                                                                  datetime.today().year - 15),
                                                                      attrs={'required': ""}))

    def clean_code_etu(self):
        data = self.cleaned_data.get("code_etu", "")
        try:
            if len(Individu.objects.filter(cod_etu=data)) == 0:
                raise forms.ValidationError("Vous devez rentrer un code étudiant valide", code='invalide')
        except ValueError:
            raise forms.ValidationError("Vous devez rentrer un code étudiant valide", code='invalide')
        return data

    def clean(self):
        data = super(CodeEtudiantForm, self).clean()
        code_etu = data.get("code_etu", 0)
        date_naissance = data.get("date_naissance", date.today())

        date_naissance = datetime(*(date_naissance.timetuple()[:6]))
        if not Individu.objects.filter(cod_etu=code_etu, date_nai_ind=date_naissance):
            raise forms.ValidationError(u"Le numéro étudiant et la date de naissance ne correspondent pas")
        return data


class InfoPersoForm(forms.ModelForm):
    """
    formulaire pour les infos perso
    """
    last_name = forms.CharField(label=u"Nom patronymique", max_length=60, help_text=u"(indiquez le nom de naissance)")
    common_name = forms.CharField(label=u"Nom d'usage", max_length=60, required=False,
                                  help_text=u"(Pour les femmes mariées, inscrivez le nom d'épouse)")
    first_name1 = forms.CharField(label=u"Prénom ", max_length=60)
    first_name2 = forms.CharField(label=u"Second prénom ", max_length=60, required=False, )
    first_name3 = forms.CharField(label=u"Troisième prénom ", max_length=60, required=False)
    birthday = django.forms.DateField(label=u"Date de naissance ", required=True, widget=SelectDateWidget(
        years=range(datetime.today().year - 15 - 80, datetime.today().year - 15), attrs={'required': ""})

    )

    code_pays_birth = forms.ModelChoiceField(label=u"Pays de naissance ",
                                             queryset=Pays.objects.all().exclude(lib_pay='').order_by('lib_pay'))

    code_departement_birth = forms.ModelChoiceField(label=u"Département de naissance ",
                                                    queryset=Departement.objects.exclude(lib_dep='ARMEES'),
                                                    required=False)
    town_birth = forms.CharField(label=u'Ville naissance :', max_length=30, required=False)
    # todo trouver le bug pour required
    code_pays_nationality = NationalityModelChoiceField(label=u"Nationalité",
                                                        queryset=Pays.objects.all().exclude(lib_pay='').order_by(
                                                            'lib_nat'))

    sex = forms.ChoiceField(label=u"Sexe ", choices=((u'', '------'), (u'M', u'Homme'), (u'F', u'Femme')))
    valid_ine = forms.ChoiceField(label=u"Confirmation de votre INE", choices=(
        ('', '------'), ('O', u'Je suis sur de mon numéro'), ('N', u"Je n'ai pas de numéro")
    ))
    ine = forms.CharField(label=u"INE/BEA ", max_length=11, required=False,
                          help_text=u'(<a href="https://www.iedparis8.net/ied/rubrique.php?id_rubrique=129#a_12L129"'
                                    u' target="_blank">Où trouver votre INE/BEA ?</a>)')

    family_status = LabelModelChoiceField(label=u"Statut familial ", queryset=SitFam.objects.all())

    situation_militaire = forms.ModelChoiceField(label=u"Situation militaire ",
                                                 queryset=SitMil.objects.all().exclude(cod_sim__in=[1, 2]),
                                                 required=False, )

    type_handicap = forms.ModelChoiceField(label=u"Handicap ", queryset=TypHandicap.objects.all(), required=False,
                                           empty_label=u"Aucun handicap")
    diplome_acces = forms.ModelChoiceField(label=u"Baccalauréat ou équivalent ", queryset=BacOuxEqu.objects.all())
    annee_obtention = forms.ChoiceField(choices=[(u'', u'-------')] + [(unicode(i), unicode(i)) for i in
                                                                       range(datetime.today().year - 70,
                                                                             datetime.today().year + 1)],
                                        label=u"Année d'obtention",
                                        help_text=u"(Année d'obtention du baccalauréat ou équivalent", required=True)

    class Meta:
        model = Individu
        fields = (
        'last_name', 'common_name', 'first_name1', 'first_name2', 'first_name3', 'birthday', 'code_pays_birth',
        'code_departement_birth', 'town_birth', 'code_pays_nationality', 'sex', 'valid_ine', 'ine', 'family_status',
        'situation_militaire', 'type_handicap', 'diplome_acces', 'annee_obtention')

    def __init__(self, *args, **kwargs):
        readonly = kwargs.pop('readonly', False)
        readonly_all = kwargs.pop('readonlyall', False)
        super(InfoPersoForm, self).__init__(*args, **kwargs)
        if readonly:
            self.fields['last_name'].widget.attrs['readonly'] = 'readonly'
            self.fields['first_name1'].widget.attrs['readonly'] = 'readonly'

            if self.instance.ine:
                self.fields['ine'].widget.attrs['readonly'] = 'readonly'
                self.fields['valid_ine'].widget.attrs['readonly'] = 'readonly'
            self.fields['sex'].widget.attrs['readonly'] = 'readonly'

        if readonly_all:
            for field in self.fields:
                self.fields[field].widget.attrs['disabled'] = 'disabled'

    def clean(self):
        """
        Plusieurs règles :
        date de naissance :
        si moins de 28 et français : situation militaire obligatoire
        date du bac > +15ans date de naissance
        si née en france, département de naissance obligatoire
        """
        data = super(InfoPersoForm, self).clean()
        code_pays_birth = data.get('code_pays_birth', None)
        birthday = data.get('birthday', None)
        annee_obtention = data.get('annee_obtention', 0)
        code_pays_nationality = data.get('code_pays_nationality', 0)
        situation_militaire = data.get('situation_militaire', None)
        ine, valid_ine = data.get('ine', None), data.get('valid_ine', None)
        if code_pays_birth == FRANCE:
            code_departement_birth, town_birth = data.get('code_departement_birth', None), data.get('town_birth', None)
            if not code_departement_birth or not town_birth:
                raise forms.ValidationError(
                    u"Vous devez saisir votre département de naissance et votre ville de naissance")
        if code_pays_nationality == FRANCE:
            now = date.today()
            birthday_28 = date(birthday.year + 28, birthday.month, birthday.day)
            dif = birthday_28 - now
            if dif > 0:  # il n'a pas 28 ans
                if situation_militaire is None:
                    raise forms.ValidationError(
                        u"Vous avez moins de 28 ans, vous devez renseigner votre situation militaire")

        if (birthday.year + 15) > int(annee_obtention):
            raise forms.ValidationError(
                u"Vous avez saisi une date d'obtention du bac incorect vis à vis de votre date de naissance")
        if valid_ine in ['O', 'P']:
            if ine == u"":
                raise forms.ValidationError(u"Vous devez saisir un INE")
        if valid_ine == u"N" and ine is not None:
            data['ine'] = None
        return data


class AdresseForm(forms.ModelForm):
    listed_number = forms.CharField(label=u'Numero de teléphone :', widget=forms.PhoneNumberInput(),
                                    help_text=u"(Sans espace et sans tiret)")
    code_pays = forms.ModelChoiceField(queryset=Pays.objects.all().order_by('lib_pay'))
    com_bdi = forms.ModelChoiceField(ComBdi.objects.all(), label=u"Code postal", required=False,
                                     widget=autocomplete_light.ChoiceWidget('ComBdiAutocomplete'))
    label_adr_1 = forms.CharField(label=u"Adresse ")
    label_adr_2 = forms.CharField(label=u"Suite de l'adresse ", required=False)
    label_adr_3 = forms.CharField(label=u"Suite de l'adresse ", required=False)
    label_adr_etr = forms.CharField(label=u"Adresse étrangère ", required=False)
    type = django.forms.CharField(widget=django.forms.HiddenInput())

    class Meta:
        model = AdresseIndividu
        exclude = ('individu',)

    def clean(self):
        data = super(AdresseForm, self).clean()
        pays = data.get('code_pays', None)
        if pays is None:
            raise forms.ValidationError(u"Vous devez choisir un pays pour votre adresse")
        if pays.cod_pay == FRANCE:
            if not data.get("com_bdi", None):
                raise forms.ValidationError(u"Vous devez choisir une commune pour votre adresse")
            else:
                if data.get('label_adr_etr', None):
                    data['label_adr_etr'] = None
        else:
            if not data.get("label_adr_etr", None):
                raise forms.ValidationError(u"Vous devez indiquer un complément d'adresse")
            else:
                if data.get('com_bdi', None):
                    data['com_bdi'] = None
        return data


class AdresseBaseFormSet(BaseInlineFormSet):
    def add_fields(self, form, index):
        super(AdresseBaseFormSet, self).add_fields(form, index)
        if index == 0:  # il s'agit de l'adrese annuel
            form.fields['type_hebergement'] = forms.ModelChoiceField(initial=self.initial_extra[0]['type_hebergement'],
                                                                     queryset=TypHebergement.objects.all(),
                                                                     widget=forms.Select(attrs={'class': 'required'}, ),
                                                                     label=u"Hébergement ",
                                                                     help_text=u"(Renseigner le type de votre hébergement annuel)")


class RecapitulatifIndividuForm(forms.Form):
    pass


ETABLISSEMENT = forms.ModelChoiceField(Etablissement.objects.all(), label=u"Code département ou code postal",
                                       required=True,
                                       widget=autocomplete_light.ChoiceWidget('EtablissementAutocomplete'))


class GenericEtablissement(forms.ModelForm):
    type_etablissement = forms.ModelChoiceField(label=u"Type d'établissement :",
                                                help_text=u"Selectionnez un type d'établissement",
                                                queryset=TypEtb.objects.filter(tem_en_sve_tpe='O').exclude(
                                                    etablissement__isnull=True).order_by('-lib_tpe'), required=False)


class PremiereInscriptionForm(forms.ModelForm):
    premier_universite_fr = forms.ModelChoiceField(label=u"Première université française ou établissement supérieur:",
                                                   queryset=Etablissement.objects.filter(cod_tpe='00'), required=False,
                                                   widget=forms.Select(attrs={"value_toggle": '!',
                                                                              'toggle_field': 'annee_premiere_inscription_universite_fr'}),
                                                   help_text=u"Choisir l'université Paris 8 s'il s'agit de votre première inscription dans l'enseignement supérieur français", )
    annee_premiere_inscription_p8 = forms.ChoiceField(
        label=u"Année de la première inscription à l'université Paris 8 :", choices=ANNEE_P8, required=False,
        help_text=u"Depuis 2000. Choisir 2013/2014  s'il s'agit de votre première inscription à l'université Paris 8")
    annee_premiere_inscription_universite_fr = forms.ChoiceField(
        label=u"Année de votre première inscription dans une université française :", choices=ANNEE_INSCRIPTION,
        help_text=u"Choisir 2013/2014 s'il s'agit de votre première inscription dans une université française.",
        required=False)
    annee_premiere_inscription_enseignement_sup_fr = forms.ChoiceField(
        label=u"Année de votre première inscription dans l'enseignement supérieur français :",
        help_text=u"Choisir 2013/2014 s'il s'agit de votre première inscription dans l'enseignement supérieur français",
        choices=ANNEE_INSCRIPTION, required=False)

    annee_derniere_inscription_universite_hors_p8 = forms.ChoiceField(
        label=u"Année de votre dernière inscription dans une université française hors Paris 8 :",
        help_text=u"Si votre dernière université n'est pas Paris 8", choices=ANNEE_INSCRIPTION, required=False)

    def clean_annee_premiere_inscription_enseignement_sup_fr(self):
        data = self.cleaned_data['annee_premiere_inscription_enseignement_sup_fr']
        if data != u'' and self.instance.individu.annee_obtention > data:
            raise forms.ValidationError(u"Vous avez choisi une date inférieure à celle de votre bac")
        if data == u'':
            data = 2013
        return data

    def clean_annee_premiere_inscription_p8(self):
        data = self.cleaned_data['annee_premiere_inscription_p8']
        if data != u'' and self.instance.individu.annee_obtention > data:
            raise forms.ValidationError(u"Vous avez choisi une date inférieure à celle de votre bac")
        if data == u'':
            data = 2013
        return data

    def clean_annee_premiere_inscription_universite_fr(self):
        data = self.cleaned_data['annee_premiere_inscription_universite_fr']
        if data != u'' and self.instance.individu.annee_obtention > data:
            raise forms.ValidationError(u"Vous avez choisi une date inférieure à celle de votre bac")
        if data == u'':
            data = 2013
        return data

    def clean_premier_universite_fr(self):
        data = self.cleaned_data['premier_universite_fr']
        if data is None:
            data = Etablissement.objects.get(cod_etb='0931827F')
        return data

    class Meta:
        model = DossierInscription
        fields = ("premier_universite_fr", "annee_premiere_inscription_p8", "annee_premiere_inscription_universite_fr",
                  "annee_premiere_inscription_enseignement_sup_fr", 'id',
        )


class ComplementBacForm(GenericEtablissement):
    bac = forms.ModelChoiceField(queryset=BacOuxEqu.objects.all(), label=u"Bac ou équivalent", )

    annee_bac = forms.ChoiceField(choices=[(u'', u'-------')] + [(unicode(i), unicode(i)) for i in
                                                                 range(datetime.today().year - 70,
                                                                       datetime.today().year + 1)],
                                  label=u"Année d'obtention",
                                  help_text=u"(Année d'obtention du baccalauréat ou équivalent)", required=True)
    etablissement_bac = ETABLISSEMENT

    mention_bac = forms.ModelChoiceField(
        label=u"Renseignez la mention qui vous a été attribuée lors de l'obtention de votre baccalauréat :",
        help_text=u"Seulement si vous avez un baccalauréat", queryset=MentionBac.objects.filter(tem_en_sve_mnb='O'),
        required=False)

    def clean_annee_bac(self):
        data = self.cleaned_data['annee_bac']
        if (self.instance.individu.birthday.year + 15) > int(data):
            raise forms.ValidationError(
                u"Vous avez saisi une date d'obtention du bac incorect vis à vis de votre date de naissance")
        return data

    class Meta:
        model = DossierInscription
        fields = ('bac', 'annee_bac', 'etablissement_bac', 'mention_bac')


class CatSocForm(forms.ModelForm):
    cat_soc_etu = forms.ModelChoiceField(label=u"Votre activité professionnelle :",
                                         queryset=CatSocPfl.objects.filter(tem_en_sve_pcs='O').order_by(
                                             '-lib_web_pcs'), )
    cat_soc_chef_famille = forms.ModelChoiceField(label=u"L'activité professionnelle du père:",
                                                  queryset=CatSocPfl.objects.filter(tem_en_sve_pcs='O').order_by(
                                                      'lib_web_pcs'), empty_label=u"Aucune", required=False, )
    cat_soc_autre_parent = forms.ModelChoiceField(label=u"L'activité professionnelle de la mère :",
                                                  queryset=CatSocPfl.objects.filter(tem_en_sve_pcs='O').order_by(
                                                      'lib_web_pcs'), empty_label=u"Aucune", required=False, )
    sportif_haut_niveau = forms.NullBooleanField(label=u"Etes vous sportif de haut niveau :",
                                                 help_text=u"Vous devrez joindre les justificatifs le cas échéant.",

                                                 widget=forms.Select(
                                                     choices=(("", "-----"), ("True", "Oui"), ("False", "Non")),
                                                     attrs={'class': 'required auto'}))
    cat_travail = forms.ModelChoiceField(queryset=DomaineActPfl.objects.filter(lib_web_dap__isnull=False),
                                         label=u"Domaine d'activité", required=False,
                                         help_text=u"Uniquement si vous travaillez")
    quotite_travail = forms.ModelChoiceField(label=u"Votre quotité de travail :",
                                             queryset=QuotiteTra.objects.filter(tem_en_sve_qtr='O'),
                                             widget=forms.Select(attrs={'class': 'auto'}),
                                             empty_label=u"Ne travaille pas", required=False)

    class Meta:
        model = DossierInscription
        fields = (
            'cat_soc_etu', 'cat_soc_chef_famille', 'cat_soc_autre_parent',

            'sportif_haut_niveau', 'quotite_travail', 'cat_travail'
        )


class DernierEtablissementForm(GenericEtablissement):
    annee_dernier_etablissement = forms.ChoiceField(label=u"Année :", choices=ANNEE, )

    dernier_etablissement = ETABLISSEMENT


    class Meta:
        model = DossierInscription
        fields = ('annee_dernier_etablissement', 'type_etablissement', 'dernier_etablissement')


class SituationAnneePrecedenteForm(forms.ModelForm):
    sise_annee_precedente = forms.ModelChoiceField(
        queryset=SituationSise.objects.filter(tem_en_sve_sis='O').order_by('-lib_sis'),
        label=u"Indiquez votre situation l’année précédente :", )

    class Meta:
        model = DossierInscription
        fields = ('sise_annee_precedente',)


class EtablissementSituationAnneePrecedenteForm(GenericEtablissement):
    etablissement_annee_precedente = ETABLISSEMENT

    class Meta:
        model = DossierInscription
        fields = ('type_etablissement', 'etablissement_annee_precedente',)


class EtablissementDernierDiplomeForm(GenericEtablissement):
    type_dernier_diplome = forms.ModelChoiceField(
        queryset=TypeDiplomeExt.objects.filter(tem_en_sve_tde='O').order_by('lib_tde'),
        label=u"Dernier diplome obtenu :", help_text=u"Quel est le dernier diplôme que vous avez obtenu ?")
    annee_dernier_diplome = forms.ChoiceField(label=u"Année d'obtention :", choices=ANNEE,
                                              help_text=u"Exemple :  si diplôme obtenu en juin 2012, indiquer 2011/2012.",
                                              widget=forms.Select(attrs={'class': 'required auto'}), )
    etablissement_dernier_diplome = ETABLISSEMENT

    class Meta:
        model = DossierInscription
        fields = (
            'type_dernier_diplome', 'annee_dernier_diplome', 'type_etablissement', 'etablissement_dernier_diplome',
        )


class TestAutreEtablissementForm(forms.ModelForm):
    autre_eta = forms.NullBooleanField(
        label=u"Indiquez si vous êtes inscrit dans un autre établissement d'enseignement pour l'année en cours :",
        help_text=u"Fréquentez-vous un autre établissement pour l’année en cours ?",
        widget=forms.Select(choices=(("", "-----"), ("True", "Oui"), ("False", "Non")), ))

    class Meta:
        model = DossierInscription
        fields = (
            'autre_eta',
        )


class AutreEtablissementForm(GenericEtablissement):
    autre_etablissement = ETABLISSEMENT

    class Meta:
        model = DossierInscription
        fields = (
            'type_etablissement', 'autre_etablissement',
        )


class ValidationForm(forms.ModelForm):
    valider = forms.CharField()

    class Meta:
        model = DossierInscription
        fields = ('id',)


class SituationSocialeForm(forms.ModelForm):
    situation_sociale = forms.ModelChoiceField(label=u"Votre situation sociale :", queryset=SitSociale.objects.all(),
                                               help_text=u'(sur présentation des justificatifs)', required=True, )
    echelon = forms.CharField(label=u"Echelon :", max_length=2, required=False, widget=forms.TextInput(
        attrs={"value_toggle": 'BO', 'toggle_field': 'situation_sociale'}), )
    num_boursier = forms.CharField(label=u"N° de boursier :", max_length=13, required=False, widget=forms.TextInput(
        attrs={"value_toggle": 'BO', 'toggle_field': 'situation_sociale'}), )
    boursier_crous = forms.NullBooleanField(label=u"Bousier du Crous de l'année précédente :", required=False,
                                            widget=forms.Select(
                                                choices=(("", "-----"), ("True", u"Oui"), ("False", u"Non")),
                                                attrs={"value_toggle": 'BO', 'toggle_field': 'situation_sociale'}))

    class Meta:
        model = DossierInscription
        fields = (
            'situation_sociale', 'echelon', 'num_boursier', 'boursier_crous',
        )


class SecuriteSocialeForm(forms.ModelForm):
    affiliation_parent = forms.ModelChoiceField(label=u"Affiliation au régime de sécurité sociale des parents :",
                                                help_text=u"Vous devrez fournir des justificatifs.",
                                                queryset=RegimeParent.objects.all(), empty_label=u"Aucune",
                                                required=False)

    non_affiliation = forms.ModelChoiceField(
        label=u"Cas de non affiliation au régime de sécurité sociale des étudiants (salarié, +28 ans ...)",
        help_text=u"Vous devrez fournir des justificatifs.", queryset=MtfNonAflSso.objects.all(), empty_label=u"Aucun",
        required=False)

    centre_payeur = forms.ChoiceField(label=u"Indiquez votre centre payeur :",
                                      choices=(('', '------'), ('SMEREP', 'SMEREP'), ('LMDE', 'LMDE')), required=False,
                                      widget=forms.Select(
                                          attrs={"value_toggle": '', 'toggle_field': 'non_affiliation'}))

    class Meta:
        model = DossierInscription
        fields = (
            'affiliation_parent', 'non_affiliation', 'num_secu', 'centre_payeur',
        )


class NumSecuForm(forms.ModelForm):
    num_secu = forms.CharField(label=u"Votre numéro de sécurité sociale :", max_length=15, min_length=5, )

    class Meta:
        model = DossierInscription
        fields = (
            'num_secu',
        )

