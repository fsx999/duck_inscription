# coding=utf-8
from __future__ import unicode_literals
from xadmin import views
import xadmin
from duck_inscription.models import Individu, SettingsEtape
from .models import Wish
from xadmin.views import filter_hook


class IncriptionDashBoard(views.website.IndexView):
    widgets = [
        [
            {"type": "qbutton", "title": "Inscription", "btns": [
                {'title': 'Reception', 'url': 'dossier_receptionne'},
                {'title': 'Dossier inscription', 'model': Individu}
            ]},
        ]
    ]
    site_title = 'Backoffice'
    title = 'Accueil'
    widget_customiz = False
xadmin.site.register_view(r'inscription/$', IncriptionDashBoard,  'inscription')


class MainDashboard(object):
    widgets = [
        [
            {"type": "qbutton", "title": "Scolarité", "btns": [

                {'title': "Inscription", 'url': 'inscription'},
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
    readonly_fields = ['etape', 'email', 'diplome_acces', 'centre_gestion', 'reins',
                       'date_validation', 'valide', 'get_transition_log']
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
        for transition in obj.transitions_logs:
            reponse += '<tr><td>{}</td><td>{}</td></tr>'.format(transition.transition, transition.timestamp.strftime('%d/%m/%Y %H:%M:%S'))
        reponse += '</table>'
        return reponse
    get_transition_log.short_description = 'parcours'
    get_transition_log.allow_tags = True


class IndividuXadmin(object):
    site_title = 'Consultation des dossiers étudiants'
    show_bookmarks = False
    fields = ('code_opi', 'last_name', 'first_name1', 'birthday', 'personal_email', 'state')
    readonly_fields = ('code_opi', 'last_name', 'first_name1', 'birthday', 'personal_email', 'get_transition_log')
    list_display = ('__unicode__', 'last_name')
    list_export = []
    list_per_page = 10
    search_fields = ('last_name', 'first_name1', 'common_name', 'code_opi', 'wishes__code_dossier')
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
        for transition in obj.transitions_logs:
            reponse += '<tr><td>{}</td><td>{}</td></tr>'.format(transition.transition, transition.timestamp.strftime('%d/%m/%Y %H:%M:%S'))
        reponse += '</table>'
        return reponse
    get_transition_log.short_description = 'parcours'
    get_transition_log.allow_tags = True

xadmin.site.register(Individu, IndividuXadmin)
xadmin.site.register(SettingsEtape)
