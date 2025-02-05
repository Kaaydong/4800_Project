"""
WSGI config for company_site project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os, sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append(BASE_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'company_site.settings'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'company_site.settings')

application = get_wsgi_application()
