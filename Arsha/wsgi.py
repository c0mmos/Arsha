"""
WSGI config for Arsha project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.core.management import call_command

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Arsha.settings.prod')

try:
    call_command('collectstatic', interactive=False, verbosity=0)
except:
    pass  # Don't fail if collectstatic fails

application = get_wsgi_application()
