# coding=utf-8
"""
Django admin helpers.
"""

from django.contrib import admin, messages
from .models import SoftDeleteQuerySet


class NoDeleteAdmin(admin.ModelAdmin):
    """
    ModelAdmin that prevents deleting.
    """

    def has_delete_permission(self, request, obj=None):
        return False


def soft_delete_action(modeladmin, request, queryset):
    assert isinstance(queryset, SoftDeleteQuerySet)
    message = "Marked {0} objects as deleted"
    num_deleted = queryset.count()
    queryset.delete()
    if num_deleted == 1:
        message = "Marked {0} object as deleted"
    messages.info(request, message.format(num_deleted))

soft_delete_action.short_description = "Delete selected"
