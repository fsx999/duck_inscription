# coding=utf-8
from io import StringIO
from PyPDF2 import PdfFileReader, PdfFileWriter
from django.core.urlresolvers import reverse_lazy, reverse
from django.db import DatabaseError
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView, View
from xworkflows import InvalidTransitionError
from duck_inscription.forms.adminx_forms import DossierReceptionForm, ImprimerEnMasseForm, ChangementCentreGestionForm, \
    DossierIncompletForm
from duck_inscription.models import Wish
try:
    from duck_inscription_payzen.models import PaiementAllModel
except ImportError:
    PaiementAllModel = Wish # TODO modifié ce hack de merde (urgence CTU)
from django.conf import settings
from duck_inscription.templatetags.lib_inscription import annee_en_cour
from xhtml2pdf import pdf as pisapdf
from django.contrib import messages


class DossierReceptionView(FormView):
    template_name = "duck_inscription/adminx/dossier_reception.html"
    form_class = DossierReceptionForm
    success_url = reverse_lazy('dossier_reception')

    def form_valid(self, form):
        code_dossier = form.cleaned_data['code_dossier']
        context = self.get_context_data()
        try:
            wish = Wish.objects.get(code_dossier=code_dossier)

            context['email'] = wish.individu.personal_email
            context['form'] = self.get_form_class()()
            wish.equivalence_receptionner()
            wish.envoi_email_reception()
            context['message'] = u'''<div class="text-success">Le dossier {}
             avec l\'email {} est bien traité</div>'''.format(wish.code_dossier, wish.individu.personal_email)
        except Wish.DoesNotExist:
            context['message'] = u'<div class="text-danger">Le dossier numéro {} n\'existe pas"</div>'.format(
                code_dossier)
        except InvalidTransitionError as e:
            context['message'] = u'<div class="text-danger">Dossier déjà traité</div>'
        # except Exception, e:
        # context['message'] = e
        context['form'] = self.get_form_class()
        return self.render_to_response(context)


class ImprimerDecisionsEquivalenceEnMasseView(FormView):
    template_name = "duck_inscription/adminx/imprimer_en_masse.html"
    form_class = ImprimerEnMasseForm
    success_url = reverse_lazy('imprimer_decisions_ordre')

    def get_all_viable_wishes(self, low, high):
        wishes = Wish.objects.filter(suivi_dossier='equivalence_reception').order_by("individu__last_name")
        return wishes[low:high]

    def get_context_data(self, **kwargs):
        context = super(ImprimerDecisionsEquivalenceEnMasseView, self).get_context_data(**kwargs)
        context['dossiers_recus'] = Wish.objects.filter(suivi_dossier='equivalence_reception').count()
        return context

    def get_wish_context_data(self, wish):
        context = self.get_context_data()
        context['voeu'] = wish
        context['individu'] = wish.individu
        context['logo_p8'] = "file://" + settings.BASE_DIR + '/duck_theme_ied/static/images/logop8.jpg'
        context['url_font'] = settings.BASE_DIR + '/duck_theme_ied/static/font/ConnectCode39.ttf'
        context['url_static'] = settings.BASE_DIR + '/duck_theme_ied/static/images/'
        context['annee_univ'] = annee_en_cour()
        return context

    def form_valid(self, form):
        low = form.cleaned_data['low']
        high = form.cleaned_data['high']
        if high > Wish.objects.filter(suivi_dossier='equivalence_reception').count():
            high = Wish.objects.filter(suivi_dossier='equivalence_reception').count()
        name = 'decisions_equivalence_de_' + str(low) + '_a_' + str(high) + ".pdf"
        response = HttpResponse(mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=' + name
        all_wishes = self.get_all_viable_wishes(low, high)
        big_pdf = pisapdf.pisaPDF()
        for wish in all_wishes:
            wish.add_decision_equi_pdf(pdf=big_pdf, request=self.request, context=self.get_wish_context_data(wish))
        big_pdf.join(response)
        return response


class DecisionEquivalencePdfAdminView(TemplateView):
    etape = "equivalence"

    def get_context_data(self, **kwargs):
        context = super(DecisionEquivalencePdfAdminView, self).get_context_data(**kwargs)
        context['voeu'] = Wish.objects.get(pk=self.kwargs['pk'])
        context['individu'] = context['voeu'].individu
        context['logo_p8'] = "file://" + settings.BASE_DIR + '/duck_theme_ied/static/images/logop8.jpg'
        context['url_font'] = settings.BASE_DIR + '/duck_theme_ied/static/font/ConnectCode39.ttf'
        context['url_static'] = settings.BASE_DIR + '/duck_theme_ied/static/images/'
        context['annee_univ'] = annee_en_cour()
        return context

    def get_file(self):
        """
        Il faut la surcharger pour les candidatures
        Doit retourner le l'url du doccument du doccument a fussionner
        """
        step = Wish.objects.get(pk=self.kwargs['pk']).etape

        return step.document_equivalence

    def render_to_response(self, context, **response_kwargs):
        response = HttpResponse(mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=%s_%s.pdf' % (self.etape, context['voeu'].etape.cod_etp)

        return context['voeu'].do_pdf_decision_equi_pdf(flux=response, request=self.request, context=context)


class ImprimerTousDecisions(TemplateView):
    def get_all_viable_wishes(self):
        wishes = Wish.objects.filter(suivi_dossier='equivalence_reception').order_by("individu__last_name")
        return wishes[0:50]

    def get_wish_context_data(self, wish):
        context = self.get_context_data()
        context['voeu'] = wish
        context['individu'] = wish.individu
        context['logo_p8'] = "file://" + settings.BASE_DIR + '/duck_theme_ied/static/images/logop8.jpg'
        context['url_font'] = settings.BASE_DIR + '/duck_theme_ied/static/font/ConnectCode39.ttf'
        context['url_static'] = settings.BASE_DIR + '/duck_theme_ied/static/images/'
        context['annee_univ'] = annee_en_cour()
        return context

    def render_to_response(self, context, **response_kwargs):
        response = HttpResponse(mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=all_deicisions_equivalence.pdf'
        all_wishes = self.get_all_viable_wishes()
        big_pdf = pisapdf.pisaPDF()
        for wish in all_wishes:
            wish.add_decision_equi_pdf(pdf=big_pdf, request=self.request, context=self.get_wish_context_data(wish))
        big_pdf.join(response)
        return response


class EquivalencePdfAdminView(TemplateView):
    template_name = "duck_inscription/wish/etiquette.html"
    etape = "equivalence"  # à surcharger pour candidature

    def get_context_data(self, **kwargs):
        context = super(EquivalencePdfAdminView, self).get_context_data(**kwargs)
        context['voeu'] = Wish.objects.get(pk=self.kwargs['pk'])
        context['individu'] = context['voeu'].individu
        context['logo_p8'] = "file://" + settings.BASE_DIR + '/duck_theme_ied/static/images/logop8.jpg'
        context['url_font'] = settings.BASE_DIR + '/duck_theme_ied/static/font/ConnectCode39.ttf'
        context['url_static'] = settings.BASE_DIR + '/duck_theme_ied/static/images/'
        context['annee_univ'] = annee_en_cour()
        return context

    def get_template_names(self):
        tempate_names = super(EquivalencePdfAdminView, self).get_template_names()
        tempate_names.append(
            'duck_inscription/wish/%s_pdf.html' % self.etape)  # permet d'avoir la meme classe pour candidature
        return tempate_names

    def get_file(self):
        """
        Il faut la surcharger pour les candidatures
        Doit retourner le l'url du doccument du doccument a fussionner
        """
        step = Wish.objects.get(pk=self.kwargs['pk']).etape

        return step.document_equivalence

    def render_to_response(self, context, **response_kwargs):
        response = HttpResponse(mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=%s_%s.pdf' % (self.etape, context['voeu'].etape.cod_etp)

        url_doc = self.get_file().file
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


class OpiView(View):
    def get(self, request, *args, **kwargs):
        opi = self.request.GET.get('opi', None)
        if opi:

            wish = Wish.objects.get(code_dossier=opi)
            try:
                wish.save_opi()
                wish.inscription_traite()
                messages.success(request, 'Etudiant {} remontee'.format(wish.individu.code_opi))
            except InvalidTransitionError:
                messages.error(request, 'Dossier déjà traité')
            except DatabaseError as e:
                messages.error(request, 'Connection à apogée impossible: {}'.format(e))

                # self.message_user('Etudiant {} remontee'.format(wish.individu.code_opi), 'success')
        return redirect('/duck_inscription/wish/')

class PiecesDossierView(FormView):
    template_name = 'duck_inscription/adminx/dossier_incomplet.html'
    form_class = DossierIncompletForm

    # def get_form(self, form_class):
    #     """
    #     Returns an instance of the form to be used in this view.
    #     """
    #     self.wish = getattr(self, 'wish', Wish.objects.get(pk=self.kwargs['pk']))
    #     return form_class(wish=self.wish, **self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super(PiecesDossierView, self).get_context_data(**kwargs)
        self.wish = getattr(self, 'wish', Wish.objects.get(pk=self.kwargs['pk']))

        context['wish'] = self.wish
        return context

class ChangementCentreGestionView(FormView):
    form_class = ChangementCentreGestionForm
    template_name = 'duck_inscription/adminx/changement_centre_gestion.html'

    def get_form(self, form_class):
        """
        Returns an instance of the form to be used in this view.
        """
        self.wish = getattr(self, 'wish', Wish.objects.get(pk=self.kwargs['pk']))
        return form_class(wish=self.wish, **self.get_form_kwargs())

    def get_form_kwargs(self):
        kwargs = super(ChangementCentreGestionView, self).get_form_kwargs()
        res = {'situation_sociale': self.wish.individu.dossier_inscription.situation_sociale,
               'centre_gestion': self.wish.centre_gestion,
               'affiliation_parent': self.wish.individu.dossier_inscription.affiliation_parent,
               'non_affiliation': self.wish.individu.dossier_inscription.non_affiliation,
               'centre_payeur': self.wish.individu.dossier_inscription.centre_payeur,
               }
        if hasattr(self.wish, 'paiementallmodel'):
            res['nombre_paiement'], res['type_paiement'] = self.wish.paiementallmodel.nb_paiement_frais, self.wish.paiementallmodel.moyen_paiement

        kwargs['initial'].update(res)
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(ChangementCentreGestionView, self).get_context_data(**kwargs)
        context['wish'] = self.wish
        return context

    def form_invalid(self, form):
        return super(ChangementCentreGestionView, self).form_invalid(form)

    def form_valid(self, form):
        clean_data = form.cleaned_data
        self.wish.centre_gestion = clean_data['centre_gestion']
        if self.wish.centre_gestion.centre_gestion != 'fp':
            try:
                paiement = self.wish.paiementallmodel
            except PaiementAllModel.DoesNotExist:
                paiement = PaiementAllModel(wish=self.wish)
            if paiement.moyen_paiement is None or paiement.moyen_paiement.type != 'CB':
                paiement.nb_paiement_frais, paiement.moyen_paiement = clean_data['nombre_paiement'], clean_data['type_paiement']


            if clean_data.get('type_paiement', None).type == 'CB':
                paiement.moyen_paiement = clean_data.get('type_paiement')
                self.wish.is_ok = True
                self.wish.state='dossier_inscription'

                paiement.state='choix_ied_fp'

            paiement.save()

        if clean_data.get('situation_sociale', None):
            self.wish.individu.dossier_inscription.situation_sociale = clean_data['situation_sociale']
            self.wish.individu.dossier_inscription.save()
        if clean_data.get('affiliation_parent', None):
            self.wish.individu.dossier_inscription.affiliation_parent = clean_data.get('affiliation_parent')
        if clean_data.get('non_affiliation', None):
            self.wish.individu.dossier_inscription.non_affiliation = clean_data.get('non_affiliation')
        if clean_data.get('centre_payeur', None):
            self.wish.individu.dossier_inscription.centre_payeur = clean_data.get('centre_payeur')
        self.wish.individu.dossier_inscription.save()
        self.wish.save()
        return HttpResponse('<div class="alert alert-success" role="alert">Le dossier a bien été modifié</div>')

    def get_success_url(self):
        return reverse('xadmin:duck_inscription_individu_change', args=(3,))


# class ChangemeCentreGestionView(FormView):
#     form_class = ChangementCentreGestionForm
#     template_name = 'duck_inscription/adminx/changement_situation.html.html'
#
#     def get_form(self, form_class):
#         """
#         Returns an instance of the form to be used in this view.
#         """
#         self.wish = getattr(self, 'wish', Wish.objects.get(pk=self.kwargs['pk']))
#         return form_class(wish=self.wish, **self.get_form_kwargs())
#
#     def get_form_kwargs(self):
#
#         return super(ChangementCentreGestionView, self).get_form_kwargs()
#
#     def get_context_data(self, **kwargs):
#         context = super(ChangementCentreGestionView, self).get_context_data(**kwargs)
#         context['wish'] = self.wish
#         return context
#
#     def form_invalid(self, form):
#         return super(ChangementCentreGestionView, self).form_invalid(form)
#
#     def form_valid(self, form):
#         clean_data = form.cleaned_data
#         self.wish.centre_gestion = clean_data['centre_gestion']
#         # if self.wish.centre_gestion.centre_gestion == 'ied':
#         #     try:
#         #         paiement = self.wish.paiementallmodel
#         #     except PaiementAllModel.DoesNotExist:
#         #         paiement = PaiementAllModel(wish=self.wish)
#         #     paiement.nb_paiement_frais, paiement.moyen_paiement = clean_data['nombre_paiement'], clean_data['type_paiement']
#         #     paiement.save()
#         # else:
#         #     try:
#         #         self.wish.paiementallmodel.delete()
#         #     except PaiementAllModel.DoesNotExist:
#         #         pass
#         # if clean_data.get('demi_annee', None):
#         #     self.wish.demi_annee = clean_data['demi_annee']
#         # if clean_data.get('situation_sociale', None):
#         #     print "coucou"
#         #     self.wish.individu.dossier_inscription.situation_sociale = clean_data['situation_sociale']
#         #     self.wish.individu.dossier_inscription.save()
#         # self.wish.save()
#         # return HttpResponse('<div class="alert alert-success" role="alert">Le dossier a bien été modifié</div>')
#
#     def get_success_url(self):
#         return reverse('xadmin:duck_inscription_individu_change', args=(3,))
#
