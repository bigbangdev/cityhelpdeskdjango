# coding=utf-8
"""Defines generalized permissions for use by API components."""

from rest_framework import permissions
from rest_framework.permissions import BasePermission


class ReadOnlyOrIsAdmin (BasePermission):
    """
    Allow access to admins or the user themselves
    """

    def _check_permission (self, request): #pylint: disable=R0201
        """Base permission check that allows “safe” requests and restricts
        “unsafe” requests to staff users."""
        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user
        if (user and user.is_authenticated() and user.is_active and user.is_staff):
            return True
        return False

    def has_permission(self, request, view):
        return self._check_permission(request)

    def has_object_permission(self, request, view, obj):
        return self._check_permission(request)
