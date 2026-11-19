from django.contrib import admin
from .models import NotaCalendario


@admin.register(NotaCalendario)
class NotaCalendarioAdmin(admin.ModelAdmin):
    list_display = ("fecha", "titulo", "usuario", "actualizado_el")
    list_filter = ("fecha",)
    search_fields = ("titulo", "contenido", "usuario__username")
