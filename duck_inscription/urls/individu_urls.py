# # -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
# from inscription.forms import (CodeEtudiantForm,
#                                DernierEtablissementForm, SituationAnneePrecedenteForm,
#                                EtablissementSituationAnneePrecedenteForm, EtablissementDernierDiplomeForm,
#                                TestAutreEtablissementForm, AutreEtablissementForm, CatSocForm, SituationSocialeForm,
#                                SecuriteSocialeForm, NumSecuForm)
# from inscription.views import (
#     DispatchIndividu,
#     test_username,
#     InfoPersoView,
#     not_inscrit_p8,
#     CodeEtuManquant,
#     AdresseIndividuView,
#     RecapitulatifIndividuView,
#     BacTestView,
#     DossierInscriptionWizard,
#     ValidationDossierInscription,
#     condition_etablissement_annee_precedente, condition_autre_cursus, SituationSocialeDossierInscription,
#     condition_centre_payeur, condition_num_secu, ValidationSituationSocialeView, IneTestView, DossierInscriptionView)
# from inscription.utils import user_verif_etape_and_login
#
# __author__ = 'paul'
#
from django.conf.urls import patterns, url
# from inscription.forms import PremiereInscriptionForm, ComplementBacForm
#
# # list_form_dossier_inscription = [
# #     PremiereInscriptionForm,
# #     ComplementBacForm,
# #     DernierEtablissementForm,
# #     SituationAnneePrecedenteForm,
# #     EtablissementSituationAnneePrecedenteForm,
# #     EtablissementDernierDiplomeForm,
# #     TestAutreEtablissementForm,
# #     AutreEtablissementForm,
# #     CatSocForm
# # ]
# # condition_dossier_inscription = {
# #     '4': condition_etablissement_annee_precedente,
# #     '7': condition_autre_cursus,
# # }
# # list_form_situation_sociale = [
# #     SituationSocialeForm,
# #     SecuriteSocialeForm,
# #     NumSecuForm
# # ]
# # condition_situation_sociale = {
# #     '1': condition_centre_payeur,
# #     '2': condition_num_secu,
# #
# # }
from duck_inscription.forms.individu_forms import CodeEtudiantForm
from duck_inscription.utils import user_verif_etape_and_login
from duck_inscription.views import DispatchIndividu, CodeEtuManquant, test_username, InfoPersoView, IneTestView, \
    BacTestView, AccueilView, not_inscrit_universite, AdresseIndividuView, RecapitulatifIndividuView

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
#                        #    url(r'^diplome/$', DiplomeAccesView.as_view(), name="diplome_acces"),
                       url(r'^recapitulatif/(?P<option>.+)',
                           user_verif_etape_and_login(RecapitulatifIndividuView.as_view()),
                           name="recap"),
                       url(r'^recapitulatif/$', user_verif_etape_and_login(RecapitulatifIndividuView.as_view()),
                           name="recap"),
#
#                        url(r'^dossier_inscription/(?P<pk>\d+)/$',
#                            login_required(
#                            DossierInscriptionView.as_view()),
#                            name="dossier_inscription"),
#
#                        url(r'^validation_dossier_inscription/(?P<pk>\d+)/$',
#                            login_required(ValidationDossierInscription.as_view()),
#                            name="validation_dossier_inscription"),
#                        # url(r'^situation_sociale/(?P<pk>\d+)/$',
#                        #     login_required(SituationSocialeDossierInscription.as_view(
#                        #         list_form_situation_sociale,
#                        #         condition_dict=condition_situation_sociale)),
#                        #     name="situation_sociale"),
#                        url(r'^validation_situation_sociale/(?P<pk>\d+)/$',
#                            login_required(ValidationSituationSocialeView.as_view()),
#                            name="validation_situation_sociale"),
)
