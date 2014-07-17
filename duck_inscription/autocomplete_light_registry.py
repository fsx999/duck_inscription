# coding=utf-8
from __future__ import unicode_literals
import autocomplete_light
from django_apogee.models import ComBdi, Etablissement


autocomplete_light.register(
    ComBdi,
    limit_choices=40,
    search_fields=['cod_bdi'],
    attrs={
        "placeholder": u'Veuillez saissir un code postal',
        'data-autocomplete-minimum-characters': 5,
        'class': 'form-control'
    })


class AutocompleteEtablissement(autocomplete_light.AutocompleteModelBase):
    limit_choices = 400
    search_fields = ['cod_dep__cod_dep']
    order_by = 'lib_etb'
    autocomplete_js_attributes = {
        "placeholder": u"Veuillez saissir un code de département (99 pour l'étranger",
        'minimum_characters': 2, }
    widget_template = "duck_inscription/individu/dossier_inscription/etablissement_widget.html"

    def choices_for_request(self):
        # return super(AutocompleteEtablissement, self).choices_for_request()
        q = self.request.GET.get('q', '')
        cod_tpe_id = self.request.GET.get('cod_tpe_id', None)
        choices = self.choices.exclude(lib_off_etb='ETAB_ETR').exclude(lib_off_etb='INCONNU').exclude(lib_etb='INCONNU').order_by('lib_etb')
        if cod_tpe_id:
            choices = choices.filter(cod_tpe_id=cod_tpe_id)
        else:
            return choices.none()
        if cod_tpe_id == '15' or cod_tpe_id == '10':
            return self.order_choices(choices)[0:self.limit_choices]
        if q:
            if len(q) == 2:
                q = '0' + q

            if q == '099':

                choices = choices.filter(cod_dep__cod_dep=q, cod_pay_adr_etb_id__isnull=True)
            else:
                if len(q) == 3:
                    choices = choices.filter(cod_dep__cod_dep=q)
                elif len(q) == 5:
                    choices = choices.filter(cod_pos_adr_etb=q)
                else:
                    return choices.none()
        else:
            return choices.none()


        return self.order_choices(choices)[0:self.limit_choices]

autocomplete_light.register(
    Etablissement,
    AutocompleteEtablissement,
    name='EtablissementAutocomplete'
)


