import sys

import django_heroku
import environ
from django.utils.translation import gettext_lazy as _

BASE_DIR = environ.Path(__file__) - 3
PROJECT_DIR = BASE_DIR.path('project')
APPS_DIR = PROJECT_DIR.path('apps')

sys.path.insert(0, str(APPS_DIR))

# Load operating system environment variables and then prepare to use them
env = environ.Env()
#  patch for https://github.com/joke2k/django-environ/issues/119
env_file = str(BASE_DIR.path('.env'))
env.read_env(env_file)

SECRET_KEY = env('DJANGO_SECRET_KEY', default='CHANGEME!!!')
ALLOWED_HOSTS = env.list('DJANGO_ALLOWED_HOSTS', default='*')  # noqa
FORCE_SCRIPT_NAME = env.str('DJANGO_FORCE_SCRIPT_NAME', default=None)
USE_X_FORWARDED_HOST = env.bool('DJANGO_USE_X_FORWARDED_HOST', default=False)

DATABASES = {
    'default': env.db('DATABASE_URL')
}

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool('DJANGO_DEBUG', True)

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
    'rest_framework_social_oauth2',
    'oauth2_provider',
    'rest_framework',
    'corsheaders',
    'widget_tweaks',
    'mptt',
    'django_filters',
)

PROJECT_APPS = (
    'venta',
)

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = (
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'project.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'project.wsgi.application'

LANGUAGE_CODE = 'es'
TIME_ZONE = env.str('DJANGO_TIME_ZONE', default='America/Argentina/Catamarca')
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('es', _('Español')),
]

LOCALE_PATHS = [str(PROJECT_DIR.path('translations'))]

STATIC_URL = '/static/'

MEDIA_ROOT = str(PROJECT_DIR.path('media'))
MEDIA_URL = env.str('DJANGO_MEDIA_URL', default='/media/')

CORS_ORIGIN_ALLOW_ALL = True


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'rest_framework_json_api.exceptions.exception_handler',
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_json_api.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser'
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework_social_oauth2.authentication.SocialAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': ('rest_framework_json_api.renderers.JSONRenderer',),
    'DEFAULT_METADATA_CLASS': 'rest_framework_json_api.metadata.JSONAPIMetadata',
    'NON_FIELD_ERRORS_KEY': 'error_messages'
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(PROJECT_DIR.path('templates'))],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'social_django.context_processors.login_redirect',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ADMINS = [administrador.split(':') for administrador in env.list('DJANGO_ADMINS', default=[])]

ACTIVAR_HERRAMIENTAS_DEBUGGING = env.bool('ACTIVAR_HERRAMIENTAS_DEBUGGING', default=True)
if ACTIVAR_HERRAMIENTAS_DEBUGGING:
    INTERNAL_IPS = ['127.0.0.1']
    INSTALLED_APPS += ('debug_toolbar', 'django_extensions')
    MIDDLEWARE = ('debug_toolbar.middleware.DebugToolbarMiddleware',) + MIDDLEWARE
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] += ('rest_framework.renderers.BrowsableAPIRenderer',)
    REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] += ('rest_framework.authentication.SessionAuthentication',)

django_heroku.settings(locals())
