# coding=utf-8
from __future__ import unicode_literals


__author__ = 'paulguichon'
from django.apps import AppConfig

class DuckInscription(AppConfig):
    name = "duck_inscription"
    label = 'duck_inscription'
    # urls = [{
    #     'regex': r'^inscription/',
    #     'module_url': 'duck_inscription.urls.adminx_urls'
    # }]
    collapse_settings = [{
        "group_label": "Duck Inscription",
        "icon": 'fa-fw fa fa-circle-o',
        "entries": [{
            "label": 'Settings Etapes',
            "icon": 'fa-fw fa fa-circle-o',
            "url": '/duck_inscription/settingsetape/',  # name or url
            "groups_permissions": [],  # facultatif
            "permissions": [],  # facultatif
        }, {
            "label": 'Cursus',
            "icon": 'fa-fw fa fa-circle-o',
            "url": '/duck_inscription/cursusetape/',  # name or url
            "groups_permissions": [],  # facultatif
            "permissions": [],  # facultatif
        }, {
            "label": ' Settings année universitaire ',
            "icon": 'fa-fw fa fa-circle-o',
            "url": '/duck_inscription/settinganneeuni/',  # name or url
            "groups_permissions": [],  # facultatif
            "permissions": [],  # facultatif
        },{
            "label": 'Catégories pièces ',
            "icon": 'fa-fw fa fa-circle-o',
            "url": '/duck_inscription/categoriepiecemodel/',  # name or url
            "groups_permissions": [],  # facultatif
            "permissions": [],  # facultatif
        },{
            "label": 'Pièces dossier',
            "icon": 'fa-fw fa fa-circle-o',
            "url": '/duck_inscription/piecedossiermodel/',  # name or url
            "groups_permissions": [],  # facultatif
            "permissions": [],  # facultatif
        }],

        "groups_permissions": [],  # facultatif
        "permissions": [],  # facultatif
    }, ]

    def ready(self):
        from django.conf.urls import url, include
        from duck_inscription.views import UserView, EmailView
        self.urls = [
            url(r'^inscription/', include('duck_inscription.urls.adminx_urls')),
            url(r'^compte/', include('duck_inscription.urls.enregistrement_urls')),
            url(r'^individu/', include('duck_inscription.urls.individu_urls')),
            url(r'^voeu/', include('duck_inscription.urls.wish_urls')),
            url(r'^test_user/$', UserView.as_view(), name='test_user'),
            url(r'^test_email/$', EmailView.as_view(), name='test_email'),
            url(r'^api/', include('duck_inscription.urls.rest_urls')),
        ]