# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from duck_inscription.views import InscriptionPdfView, CandidaturePdfView
from duck_inscription.views.adminx_views import EquivalencePdfAdminView, \
    DecisionEquivalencePdfAdminView, ImprimerTousDecisions, ImprimerDecisionsEquivalenceEnMasseView, \
    ChangementCentreGestionView, OpiView

urlpatterns = patterns('',
                       # url(r'dossier_receptionner/$', login_required(DossierReceptionView.as_view()),
                       #     name='dossier_receptionner'),
                        url(r'imprimer_decisions_ordre/$', login_required(ImprimerDecisionsEquivalenceEnMasseView.as_view()),
                           name='imprimer_decisions_ordre'),
                       url(r'^impression_dossier_equivalence/(?P<pk>\d+)/$', login_required(EquivalencePdfAdminView.as_view()),
                           name="impression_equivalence"),
                       url(r'^impression_dossier_decisio_equivalence/(?P<pk>\d+)/$',
                           login_required(DecisionEquivalencePdfAdminView.as_view()),
                           name="impression_decision_equivalence"),
                       url(r'^inscription_pdf/(?P<pk>\d+)/$', login_required(InscriptionPdfView.as_view()),
                                                  name="inscription_pdf"),
                       url(r'^candidature_pdf/(?P<pk>\d+)/$', login_required(CandidaturePdfView.as_view()),
                           name="candidature_pdf"),
                       url(r'^changement_centre/(?P<pk>\d+)/$', login_required(ChangementCentreGestionView.as_view()),
                           name="changement_centre"),
                       url(r'^remontee_opi/$', login_required(OpiView.as_view()),
                           name="remontee_opi"),
                       )

