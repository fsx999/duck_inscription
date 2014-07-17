# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import StringIO
import os
from tempfile import TemporaryFile, NamedTemporaryFile
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
import datetime
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from django.shortcuts import redirect
from django.template import RequestContext
from django.template.loader import render_to_string
from django.views.generic import TemplateView, View, UpdateView
from django.views.generic.edit import FormView
from floppyforms import ModelChoiceField
from wkhtmltopdf.views import PDFTemplateResponse, PDFTemplateView
import xworkflows
import json
from duck_inscription.forms import WishGradeForm, ListeDiplomeAccesForm, DemandeEquivalenceForm, \
    ListeAttenteEquivalenceForm, NoteMasterForm, ListeAttenteCandidatureForm, ChoixPaiementDroitForm, DemiAnneeForm, \
    NbPaiementPedaForm, ValidationPaiementForm, ListeAttenteInscriptionForm
from duck_inscription.models import Wish, SettingsEtape, NoteMasterModel, CentreGestionModel, PaiementAllModel, \
    DossierInscription
from xhtml2pdf import pdf as pisapdf
from xhtml2pdf import pisa
from duck_inscription.templatetags.lib_inscription import annee_en_cour
from django.conf import settings
from settings import BASE_DIR

__author__ = 'paul'


class NewWishView(FormView):
    template_name = "duck_inscription/wish/new_wish.html"
    form_class = WishGradeForm

    def form_valid(self, form):
        etape = form.cleaned_data['etape']
        individu = self.request.user.individu

        if not individu.wishes.filter(etape=etape).count() == 0:
            return redirect(reverse("accueil"))
        wish = Wish.objects.get_or_create(etape=etape, individu=individu)[0]
        wish.save()
        wish.ouverture_equivalence()
        return redirect(wish.get_absolute_url())


class StepView(TemplateView):
    def get(self, request, *args, **kwargs):
        if self.request.GET.get("diplome", "") != "":
            step_wish = []
            for wish in self.request.user.individu.wishes.all():
                for step in wish.etape.diplome.settingsetape_set.exclude(date_ouverture_candidature__isnull=False):
                    step_wish.append(step.pk)

            etape = ModelChoiceField(
                queryset=SettingsEtape.objects.filter(diplome=self.request.GET.get("diplome")).exclude(
                    pk__in=step_wish).exclude(is_inscription_ouverte=False).order_by('label'), )
            return HttpResponse(
                etape.widget.render(name='etape', value='', attrs={'id': 'id_etape', 'class': "required"}))

        return HttpResponse('echec')


class DeleteWish(View):
    def get(self, request, *args, **kwargs):
        self.request.user.individu.wishes.filter(pk=kwargs.get('pk', None)).delete()
        return redirect(reverse("accueil"))


class OuvertureEquivalence(TemplateView):
    template_name = "duck_inscription/wish/ouverture_equivalence.html"

    def get_context_data(self, **kwargs):
        context = super(OuvertureEquivalence, self).get_context_data(**kwargs)
        context['date'] = self.request.user.individu.wishes.get(pk=self.kwargs['pk']).etape.date_ouverture_equivalence
        return context

    def get(self, request, *args, **kwargs):
        wish = self.request.user.individu.wishes.get(pk=self.kwargs['pk'])
        try:
            wish.liste_diplome()
            return redirect(wish.get_absolute_url())
        except xworkflows.base.ForbiddenTransition:
            return super(OuvertureEquivalence, self).get(request, *args, **kwargs)


class ListeDiplomeAccesView(FormView):
    template_name = "duck_inscription/wish/liste_diplome_acces.html"
    form_class = ListeDiplomeAccesForm

    def get_context_data(self, **kwargs):
        context = super(ListeDiplomeAccesView, self).get_context_data(**kwargs)
        try:
            context['wish'] = self.request.user.individu.wishes.get(pk=self.kwargs['pk'])
        except Wish.DoesNotExist:
            return redirect(reverse("accueil"))
        return context

    def get_form(self, form_class):
        wish = self.request.user.individu.wishes.get(pk=self.kwargs['pk'])
        return form_class(step=wish.etape, **self.get_form_kwargs())

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        try:
            form = self.get_form(form_class)
        except Wish.DoesNotExist:
            return redirect(reverse("accueil"))
        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        try:
            form = self.get_form(form_class)
        except Wish.DoesNotExist:
            return redirect(reverse("home"))
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return super(ListeDiplomeAccesView, self).form_invalid(form)

    def form_valid(self, form):
        data = form.cleaned_data
        wish = self.request.user.individu.wishes.get(pk=self.kwargs['pk'])
        wish.diplome_acces = data['liste_diplome']
        wish.demande_equivalence()
        return redirect(wish.get_absolute_url())


class DemandeEquivalenceView(FormView):
    template_name = "duck_inscription/wish/demande_equivalence.html"
    form_class = DemandeEquivalenceForm

    def form_valid(self, form):
        data = form.cleaned_data
        wish = self.request.user.individu.wishes.get(pk=self.kwargs['pk'])
        if json.loads(data['demande_equivalence'].lower()):
            wish.equivalence()
        else:
            wish.ouverture_candidature()
        # wish.dispatch()
        return redirect(wish.get_absolute_url())


class ListeAttenteEquivalenceView(TemplateView):
    template_name = 'duck_inscription/wish/liste_attente_equivalence.html'

    def get_context_data(self, **kwargs):
        context = super(ListeAttenteEquivalenceView, self).get_context_data(**kwargs)
        context['wish'] = self.request.user.individu.wishes.get(pk=self.kwargs['pk'])
        return context


class EquivalenceView(TemplateView):
    template_name = "duck_inscription/wish/equivalence.html"

    def get(self, request, *args, **kwargs):
        wish = request.user.individu.wishes.get(pk=self.kwargs['pk'])
        if request.GET.get("valide", False):
            wish.valide = True
            wish.save()
        context = self.get_context_data()
        context['wish'] = wish
        return self.render_to_response(context)


class EquivalencePdfView(TemplateView):
    template_name = "duck_inscription/wish/etiquette.html"
    etape = "equivalence"  # à surcharger pour candidature

    def get_context_data(self, **kwargs):
        context = super(EquivalencePdfView, self).get_context_data(**kwargs)
        context['individu'] = self.request.user.individu
        context['voeu'] = self.request.user.individu.wishes.get(pk=self.kwargs['pk'])
        context['logo_p8'] = "file://" + settings.BASE_DIR + '/duck_theme_ied/static/images/logop8.jpg'
        context['url_font'] = settings.BASE_DIR + '/duck_theme_ied/static/font/ConnectCode39.ttf'
        context['url_static'] = settings.BASE_DIR + '/duck_theme_ied/static/images/'
        context['annee_univ'] = annee_en_cour()

        return context

    def get_template_names(self):
        tempate_names = super(EquivalencePdfView, self).get_template_names()
        tempate_names.append(
            'duck_inscription/wish/%s_pdf.html' % self.etape)  # permet d'avoir la meme classe pour candidature
        return tempate_names

    def get_file(self):
        """
        Il faut la surcharger pour les candidatures
        Doit retourner le l'url du doccument du doccument a fussionner
        """
        step = self.request.user.individu.wishes.get(pk=self.kwargs['pk']).etape

        return step.document_equivalence

    def render_to_response(self, context, **response_kwargs):
        response = HttpResponse(mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=%s_%s.pdf' % (self.etape, context['voeu'].etape.cod_etp)
        try:
            url_doc = self.get_file().file
        except Wish.DoesNotExist:
            return redirect(self.request.user.individu.get_absolute_url())
        context['url_doc'] = url_doc
        url_doc.open('r')

        context['num_page'] = self._num_page(url_doc)  # on indique le nombre de page pour la page 1

        return context['voeu'].do_pdf_equi(flux=response, templates=self.get_template_names(), request=self.request,
                                           context=context)

    def _num_page(self, url_doc):
        return PdfFileReader(url_doc).getNumPages()


    def do_pdf(self, file):
        """
        retourne un pdf sans la première page
        """
        result = StringIO.StringIO()
        output = PdfFileWriter()
        input1 = PdfFileReader(file)
        for x in range(1, input1.getNumPages()):
            output.addPage(input1.getPage(x))
        output.write(result)

        return result


class OuvertureCandidature(TemplateView):
    template_name = "duck_inscription/wish/ouverture_candidature.html"

    def get_context_data(self, **kwargs):
        context = super(OuvertureCandidature, self).get_context_data(**kwargs)
        try:
            context['wish'] = self.wish
        except AttributeError:
            context['wish'] = self.request.user.individu.wishes.get(pk=self.kwargs['pk'])
        return context

    def get(self, request, *args, **kwargs):
        self.wish = self.request.user.individu.wishes.get(pk=self.kwargs['pk'])
        try:
            self.wish.note_master()
            return redirect(self.wish.get_absolute_url())
        except xworkflows.ForbiddenTransition:
            return super(OuvertureCandidature, self).get(request, *args, **kwargs)


class NoteMasterView(FormView):
    form_class = NoteMasterForm
    template_name = "duck_inscription/wish/note_master.html"

    def form_valid(self, form):
        wish = self.request.user.individu.wishes.get(pk=self.kwargs['pk'])
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

    def get_file(self):
        """
        Il faut la surcharger pour les candidatures
        Doit retourner le l'url du doccument du doccument a fussionner
        """
        step = self.request.user.individu.wishes.get(pk=self.kwargs['pk']).etape

        return step.document_candidature

    def render_to_response(self, context, **response_kwargs):
        response = HttpResponse(mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=%s_%s.pdf' % (self.etape, context['voeu'].etape.cod_etp)
        try:
            url_doc = self.get_file().file
        except Wish.DoesNotExist:
            return redirect(self.request.user.individu.get_absolute_url())
        context['url_doc'] = url_doc
        url_doc.open('r')

        context['num_page'] = self._num_page(url_doc)  # on indique le nombre de page pour la page 1

        return context['voeu'].do_pdf_candi(flux=response, templates=self.get_template_names(), request=self.request,
                                            context=context)


class ListeAttenteCandidatureView(ListeAttenteEquivalenceView):
    template_name = 'wish/liste_attente_candidature.html'
    form_class = ListeAttenteCandidatureForm

    def get(self, request, *args, **kwargs):
        return super(ListeAttenteEquivalenceView, self).get(request, *args, **kwargs)


class OuverturePaiementView(TemplateView):
    template_name = "duck_inscription/wish/ouverture_paiement.html"

    def get_context_data(self, **kwargs):
        context = super(OuverturePaiementView, self).get_context_data(**kwargs)
        context['wish'] = self.request.user.individu.wishes.get(pk=self.kwargs['pk'])
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
            wish.droit_universitaire()
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
        #
        # try:
        #     if wish.individu.dossier_inscription.etape != 'recapitulatif':
        #         wish.etape = wish.dispatch_etape = "ouverture_paiement"
        #         wish.save()
        #         return redirect(wish.get_absolute_url())
        # except DossierInscription.DoesNotExist:
        #     wish.etape = wish.dispatch_etape = "ouverture_paiement"
        #     wish.save()
        #     return redirect(wish.get_absolute_url())
        #
        # if \
        #             wish.individu.dossier_inscription.dernier_etablissement == None:
        #     wish.etape = wish.dispatch_etape = "ouverture_paiement"
        #     wish.save()
        #     return redirect(wish.get_absolute_url())

        if request.GET.get("valide", False):
            wish.valide_liste()
            if not wish.centre_gestion:
                wish.centre_gestion = CentreGestionModel.objects.get(centre_gestion='ied')

            if not wish.is_ok and not wish.is_reins_formation() and not wish.centre_gestion.centre_gestion == 'fp':
                wish.liste_attente_inscription()
                return redirect(wish.get_absolute_url())
        context = self.get_context_data()
        context['wish'] = wish
        return self.render_to_response(context)


class ListeAttenteInscriptionView(ListeAttenteCandidatureView):
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
            return redirect(reverse('home'))
        return redirect(wish.get_absolute_url())

    # def get_context_data(self, **kwargs):
    #     context = super(ListeAttenteEquivalenceView, self).get_context_data(**kwargs)
    #     if self.wish:
    #         context['wish'] = self.wish
    #     else:
    #         self.wish = context['wish'] = self.request.user.individu.wishes.get(pk=self.kwargs['pk'])
    #     return context

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
        context['individu'] = self.request.user.individu
        try:
            context['wish'] = context['voeu'] = self.request.user.individu.wishes.select_related().get(
                pk=self.kwargs['pk'])
        except Wish.DoesNotExist:
            return redirect(reverse('home'))
        try:
            context['paiement_droit'] = context['wish'].paiementallmodel
        except PaiementAllModel.DoesNotExist:
            context['wish'].droit_universitaire()
            return redirect(context['wish'].get_absolute_url())
        if not context['wish'].centre_gestion:
            context['wish'].centre_gestion = CentreGestionModel.objects.get(centre_gestion='ied')
            context['wish'].save()
        if context['wish'].centre_gestion.centre_gestion == 'ied':
            context['paiement_frais'] = context['wish'].paiementallmodel
            try:
                context['tarif_versement_frais'] = context['wish'].frais_peda() / context['paiement_frais'].nb_paiement_frais
            except ZeroDivisionError:
                #context['wish'].paiementmodel_set.all().delete()

                context['wish'].etape = context['wish'].dispatch_etape = 'droit_universitaire'
                context['wish'].save()
                return redirect(context['wish'].get_absolute_url())
        context['static'] = os.path.join(BASE_DIR+'/duck_inscription/duck_theme_ied/static/images/').replace('\\', '/')
        # context['annee_univ'] = '%s-%s' % (ANNEE_UNIV, ANNEE_UNIV + 1)

        return context

    def get_template_names(self):
        tempate_names = super(InscriptionPdfView, self).get_template_names()
        tempate_names.append('duck_inscription/wish/%s_pdf.html' % (self.etape,))  # permet d'avoir la meme classe pour candidature
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
        pdf.addFromFileName(wish.etape.annee.transfert_pdf.file)
        pdf.addFromFileName(wish.etape.annee.bourse_pdf.file)
        pdf.addFromFileName(wish.etape.annee.pieces_pdf.file)

        pdf.join(response)
        return response


# class NewAuditeurView(FormView):
#     form_class = NewAuditeurForm
#     template_name = "auditeur_libre/new_auditeur.html"
#
#     def form_valid(self, form):
#         if form.cleaned_data['auditeur'] is True:
#             individu = self.request.user.individu
#             wish = Wish.objects.create(
#                 etape="auditeur",
#                 dispatch_etape="auditeur",
#                 individu=individu,
#                 step=Step.objects.get(name="L1NPSY"),
#                 is_reins=False,
#                 code_dossier=individu.code_opi,
#                 is_auditeur=True
#             )
#             return redirect(wish.get_absolute_url(), pk=wish.id)
#
#         return redirect('home')
#
#     def form_invalid(self, form):
#         print "coucuo"
#         return super(NewAuditeurView, self).form_invalid(form)
#
#
# class AuditeurView(TemplateView):
#     template_name = "auditeur_libre/auditeur.html"
#
#     def get_context_data(self, **kwargs):
#         context = super(AuditeurView, self).get_context_data(**kwargs)
#         context['wish'] = self.request.user.individu.wishes.get(pk=self.kwargs['pk'])
#         return context
#
#     def get(self, request, *args, **kwargs):
#         context = self.get_context_data(**kwargs)
#         if request.GET.get("valide", False):
#             context['wish'].valide = True
#             context['wish'].save()
#         return self.render_to_response(context)
#
#
# class AuditeurPdfView(TemplateView):
#     template_name = "auditeur_libre/pdf_auditeur.html"
#     templates = {
#         'dossier_inscription': "auditeur_libre/pdf_auditeur.html",
#         'formulaire_paiement_droit': "auditeur_libre/formulaire_paiement_frais.html",
#         'etiquette': 'wish/etiquette.html',
#     }
#
#     def get_context_data(self, **kwargs):
#         context = super(AuditeurPdfView, self).get_context_data(**kwargs)
#         context['student'] = context['individu'] = self.request.user.individu
#
#         context['wish'] = context['voeu'] = self.request.user.individu.wishes.select_related().get(pk=self.kwargs['pk'])
#         context['static'] = PROJECT_DIR + '/documents/static/images/'
#         context['annee_univ'] = '%s-%s' % (ANNEE_UNIV, ANNEE_UNIV + 1)
#
#         return context
#
#     def render_to_response(self, context, **response_kwargs):
#         response = HttpResponse(mimetype='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename=auditeur_libre.pdf'
#         pdf = pisapdf.pisaPDF()
#         pdf.addDocument(pisa.CreatePDF(
#             render_to_string(self.templates['etiquette'], context, context_instance=RequestContext(self.request))))
#         pdf.addDocument(pisa.CreatePDF(render_to_string(self.templates['dossier_inscription'], context,
#                                                         context_instance=RequestContext(self.request))))
#         pdf.addDocument(pisa.CreatePDF(render_to_string(self.templates['formulaire_paiement_droit'], context,
#                                                         context_instance=RequestContext(self.request))))
#         pdf.join(response)
#         return response
