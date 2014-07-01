# coding=utf-8
import floppyforms as forms
from duck_inscription.models import SettingsEtape


class DossierReceptionForm(forms.Form):
    code_dossier = forms.CharField(label=u'Code du dossier', max_length=15)

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
                msg = u"Veuillez renseigner l'étape"
                self._errors["etapes"] = self.error_class([msg])
        return self.cleaned_data

    class Media:
        js = ('js/equivalence.js', )
