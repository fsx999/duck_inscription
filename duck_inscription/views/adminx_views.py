# coding=utf-8
from io import StringIO
from PyPDF2 import PdfFileReader, PdfFileWriter
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView, View
from django_xworkflows.xworkflow_log.models import TransitionLog
from xworkflows import InvalidTransitionError
from duck_inscription.forms.adminx_forms import DossierReceptionForm, ImprimerEnMasseForm, ChangementCentreGestionForm
from duck_inscription.models import Wish
from django.conf import settings
from duck_inscription.templatetags.lib_inscription import annee_en_cour
from xhtml2pdf import pdf as pisapdf
from xhtml2pdf import pisa
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
             avec l\'email {} est bien trairé</div>'''.format(wish.code_dossier, wish.individu.personal_email)
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
            if wish.suivi_dossier.is_inscription_traite:
                messages.error(request, u'Le dossier a déjà été traité')

            else:
                wish.save_opi()
                wish.inscription_traite()
                messages.success(request, 'Etudiant {} remontee'.format(wish.individu.code_opi))
                # self.message_user('Etudiant {} remontee'.format(wish.individu.code_opi), 'success')
        return redirect('/duck_inscription/wish/')


class ChangementCentreGestionView(FormView):
    form_class = ChangementCentreGestionForm
    template_name = 'duck_inscription/adminx/changement_centre_gestion.html'

    def get_context_data(self, **kwargs):
        context = super(ChangementCentreGestionView, self).get_context_data(**kwargs)
        context['wish'] = Wish.objects.get(pk=self.kwargs['pk'])
        return context

    def form_invalid(self, form):
        return super(ChangementCentreGestionView, self).form_invalid(form)

    def form_valid(self, form):
        return super(ChangementCentreGestionView, self).form_valid(form)

    def get_success_url(self):
        return reverse('xadmin:duck_inscription_individu_change', args=(3,))


