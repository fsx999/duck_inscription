# coding=utf-8
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from duck_inscription.views.adminx_views import DossierReceptionView

urlpatterns = patterns('',
                       url(r'dossier_receptionner/$', login_required(DossierReceptionView.as_view()), name='dossier_receptionne'),
                       )
