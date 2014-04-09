# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse
from django.http import HttpResponse

from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from floppyforms import ModelChoiceField

from duck_inscription.forms import WishGradeForm
from duck_inscription.models import Wish, SettingsEtape

__author__ = 'paul'


class NewWishView(FormView):
    template_name = "duck_inscription/wish/new_wish.html"
    form_class = WishGradeForm

    def form_valid(self, form):
        etape = form.cleaned_data['etape']
        individu = self.request.user.individu

        if not individu.wishes.filter(etape=etape).count() == 0:
            return redirect(reverse("accueil"))
        wish = Wish(etape=etape, individu=individu)
        wish.save()
        wish.dispatch()
        return redirect(wish.get_absolute_url())


class StepView(TemplateView):
    def get(self, request, *args, **kwargs):
        if self.request.GET.get("diplome", "") != "":
            step_wish = []
            for wish in self.request.user.individu.wishes.all():
                step_wish.append(wish.step.pk)

            etape = ModelChoiceField(queryset=SettingsEtape.objects.filter(
                diplome=self.request.GET.get("diplome")).exclude(pk__in=step_wish).order_by('label'),
            )
            return HttpResponse(etape.widget.render(name='step', value='', attrs={'id': 'id_step', 'class': "required"}))

        return HttpResponse('echec')
#
#
# class DeleteWish(View):
#
#     def get(self, request, *args, **kwargs):
#         #self.request.user.individu.wishes.filter(pk=kwargs.get('pk', None)).delete()
#         return redirect(reverse("home"))
#
#
# class ListeDiplomeAccesView(FormView):
#     template_name = "wish/liste_diplome_acces.html"
#     form_class = ListeDiplomeAccesForm
#
#     def get_context_data(self, **kwargs):
#         context = super(ListeDiplomeAccesView, self).get_context_data(**kwargs)
#         try:
#             context['wish'] = self.request.user.individu.wishes.get(pk=self.kwargs['pk'])
#         except Wish.DoesNotExist:
#             return redirect(reverse("home"))
#         return context
#
#     def get_form(self, form_class):
#         wish = self.request.user.individu.wishes.get(pk=self.kwargs['pk'])
#         return form_class(step=wish.step, **self.get_form_kwargs())
#
#     def get(self, request, *args, **kwargs):
#         form_class = self.get_form_class()
#         try:
#             form = self.get_form(form_class)
#         except Wish.DoesNotExist:
#             return redirect(reverse("home"))
#         return self.render_to_response(self.get_context_data(form=form))
#
#     def post(self, request, *args, **kwargs):
#         form_class = self.get_form_class()
#         try:
#             form = self.get_form(form_class)
#         except Wish.DoesNotExist:
#             return redirect(reverse("home"))
#         if form.is_valid():
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)
#
#     def form_invalid(self, form):
#         return super(ListeDiplomeAccesView, self).form_invalid(form)
#
#     def form_valid(self, form):
#         data = form.cleaned_data
#         wish = self.request.user.individu.wishes.get(pk=self.kwargs['pk'])
#         wish.diplome_acces = data['liste_diplome']
#
#         wish.dispatch()
#
#         return redirect(wish.get_absolute_url())
#
#
# class DemandeEquivalenceView(FormView):
#     template_name = "wish/demande_equivalence.html"
#     form_class = DemandeEquivalenceForm
#
#     def form_valid(self, form):
#         data = form.cleaned_data
#         wish = self.request.user.individu.wishes.get(pk=self.kwargs['pk'])
#         wish.demande_equivalence = True if data['demande_equivalence'] == u"True" else False
#         wish.dispatch()
#         return redirect(wish.get_absolute_url())
#
#
# class OuvertureEquivalence(TemplateView):
#     template_name = "wish/ouverture_equivalence.html"
#
#     def get_context_data(self, **kwargs):
#         context = super(OuvertureEquivalence, self).get_context_data(**kwargs)
#         context['date'] = self.request.user.individu.wishes.get(pk=self.kwargs['pk']).step.debut_equivalence
#         return context
#
#     def get(self, request, *args, **kwargs):
#         wish = self.request.user.individu.wishes.get(pk=self.kwargs['pk'])
#
#         if wish.dispatch():
#             return redirect(wish.get_absolute_url())
#         return super(OuvertureEquivalence, self).get(request, *args, **kwargs)
#
#
# class ListeAttenteEquivalenceView(FormView):
#     template_name = 'wish/liste_attente_equivalence.html'
#     form_class = ListeAttenteEquivalenceForm
#
#     def get_context_data(self, **kwargs):
#         context = super(ListeAttenteEquivalenceView, self).get_context_data(**kwargs)
#         if hasattr(self, 'wish'):
#             context['wish'] = self.wish
#         else:
#             self.wish = context['wish'] = self.request.user.individu.wishes.get(pk=self.kwargs['pk'])
#         return context
#
#     def get(self, request, *args, **kwargs):
#         if not hasattr(self, 'wish'):
#             self.wish = self.request.user.individu.wishes.get(pk=self.kwargs['pk'])
#         if datetime.date.today() > self.wish.step.fin_attente_equivalence:
#             #self.wish.delete()
#             return redirect(reverse('fin_liste_attente_equivalence'))
#         return super(ListeAttenteEquivalenceView, self).get(request, *args, **kwargs)
#
#     def form_valid(self, form):
#         wish = self.get_context_data()['wish']
#         demande_attente = form.cleaned_data['demande_attente']
#         if demande_attente == 'O':
#             wish.liste_attente = True
#             wish.save()
#         else:
#             #wish.delete()
#             return redirect(reverse('home'))
#         return redirect(wish.get_absolute_url())
#
#
# class EquivalenceView(TemplateView):
#     template_name = "wish/equivalence.html"
#
#     def get(self, request, *args, **kwargs):
#         wish = request.user.individu.wishes.get(pk=self.kwargs['pk'])
#         if request.GET.get("valide", False):
#             wish.valide = True
#             wish.save()
#         context = self.get_context_data()
#         context['wish'] = wish
#         return self.render_to_response(context)
#
#         #        return super(EquivalenceView, self).get(request, *args, **kwargs)
#
#
# class EquivalencePdfView(TemplateView):
#     template_name = "wish/etiquette.html"
#     etape = "equivalence"  # à surcharger pour candidature
#
#     def get_context_data(self, **kwargs):
#         context = super(EquivalencePdfView, self).get_context_data(**kwargs)
#         context['individu'] = self.request.user.individu
#         context['voeu'] = self.request.user.individu.wishes.get(pk=self.kwargs['pk'])
#         context['static'] = PROJECT_DIR + '/documents/static/images/'
#         context['annee_univ'] = '%s-%s' % (ANNEE_UNIV, ANNEE_UNIV + 1)
#
#         return context
#
#     def get_template_names(self):
#         tempate_names = super(EquivalencePdfView, self).get_template_names()
#         tempate_names.append('wish/%s_pdf.html' % self.etape)  # permet d'avoir la meme classe pour candidature
#         return tempate_names
#
#     def get_file(self):
#         """
#         Il faut la surcharger pour les candidatures
#         Doit retourner le l'url du doccument du doccument a fussionner
#         """
#         step = self.request.user.individu.wishes.get(pk=self.kwargs['pk']).step
#
#         return step.document_equivalence
#
#     def render_to_response(self, context, **response_kwargs):
#         response = HttpResponse(mimetype='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename=%s_%s.pdf' % (self.etape, context['voeu'].step.name)
#         try:
#             url_doc = self.get_file().file
#         except Wish.DoesNotExist:
#             return redirect(self.request.user.individu.get_absolute_url())
#         url_doc.open('r')
#
#         context['num_page'] = self._num_page(url_doc)  # on indique le nombre de page pour la page 1
#
#         pdf = pisapdf.pisaPDF()
#         for template in self.get_template_names():
#             pdf.addDocument(pisa.CreatePDF(render_to_string(template, context, context_instance=RequestContext(
#                 self.request))))  # on construit le pdf
#             #il faut fusionner la suite
#         pdf.addFromFile(self.do_pdf(url_doc))
#
#         pdf.join(response)
#         return response
#
#     def _num_page(self, url_doc):
#         return PdfFileReader(url_doc).getNumPages()
#
#
#     def do_pdf(self, file):
#         """
#         retourne un pdf sans la première page
#         """
#         result = StringIO.StringIO()
#         output = PdfFileWriter()
#         input1 = PdfFileReader(file)
#         for x in range(1, input1.getNumPages()):
#             output.addPage(input1.getPage(x))
#         output.write(result)
#
#         return result
#
#
# class OuvertureCandidature(TemplateView):
#     template_name = "wish/ouverture_candidature.html"
#
#     def get_context_data(self, **kwargs):
#         context = super(OuvertureCandidature, self).get_context_data(**kwargs)
#         context['date'] = self.request.user.individu.wishes.get(pk=self.kwargs['pk']).step.debut_candidature
#         context['wish'] = self.request.user.individu.wishes.get(pk=self.kwargs['pk'])
#         return context
#
#     def get(self, request, *args, **kwargs):
#         wish = self.request.user.individu.wishes.get(pk=self.kwargs['pk'])
#
#         if wish.dispatch():
#             return redirect(wish.get_absolute_url())
#         return super(OuvertureCandidature, self).get(request, *args, **kwargs)
#
#
# class NoteMasterView(FormView):
#     form_class = NoteMasterForm
#     template_name = "wish/note_master.html"
#
#     def form_valid(self, form):
#         wish = self.request.user.individu.wishes.get(pk=self.kwargs['pk'])
#         form.instance.wish = wish
#         form.save()
#         if wish.dispatch():
#             return redirect(wish.get_absolute_url())
#         return super(NoteMasterView, self).form_valid(form)
#
#
# class CandidatureView(EquivalenceView):
#     template_name = "wish/candidature.html"
#
#
# class CandidaturePdfView(EquivalencePdfView):
#     etape = "candidature"
#
#     def get_file(self):
#         """
#         Il faut la surcharger pour les candidatures
#         Doit retourner le l'url du doccument du doccument a fussionner
#         """
#         step = self.request.user.individu.wishes.get(pk=self.kwargs['pk']).step
#
#         return step.document_candidature
#
#
# class ListeAttenteCandidatureView(ListeAttenteEquivalenceView):
#     template_name = 'wish/liste_attente_candidature.html'
#     form_class = ListeAttenteCandidatureForm
#
#     def get(self, request, *args, **kwargs):
#         return super(ListeAttenteEquivalenceView, self).get(request, *args, **kwargs)
#
#
# class OuverturePaiementView(TemplateView):
#     template_name = "wish/ouverture_paiement.html"
#
#     def get_context_data(self, **kwargs):
#         context = super(OuverturePaiementView, self).get_context_data(**kwargs)
#         context['wish'] = self.request.user.individu.wishes.get(pk=self.kwargs['pk'])
#         return context
#
#     def get(self, request, *args, **kwargs):
#         context = self.get_context_data(**kwargs)
#         wish = context['wish']
#         if wish.etape == 'ouverture_paiement' or wish.dispatch_etape == 'ouverture_paiement' and wish.etape != wish.dispatch_etape:
#             wish.etape = wish.dispatch_etape = 'ouverture_paiement'
#             wish.save()
#         if wish.dispatch():
#
#             return redirect(wish.get_absolute_url())
#         return self.render_to_response(context)
#
#
# class ChoixIedFpView(TemplateView):
#     template_name = "wish/choix_ied_fp.html"
#
#     def get(self, request, *args, **kwargs):
#         centre = self.request.GET.get('centre', None)
#         if centre in ['ied', 'fp']:
#             wish = self.request.user.individu.wishes.get(pk=self.kwargs['pk'])
#             wish.centre_gestion = CentreGestionModel.objects.get(centre_gestion=centre)
#             wish.dispatch()
#             return redirect(wish.get_absolute_url())
#         return super(ChoixIedFpView, self).get(request, *args, **kwargs)
#
#
# class DroitView(UpdateView):
#     model = PaiementAllModel
#     template_name = "inscription/dossier_inscription/base_formulaire.html"
#     forms = {
#         'droit_univ': ChoixPaiementDroitForm,
#         'choix_demi_annee': DemiAnneeForm,
#         'nb_paiement': NbPaiementPedaForm,
#         "recapitulatif": ValidationPaiementForm
#     }
#
#     def get_template_names(self):
#         if self.object.etape == "recapitulatif":
#             return "inscription/wish/recapitulatif.html"
#         return self.template_name
#
#     def post(self, request, *args, **kwargs):
#         if request.POST.get('precedent', None):
#             self.object = self.get_object()
#             if self.object.precedente_etape():
#                 return redirect(reverse(self.request.resolver_match.url_name, kwargs=self.kwargs))
#         return super(DroitView, self).post(request, *args, **kwargs)
#
#     def get_success_url(self):
#         if self.object.next_etape():
#             return reverse(self.request.resolver_match.url_name, kwargs=self.kwargs)
#         else:
#             wish = self.request.user.individu.wishes.get(pk=self.kwargs['pk'])
#             wish.etape = wish.dispatch_etape = 'inscription'
#             wish.save()
#             return wish.get_absolute_url()
#
#     def get_form_class(self):
#         return self.forms[self.object.etape]
#
#     def get_object(self, queryset=None):
#         wish = self.request.user.individu.wishes.get(pk=self.kwargs['pk'])
#         return PaiementAllModel.objects.get_or_create(wish=wish)[0]
#
#
# class InscriptionView(TemplateView):
#     template_name = "wish/inscription.html"
#
#     def get(self, request, *args, **kwargs):
#         wish = request.user.individu.wishes.get(pk=self.kwargs['pk'])
#
#
#         try:
#             if wish.individu.dossier_inscription.etape != 'recapitulatif':
#                 wish.etape = wish.dispatch_etape = "ouverture_paiement"
#                 wish.save()
#                 return redirect(wish.get_absolute_url())
#         except DossierInscription.DoesNotExist:
#             wish.etape = wish.dispatch_etape = "ouverture_paiement"
#             wish.save()
#             return redirect(wish.get_absolute_url())
#
#         if \
#                     wish.individu.dossier_inscription.dernier_etablissement == None:
#             wish.etape = wish.dispatch_etape = "ouverture_paiement"
#             wish.save()
#             return redirect(wish.get_absolute_url())
#
#         if request.GET.get("valide", False):
#             wish.valide_liste()
#             if not wish.centre_gestion:
#                 wish.centre_gestion = CentreGestionModel.objects.get(centre_gestion='ied')
#
#             if not wish.is_ok and not wish.is_reins_formation() and not wish.centre_gestion.centre_gestion == 'fp':
#                 wish.etape = wish.dispatch_etape = 'liste_attente_inscription'
#                 wish.save()
#                 return redirect(wish.get_absolute_url())
#         context = self.get_context_data()
#         context['wish'] = wish
#         return self.render_to_response(context)
#
#
# class ListeAttenteInscriptionView(ListeAttenteCandidatureView):
#     template_name = 'wish/liste_attente_inscription.html'
#     form_class = ListeAttenteInscriptionForm
#
#     def form_valid(self, form):
#         wish = self.get_context_data()['wish']
#         demande_attente = form.cleaned_data['demande_attente']
#         if demande_attente == 'O':
#             wish.liste_attente = True
#             if not wish.date_liste_inscription:
#                 wish.date_liste_inscription = datetime.datetime.today()
#             wish.save()
#         else:
#             #wish.delete()
#             return redirect(reverse('home'))
#         return redirect(wish.get_absolute_url())
#
#     # def get_context_data(self, **kwargs):
#     #     context = super(ListeAttenteEquivalenceView, self).get_context_data(**kwargs)
#     #     if self.wish:
#     #         context['wish'] = self.wish
#     #     else:
#     #         self.wish = context['wish'] = self.request.user.individu.wishes.get(pk=self.kwargs['pk'])
#     #     return context
#
# ##le dossier d'inscription
#
#
# class InscriptionPdfView(TemplateView):
#     template_name = "wish/ordre_virement.html"
#     templates = {
#         'dossier_inscription': "wish/dossier_inscription_pdf.html",
#         'ordre_virement': "wish/ordre_virement.html",
#         'formulaire_paiement_frais': "wish/formulaire_paiement_frais.html",
#         'formulaire_paiement_droit': "wish/formulaire_paiement_droit.html",
#         'etiquette': 'wish/etiquette.html',
#         'autorisation_photo': 'wish/autorisation_photo.html'
#     }
#
#     def get_context_data(self, **kwargs):
#         context = super(InscriptionPdfView, self).get_context_data(**kwargs)
#         context['individu'] = self.request.user.individu
#         try:
#             context['wish'] = context['voeu'] = self.request.user.individu.wishes.select_related().get(
#                 pk=self.kwargs['pk'])
#         except Wish.DoesNotExist:
#             return redirect(reverse('home'))
#         try:
#             context['paiement_droit'] = context['wish'].paiementallmodel
#         except PaiementAllModel.DoesNotExist:
#             context['wish'].etape = context['wish'].dispatch_etape = 'droit_universitaire'
#             context['wish'].save()
#             return redirect(context['wish'].get_absolute_url())
#         if not context['wish'].centre_gestion:
#             context['wish'].centre_gestion = CentreGestionModel.objects.get(centre_gestion='ied')
#             context['wish'].save()
#         if context['wish'].centre_gestion.centre_gestion == 'ied':
#             context['paiement_frais'] = context['wish'].paiementallmodel
#             try:
#                 context['tarif_versement_frais'] = context['wish'].frais_peda() / context['paiement_frais'].nb_paiement_frais
#             except ZeroDivisionError:
#                 #context['wish'].paiementmodel_set.all().delete()
#
#                 context['wish'].etape = context['wish'].dispatch_etape = 'droit_universitaire'
#                 context['wish'].save()
#                 return redirect(context['wish'].get_absolute_url())
#
#         context['static'] = os.path.join(os.path.dirname(__file__),
#                                          PROJECT_DIR+'/documents/static/images/').replace('\\', '/')
#         context['annee_univ'] = '%s-%s' % (ANNEE_UNIV, ANNEE_UNIV + 1)
#
#         return context
#
#     def get_template_names(self):
#         tempate_names = super(InscriptionPdfView, self).get_template_names()
#         tempate_names.append('wish/%s_pdf.html' % (self.etape,))  # permet d'avoir la meme classe pour candidature
#         return tempate_names
#
#     def render_to_response(self, context, **response_kwargs):
#     #        response = HttpResponse("coucoucou")
#         response = HttpResponse(mimetype='application/pdf')
#         try:
#             response['Content-Disposition'] = 'attachment; filename=inscription_%s.pdf' % context['wish'].step.name
#         except KeyError:
#             return redirect(reverse('home'))
#             #        f = open('documents/static/inscription.pdf','w')
#
#         pdf = pisapdf.pisaPDF()
#         wish = context['wish']
#         if not wish.centre_gestion:
#             wish.centre_gestion = CentreGestionModel.objects.get(centre_gestion='ied')
#             wish.save()
#         if wish.centre_gestion.centre_gestion == 'ied':
#             pdf.addDocument(pisa.CreatePDF(render_to_string(self.templates['etiquette'], context,
#                                                             context_instance=RequestContext(self.request))))
#
#         pdf.addDocument(pisa.CreatePDF(render_to_string(self.templates['dossier_inscription'], context,
#                                                         context_instance=RequestContext(self.request))))
#         pdf.addDocument(pisa.CreatePDF(render_to_string(self.templates['autorisation_photo'], context,
#                                                         context_instance=RequestContext(self.request))))
#
#         if not wish.centre_gestion:
#             c = CentreGestionModel.objects.get(centre_gestion='ied')
#             wish.centre_gestion = c
#             wish.save()
#         if wish.centre_gestion.centre_gestion == 'ied':
#             pdf.addDocument(pisa.CreatePDF(render_to_string(self.templates['formulaire_paiement_droit'], context,
#                                                             context_instance=RequestContext(self.request))))
#             pdf.addDocument(pisa.CreatePDF(render_to_string(self.templates['formulaire_paiement_frais'], context,
#                                                             context_instance=RequestContext(self.request))))
#             if not wish.paiementallmodel.moyen_paiement:
#                 wish.etape = wish.dispatch_etape = 'droit_universitaire'
#                 wish.save()
#                 return redirect(wish.get_absolute_url())
#
#             if wish.paiementallmodel.moyen_paiement.type == 'v':
#                 pdf.addDocument(pisa.CreatePDF(render_to_string(self.templates['ordre_virement'], context,
#                                                                 context_instance=RequestContext(self.request))))
#
#         pdf.addFromFileName(
#             os.path.join(
#                 os.path.dirname(__file__),
#                 '../documents/transfert.pdf').replace('\\', '/'))
#         pdf.addFromFileName(
#             os.path.join(
#                 os.path.dirname(__file__),
#                 '../documents/bourse.pdf').replace('\\', '/'))
#         pdf.addFromFileName(
#             os.path.join(
#                 os.path.dirname(__file__),
#                 '../documents/pieces.pdf').replace('\\', '/'))
#                # pdf.join(f)
#         pdf.join(response)
#         return response
#
#
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
