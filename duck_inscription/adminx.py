# coding=utf-8
from __future__ import unicode_literals
import xadmin
from xadmin import views
from duck_inscription.models import Individu
from .models import Wish

from xadmin.sites import site
class MainDashboard(object):
    widgets = [
        [
            {"type": "html", "title": "Test Widget", "content": "<h3> Welcome to Xadmin! </h3>"},


        ],
        [
            {"type": "qbutton", "title": "Quick Start", "btns": [{'title': "Google", 'url': "http://www.google.com"},
                                                                 {'model': Individu}
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

    def get_site_menu(self):
        return ({
            "title": 'cocouu',
            'menus': ({
                'title': 'test',
                'url': 'http://google.fr'
            },)
        },)
xadmin.site.register(views.CommAdminView, GlobalSetting)



class WishAdmin(object):

    def email(self, obj):
        return '{}'.format(obj.individu.personal_email)
    email.short_description = 'email'
    email.is_column = True

    list_display = ('individu', 'etape', 'email')
    search_fields = ['individu__last_name', 'individu__first_name1', 'code_dossier']
    list_filter = ['etape']
    hidden_menu = True
    actions = None
    save_as = False
    export = None
    fields = ['individu', 'etape', 'is_reins', 'state', 'email']

    readonly_fields = ['individu', 'etape', 'is_reins', 'date_validation', 'state', 'email']
    # exclude = ('centre_gestion', 'diplome_acces', 'valide', 'annee')
    list_export = []
    show_bookmarks = False
    list_per_page = 10



    def get_readonly_fields(self):
        # if self.request.user.is_superuser:
        #     return ()
        return self.readonly_fields



    # def has_change_permission(self, obj=None):
    #     return False


class IndividuXadmin(object):
    site_title = 'Consultation des dossiers étudiants'
    show_bookmarks = False
    fields = ('code_opi','last_name', 'first_name1', 'birthday', 'user')
    list_export = []
    list_per_page = 10
    search_fields = ('last_name', 'first_name1', 'code_opi', 'wishes__code_dossier')
    list_exclude = ('id', 'state', 'personal_email_save', 'opi_save', 'year')
    # show_detail_fields = ['user']

    def has_add_permission(self):
        return False



    def has_delete_permission(self, obj=None):
        return False

xadmin.site.register(Individu, IndividuXadmin)
xadmin.site.register(Wish, WishAdmin)
