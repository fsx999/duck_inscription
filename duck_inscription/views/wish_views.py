# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import datetime
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from django.shortcuts import redirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.generic import TemplateView, View, UpdateView
from django.views.generic.edit import FormView
from floppyforms import ModelChoiceField
import xworkflows
import json
from duck_inscription.forms import WishGradeForm, ListeDiplomeAccesForm, DemandeEquivalenceForm, \
    NoteMasterForm, ListeAttenteCandidatureForm, ChoixPaiementDroitForm, DemiAnneeForm, \
    NbPaiementPedaForm, ValidationPaiementForm, ListeAttenteInscriptionForm, ListeAttenteEquivalenceForm
from duck_inscription.models import Wish, SettingsEtape, NoteMasterModel, CentreGestionModel, PaiementAllModel, \
    SettingAnneeUni
from xhtml2pdf import pdf as pisapdf
from xhtml2pdf import pisa
from django.conf import settings
from duck_inscription.views import IndividuMixin

__author__ = 'paul'


class WishIndividuMixin(object):
    """
    recupere le voeu à partir du pk si user = staff, ou bien à partir de l'user
    """

    @property
    def individu(self):
        """
        :return: l'individu en fonction du pk de l'url (en fonction des droits)
        """
        individu = getattr(self, '_individu', None)
        if not individu:
            self._individu = self.wish.individu
            return self._individu
        return individu

    @property
    def wish(self):
        """
        :return: le voeu en fonction du pk de l'url (en fonction des droits)
        """
        wish = getattr(self, '_wish', None)
        if not wish:
            if self.request.user.is_staff:
                self._wish = Wish.objects.get(pk=self.kwargs['pk'])
            else:
                self._wish = self.request.user.individu.wishes.get(pk=self.kwargs['pk'])
            return self._wish
        return wish


class NewWishView(FormView, IndividuMixin):
    """
    permet de créer un voeu
    """
    template_name = "duck_inscription/wish/new_wish.html"
    form_class = WishGradeForm

    def get_context_data(self, **kwargs):
        context = super(NewWishView, self).get_context_data(**kwargs)
        context['individu'] = self.individu
        return context

    def form_valid(self, form):
        etape = form.cleaned_data['etape']
        individu = self.individu
        annee = SettingAnneeUni.objects.filter(inscription=True).last()
        if not individu.wishes.filter(etape=etape).count() == 0:  # verifi qu'un voeu sur l'étape n'existe pas
            return redirect(reverse("accueil", kwargs={'pk': individu.pk}))
        wish = Wish.objects.get_or_create(etape=etape, individu=individu, annee=annee)[0]
        wish.save()
        wish.ouverture_equivalence()
        return redirect(wish.get_absolute_url())


class StepView(TemplateView, IndividuMixin):
    """
    la vue qui retourne un widget contenant les etapes d'un diplome
    """
    def get(self, request, *args, **kwargs):
        if self.request.GET.get("diplome", "") != "":
            step_wish = [wish.etape for wish in self.individu.wishes.all()]
            liste_pk = []
            for step in step_wish:
                # liste etapes des diplomes déjà utilisé
                liste_pk.extend(step.cursus.settingsetape_set.values_list('pk', flat=True))
            # les étapes moins les étapes des diplomes déjà utilisés
            etape = ModelChoiceField(
                queryset=SettingsEtape.objects.filter(diplome=self.request.GET.get("diplome")).exclude(
                    pk__in=liste_pk).exclude(is_inscription_ouverte=False).order_by('label'), )  #
            return HttpResponse(
                etape.widget.render(name='etape', value='', attrs={'id': 'id_etape', 'class': "required"}))

        return HttpResponse('echec')


class DeleteWish(View):
    """
    suppression du voeu
    """
    def get(self, request, *args, **kwargs):
        if self.request.user.is_staff:
            wish = Wish.objects.get(pk=kwargs.get('pk', None))
        else:
            wish = self.request.user.individu.wishes.get(pk=kwargs.get('pk', None))
        individu = wish.individu
        wish.delete()
        return redirect(reverse("accueil", kwargs={'pk': individu.pk}))


class OuvertureEquivalence(TemplateView, WishIndividuMixin):
    """
    Ouverture des équivalences
    """
    template_name = "duck_inscription/wish/ouverture_equivalence.html"

    def get_context_data(self, **kwargs):
        context = super(OuvertureEquivalence, self).get_context_data(**kwargs)
        context['individu'] = self.individu
        context['date'] = self.wish.etape.date_ouverture_equivalence
        return context

    def get(self, request, *args, **kwargs):
        wish = self.wish
        try:
            wish.liste_diplome()  # si l'étape est ouverte, la transition s'effectue
            return redirect(wish.get_absolute_url())
        except xworkflows.base.ForbiddenTransition:
            # la transition n'est pas autorisé (étape non ouverte) on affiche le template
            return super(OuvertureEquivalence, self).get(request, *args, **kwargs)


class ListeDiplomeAccesView(FormView, WishIndividuMixin):
    """

    """
    template_name = "duck_inscription/wish/liste_diplome_acces.html"
    form_class = ListeDiplomeAccesForm

    def get_context_data(self, **kwargs):
        context = super(ListeDiplomeAccesView, self).get_context_data(**kwargs)
        try:
            context['wish'] = self.wish
        except Wish.DoesNotExist:
            return redirect(reverse("accueil", kwargs={'pk': self.individu.pk}))
        return context

    def get_form(self, form_class):
        wish = self.wish
        return form_class(step=wish.etape, **self.get_form_kwargs())

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        try:
            form = self.get_form(form_class)
        except Wish.DoesNotExist:
            return redirect(reverse("accueil", kwargs={'pk': self.individu.pk}))
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        try:
            form = self.get_form(form_class)
        except Wish.DoesNotExist:
            return redirect(reverse("accueil", kwargs={'pk': self.individu.pk}))
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return super(ListeDiplomeAccesView, self).form_invalid(form)

    def form_valid(self, form):
        data = form.cleaned_data
        wish = self.wish
        wish.diplome_acces = data['liste_diplome']
        wish.demande_equivalence()
        return redirect(wish.get_absolute_url())


class DemandeEquivalenceView(FormView, WishIndividuMixin):
    template_name = "duck_inscription/wish/demande_equivalence.html"
    form_class = DemandeEquivalenceForm

    def get_context_data(self, **kwargs):
        context = super(DemandeEquivalenceView, self).get_context_data(**kwargs)
        context['wish'] = self.wish
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        wish = self.wish
        if json.loads(data['demande_equivalence'].lower()):
            wish.equivalence()
        else:
            wish.ouverture_candidature()
        return redirect(wish.get_absolute_url())


class ListeAttenteEquivalenceView(FormView, WishIndividuMixin):
    template_name = 'duck_inscription/wish/liste_attente_equivalence.html'
    form_class = ListeAttenteEquivalenceForm

    def get_context_data(self, **kwargs):
        context = super(ListeAttenteEquivalenceView, self).get_context_data(**kwargs)
        context['wish'] = self.wish
        return context

    def form_valid(self, form):
        wish = self.wish
        demande_attente = form.cleaned_data['demande_attente']
        if demande_attente == 'O':
            print "coucou"
            wish.mis_liste_attente_equi()
        elif demande_attente == 'N':
            individu = wish.individu
            wish.delete()
            return redirect(reverse('accueil', kwargs={'pk': individu.pk}))
        return redirect(wish.get_absolute_url())


class EquivalenceView(TemplateView, WishIndividuMixin):
    template_name = "duck_inscription/wish/equivalence.html"

    def get(self, request, *args, **kwargs):
        wish = self.wish
        if request.GET.get("valide", False):
            wish.valide = True
            wish.save()
        context = self.get_context_data()
        context['wish'] = wish
        return self.render_to_response(context)


class EquivalencePdfView(TemplateView, WishIndividuMixin):
    template_name = "duck_inscription/wish/etiquette.html"
    etape = "equivalence"  # à surcharger pour candidature
    fonction_impression = 'do_pdf_equi'

    def render_to_response(self, context, **response_kwargs):

        try:
            wish = self.wish
        except Wish.DoesNotExist:
            return redirect(self.individu.get_absolute_url())

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=%s_%s.pdf' % (self.etape, wish.etape.cod_etp)

        response.write(getattr(wish, self.fonction_impression)(request=self.request, context=context))
        return response


class OuvertureCandidature(TemplateView, WishIndividuMixin):
    template_name = "duck_inscription/wish/ouverture_candidature.html"

    def get_context_data(self, **kwargs):
        context = super(OuvertureCandidature, self).get_context_data(**kwargs)
        context['wish'] = self.wish
        return context

    def get(self, request, *args, **kwargs):
        try:
            self.wish.note_master()
            return redirect(self.wish.get_absolute_url())
        except xworkflows.ForbiddenTransition:
            return super(OuvertureCandidature, self).get(request, *args, **kwargs)


class NoteMasterView(FormView, WishIndividuMixin):
    form_class = NoteMasterForm
    template_name = "duck_inscription/wish/note_master.html"

    def form_valid(self, form):
        wish = self.wish
        try:
            if getattr(wish, 'notemastermodel', None):
                form.instance.pk = wish.notemastermodel.pk
        except NoteMasterModel.DoesNotExist:
            pass
        form.instance.wish = wish
        form.save()
        try:
            wish.candidature()
            return redirect(wish.get_absolute_url())
        except xworkflows.ForbiddenTransition:
            return super(NoteMasterView, self).form_valid(form)


class CandidatureView(EquivalenceView):
    template_name = "duck_inscription/wish/candidature.html"



class CandidaturePdfView(EquivalencePdfView):
    etape = "candidature"
    fonction_impression = 'do_pdf_candi'


class ListeAttenteCandidatureView(ListeAttenteEquivalenceView):
    template_name = 'duck_inscription/wish/liste_attente_candidature.html'
    form_class = ListeAttenteCandidatureForm

    def form_valid(self, form):
        wish = self.wish
        demande_attente = form.cleaned_data['demande_attente']
        if demande_attente == 'O':
            wish.mis_liste_attente_candi()
        elif demande_attente == 'N':
            individu = wish.individu
            wish.delete()
            return redirect(reverse('accueil', kwargs={'pk': individu.pk}))
        return redirect(wish.get_absolute_url())

class OuverturePaiementView(TemplateView, WishIndividuMixin):
    template_name = "duck_inscription/wish/ouverture_paiement.html"

    def get_context_data(self, **kwargs):
        context = super(OuverturePaiementView, self).get_context_data(**kwargs)
        context['wish'] = self.wish
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        wish = context['wish']
        try:

            wish.dossier_inscription()
            return redirect(wish.get_absolute_url())
        except xworkflows.ForbiddenTransition as e:
            pass
        return self.render_to_response(context)


class ChoixIedFpView(TemplateView):
    template_name = "duck_inscription/wish/choix_ied_fp.html"

    def get(self, request, *args, **kwargs):
        centre = self.request.GET.get('centre', None)
        if centre in ['ied', 'fp']:
            wish = self.request.user.individu.wishes.get(pk=self.kwargs['pk'])
            wish.centre_gestion = CentreGestionModel.objects.get(centre_gestion=centre)
            try:
                if centre == 'fp':
                    wish.inscription()
                else:
                    wish.droit_universitaire()
            except xworkflows.InvalidTransitionError:
                pass
            return redirect(wish.get_absolute_url())
        return super(ChoixIedFpView, self).get(request, *args, **kwargs)


class DroitView(UpdateView):
    model = PaiementAllModel
    template_name = "duck_inscription/individu/dossier_inscription/base_formulaire.html"
    forms = {
        'droit_univ': ChoixPaiementDroitForm,
        'choix_demi_annee': DemiAnneeForm,
        'nb_paiement': NbPaiementPedaForm,
        "recapitulatif": ValidationPaiementForm
    }

    def get_template_names(self):
        if self.object.etape == "recapitulatif":
            return "duck_inscription/wish/recapitulatif.html"
        return self.template_name

    def post(self, request, *args, **kwargs):
        if request.POST.get('precedent', None):
            self.object = self.get_object()
            if self.object.precedente_etape():
                return redirect(reverse(self.request.resolver_match.url_name, kwargs=self.kwargs))
        return super(DroitView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        if self.object.next_etape():
            return reverse(self.request.resolver_match.url_name, kwargs=self.kwargs)
        else:
            wish = self.request.user.individu.wishes.get(pk=self.kwargs['pk'])

            wish.inscription()
            return wish.get_absolute_url()

    def get_form_class(self):
        return self.forms[self.object.etape]

    def get_object(self, queryset=None):
        wish = self.request.user.individu.wishes.get(pk=self.kwargs['pk'])
        return PaiementAllModel.objects.get_or_create(wish=wish)[0]


class InscriptionView(TemplateView):
    template_name = "duck_inscription/wish/inscription.html"

    def get(self, request, *args, **kwargs):
        wish = request.user.individu.wishes.get(pk=self.kwargs['pk'])

        if request.GET.get("valide", False):
            wish.valide_liste()
            if not wish.centre_gestion:
                wish.centre_gestion = CentreGestionModel.objects.get(centre_gestion='ied')

            if not wish.is_ok and not wish.is_reins_formation() and not wish.centre_gestion.centre_gestion == 'fp':
                try:
                    wish.liste_attente_inscription()
                except xworkflows.InvalidTransitionError:
                    pass
                return redirect(wish.get_absolute_url())
        context = self.get_context_data()
        context['wish'] = wish
        return self.render_to_response(context)


class ListeAttenteInscriptionView(FormView):
    template_name = 'duck_inscription/wish/liste_attente_inscription.html'
    form_class = ListeAttenteInscriptionForm

    def form_valid(self, form):
        wish = self.get_context_data()['wish']
        demande_attente = form.cleaned_data['demande_attente']
        if demande_attente == 'O':
            wish.liste_attente = True
            if not wish.date_liste_inscription:
                wish.date_liste_inscription = datetime.datetime.today()
            wish.save()
        else:
            wish.delete()
            return redirect(reverse('accueil'))
        return redirect(wish.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super(ListeAttenteInscriptionView, self).get_context_data(**kwargs)
        self.wish = context['wish'] = self.request.user.individu.wishes.get(pk=self.kwargs['pk'])
        return context


# ##le dossier d'inscription


class InscriptionPdfView(TemplateView):
    template_name = "duck_inscription/wish/ordre_virement.html"
    templates = {
        'dossier_inscription': "duck_inscription/wish/dossier_inscription_pdf.html",
        'ordre_virement': "duck_inscription/wish/ordre_virement.html",
        'formulaire_paiement_frais': "duck_inscription/wish/formulaire_paiement_frais.html",
        'formulaire_paiement_droit': "duck_inscription/wish/formulaire_paiement_droit.html",
        'etiquette': 'duck_inscription/wish/etiquette.html',
        'autorisation_photo': 'duck_inscription/wish/autorisation_photo.html'
    }

    def get_context_data(self, **kwargs):
        context = super(InscriptionPdfView, self).get_context_data(**kwargs)
        if self.request.user.is_staff:
            context['wish'] = context['voeu'] = Wish.objects.get(pk=self.kwargs['pk'])
            context['individu'] = context['wish'].individu
        else:
            context['individu'] = self.request.user.individu
            try:
                context['wish'] = context['voeu'] = self.request.user.individu.wishes.select_related().get(
                    pk=self.kwargs['pk'])
            except Wish.DoesNotExist:
                return redirect(reverse('accueil'))

        if not context['wish'].centre_gestion:
            context['wish'].centre_gestion = CentreGestionModel.objects.get(centre_gestion='ied')
            context['wish'].save()
        if context['wish'].centre_gestion.centre_gestion == 'ied':
            context['paiement_frais'] = context['wish'].paiementallmodel
            try:
                context['tarif_versement_frais'] = context['wish'].frais_peda() / context[
                    'paiement_frais'].nb_paiement_frais
            except ZeroDivisionError:
                context['wish'].droit_universitaire()
                context['wish'].save()
                return redirect(context['wish'].get_absolute_url())
        context['static'] = os.path.join(settings.BASE_DIR + '/duck_inscription/duck_theme_ied/static/images/').replace(
            '\\', '/')
        return context

    def get_template_names(self):
        tempate_names = super(InscriptionPdfView, self).get_template_names()
        tempate_names.append('duck_inscription/wish/%s_pdf.html' % (self.etape,))
        return tempate_names

    def render_to_response(self, context, **response_kwargs):
        response = HttpResponse(mimetype='application/pdf')
        try:
            response['Content-Disposition'] = 'attachment; filename=inscription_%s.pdf' % context['wish'].etape.label
        except KeyError:
            return redirect(reverse('home'))

        pdf = pisapdf.pisaPDF()
        wish = context['wish']
        if not wish.centre_gestion:
            wish.centre_gestion = CentreGestionModel.objects.get(centre_gestion='ied')
            wish.save()
        if wish.centre_gestion.centre_gestion == 'ied':
            pdf.addDocument(pisa.CreatePDF(render_to_string(self.templates['etiquette'], context,
                                                            context_instance=RequestContext(self.request))))

        pdf.addDocument(pisa.CreatePDF(render_to_string(self.templates['dossier_inscription'], context,
                                                        context_instance=RequestContext(self.request))))
        pdf.addDocument(pisa.CreatePDF(render_to_string(self.templates['autorisation_photo'], context,
                                                        context_instance=RequestContext(self.request))))

        if not wish.centre_gestion:
            c = CentreGestionModel.objects.get(centre_gestion='ied')
            wish.centre_gestion = c
            wish.save()
        if wish.centre_gestion.centre_gestion == 'ied':
            pdf.addDocument(pisa.CreatePDF(render_to_string(self.templates['formulaire_paiement_droit'], context,
                                                            context_instance=RequestContext(self.request))))
            pdf.addDocument(pisa.CreatePDF(render_to_string(self.templates['formulaire_paiement_frais'], context,
                                                            context_instance=RequestContext(self.request))))
            if not wish.paiementallmodel.moyen_paiement:
                wish.droit_universitaire()
                return redirect(wish.get_absolute_url())

            if wish.paiementallmodel.moyen_paiement.type == 'v':
                pdf.addDocument(pisa.CreatePDF(render_to_string(self.templates['ordre_virement'], context,
                                                                context_instance=RequestContext(self.request))))
        pdf.addFromFileName(wish.etape.annee.transfert_pdf.file.file.name)
        pdf.addFromFileName(wish.etape.annee.bourse_pdf.file.file.name)
        pdf.addFromFileName(wish.etape.annee.pieces_pdf.file.file.name)

        pdf.join(response)
        return response
