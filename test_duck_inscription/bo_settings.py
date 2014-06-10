"""
Django settings for duck_inscription project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.core.urlresolvers import reverse_lazy
from import_settings import *


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'deh*%fl_7p&+5^(ry7116z&^-)nzyi#_iaww__6^i7m#-%3bsl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True


ROOT_URLCONF = 'test_duck_inscription.bo_urls'

WSGI_APPLICATION = 'test_duck_inscription.bo_wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/



LOGIN_URL = '/'

from django.conf import settings
TEMPLATE_CONTEXT_PROCESSORS = settings.TEMPLATE_CONTEXT_PROCESSORS + ("django.core.context_processors.request",)

try:
    import bo_local_settings
    from bo_local_settings import *

except ImportError:
    bo_local_settings = object
    print "pas de local settings"
SITE_ID = 2
try:
    if DEBUG:
        DEV_APPS = getattr(bo_local_settings, 'DEV_APPS', ())
        INSTALLED_APPS += DEV_APPS
        MIDDLEWARE_CLASSES = ('debug_toolbar.middleware.DebugToolbarMiddleware',) +\
                              MIDDLEWARE_CLASSES + ('devserver.middleware.DevServerMiddleware',)
    INSTALLED_APPS = getattr(bo_local_settings, 'FIRST_APPS', ()) + INSTALLED_APPS + getattr(bo_local_settings,
                                                                                          'LAST_APPS', ())

except NameError:
    print "erreur"

if DEBUG:
    COMPRESS_ENABLED = False
else:
    COMPRESS_ENABLED = False

WKHTMLTOPDF_CMD = BASE_DIR+'/wkhtmltopdf'

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.request",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "sekizai.context_processors.sekizai",
)
