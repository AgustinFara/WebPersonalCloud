# ==============================================================================
# IMPORTS
# ==============================================================================

import os

from django.core.wsgi import get_wsgi_application

# ==============================================================================
# Web Server Gateway Interface (WSGI) configuration for webpersonal project.
# It exposes the WSGI callable as a module-level variable named `application`
# ==============================================================================

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webpersonal.settings')
application = get_wsgi_application()
