# coding=utf-8
from __future__ import unicode_literals
from django.conf import settings
import floppyforms as forms
from django_apogee.models import SitSociale, RegimeParent, MtfNonAflSso
from duck_inscription.models import SettingsEtape, CentreGestionModel
try:
    from duck_inscription_payzen.models import MoyenPaiementModel
except ImportError:
    MoyenPaiementModel = SitSociale


class DossierReceptionForm(forms.Form):
    code_dossier = forms.CharField(label='Code du dossier', max_length=15)

    class Media:
        js = ('js/dossier_reception.js', )


class ImprimerEnMasseForm(forms.Form):
    low = forms.IntegerField(label='A partir de:')
    high = forms.IntegerField(label='Jusqu:')


class EquivalenceForm(DossierReceptionForm):
    etapes = forms.ModelChoiceField(queryset=SettingsEtape.objects.all(), required=True)
    choix = forms.ChoiceField(
        choices=(('complet', 'Complet'), ('accepte', 'Accepté'),
                 ('incomplet', 'Incomplet'), ('refuse', 'Refusé'),
                 ('autoriser_inscription', "Autoriser à s'inscrire (sans candidature)"),
                 ('autoriser_equivalence', "Sortir de liste d'attente d'equivalence")),
        widget=forms.RadioSelect(), required=True)
    motif = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *arg, **kwargs):
        queryset = kwargs['queryset']
        del kwargs['queryset']
        super(EquivalenceForm, self).__init__(*arg, **kwargs)

        self.fields['etapes'] = forms.ModelChoiceField(queryset=queryset, required=False)

    def clean(self):
        etape = self.cleaned_data.get('etapes', None)
        choix = self.cleaned_data.get('choix', None)
        if choix == 'complet':
            if etape is None:
                msg = "Veuillez renseigner l'étape"
                self._errors["etapes"] = self.error_class([msg])
        return self.cleaned_data

    class Media:
        js = ('js/equivalence.js', )


class CandidatureForm(DossierReceptionForm):
    choix = forms.ChoiceField(
        choices=(
            ('complet', u"Complet"),
            ('accepte', u'Accepté'),
            ('incomplet', u'Incomplet'),
            ('refuse', u'Refusé'),
            ('attente', u"Accepté mais mis en liste d'attente"),
            ('ouvert', 'Autorisé à candidater')),
        widget=forms.RadioSelect(),
        required=True)
    motif = forms.CharField(widget=forms.Textarea, required=False)

    class Media:
        js = ('js/candidature.js',)


class InscriptionForm(DossierReceptionForm):
    choix = forms.ChoiceField(
        choices=(
            ('complet', u"Complet"),
            ('incomplet', u'Incomplet sans renvoi'),
            ('incomplet_renvoi', u'Incomplet avec renvoi'),
            ('refuse', u'Refusé'),
            ('annule', u'Annulé'),
            ('ouvert', 'Autorisé à s\'inscrire')),
        widget=forms.RadioSelect(), required=True)
    motif = forms.CharField(widget=forms.Textarea, required=False)

    class Media:
        js = ('js/inscription.js',)


class ChangementCentreGestionForm(forms.Form):

    def __init__(self, wish, *args, **kwargs):
        self.wish = wish
        super(ChangementCentreGestionForm, self).__init__(*args, **kwargs)
        if wish.paiementallmodel.moyen_paiement.type ==  'CB':
            del self.fields['type_paiement']
            del self.fields['nombre_paiement']
        # if wish.etape.semestre:
        #     self.fields['demi_annee'] = forms.BooleanField(required=False)

    centre_gestion = forms.ModelChoiceField(queryset=CentreGestionModel.objects.all())
    nombre_paiement = forms.ChoiceField(choices=(("1", '1'), ('2', '2'), ('3', '3')), required=False)
    type_paiement = forms.ModelChoiceField(queryset=MoyenPaiementModel.objects.all(), required=False)
    situation_sociale = forms.ModelChoiceField(queryset=SitSociale.objects.all(), required=False)
    affiliation_parent = forms.ModelChoiceField(label=u"Affiliation au régime de sécurité sociale des parents :",
                                                help_text=u"Vous devrez fournir des justificatifs.",
                                                queryset=RegimeParent.objects.all(), empty_label=u"Aucune",
                                                required=False)

    non_affiliation = forms.ModelChoiceField(
        label=u"Cas de non affiliation au régime de sécurité sociale des étudiants (salarié, +28 ans ...)",
        help_text=u"Vous devrez fournir des justificatifs.", queryset=MtfNonAflSso.objects.all(), empty_label=u"Aucun",
        required=False)

    centre_payeur = forms.ChoiceField(label=u"Indiquez votre centre payeur :",
                                      choices=settings.CENTRE_SECU, required=False,
                                      widget=forms.Select(
                                          attrs={"value_toggle": '', 'toggle_field': 'non_affiliation'}))


    def clean(self):
        if not self.wish.state.is_inscription:
            raise forms.ValidationError('le voeu doit être en inscription')
        return super(ChangementCentreGestionForm, self).clean()




