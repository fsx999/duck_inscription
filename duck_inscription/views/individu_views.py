# coding=utf-8
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import RedirectView, FormView
from duck_inscription.forms.individu_forms import CodeEtudiantForm
from duck_inscription.models import Individu
from django_apogee.models import Individu as IndividuApogee


@login_required
@csrf_exempt
def test_username(request):
    if request.method == 'GET':
        cod_etu = request.GET.get("cod_etu", "")
        date_naissance = request.GET.get("date_naissance", "")
        try:
            if IndividuApogee.objects.filter(COD_ETU=cod_etu, date_nai_ind=date_naissance).count() != 0:
                return HttpResponse('true')
        except ValueError:
            pass
    return HttpResponse('false')


class DispatchIndividu(RedirectView):
    def get_redirect_url(self, **kwargs):
        Individu.objects.get_or_create(user=self.request.user, personal_email=self.request.user.email)
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
        individu.last_name = ia.LIB_NOM_PAT_IND
        individu.first_name1 = ia.LIB_PR1_IND
        individu.birthday = ia.DATE_NAI_IND
        individu.ine = ia.ine()
        individu.valid_ine = "O"
        individu.sex = ia.COD_SEX_ETU
        individu.etape = "info_perso"
        individu.save()

        return redirect(self.get_success_url())

@login_required()
def not_inscrit_universite(request):
    individu = request.user.individu
    individu.etape = "info_perso"
    individu.save()
    return redirect(individu.get_absolute_url())
