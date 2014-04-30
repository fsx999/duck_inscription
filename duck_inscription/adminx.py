# coding=utf-8
from __future__ import unicode_literals
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse, reverse_lazy
from xadmin.models import UserWidget, UserSettings
import xadmin
from xadmin import views
from xadmin.plugins.details import DetailsPlugin
from duck_inscription.models import Individu, SettingsEtape
from .models import Wish

from xadmin.sites import site
from xadmin.views import filter_hook
from xadmin.views.dashboard import WidgetDataError


class IncriptionDashBoard(views.website.IndexView):
    widgets = [
        [
            {"type": "qbutton", "title": "Inscription", "btns": [
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
            {"type": "qbutton", "title": "Scolarité", "btns": [{'title': "Inscription", 'url': 'inscription'},
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
    readonly_fields = ['etape', 'email', 'diplome_acces', 'centre_gestion', 'reins', 'state',
                       'suivi_dossier', 'date_validation', 'valide']
    exclude = ('annee', 'is_reins')
    can_delete = False
    hidden_menu = True

class IndividuXadmin(object):

    site_title = 'Consultation des dossiers étudiants'
    show_bookmarks = False
    fields = ('code_opi', 'last_name', 'first_name1', 'birthday', 'personal_email', 'state')
    readonly_fields = ('code_opi', 'last_name', 'first_name1', 'birthday', 'personal_email')
    list_display =('__unicode__', 'last_name')
    list_export = []
    list_per_page = 10
    search_fields = ('last_name', 'first_name1', 'code_opi', 'wishes__code_dossier')
    list_exclude = ('id', 'personal_email_save', 'opi_save', 'year')
    list_select_related = None
    use_related_menu = False
    inlines = [WishInline]
    hidden_menu = True


    def has_add_permission(self):
        return False


    def has_delete_permission(self, obj=None):
        return False

xadmin.site.register(Individu, IndividuXadmin)
xadmin.site.register(SettingsEtape)
