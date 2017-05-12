"""
WSGI config for cityhelpdesk project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from utility.annoying import get_str, fetch_env


env_file = get_str("ENV_FILE", os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../../.env")))
env = fetch_env(env_file)
os.environ.update(env)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cityhelpdesk.settings")

application = get_wsgi_application()
