from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    pass
