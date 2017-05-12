from django.db import models
from django.utils.timezone import now


class SoftDeleteQuerySet(models.QuerySet):
    """Maps :meth:`delete` to a soft delete."""
    def delete(self):
        self.filter(is_deleted=False).update(deleted_at=now(), is_deleted=True)


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        return SoftDeleteQuerySet(model=self.model, using=self._db, hints=self._hints)

    def active(self, **kwargs):
        return self.get_queryset().filter(is_deleted=False, **kwargs)

    def deleted(self, **kwargs):
        return self.get_queryset().filter(is_deleted=True, **kwargs)
