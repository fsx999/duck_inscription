"""
Django settings for duck_inscription project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

from import_settings import *
SITE_ID = 1
TARIF_MEDICAL = 5.10
TARIF_SECU = 213
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'deh*%fl_7p&+5^(ry7116z&^-)nzyi#_iaww__6^i7m#-%3bsl'

# SECURITY WARNING: don't run with debug turned on in production!

ROOT_URLCONF = 'test_duck_inscription.urls'

WSGI_APPLICATION = 'test_duck_inscription.wsgi.application'



LOGIN_URL = 'auth_login'

from django.conf import settings
TEMPLATE_CONTEXT_PROCESSORS = settings.TEMPLATE_CONTEXT_PROCESSORS + ("django.core.context_processors.request",)

try:
    import local_settings
    from local_settings import *

except ImportError:
    local_settings = object
    print "pas de local settings"

try:
    if DEBUG:
        DEV_APPS = getattr(local_settings, 'DEV_APPS', ())
        INSTALLED_APPS += DEV_APPS
        MIDDLEWARE_CLASSES = ('debug_toolbar.middleware.DebugToolbarMiddleware',) +\
                              MIDDLEWARE_CLASSES + ('devserver.middleware.DevServerMiddleware',)
    INSTALLED_APPS = getattr(local_settings, 'FIRST_APPS', ()) + INSTALLED_APPS + getattr(local_settings,
                                                                                          'LAST_APPS', ())

except NameError:
    print "erreur"

if DEBUG:
    COMPRESS_ENABLED = False
else:
    COMPRESS_ENABLED = False

WKHTMLTOPDF_CMD = BASE_DIR+'/wkhtmltopdf'
