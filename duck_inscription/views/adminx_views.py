# coding=utf-8
from io import StringIO
from PyPDF2 import PdfFileReader, PdfFileWriter
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView
from django_xworkflows.xworkflow_log.models import TransitionLog
from xworkflows import InvalidTransitionError
from duck_inscription.forms.adminx_forms import DossierReceptionForm
from duck_inscription.models import Wish
from django.conf import settings
from duck_inscription.templatetags.lib_inscription import annee_en_cour


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
            context['message'] = u'<div class="text-danger">Le dossier numéro {} n\'existe pas"</div>'.format(code_dossier)
        except InvalidTransitionError as e:
            context['message'] = u'<div class="text-danger">Dossier déjà traité</div>'
        # except Exception, e:
        #     context['message'] = e
        context['form'] = self.get_form_class()
        return self.render_to_response(context)


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

        url_doc = self.get_file().file
        context['url_doc'] = url_doc
        url_doc.open('r')


        return context['voeu'].do_pdf_decision_equi_pdf(flux=response,
                                                        request=self.request,
                                                        context=context)


class ImprimerTousDecisions(TemplateView):

    def get_all_viable_wishes(self):
        t = ContentType.objects.get(model='wish')
        pks = [t.content_id for t in TransitionLog.objects.filter(content_type=t, transition='equivalence_reception')]
        wishes = Wish.objects.filter(pk__in=pks, etape__cod_etp__in=['L1NPSY', 'L2NPSY', 'L3NPSY'])
        print "NOW WATCH THIS"
        print wishes.all.count()
        return wishes


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
        url_doc = all_wishes[0].etape.document_equivalence
        context['url_doc'] = url_doc
        url_doc.open('r')
        for wish in all_wishes:
            wish.do_pdf_decision_equi_pdf(flux=response,
                                          request=self.request,
                                          context=self.get_wish_context_data(wish)
                                          )
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
        tempate_names.append('duck_inscription/wish/%s_pdf.html' % self.etape)  # permet d'avoir la meme classe pour candidature
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

        return context['voeu'].do_pdf_equi(flux=response,
                                           templates=self.get_template_names(),
                                           request=self.request,
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