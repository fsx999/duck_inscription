# # -*- coding: utf-8 -*-
from django.conf.urls import  url
from django.contrib.auth.decorators import login_required
from duck_inscription.utils import wish_verif_etape_and_login
from duck_inscription import views

urlpatterns = [
    url(r'^nouveau_voeu/(?P<pk>\d+)$', login_required(views.NewWishView.as_view()), name='new_wish'),
    url(r'^liste_etape/(?P<pk>\d+)/$', login_required(views.StepView.as_view()), name="liste_etape"),
    url(r'^supprimer_voeu/(?P<pk>\d+)/$', login_required(views.DeleteWish.as_view()), name="delete_wish"),
    url(r'^liste_diplome/(?P<pk>\d+)/$', wish_verif_etape_and_login(views.ListeDiplomeAccesView.as_view()),
        name="liste_diplome"), url(r'^demande_equivalence/(?P<pk>\d+)/$',
                                   wish_verif_etape_and_login(views.DemandeEquivalenceView.as_view()),
                                   name="demande_equivalence"),
    url(r'ouverture_equivalence/(?P<pk>\d+)/$',
        wish_verif_etape_and_login(views.OuvertureEquivalence.as_view()), name="ouverture_equivalence"),
    url(r'^equivalence/(?P<pk>\d+)/$', wish_verif_etape_and_login(views.EquivalenceView.as_view()),
        name="equivalence"),
    url(r'^equivalence_pdf/(?P<pk>\d+)/$', login_required(views.EquivalencePdfView.as_view()),
        name="equivalence_pdf"),  #
    url(r'^liste_attente_equivalence/(?P<pk>\d+)/$',
        wish_verif_etape_and_login(views.ListeAttenteEquivalenceView.as_view()),
        name="liste_attente_equivalence"),
    url(r'^liste_attente_equivalence/(?P<pk>\d+)/$',
        wish_verif_etape_and_login(views.ListeAttenteEquivalenceView.as_view()),
        name="mis_liste_attente_equi"),

    url(r'^ouverture_candidature/(?P<pk>\d+)/$',
        wish_verif_etape_and_login(views.OuvertureCandidature.as_view()), name="ouverture_candidature"),
    url(r'^note_master/(?P<pk>\d+)/$', wish_verif_etape_and_login(views.NoteMasterView.as_view()),
        name="note_master"),
    url(r'^candidature/(?P<pk>\d+)/$', wish_verif_etape_and_login(views.CandidatureView.as_view()),
        name="candidature"),
    url(r'^candidature_pdf/(?P<pk>\d+)/$', login_required(views.CandidaturePdfView.as_view()),
        name="candidature_pdf"),
    url(r'^liste_attente_candidature/(?P<pk>\d+)/$',
        wish_verif_etape_and_login(
            views.ListeAttenteCandidatureView.as_view()),
        name="liste_attente_candidature"),
    url(r'^liste_attente_candidature/(?P<pk>\d+)/$',
        wish_verif_etape_and_login(
            views.ListeAttenteCandidatureView.as_view()),
        name="mis_liste_attente_candi"),


    url(r'^inscription/(?P<pk>\d+)/$', wish_verif_etape_and_login(views.InscriptionView.as_view()),
        name="inscription"),
    url(r'^liste_attente_inscription/(?P<pk>\d+)/$',
        wish_verif_etape_and_login(views.ListeAttenteInscriptionView.as_view()),
        name="liste_attente_inscription"),

    url(r'^inscription_pdf/(?P<pk>\d+)/$', login_required(views.InscriptionPdfView.as_view()),
        name="inscription_pdf"),

]
