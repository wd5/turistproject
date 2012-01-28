# -*- coding: utf-8 -*-

import os
PROJECT_DIR = os.path.abspath(os.path.dirname(__file__)) 

LOCALSERVER = True

ADMINS = (
    ('admin', 'admin@example.com'),
)

MEDIA_ROOT = os.path.join(PROJECT_DIR, '../media/')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(PROJECT_DIR, '../static/')
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'test.db',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# activation via email
AUTH_USER_EMAIL_UNIQUE = True
EMAIL_HOST = 'localhost'
#EMAIL_PORT = 1025
#EMAIL_HOST_USER = ''
#EMAIL_HOST_PASSWORD = ''
#EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'info@example.com'
