from django.contrib import admin
from import_export.admin import ImportExportMixin

from .models import Comment, Review


@admin.register(Review)
class ReviewAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('pk', 'title', 'text', 'author', 'pub_date')
    search_fields = ('text', )
    list_filter = ('pub_date', )
    empty_value_display = '--пусто--'


@admin.register(Comment)
class CommentAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('review', 'text', 'author', 'pub_date')
    list_filter = ('pub_date', )
    search_fields = ('text', )
