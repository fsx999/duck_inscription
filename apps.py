# coding=utf-8
from __future__ import unicode_literals
__author__ = 'paulguichon'
from django.apps import AppConfig

class DuckInscription(AppConfig):
    name = "duck_inscription"
    label = 'duck_inscription'

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

