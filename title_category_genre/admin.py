from django.contrib import admin
from import_export.admin import ImportExportMixin

from .models import Category, Genre, Title


class CategoryAdmin(ImportExportMixin, admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", )}
    list_display = ("pk", "name", "slug")
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "-пусто-"


class GenreAdmin(ImportExportMixin, admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name", )}
    list_display = ("pk", "name", "slug")
    search_fields = ("name",)
    list_filter = ("name",)
    empty_value_display = "-пусто-"


class TitleAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ("pk", "name", "year", "description", "category")
    search_fields = ("name",)
    list_filter = ("year",)
    empty_value_display = "-пусто-"


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
