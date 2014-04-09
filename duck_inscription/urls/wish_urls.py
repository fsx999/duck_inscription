# # -*- coding: utf-8 -*-
# from django.views.generic.base import TemplateView
# from inscription.utils import wish_verif_etape_and_login
#
# from inscription.views import (StepView,
#                                DeleteWish,
#                                ListeDiplomeAccesView,
#                                EquivalenceView,
#                                OuvertureEquivalence,
#                                ListeAttenteEquivalenceView,
#                                DemandeEquivalenceView,
#                                OuvertureCandidature,
#                                CandidatureView,
#                                ListeAttenteCandidatureView,
#                                OuverturePaiementView,
#                                EquivalencePdfView,
#                                CandidaturePdfView,
#                                ChoixIedFpView,
#                                InscriptionView, InscriptionPdfView,
#                                ListeAttenteInscriptionView, NewAuditeurView,
#                                AuditeurView, AuditeurPdfView, NewWishView,
#                                NoteMasterView, DroitView)
#
# __author__ = 'paul'
from django.conf.urls import patterns, url
# from django.contrib.auth.decorators import login_required
#
from duck_inscription.views import NewWishView, StepView

urlpatterns = patterns('',
                       url(r'^nouveau_voeu/$', NewWishView.as_view(), name='new_wish'),
                       url(r'^liste_etape/$', StepView.as_view(), name="liste_etape"),
#                        url(r'^supprimer_voeu/(?P<pk>\d+)/$', login_required(DeleteWish.as_view()), name="delete_wish"),
#                        url(r'^liste_diplome/(?P<pk>\d+)/$', login_required(ListeDiplomeAccesView.as_view()),
#                            name="liste_diplome"),
#                        url(r'^demande_equivalence/(?P<pk>\d+)/$',
#                            wish_verif_etape_and_login(DemandeEquivalenceView.as_view()),
#                            name="demande_equivalence_etape"),
#                        url(r'ouverture_equivalence/(?P<pk>\d+)/$',
#                            wish_verif_etape_and_login(OuvertureEquivalence.as_view()), name="ouverture_equivalence"),
#                        url(r'^equivalence/(?P<pk>\d+)/$', wish_verif_etape_and_login(EquivalenceView.as_view()),
#                            name="equivalence"),
#                        url(r'^equivalence_pdf/(?P<pk>\d+)/$', login_required(EquivalencePdfView.as_view()),
#                            name="equivalence_pdf"),
#
#                        url(r'^liste_attente_equivalence/(?P<pk>\d+)/$',
#                            wish_verif_etape_and_login(ListeAttenteEquivalenceView.as_view()),
#                            name="liste_attente_equivalence"),
#                        url(r'^fin_liste_attente_equivalence/$',
#
#                            TemplateView.as_view(template_name='wish/fin_liste_attente_equivalence.html'),
#                            name="fin_liste_attente_equivalence"),
#
#                        url(r'^ouverture_candidature/(?P<pk>\d+)/$',
#                            wish_verif_etape_and_login(OuvertureCandidature.as_view()), name="ouverture_candidature"),
#                        url(r'^note_master/(?P<pk>\d+)/$',
#                            wish_verif_etape_and_login(NoteMasterView.as_view()), name="note_master"),
#                        url(r'^candidature/(?P<pk>\d+)/$', wish_verif_etape_and_login(CandidatureView.as_view()),
#                            name="candidature"),
#                        url(r'^candidature_pdf/(?P<pk>\d+)/$', login_required(CandidaturePdfView.as_view()),
#                            name="candidature_pdf"),
#                        url(r'^liste_attente_candidature/(?P<pk>\d+)/$',
#                            wish_verif_etape_and_login(ListeAttenteCandidatureView.as_view()),
#                            name="liste_attente_candidature"),
#                        url(r'^ouverture_paiement/(?P<pk>\d+)/$',
#                            wish_verif_etape_and_login(OuverturePaiementView.as_view()), name="ouverture_paiement"),
#                        url(r'^choix_ied_fp/(?P<pk>\d+)/$', wish_verif_etape_and_login(ChoixIedFpView.as_view()),
#                            name="choix_ied_fp"),
#                        url(r'^droit_univ/(?P<pk>\d+)/$',
#                            wish_verif_etape_and_login(DroitView.as_view()),
#                            name="droit_universitaire"),
#                        url(r'^inscription/(?P<pk>\d+)/$', wish_verif_etape_and_login(InscriptionView.as_view()),
#                            name="inscription"),
#                        url(r'^liste_attente_inscription/(?P<pk>\d+)/$',
#                            wish_verif_etape_and_login(ListeAttenteInscriptionView.as_view()),
#                            name="liste_attente_inscription"),
#
#                        url(r'^inscription_pdf/(?P<pk>\d+)/$', login_required(InscriptionPdfView.as_view()),
#                            name="inscription_pdf"),
#                        url(r'^auditeur_libre/$', login_required(NewAuditeurView.as_view()), name='new_auditeur'),
#                        url(r'^auditeur/(?P<pk>\d+)/$', login_required(AuditeurView.as_view()), name="auditeur"),
#                        url(r'do_pdf_auditeur/(?P<pk>\d+)/$', login_required(AuditeurPdfView.as_view()),
#                            name="do_pdf_auditeur"),
)
