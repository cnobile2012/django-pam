from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.abspath(os.path.join(
            BASE_DIR, '..', 'data', 'db.sqlite3')),
        }
    }


ALLOWED_HOSTS = [
    '127.0.0.1'
    ]

# email settings
EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_REPLY_TO = 'donotreply@'

# Logging
LOG_ENV = 'travis'
EXAMPLES_LOG_FILE = '{}/{}-examples.log'.format(LOG_DIR, LOG_ENV)
DJANGO_PAM_LOG_FILE = '{}/{}-django-pam.log'.format(LOG_DIR, LOG_ENV)

LOGGING.get('handlers', {}).get(
    'examples_file', {})['filename'] = EXAMPLES_LOG_FILE
LOGGING.get('handlers', {}).get(
    'django_pam_file', {})['filename'] = DJANGO_PAM_LOG_FILE

LOGGING.get('loggers', {}).get('django.request', {})['level'] = 'DEBUG'
LOGGING.get('loggers', {}).get('examples', {})['level'] = 'DEBUG'
LOGGING.get('loggers', {}).get('django_pam', {})['level'] = 'DEBUG'
