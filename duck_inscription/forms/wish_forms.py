# -*- coding: utf-8 -*-
import floppyforms as forms
from django_apogee.models import Diplome
from duck_inscription.models import DiplomeEtape, SettingsEtape, ListeDiplomeAces


__author__ = 'paul'



class WishGradeForm(forms.Form):
    diplome = forms.ModelChoiceField(queryset=DiplomeEtape.objects.exclude(is_inscription_ouverte=False), label=u"Diplôme :",
                                    help_text=u"(Veuillez choisir un diplôme)")

    etape = forms.ModelChoiceField(queryset=SettingsEtape.objects.exclude(is_inscription_ouverte=False), label=u"Niveau :",
                                  help_text=u"(Veuillez choisier le niveau de votre diplôme)")




class ListeDiplomeAccesForm(forms.Form):
    liste_diplome = forms.ModelChoiceField(queryset=ListeDiplomeAces.objects.all())

    def __init__(self, *args, **kwargs):
        step = kwargs.pop('step')
        super(ListeDiplomeAccesForm, self).__init__(*args, **kwargs)
        self.fields['liste_diplome'] = forms.ModelChoiceField(
            queryset=step.diplome_aces.all(),
            label=u"Diplôme d'accès",
            empty_label=u"Aucun diplôme de la liste",
            required=False
        )
#
#
class DemandeEquivalenceForm(forms.Form):
    demande_equivalence = forms.ChoiceField(choices=(('', '-------'), ('False', 'Non'), ('True', 'Oui')),
                                            label=u"Demande d'équivalence",
                                            help_text=u"(Renseignez si vous souhaitez faire une"
                                                      u" demande d'équivalence ou pas)")

#
# class ListeAttenteEquivalenceForm(forms.Form):
#     demande_attente = forms.ChoiceField(choices=(('O', 'Oui'), ('N', 'Non')),
#                                         label=u"Voulez-vous être mis en liste d'attente ?")
#
#
# class NoteMasterForm(forms.ModelForm):
#     moyenne_general = forms.FloatField(label=u"Moyenne générale", max_value=20, min_value=0, required=False)
#     note_memoire = forms.FloatField(label=u"Note du mémoire", max_value=20, min_value=0, required=False)
#     note_stage = forms.FloatField(label=u"Note du stage", max_value=20, min_value=0, required=False)
#
#     class Meta:
#         model = NoteMasterModel
#         fields = ('moyenne_general', 'note_memoire', 'note_stage')
#
#
# class ListeAttenteCandidatureForm(forms.Form):
#     demande_attente = forms.ChoiceField(choices=(('O', 'Oui'), ('N', 'Non')),
#                                         label=u"Voulez-vous être mis en liste d'attente ?")
#
#
# class ListeAttenteInscriptionForm(forms.Form):
#     demande_attente = forms.ChoiceField(choices=(('O', 'Oui'), ('N', 'Non')),
#                                         label=u"Voulez-vous être mis en liste d'attente ?")
#
#
# class ChoixPaiementDroitForm(forms.ModelForm):
#
#     class Meta:
#         model = PaiementAllModel
#         fields = ('moyen_paiement',)
#
#
# class DemiAnneeForm(forms.ModelForm):
#     demi_annee = forms.BooleanField(widget=forms.Select(choices=(('', '----'),
#                                                                  ('1', "Je m'inscris à un semestre"),
#                                                                  ('0', "Je m'inscris à une année entière")),),
#                                     required=False)
#
#
#     class Meta:
#         model = PaiementAllModel
#         fields = ('demi_annee',)
#
#
# class NbPaiementPedaForm(forms.ModelForm):
#
#     def __init__(self, *args, **kwargs):
#         super(NbPaiementPedaForm, self).__init__(*args, **kwargs)
#         choices = [('', '-----')] + [(x + 1, x + 1) for x in range(self.instance.wish.step.nb_paiement)]
#         self.fields['nb_paiement_frais'] = forms.ChoiceField(choices=choices, label=u"Nombre de paiements")
#
#     class Meta:
#         model = PaiementAllModel
#         fields = ('nb_paiement_frais',)
#
#
# class ValidationPaiementForm(forms.ModelForm):
#     valider = forms.CharField()
#
#     class Meta:
#         model = PaiementAllModel
#         fields = ('id',)
#
#
# class NewAuditeurForm(forms.Form):
#     auditeur = forms.NullBooleanField(
#         label=u"Voullez vous faire une demande de préinscription en tant qu'auditeur libre",
#         widget=forms.Select(
#             choices=(("", "-----"), ("True", "Oui"), ("False", "Non")),
#             attrs={'class': 'required auto'}
#         )
#     )
#
#     def clean_auditeur(self):
#         if self.cleaned_data.get('auditeur', None) is None:
#             raise forms.ValidationError(u'Vous devez choisir')
#         return self.cleaned_data.get('auditeur', None)
#
