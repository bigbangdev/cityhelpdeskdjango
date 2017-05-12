# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.db.models import Q

from dal import autocomplete

from .models import Profile
