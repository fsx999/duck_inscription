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
(r'^forum/', include('djangobb_forum.urls', namespace='djangobb')),
                      )
from wiki.urls import get_pattern as get_wiki_pattern
from django_notify.urls import get_pattern as get_nyt_pattern
urlpatterns += patterns('',
    (r'^notifications/', get_nyt_pattern()),
    (r'^wiki/', get_wiki_pattern())
)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += patterns('', url(r'^__debug__/', include(debug_toolbar.urls)), )
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns('',
        (r'^static_tel/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),
)


