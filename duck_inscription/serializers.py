from rest_framework import serializers
from django_apogee.models import TypHebergement, BacOuxEqu, SitMil, TypHandicap, AnneeUni
from duck_inscription.models import Individu, Pays, Departement, SitFam


class AnneeUniSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AnneeUni



class BacOuxEquSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = BacOuxEqu


class DepartementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Departement


class IndividuSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Individu
        exclude = ('user', )


class PaysSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Pays


class SitFamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SitFam


class SitMilSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SitMil


class TypHandicapSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TypHandicap


class TypHebergementSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TypHebergement


