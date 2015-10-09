# -*- coding: utf-8 -*-
from registration.backends.default.views import RegistrationView

from duck_inscription.forms import PasswordRest, LoginIED, EmailRegistrationForm

__author__ = 'paul'

from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^login/$',
        'django.contrib.auth.views.login', {'template_name': 'registration/login.html',
                                            'authentication_form': LoginIED}, name="auth_login"),

    url(r'^password/reset/$', 'django.contrib.auth.views.password_reset', {'password_reset_form': PasswordRest},
        name='auth_password_reset'),
    url(r'^register/$',
        RegistrationView.as_view(form_class=EmailRegistrationForm),
        name='registration_register'),
    url('^password_reset_done', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    (r'', include('registration.backends.default.urls')),
)
