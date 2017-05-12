# -*- coding: utf-8 -*-
import os
from uuid import uuid4

from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.deconstruct import deconstructible
from django.conf import settings


@deconstructible
class PathAndRename(object):

    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.path, filename)

path_and_rename_full = PathAndRename("images/proofs/")


class Category(models.Model):

    title = models.CharField(_("Título"), max_length=100)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _("Categories")
        ordering = ('title',)

    def __unicode__(self):
        return self.title


class Subcategory(models.Model):

    title = models.CharField(_("Título"), max_length=100)
    category = models.ForeignKey(Category, related_name="subcategories")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Subcategory")
        verbose_name_plural = _("Subcategories")
        ordering = ('title',)

    def __unicode__(self):
        return self.title


class Ticket(models.Model):

    OPEN_STATUS = 1
    REOPENED_STATUS = 2
    RESOLVED_STATUS = 3
    CLOSED_STATUS = 4
    DUPLICATE_STATUS = 5

    STATUS_CHOICES = (
        (OPEN_STATUS, _('Abierto')),
        (REOPENED_STATUS, _('Reabierto')),
        (RESOLVED_STATUS, _('Resuelto')),
        (CLOSED_STATUS, _('Cerrado')),
        (DUPLICATE_STATUS, _('Duplicado')),
    )

    PRIORITY_CHOICES = (
        (1, _("1. Crítico")),
        (2, _("2. Alto")),
        (3, _("3. Normal")),
        (4, _("4. Bajo")),
        (5, _("5. Muy Bajo")),
    )

    title = models.CharField(_("Título"), max_length=200)
    description = models.TextField(_("Descripción"), blank=True, null=True,
                                   help_text=_("Descripción de la solicitud"))
    address = models.TextField(_("Dirección"), blank=True, null=True,
                               help_text=_("Dirección postal de la solicitud"))
    subcategory = models.ForeignKey(Subcategory, related_name="tickets")
    submitter = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="tickets",
                                  verbose_name=_("Reportado por:"))
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='assignments',
                                    blank=True, null=True, verbose_name=_("Asignado a:"))
    status = models.IntegerField(_("Estado"), choices=STATUS_CHOICES, default=OPEN_STATUS)
    on_hold = models.BooleanField(_("Detenida"), blank=True, default=False,
                                  help_text=_('Opción para pausar.'))
    resolution = models.TextField(_("Solución"), blank=True, null=True,
                                  help_text=_("Descripción de solución realizada"))
    priority = models.IntegerField(_("Prioridad"), choices=PRIORITY_CHOICES,
                                   default=3, blank=3,
                                   help_text=_("1 = Prioridad más alta, 5 = Muy baja Prioridad"))
    point = models.PointField(_("Coordenadas de la solicitud".decode('utf-8')),)
    photo = models.ImageField(_("Imagen problema".decode('utf-8')), upload_to=path_and_rename_full,
                              blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Ticket")
        verbose_name_plural = _("Tickets")
        ordering = ('created',)
        get_latest_by = "created"

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.priority:
            self.priority = 3
        super(Ticket, self).save(*args, **kwargs)


class FollowUp(models.Model):
    """
    A FollowUp is a comment and/or change to a ticket. We keep a simple
    title, the comment entered by the user, and the new status of a ticket
    to enable easy flagging of details on the view-ticket page.
    The title is automatically generated at save-time, based on what action
    the user took.
    """

    ticket = models.ForeignKey(Ticket, verbose_name=_('Ticket'))
    created = models.DateTimeField(_("Fecha de Creación"), auto_now_add=True)
    title = models.CharField(_("Título"), max_length=200, blank=True, null=True,)
    comment = models.TextField(_("Comentario"), blank=True, null=True,)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
                             verbose_name=_('Usuario'),)
    new_status = models.IntegerField(_("Nuevo Estado"), choices=Ticket.STATUS_CHOICES,
                                     blank=True, null=True,
                                     help_text=_("Nuevo estado del Ticker si este cambió"))

    class Meta:
        ordering = ('date',)
        verbose_name = _('Seguimiento')
        verbose_name_plural = _('Seguimientos')

    def __unicode__(self):
        return u"%s" % self.title

    def save(self, *args, **kwargs):
        t = self.ticket
        if t.status is not self.new_status:
            t.status = self.new_status
            t.save()
        super(FollowUp, self).save(*args, **kwargs)
