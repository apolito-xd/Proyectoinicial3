from django.contrib import admin

from django.contrib import admin
from .models import Ensayo, Pregunta, Resultado


class PreguntaInline(admin.TabularInline):
    model = Pregunta
    extra = 1


@admin.register(Ensayo)
class EnsayoAdmin(admin.ModelAdmin):
    list_display = ("titulo", "materia")
    inlines = [PreguntaInline]


admin.site.register(Resultado)
