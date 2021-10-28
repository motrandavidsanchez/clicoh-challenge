from .base import *

SECRET_KEY = 'CHANGEME!!!'
DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

MEDIA_ROOT = str(PROJECT_DIR.path('test_media'))

OAUTH2_PROVIDER = {
    # this is the list of available scopes
    'SCOPES': ['read', 'write', 'groups']
}
