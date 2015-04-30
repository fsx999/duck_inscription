# coding=utf-8
__author__ = 'paulguichon'
from django.test import TestCase


class IndividuTestCase(TestCase):

    def setUp(self):
        print "coucou"

    def test_individu(self):
        print "re coucou"