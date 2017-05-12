# coding=utf-8
from __future__ import absolute_import
import logging
try:
    # Python 3
    from urllib.parse import urlparse
except ImportError:
    # Python 2
    from urlparse import urlparse
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
logger = logging.getLogger(__name__)

try:
    import redis
except ImportError:
    raise ImproperlyConfigured("Redis not installed. Try `pip install redis`")

url = getattr(settings, "REDIS_URL", None)
options = getattr(settings, "REDIS_OPTIONS", {})
if not url:
    raise ImproperlyConfigured("Redis url is not set and required.")
