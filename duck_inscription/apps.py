# coding=utf-8
from __future__ import unicode_literals
__author__ = 'paulguichon'
from django.apps import AppConfig


class DuckInscriptionConfig(AppConfig):
    verbose_name = 'inscription'
    models_module = 'models'

