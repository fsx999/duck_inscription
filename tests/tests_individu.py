# coding=utf-8
from django_apogee.factories.individu_factories import IndividuFactory
from django_apogee.models import Individu
from datetime import date
from duck_inscription.forms import CodeEtudiantForm

__author__ = 'paulguichon'
from django.test import TestCase


class IndividuTestCase(TestCase):

    def setUp(self):
        IndividuFactory.create_individu_with_two_adresses()

    def test_individu_code_form(self):
        individu = Individu.objects.all().first()

        date_naissance_false = date.today()
        cod_etu = individu.cod_etu
        form = CodeEtudiantForm(data={'date_naissance': individu.date_nai_ind,
                                      'code_etu': individu.cod_etu})
        self.assertTrue(form.is_valid())
        form = CodeEtudiantForm(data={'date_naissance': date_naissance_false,
                                      'code_etu': individu.cod_etu})
        self.assertFalse(form.is_valid())
        form = CodeEtudiantForm(data={'date_naissance': date_naissance_false,
                                      'code_etu': '0'})
        self.assertFalse(form.is_valid())