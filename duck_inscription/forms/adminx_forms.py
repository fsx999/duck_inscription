# coding=utf-8
import floppyforms as forms


class DossierReceptionForm(forms.Form):
    code_dossier = forms.CharField(label=u'Code du dossier', max_length=15)


class ImprimerEnMasseForm(forms.Form):
    low = forms.IntegerField(label='A partir de:')
    high = forms.IntegerField(label='Jusqu:')