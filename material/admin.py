from django.contrib import admin

from .models import Material





@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("titulo", "materia", "subido_el")
    list_filter = ("materia",)
    