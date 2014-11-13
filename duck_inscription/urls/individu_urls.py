# # -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.conf.urls import patterns, url
from duck_inscription.forms.individu_forms import CodeEtudiantForm
from duck_inscription.utils import user_verif_etape_and_login
from duck_inscription.views import DispatchIndividu, CodeEtuManquant, test_username, InfoPersoView, IneTestView, \
    BacTestView, AccueilView, not_inscrit_universite, AdresseIndividuView, RecapitulatifIndividuView, \
    DossierInscriptionView

urlpatterns = patterns('',
                       url(r'^accueil/', user_verif_etape_and_login(AccueilView.as_view()), name='accueil'),
                       url(r'^$', login_required(DispatchIndividu.as_view()), name="dispatch"),
                       url(r'^premiere_connexion/$', user_verif_etape_and_login(CodeEtuManquant.as_view(
                           form_class=CodeEtudiantForm, premiere_connection="True")),
                           name="first_connection"),
                       url(r'^test_individu/$', test_username, name="test_individu"),
                       url(r'^test_bac/$', BacTestView.as_view(), name="validation_annee_bac"),
                       url(r'^individu/$', user_verif_etape_and_login(InfoPersoView.as_view()), name="individu"),
                       url(r'^not_inscrit_universite/$', not_inscrit_universite, name="not_inscrit_universite"),
                       url(r'^code_etudiant/$', user_verif_etape_and_login(CodeEtuManquant.as_view()),
                           name="code_etu_manquant"),
                       url(r'^test_ine/$', IneTestView.as_view(),
                           name="test_ine"),
                       url(r'^adresse/$', user_verif_etape_and_login(AdresseIndividuView.as_view()), name="adresse"),
                       url(r'^recapitulatif/(?P<option>.+)',
                           user_verif_etape_and_login(RecapitulatifIndividuView.as_view()),
                           name="recap"),
                       url(r'^recapitulatif/$', user_verif_etape_and_login(RecapitulatifIndividuView.as_view()),
                           name="recap"),
                       url(r'^dossier_inscription/(?P<pk>\d+)/$',
                           login_required(DossierInscriptionView.as_view()),
                           name="dossier_inscription"),)
