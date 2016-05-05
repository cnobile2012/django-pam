#
# app.wsgi
#
# mod_wsgi hook file
#

import os, sys

SITE = "example_site"
SERVER_CONF = os.path.dirname(__file__)
BASE_SITE_PATH = os.path.abspath(os.path.join(SERVER_CONF, '..'))

# DO NOT EDIT BELOW THIS LINE
not sys.path.count(BASE_SITE_PATH) and sys.path.insert(0, BASE_SITE_PATH)

from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = '%s.settings' % SITE

application = get_wsgi_application()
