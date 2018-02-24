# Django settings for testproject project.

import django

DEBUG = True
DEBUG_PROPAGATE_EXCEPTIONS = True

ADMINS = ()
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}


TIME_ZONE = 'Europe/Riga'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
MEDIA_ROOT = ''
MEDIA_URL = ''
SECRET_KEY = 'vaO4Y<g#YRWG8;Md8noiLp>.w(w~q_b=|1`?9<x>0KxA%UB!63'

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]

if django.VERSION < (1, 10):
    MIDDLEWARE_CLASSES = MIDDLEWARE + [
        'django.contrib.auth.middleware.AuthenticationMiddleware',
    ]
else:
    MIDDLEWARE += [
        'django.middleware.security.SecurityMiddleware',
    ]

ROOT_URLCONF = 'suit.tests.urls'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',

    'suit',
    'suit.tests.templatetags',
    'django.contrib.admin',
)

STATIC_URL = '/static/'

try:
    from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

    TEMPLATE_DEBUG = DEBUG

    TEMPLATE_LOADERS = (
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )

    TEMPLATE_DIRS = ()

    TEMPLATE_CONTEXT_PROCESSORS = list(TCP) + [
        'django.core.context_processors.request',
    ]
except ImportError:  # Django 1.9+
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

SUIT_CONFIG = {}
TEST_RUNNER = 'suit.tests.SuitTestRunner'
