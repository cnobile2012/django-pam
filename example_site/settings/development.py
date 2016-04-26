from .base import *


DEBUG = True

TEMPLATES[0]['OPTIONS']['debug'] = DEBUG


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.abspath(os.path.join(
            BASE_DIR, '..', 'data', 'db.sqlite3')),
        }
    }

# Add to the MIDDLEWARE_CLASSES here.
MIDDLEWARE_CLASSES.append('debug_toolbar.middleware.DebugToolbarMiddleware')

# Add to the INSTALLED_APPS here.
INSTALLED_APPS.append('debug_toolbar')
INSTALLED_APPS.append('django_nose')

# Django Debug Toolbar
INTERNAL_IPS = ('127.0.0.1',)

# Use nose to run all tests
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

NOSE_ARGS = [
    '--with-coverage',
    '--cover-package=django_pam',
    '--cover-erase',
    ]

# Setup Logging
LOG_ENV = 'development'
EXAMPLES_LOG_FILE = '{}/{}-examples.log'.format(LOG_DIR, LOG_ENV)
DJANGO_PAM_LOG_FILE = '{}/{}-django-pam.log'.format(LOG_DIR, LOG_ENV)

LOGGING.get('handlers', {}).get(
    'examples_file', {})['filename'] = EXAMPLES_LOG_FILE
LOGGING.get('handlers', {}).get(
    'django_pam_file', {})['filename'] = DJANGO_PAM_LOG_FILE

LOGGING.get('loggers', {}).get('django.request', {})['level'] = 'DEBUG'
LOGGING.get('loggers', {}).get('examples', {})['level'] = 'DEBUG'
LOGGING.get('loggers', {}).get('django_pam', {})['level'] = 'DEBUG'
