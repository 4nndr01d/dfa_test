from django.contrib import admin

from pictures.models import Picture


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'file',)
