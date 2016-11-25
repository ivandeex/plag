"""
PRAG server.
Django settings.
"""

import os
import environ
from django import VERSION as django_version  # noqa


root = environ.Path(__file__) - 2
env = environ.Env()
if os.path.exists(root('.env')):
    env.read_env(root('.env'))


# Base settings

BASE_DIR = root()

DEBUG = env.bool('DEBUG', False)
DEBUG_SQL = env.bool('DEBUG_SQL', DEBUG)

TESTING = False
TEST_LIVESERVER = env.bool('TEST_LIVESERVER', False)

# ALLOWED_HOSTS is required by production mode
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost'])

# INTERNAL_IPS is required by debug toolbar and debug context processor
# Please ensure that your browser's host IP is in this list and your
# proxy server sends X-Real-IP and X-Forwarded-For headers to Django.
# Else, the `if debug` sections in templates will be disabled.
INTERNAL_IPS = env.list('INTERNAL_IPS', default=['127.0.0.1'])

SECRET_KEY = env.str('SECRET_KEY', 'please change me')

ROOT_URLCONF = 'server.urls'
WSGI_APPLICATION = 'server.wsgi.application'

DATABASES = {
    'default': env.db()
}


# Internationalization

USE_I18N = True
LOCALE_PATHS = []
LANGUAGE_CODE = 'en-us'
LANGUAGE_COOKIE_NAME = 'lang'

LANGUAGES = [
    ('en', u'English (US)'),
]

# Localization
USE_L10N = False

# Time zone
USE_TZ = True
TIME_ZONE = 'UTC'


# Applications

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',

    'whitenoise.runserver_nostatic',  # same as manage.py runserver --nostatic
    'django.contrib.staticfiles',     # for manage.py collectstatic
]


MIDDLEWARE = [
    'server.middleware.RealRemoteIPMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.locale.LocaleMiddleware',
    # 'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


DEBUG_EXT = env.bool('DEBUG_EXT', DEBUG)

if DEBUG_EXT:
    INSTALLED_APPS.append('django_extensions')

DEBUG_TOOLBAR_ENABLED = env.bool('DEBUG_TOOLBAR', True)

if DEBUG and DEBUG_TOOLBAR_ENABLED:
    INSTALLED_APPS += ['debug_toolbar']
    DEBUG_TOOLBAR_CONFIG = {'SHOW_COLLAPSED': True}

    # Use index=1 to insert *after* RealRemoteIPMiddleware
    MIDDLEWARE.insert(1, 'debug_toolbar.middleware.DebugToolbarMiddleware')


# Templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            root('templates')
        ],
        'APP_DIRS': False,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                # Cache all templates in memory, when in production mode:
                ('django.template.loaders.cached.Loader', [
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ]),
            ],
        },
    },
]

if DEBUG:
    # Activate app_directories loader and remove caching loader, when in debug mode:
    TEMPLATES[0]['APP_DIRS'] = True
    del TEMPLATES[0]['OPTIONS']['loaders']


# Caching and Sessions

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'app-locmem',
        'TIMEOUT': 60 if DEBUG else 300,
        'OPTIONS': {
            'MAX_ENTRIES': 100,
        },
    }
}

DEBUG_SESSIONS = env.bool('DEBUG_SESSIONS', False)
if DEBUG_SESSIONS:
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'


# Authentication

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(process)d] [%(levelname)s %(module)s] %(message)s',
        },
    },
    'handlers': {
        'debug_console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django.db': {
            'handlers': ['debug_console'],
            'level': 'DEBUG' if DEBUG_SQL else 'CRITICAL',
            'propagate': False,
        },
        'app': {
            'handlers': ['debug_console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
}


# Static files

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_URL = '/static/'
STATIC_ROOT = root('static')

STATICFILES_DIRS = [
    root('public')
]

NGINX_SENDFILE_ROOT = root('temp')
NGINX_SENDFILE_URL = env.str('NGINX_SENDFILE_URL', '')
