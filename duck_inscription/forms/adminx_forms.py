# coding=utf-8
from __future__ import unicode_literals
import floppyforms as forms
from django_apogee.models import CentreGestion
from duck_inscription.models import SettingsEtape


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
        choices=(('complet', 'Complet'), ('accepte', 'Accepté'), ('incomplet', 'Incomplet'), ('refuse', 'Refusé')),
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
            ('ouvert', 'Autorisé à s\'inscrire')),
        widget=forms.RadioSelect(), required=True)
    motif = forms.CharField(widget=forms.Textarea, required=False)

    class Media:
        js = ('js/inscription.js',)


class ChangementCentreGestionForm(forms.Form):
    centre_gestion = forms.ModelChoiceField(queryset=CentreGestion.objects.all())
