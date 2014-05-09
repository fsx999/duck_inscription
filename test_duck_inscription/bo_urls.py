from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
import xadmin
admin.autodiscover()
xadmin.autodiscover()

from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns('',
                        url(r'^inscription/', include('duck_inscription.urls.adminx_urls')),
                        url(r'admin/', include(admin.site.urls)),
                       url(r'^', include(xadmin.site.urls)),

                      )

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += patterns('', url(r'^__debug__/', include(debug_toolbar.urls)), )
    urlpatterns += staticfiles_urlpatterns()

