"""
Django settings for duck_inscription project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'deh*%fl_7p&+5^(ry7116z&^-)nzyi#_iaww__6^i7m#-%3bsl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

STATIC_ROOT = os.path.join(BASE_DIR, '../static').replace('\\', '/')
MEDIA_ROOT = os.path.join(BASE_DIR, '../static_tel').replace('\\', '/')

# Application definition

INSTALLED_APPS = (
    'django_xworkflows.xworkflow_log',
    'duck_theme_ied',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'duck_inscription',
    'django_extensions',
    'django_apogee',
    'south',
    'registration',
    'captcha',
    'compressor',
    'floppyforms',
    'django_xworkflows',
    'autocomplete_light',
)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'test_duck_inscription.urls'

WSGI_APPLICATION = 'test_duck_inscription.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # 'django.template.loaders.eggs.Loader',


)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
    'compressor.finders.CompressorFinder',
)


SOUTH_DATABASE_ADAPTERS = {
    'default': 'south.db.postgresql_psycopg2',
    'oracle': 'south.db.sqlite3',
}
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Europe/Paris'

USE_I18N = True

USE_L10N = True

USE_TZ = False  # Important, toujours False


STATIC_URL = '/static/'

COMPRESS_OFFLINE = False

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates').replace('\\', '/'),
)

ACCOUNT_ACTIVATION_DAYS = 1

LOGIN_URL = 'auth_login'

from django.conf import settings
TEMPLATE_CONTEXT_PROCESSORS = settings.TEMPLATE_CONTEXT_PROCESSORS + ("django.core.context_processors.request",)

try:
    # import local_settings
    from local_settings import *
    if DEBUG:
        INSTALLED_APPS += DEV_APPS
        MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',) +\
                              MIDDLEWARE_CLASSES + ('devserver.middleware.DevServerMiddleware',)

except (ImportError, NameError):
    pass
if DEBUG:
    COMPRESS_ENABLED = False
else:
    COMPRESS_ENABLED = False
