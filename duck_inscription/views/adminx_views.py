# coding=utf-8
from django.core.urlresolvers import reverse_lazy
from django.views.generic import FormView
from xworkflows import InvalidTransitionError
from duck_inscription.forms.adminx_forms import DossierReceptionForm
from duck_inscription.models import Wish


class DossierReceptionView(FormView):
    template_name = "duck_inscription/adminx/dossier_reception.html"
    form_class = DossierReceptionForm
    success_url = reverse_lazy('dossier_reception')
    # def get(self, request, *args, **kwargs):
    #     return super(DossierReceptionView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        code_dossier = form.cleaned_data['code_dossier']
        context = self.get_context_data()
        try:
            wish = Wish.objects.get(code_dossier=code_dossier)

            context['email'] = wish.individu.personal_email
            context['form'] = self.get_form_class()()
            # wish.equivalence_receptionner()
            context['result'] = wish.envoi_email_reception()
        except Wish.DoesNotExist:
            context['message'] = u"Le dossier numéro %s n'existe pas" % (code_dossier,)
        except InvalidTransitionError as e:
            context['message'] = u'<div class="text-danger">Dossier déjà traité</div>'
        # except Exception, e:
        #     context['message'] = e
        context['form'] = self.get_form_class()
        return self.render_to_response(context)
    #
    # def envoie_mail(self, wish):
    #     if wish.etape == "equivalence":
    #         etape = u"d'équivalence"
    #         etape_dossier = Etape.objects.get(name="equivalence_reception")
    #     elif wish.etape == "candidature":
    #         etape = u"de candidature"
    #         etape_dossier = Etape.objects.get(name="candidature_reception")
    #     elif wish.etape in [u"inscription", 'liste_attente_inscription', 'ouverture_paiement', 'dossier_inscription']:
    #         etape = u"d'inscripiton"
    #         etape_dossier = Etape.objects.get(name="inscription_reception")
    #         if not wish.date_reception_inscription:
    #             wish.date_reception_inscription = datetime.datetime.today()
    #             wish.save()
    #     else:
    #         raise Exception(u"Etape inconnu")
    #     site = Site.objects.get(id=settings.SITE_ID)
    #     sujet = u"[ IED ] : Réception de votre dossier %s" % (etape,)
    #     message = render_to_string("backoffice/dossier_receptionne/email_reception.html",
    #                                {'site': site, 'etape': etape})
    #     etapes = wish.etapedossier_set.order_by('-date')
    #     name_etape = {'equivalence': ['equivalence_complet', 'equivalence_traite'],
    #                   'candidature': ['candidature_complet', 'candidature_traite'],
    #                   'inscription': ['inscription_complet']}
    #     if len(etapes):
    #         if wish.etape in ['equivalence', 'candidature', 'inscription']:
    #             if etapes[0].etape == etape_dossier or etapes[0].etape.name in name_etape[wish.etape]:
    #                 return False
    #
    #     if settings.DEBUG:
    #         send_mail(sujet, message, "nepasrepondre@iedparis8.net", ["paul.guichon@iedparis8.net"])
    #     else:
    #         send_mail(sujet, message, "nepasrepondre@iedparis8.net", [wish.individu.personal_email])
    #
    #     EtapeDossier.objects.create(etape=etape_dossier, wish=wish)
    #     return True
