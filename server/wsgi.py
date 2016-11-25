"""
PRAG server
WSGI config.
"""
import os
import logging
import prag
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
application = get_wsgi_application()

logging.getLogger('app').info('PRAG server started, v%s', prag.version)
