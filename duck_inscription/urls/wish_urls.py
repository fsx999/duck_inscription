# # -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from duck_inscription.utils import wish_verif_etape_and_login
from duck_inscription.views import NewWishView, StepView, ListeDiplomeAccesView, DemandeEquivalenceView, \
    EquivalenceView, DeleteWish, OuvertureCandidature, OuvertureEquivalence, OuverturePaiementView, EquivalencePdfView, \
    ListeAttenteEquivalenceView, NoteMasterView, CandidatureView, CandidaturePdfView, ListeAttenteCandidatureView, \
    ChoixIedFpView, DroitView, InscriptionView, ListeAttenteInscriptionView, InscriptionPdfView


urlpatterns = patterns('', url(r'^nouveau_voeu/(?P<pk>\d+)$', login_required(NewWishView.as_view()), name='new_wish'),
                       url(r'^liste_etape/(?P<pk>\d+)/$', login_required(StepView.as_view()), name="liste_etape"),
                       url(r'^supprimer_voeu/(?P<pk>\d+)/$', login_required(DeleteWish.as_view()), name="delete_wish"),
                       url(r'^liste_diplome/(?P<pk>\d+)/$', wish_verif_etape_and_login(ListeDiplomeAccesView.as_view()),
                           name="liste_diplome"), url(r'^demande_equivalence/(?P<pk>\d+)/$',
                                                      wish_verif_etape_and_login(DemandeEquivalenceView.as_view()),
                                                      name="demande_equivalence"),
                       url(r'ouverture_equivalence/(?P<pk>\d+)/$',
                           wish_verif_etape_and_login(OuvertureEquivalence.as_view()), name="ouverture_equivalence"),
                       url(r'^equivalence/(?P<pk>\d+)/$', wish_verif_etape_and_login(EquivalenceView.as_view()),
                           name="equivalence"),
                       url(r'^equivalence_pdf/(?P<pk>\d+)/$', login_required(EquivalencePdfView.as_view()),
                           name="equivalence_pdf"),  #
                       url(r'^liste_attente_equivalence/(?P<pk>\d+)/$',
                           wish_verif_etape_and_login(ListeAttenteEquivalenceView.as_view()),
                           name="liste_attente_equivalence"),
                       url(r'^liste_attente_equivalence/(?P<pk>\d+)/$',
                           wish_verif_etape_and_login(ListeAttenteEquivalenceView.as_view()),
                           name="mis_liste_attente_equi"),

                       url(r'^ouverture_candidature/(?P<pk>\d+)/$',
                           wish_verif_etape_and_login(OuvertureCandidature.as_view()), name="ouverture_candidature"),
                       url(r'^note_master/(?P<pk>\d+)/$', wish_verif_etape_and_login(NoteMasterView.as_view()),
                           name="note_master"),
                       url(r'^candidature/(?P<pk>\d+)/$', wish_verif_etape_and_login(CandidatureView.as_view()),
                           name="candidature"),
                       url(r'^candidature_pdf/(?P<pk>\d+)/$', login_required(CandidaturePdfView.as_view()),
                           name="candidature_pdf"),
                       url(r'^liste_attente_candidature/(?P<pk>\d+)/$',
                                                        wish_verif_etape_and_login(
                                                            ListeAttenteCandidatureView.as_view()),
                                                        name="liste_attente_candidature"),
                       url(r'^liste_attente_candidature/(?P<pk>\d+)/$',
                                                        wish_verif_etape_and_login(
                                                            ListeAttenteCandidatureView.as_view()),
                                                        name="mis_liste_attente_candi"),
                       url(r'^ouverture_inscription/(?P<pk>\d+)/$',
                           wish_verif_etape_and_login(OuverturePaiementView.as_view()), name="ouverture_inscription"),
                       url(r'^choix_ied_fp/(?P<pk>\d+)/$', wish_verif_etape_and_login(ChoixIedFpView.as_view()),
                                                  name="choix_ied_fp"),
                       url(r'^droit_univ/(?P<pk>\d+)/$',
                                                  wish_verif_etape_and_login(DroitView.as_view()),
                                                  name="droit_univ"),
                      url(r'^inscription/(?P<pk>\d+)/$', wish_verif_etape_and_login(InscriptionView.as_view()),
                                                  name="inscription"),
                      url(r'^liste_attente_inscription/(?P<pk>\d+)/$',
                                                  wish_verif_etape_and_login(ListeAttenteInscriptionView.as_view()),
                                                  name="liste_attente_inscription"),

                      url(r'^inscription_pdf/(?P<pk>\d+)/$', login_required(InscriptionPdfView.as_view()),
                                                  name="inscription_pdf"),

                       )
