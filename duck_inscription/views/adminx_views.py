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

