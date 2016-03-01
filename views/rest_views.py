# coding=utf-8
from __future__ import unicode_literals
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import authentication, permissions
from duck_inscription.models import SettingsEtape
from duck_inscription.serializers import StatistiqueInscriptionSerializer
__author__ = 'paulguichon'


class StatistiqueView(generics.ListAPIView):
    """
    View to show all statistique.
    """
    queryset = SettingsEtape.objects.all()
    serializer_class = StatistiqueInscriptionSerializer
    permission_classes = (permissions.IsAuthenticated,)
