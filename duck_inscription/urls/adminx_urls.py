# coding=utf-8
from django.conf.urls import patterns, url
from duck_inscription.views.adminx_views import DossierReceptionView

urlpatterns = patterns('',
                       url(r'dossier_receptionner/$', DossierReceptionView, name='dossier_receptionne'),
                       )
