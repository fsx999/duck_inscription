# coding=utf-8
from __future__ import unicode_literals
from xadmin import views
import xadmin
from duck_inscription.models import Individu
from duck_inscription.models import Wish

class BaseSetting(object):
    use_bootswatch = True


xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSetting(object):
    menu_style = 'accordion'
    global_search_models = [Individu, Wish]
    global_add_models = []


xadmin.site.register(views.CommAdminView, GlobalSetting)

class MainDashboard(object):
    widgets = [[{"type": "qbutton", "title": "Scolarité", "btns": [

        {'title': "Pré-Inscription", 'url': 'inscription'}, {'title': "Statistique", 'url': 'statistiques'},
        {'title': 'Extraction', 'url': 'extraction'}]}, ]]
    site_title = 'Backoffice'
    title = 'Accueil'
    widget_customiz = False
xadmin.site.register(views.website.IndexView, MainDashboard)


class IncriptionDashBoard(views.website.IndexView):
    widgets = [[{"type": "qbutton", "title": "Gestion dossier",
                 "btns": [{'title': 'Reception', 'url': '/dossier_receptionner'},
                          {'title': 'Gestion Equivalence', 'url': '/dossier_equivalence'},
                          {'title': 'Gestion Candidature', 'url': '/dossier_candidature'},
                          {'title': 'Gestion Dossier inscription', 'url': '/traitement_inscription'},
                          {'title': 'Gestion Dossier inscription Auditeur', 'url': '/traitement_inscription_auditeur'},
                          {'title': 'Remontee opi', 'model': Wish},
                          ]},
                {"type": "qbutton", "title": "Consultation des dossiers",
                "btns": [{'title': 'Consultation dossier inscription', 'model': Individu},
                         {'title': 'Consultation dossier inscription etudiant apogeé', 'url':'/django_apogee/individu'}]}
               ]]
    site_title = 'Backoffice'
    title = 'Accueil'
    widget_customiz = False
xadmin.site.register_view(r'^inscription/$', IncriptionDashBoard, 'inscription')


class StatistiqueDashBoard(views.website.IndexView):
    widgets = [[{"type": "qbutton", "title": "Inscription",
                 "btns": [{'title': 'Statistique Pal (équivalence, candidature)', 'url': '/stats_pal'},
                          {'title': 'Statistique Piel (préinscription)', 'url': '/stats_piel'},
                          {'title': 'Statistique Apogee (inscrit)', 'url': '/stats_apogee'},
                          ]}, ]]
    site_title = 'Backoffice'
    title = 'Accueil'
    widget_customiz = False
xadmin.site.register_view(r'^statistiques/$', StatistiqueDashBoard, 'statistiques')
