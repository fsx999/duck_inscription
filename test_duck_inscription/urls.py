import autocomplete_light
autocomplete_light.autodiscover()
from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from duck_inscription.forms.enregistrement_forms import LoginIED

from duck_inscription.views.enregistrement_views import UserView, EmailView

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    (r'^$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html',
                                                'authentication_form': LoginIED}),
    url(r'^admin/', include(admin.site.urls)),
    (r'^compte/', include('duck_inscription.urls.enregistrement_urls')),
    (r'^individu/', include('duck_inscription.urls.individu_urls')),
    (r'^voeu/', include('duck_inscription.urls.wish_urls')),
    url(r'^test_user/$', UserView.as_view(), name='test_user'),
    url(r'^test_email/$', EmailView.as_view(), name='test_email'),
)
urlpatterns += patterns('',
    url(r'^captcha/', include('captcha.urls')),
)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
    urlpatterns += staticfiles_urlpatterns()

GRAPPELLI_SWITCH_USER = True
