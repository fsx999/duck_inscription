# coding=utf-8
from __future__ import unicode_literals
import xadmin
from xadmin import views
from .models import Wish


class MainDashboard(object):
    widgets = [
        [
            {"type": "html", "title": "Test Widget", "content": "<h3> Welcome to Xadmin! </h3>"},


        ],
        [
            {"type": "qbutton", "title": "Quick Start", "btns": [{'title': "Google", 'url': "http://www.google.com"},
                                                                 {'model': Wish}]},
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

    # menu_style = 'default'#'accordion'
    menu_style = 'accordion'
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
    fields = ['individu', 'etape', 'is_reins', 'state']
    readonly_fields = ['individu', 'etape', 'is_reins', 'date_validation', 'state', 'email']
    exclude = ('centre_gestion', 'diplome_acces', 'valide', 'annee')
    list_export = []
    show_bookmarks = False
    list_per_page = 10

    def get_readonly_fields(self):
        # if self.request.user.is_superuser:
        #     return ()
        return self.readonly_fields

    def has_add_permission(self):
        return False

    def has_delete_permission(self, obj=None):
        return False

    # def has_change_permission(self, obj=None):
    #     return False

xadmin.site.register(Wish, WishAdmin)
