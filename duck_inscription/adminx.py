# coding=utf-8
from __future__ import unicode_literals
from crispy_forms.bootstrap import TabHolder, Tab
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from xworkflows import InvalidTransitionError
from duck_inscription.forms.adminx_forms import DossierReceptionForm
from duck_inscription.xadmin_plugins.topnav import IEDPlugin
from xadmin.layout import Main, Fieldset, Container, Side
from xadmin.plugins.inline import Inline
from xadmin import views
import xadmin
from duck_inscription.models import Individu, SettingsEtape, WishWorkflow
from .models import Wish, SuiviDossierWorkflow, IndividuWorkflow
from xadmin.util import User
from xadmin.views import filter_hook, CommAdminView


class IncriptionDashBoard(views.website.IndexView):
    widgets = [
        [
            {"type": "qbutton", "title": "Inscription", "btns": [
                {'title': 'Reception', 'url': 'dossier_receptionner'},
                {'title': 'Dossier inscription', 'model': Individu},
                {'title': 'Imprimer decisions ', 'url': 'imprimer_decisions_ordre'}
            ]},
        ]
    ]
    site_title = 'Backoffice'
    title = 'Accueil'
    widget_customiz = False
xadmin.site.register_view(r'inscription/$', IncriptionDashBoard,  'inscription')

class StatistiqueDashBoard(views.website.IndexView):
    widgets = [
        [
            {"type": "qbutton", "title": "Inscription", "btns": [
                {'title': 'Reception', 'url': 'dossier_receptionner'},
                {'title': 'Dossier inscription', 'model': Individu},
                {'title': 'Imprimer decisions ', 'url': 'imprimer_decisions_ordre'}
            ]},
        ]
    ]
    site_title = 'Backoffice'
    title = 'Accueil'
    widget_customiz = False
xadmin.site.register_view(r'statistiques/$', StatistiqueDashBoard,  'statistiques')


class DossierReception(views.FormAdminView):
    form = DossierReceptionForm
    title = 'Dossier Reception'

    def get_redirect_url(self):
        return self.get_admin_url('dossier_receptionner')

    def post(self, request, *args, **kwargs):
        self.instance_forms()
        self.setup_forms()

        if self.valid_forms():
            code_dossier = self.form_obj.cleaned_data['code_dossier']

            try:
                wish = Wish.objects.get(code_dossier=code_dossier)
                wish.equivalence_receptionner()
                wish.envoi_email_reception()
                msg = u'''Le dossier {} avec l\'email {} est bien trairé'''.format(wish.code_dossier, wish.individu.personal_email)
                self.message_user(msg, 'success')
            except Wish.DoesNotExist:
                msg = u'Le dossier numéro {} n\'existe pas'.format(code_dossier)
                self.message_user(msg, 'error')
            except InvalidTransitionError as e:
                msg = u'Dossier déjà traité'
                self.message_user(msg, 'error')
            return HttpResponseRedirect(self.get_redirect_url())
        return self.get_response()

xadmin.site.register_view(r'dossier_receptionner/$', DossierReception,  'dossier_receptionner')




class MainDashboard(object):
    widgets = [
        [
            {"type": "qbutton", "title": "Scolarité", "btns": [

                {'title': "Pré-Inscription", 'url': 'inscription'},
                {'title': "Statistique", 'url': 'statistiques'},
            ]},
        ]
    ]
    site_title = 'Backoffice'
    title = 'Accueil'
    widget_customiz = False

xadmin.site.register(views.website.IndexView, MainDashboard)



class BaseSetting(object):
    use_bootswatch = True


xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSetting(object):
    menu_style = 'accordion'
    global_search_models = [Individu]
    global_add_models = []


xadmin.site.register(views.CommAdminView, GlobalSetting)


class WishInline(object):

    def email(self, obj):
        return obj.individu.personal_email

    def reins(self, obj):
        if obj.is_reins:
            return 'oui'
        else:
            return 'non'
    reins.short_description = 'Réinscription'

    model = Wish
    extra = 0
    style = 'table'
    fields = ['email', 'annee']
    readonly_fields = ['code_dossier', 'etape', 'diplome_acces', 'centre_gestion', 'reins',
                       'date_validation', 'valide', 'get_transition_log', 'get_suivi_dossier', 'print_dossier_equi']
    exclude = ('annee', 'is_reins')
    can_delete = True
    hidden_menu = True

    @filter_hook
    def get_readonly_fields(self):
        if self.request.user.is_superuser:
            return self.readonly_fields
        else:
            return self.readonly_fields + ['state', 'suivi_dossier']

    def get_transition_log(self, obj):
        reponse = '<table>'
        for transition in obj.parcours_dossier.all():
            reponse += '<tr><td>{}</td><td>{}</td></tr>'.format(WishWorkflow.states[transition.to_state].title, transition.timestamp.strftime('%d/%m/%Y %H:%M:%S'))
        reponse += '</table>'
        return reponse
    get_transition_log.short_description = 'parcours'
    get_transition_log.allow_tags = True


    def get_suivi_dossier(self, obj):
        reponse = '<table>'
        print obj.etape_dossier.all()
        for transition in obj.etape_dossier.all():
            reponse += '<tr><td>{}</td><td>{}</td></tr>'.format(SuiviDossierWorkflow.states[transition.to_state].title, transition.timestamp.strftime('%d/%m/%Y %H:%M:%S'))
        reponse += '</table>'
        return reponse
    get_suivi_dossier.short_description = 'suivi'
    get_suivi_dossier.allow_tags = True

    def print_dossier_equi(self, obj):
        url = reverse('impression_equivalence', kwargs={'pk': obj.pk})
        url2 = reverse('impression_decision_equivalence', kwargs={'pk': obj.pk})
        reponse = '<a href="{}" class="btn btn-primary">Impression</a>'.format(url)
        reponse +='<a href="{}" class="btn btn-primary">ImpressionDecision</a>'.format(url2)
        return reponse
    print_dossier_equi.allow_tags = True
    print_dossier_equi.short_description = 'Impression dossier équivalence'


class IndividuXadmin(object):
    site_title = 'Consultation des dossiers étudiants'
    show_bookmarks = False
    fields = ('code_opi', 'last_name', 'first_name1', 'birthday', 'personal_email', 'state')
    readonly_fields = ('code_opi', 'last_name', 'first_name1', 'birthday', 'personal_email', 'get_transition_log')
    list_display = ('__unicode__', 'last_name')
    list_export = []
    list_per_page = 10
    search_fields = ('last_name', 'first_name1', 'common_name', 'student_code', 'code_opi', 'wishes__code_dossier')
    list_exclude = ('id', 'personal_email_save', 'opi_save', 'year')
    list_select_related = None
    use_related_menu = False
    inlines = [WishInline]
    hidden_menu = True

    def has_add_permission(self):
        return False

    def has_delete_permission(self, obj=None):
        return False

    @filter_hook
    def get_readonly_fields(self):
        if self.request.user.is_superuser:
            return self.readonly_fields
        else:
            return self.readonly_fields + ('state', )

    def get_transition_log(self, obj):
        reponse = '<table>'
        for transition in obj.etape_dossier.all():
            reponse += '<tr><td>{}</td><td>{}</td></tr>'.format(IndividuWorkflow.states[transition.to_state], transition.timestamp.strftime('%d/%m/%Y %H:%M:%S'))
        reponse += '</table>'
        return reponse
    get_transition_log.short_description = 'parcours'
    get_transition_log.allow_tags = True


class SettingsEtapeXadmin(object):
    exclude = ('lib_etp', 'cod_cyc', 'cod_cur', 'annee')
    form_layout = (
        Main(
            Fieldset('Etape',
                     'cod_etp',
                     'diplome',
                     'label',
                     'label_formation'),
            TabHolder(
                Tab('Equivalence',
                    Fieldset('',
                             'date_ouverture_equivalence',
                             'date_fermeture_equivalence',
                             'document_equivalence',
                             'path_template_equivalence',
                             'grille_de_equivalence')),
                Tab('Candidature',
                    Fieldset('',
                             'date_ouverture_candidature',
                             'date_fermeture_candidature',
                             'note_maste',
                             'document_candidature',)),


            )
        ),
        Side(Fieldset('Settings',
                      'required_equivalence',
                      'is_inscription_ouverte'))
    )


xadmin.site.register(Individu, IndividuXadmin)
xadmin.site.register(SettingsEtape, SettingsEtapeXadmin)
# xadmin.site.register_plugin(IEDPlugin, CommAdminView)
