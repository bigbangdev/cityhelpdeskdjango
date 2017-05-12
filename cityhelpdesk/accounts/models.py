# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from uuid import uuid4

from django.db import models
from django.utils.deconstruct import deconstructible
from django.contrib.auth.models import User


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


path_and_rename_full = PathAndRename("profiles/pics/")


class Profile(models.Model):

    user = models.OneToOneField(User, related_name="profile")
    mobile = models.CharField("Teléfono Celular", max_length=50)
    photo = models.ImageField(upload_to=path_and_rename_full, null=True, blank=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    def __str__(self):
        return self.usuario.username

    # @models.permalink
    # def get_absolute_url(self):
    #     return ('')
