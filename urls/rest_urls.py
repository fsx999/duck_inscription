from django.conf.urls import url, include
from rest_framework import routers, viewsets
from django_apogee.models import Pays, Departement, SitFam, TypHebergement, BacOuxEqu, SitMil, TypHandicap, AnneeUni
from duck_inscription.models import Individu
from duck_inscription.serializers import IndividuSerializer, PaysSerializer, DepartementSerializer, SitFamSerializer, \
    TypHebergementSerializer, BacOuxEquSerializer, SitMilSerializer, TypHandicapSerializer, AnneeUniSerializer
from duck_inscription import views

class AnneeUniViewSet(viewsets.ModelViewSet):
    queryset = AnneeUni.objects.all()
    serializer_class = AnneeUniSerializer


class BacOuxEquViewSet(viewsets.ModelViewSet):
    queryset = BacOuxEqu.objects.all()
    serializer_class = BacOuxEquSerializer


class DepartementViewSet(viewsets.ModelViewSet):
    queryset = Departement.objects.all()
    serializer_class = DepartementSerializer


class IndividuViewSet(viewsets.ModelViewSet):
    queryset = Individu.objects.all()
    serializer_class = IndividuSerializer


class PaysViewSet(viewsets.ModelViewSet):
    queryset = Pays.objects.all()
    serializer_class = PaysSerializer


class SitFamViewSet(viewsets.ModelViewSet):
    queryset = SitFam.objects.all()
    serializer_class = SitFamSerializer


class SitMilViewSet(viewsets.ModelViewSet):
    queryset = SitMil.objects.all()
    serializer_class = SitMilSerializer


class TypHandicapViewSet(viewsets.ModelViewSet):
    queryset = TypHandicap.objects.all()
    serializer_class = TypHandicapSerializer


class TypHebergementViewSet(viewsets.ModelViewSet):
    queryset = TypHebergement.objects.all()
    serializer_class = TypHebergementSerializer


router = routers.DefaultRouter(trailing_slash=False)
router.register(r'anneeuni', AnneeUniViewSet)
router.register(r'bacouxequ', BacOuxEquViewSet)
router.register(r'departements', DepartementViewSet)
router.register(r'individus', IndividuViewSet)
router.register(r'pays', PaysViewSet)
router.register(r'sitfam', SitFamViewSet)
router.register(r'sitmil', SitMilViewSet)
router.register(r'typhandicap', TypHandicapViewSet)
router.register(r'typehebergement', TypHebergementViewSet)


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^v1/statistique_inscription', views.StatistiqueView.as_view(), name='statistique_inscription_v1')
]