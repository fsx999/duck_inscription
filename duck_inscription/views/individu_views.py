# coding=utf-8
from __future__ import unicode_literals
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView, FormView, View, UpdateView, TemplateView
from extra_views import InlineFormSetView
from duck_inscription.forms.individu_forms import CodeEtudiantForm, InfoPersoForm, AdresseForm, AdresseBaseFormSet, \
    RecapitulatifIndividuForm, GMT0
from duck_inscription.models.individu_models import Individu as IndividuInscription, AdresseIndividu
from django_apogee.models import Individu as IndividuApogee
from django_apogee.models import BacOuxEqu
from duck_inscription.utils import verif_ine


class AccueilView(TemplateView):
    template_name = "duck_inscription/home/accueil.html"

    def get_context_data(self, **kwargs):
        context = super(AccueilView, self).get_context_data(**kwargs)
        context['wishes'] = self.request.user.individu.wishes.all()
        # context['auditeur'] = self.request.user.individu.wishes.filter(is_auditeur=True).count()
        return context


@login_required
@csrf_exempt
def test_username(request):
    if request.method == 'GET':
        cod_etu = request.GET.get("cod_etu", "")
        date_naissance = request.GET.get("date_naissance", "")
        print cod_etu, date_naissance
        try:
            if IndividuApogee.objects.filter(COD_ETU=cod_etu, date_nai_ind=date_naissance).count() != 0:
                return HttpResponse('true')
        except ValueError:
            pass
    return HttpResponse('false')


class DispatchIndividu(RedirectView):
    def get_redirect_url(self, **kwargs):
        IndividuInscription.objects.get_or_create(user=self.request.user, personal_email=self.request.user.email)
        return self.request.user.individu.get_absolute_url()


class CodeEtuManquant(FormView):
    form_class = CodeEtudiantForm
    template_name = "duck_inscription/individu/code_etudiant.html"
    premiere_connection = False  # parametre pour le code etudiant manquant si individu n'a pas pas renseigné

    def get_success_url(self):
        return self.request.user.individu.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super(CodeEtuManquant, self).get_context_data(**kwargs)
        context['premiere_connection'] = self.premiere_connection
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        individu = self.request.user.individu
        individu.student_code = data['code_etu']
        ia = IndividuApogee.objects.get(cod_etu=individu.student_code)
        individu.last_name = ia.lib_nom_pat_ind
        individu.first_name1 = ia.lib_pr1_ind
        individu.first_name2 = ia.lib_pr2_ind
        individu.first_name3 = ia.lib_pr3_ind
        individu.birthday = ia.date_nai_ind
        individu.ine = ia.ine()
        individu.valid_ine = "O"
        individu.sex = ia.cod_sex_etu
        individu.save()
        individu.modif_individu()
        return redirect(self.get_success_url())


@login_required()
def not_inscrit_universite(request):
    individu = request.user.individu
    individu.modif_individu()
    return redirect(individu.get_absolute_url())


class IneTestView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("true" if verif_ine(request.GET.get('ine', "")) else "false")


class BacTestView(View):
    def get(self, request, *args, **kwargs):
        message = "false"
        try:
            bac = request.GET.get('bac')
            annee_obtention = request.GET.get("annee_obtention")

            bac = BacOuxEqu.objects.get(pk=bac)
            annee_min = bac.daa_deb_vld_bac
            annee_max = bac.daa_fin_vld_bac
            if annee_min and annee_min > annee_obtention:
                return HttpResponse(message)
            if annee_max and annee_max < annee_obtention:
                return HttpResponse(message)

            message = "true"
        except:
            pass
        return HttpResponse(message)


class InfoPersoView(UpdateView):
    form_class = InfoPersoForm
    template_name = "duck_inscription/individu/info_peso.html"
# 2895018275V

    def get_context_data(self, **kwargs):
        context = super(InfoPersoView, self).get_context_data(**kwargs)
        context['individu'] = self.request.user.individu
        return context

    def get_object(self, queryset=None):
        return self.request.user.individu

    def get_success_url(self):
        return self.request.user.individu.get_absolute_url()

    def get_form_kwargs(self):
        kwargs = super(InfoPersoView, self).get_form_kwargs()

        if self.request.user.individu.student_code:
            kwargs.update({'readonly': True})
        return kwargs

    def get(self, request, *args, **kwargs):
        revenir = request.GET.get('revenir', None)
        individu = request.user.individu
        if revenir == "ok" and individu.student_code is None:
            individu.first_connection()
            return redirect(individu.get_absolute_url())

        return super(InfoPersoView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        data = form.cleaned_data
        individu = self.request.user.individu
        birthday = data['birthday']
        gt0 = GMT0()
        arg = {'tzinfo': gt0}
        birthday = datetime(*(birthday.timetuple()[:6]), **arg)
        taille_individu = IndividuApogee.objects.filter(
            lib_nom_pat_ind=data['last_name'].upper(),
            lib_pr1_ind=data['first_name1'].upper(),
            date_nai_ind=data['birthday']).count()
        if taille_individu and not individu.student_code:
            individu.code_etud_manquant()
        else:
            if individu.student_code:  # l'étudiant a un numéro, on n'enregistre pas nom,prénom, date de naissance
                data['last_name'] = individu.last_name
                data["first_name1"] = individu.first_name1
                data['birthday'] = individu.birthday
            for key in data:
                setattr(individu, key, data[key])
            individu.modif_adresse()
        individu.save()
        return redirect(self.get_success_url())

    # def get_initial(self):
    #     initial = super(InfoPersoView, self).get_initial()
    #     individu = self.request.user.individu
    #     if self.request.user.individu.student_code:
    #         return initial.update({
    #             'last_name': individu.last_name,
    #             'first_name1': individu.first_name1,
    #             'birthday': individu.birthday,
    #             'ine': individu.ine,
    #         })


class AdresseIndividuView(InlineFormSetView):
    form_class = AdresseForm
    formset_class = AdresseBaseFormSet
    extra = 2
    max_num = 2
    template_name = "duck_inscription/individu/adresse.html"
    model = IndividuInscription
    inline_model = AdresseIndividu
    fk_name = 'individu'
    can_delete = False

    def get_initial(self):
        return [{'type_hebergement': self.request.user.individu.type_hebergement_annuel}]

    # def get_formset_kwargs(self):
    #     kwargs = super(AdresseIndividuView, self).get_formset_kwargs()
    #     kwargs['initial'] = [{'type_hebergement': self.request.user.individu.type_hebergement_annuel}]
    #     return kwargs

    def formset_valid(self, formset):
        try:
            self.request.user.individu.type_hebergement_annuel = formset.cleaned_data[0]['type_hebergement']
        except KeyError:
            return redirect(self.request.user.individu.get_absolute_url())
        self.request.user.individu.save()
        return super(AdresseIndividuView, self).formset_valid(formset)

    def get_queryset(self):
        individu = self.request.user.individu
        return AdresseIndividu.objects.filter(individu=individu).order_by('type')

    def get_success_url(self):
        self.request.user.individu.recap()
        return self.request.user.individu.get_absolute_url()

    def get_object(self, queryset=None):
        return self.request.user.individu


class RecapitulatifIndividuView(FormView):
    template_name = "duck_inscription/individu/recapitulatif_individu.html"
    form_class = RecapitulatifIndividuForm

    def get_success_url(self):
        return self.request.user.individu.get_absolute_url()

    def get_context_data(self, **kwargs):

        context = super(RecapitulatifIndividuView, self).get_context_data(**kwargs)
        context['individu'] = InfoPersoForm(instance=self.request.user.individu)
        adresses = self.request.user.individu.adresses.all().order_by('type')
        context['type_hebergement_annuel'] = self.request.user.individu.type_hebergement_annuel
        context['adresses'] = []
        for adresse in adresses:
            # context['adresses'].append(AdresseFormReadOnly(instance=adresse))
            adresseForm = AdresseForm(instance=adresse)
            if adresseForm['type'].value() == u"1":
                adresseForm.type_hidden = 1
            adresseForm.fields.pop('type')
            context['adresses'].append(adresseForm)

        return context

    def get(self, request, *args, **kwargs):
        if self.kwargs.get('option', None) in ['modif_adresse', 'modif_individu']:

            getattr(self.request.user.individu, self.kwargs['option'])()

            return redirect(self.get_success_url())

        return super(RecapitulatifIndividuView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        self.request.user.individu.accueil()
        return redirect(self.get_success_url())
