# coding=utf-8
from __future__ import unicode_literals
from .individu_views import *
from enregistrement_views import *
from wish_views import *

class PiecesManquantesPdfView(TemplateView):
    template_name = "duck_inscription/wish/etiquette.html"