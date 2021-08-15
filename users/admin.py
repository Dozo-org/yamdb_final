from django.contrib import admin
from import_export.admin import ImportExportMixin

from .models import CustomUser


class CustomUserAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ("email", "username", "role", "confirmation_code")


admin.site.register(CustomUser, CustomUserAdmin)
