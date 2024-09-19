from django.contrib import admin
from django.db import models


class DateMixinAdmin(admin.ModelAdmin):
    readonly_fields = ("created_at", "updated_at",)
