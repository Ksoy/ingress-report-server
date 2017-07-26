#!/usr/bin/env python3
"""
WSGI config for ingress_report project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import site
import sys

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ingress_report.settings")
site.addsitedir('/home/fuckagents/ingress-report-server/venv/lib/python3.5/site-packages')
sys.path.append('/home/fuckagents/ingress-report-server')

application = get_wsgi_application()

