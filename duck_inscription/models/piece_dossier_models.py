# -*- coding: utf8 -*-
from django.utils.six import python_2_unicode_compatible
from .wish_models import Wish

from django.db import models

@python_2_unicode_compatible
class CategoriePieceModel(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Catégorie pièces"
        verbose_name_plural = "Catégories pièces"


@python_2_unicode_compatible
class PieceDossierModel(models.Model):
    label = models.TextField()
    category = models.ForeignKey(CategoriePieceModel)

    def __str__(self):
        return "({}) {}".format(self.category.name, self.label)

    def value(self):
        return str(self.id)
    class Meta:
        verbose_name = "Pièce dossier"
        verbose_name_plural = "Pièces dossier"


class PiecesManquantesDossierWishModel(models.Model):
    pieces = models.ManyToManyField(PieceDossierModel)
    wish = models.OneToOneField(Wish, related_name='dossier_pieces_manquantes')
    date = models.DateTimeField(auto_now_add=True)
    # date = models.DateTimeField(auto_now=True)

