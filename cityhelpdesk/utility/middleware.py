from django.conf import settings
from django.utils.cache import patch_vary_headers, patch_cache_control
from rest_framework import permissions


class CacheMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not settings.DEBUG and request.method in permissions.SAFE_METHODS and response.status_code == 200:
            patch_cache_control(response, private=True, max_age=604800)
            patch_vary_headers(response, ["Cookie", "Authorization"])
        return response
