from django.conf import settings
from django.db import models


class NotaCalendario(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notas_calendario",
    )
    fecha = models.DateField(db_index=True)
    titulo = models.CharField(max_length=120)
    contenido = models.TextField(blank=True)
    creado_el = models.DateTimeField(auto_now_add=True)
    actualizado_el = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["fecha", "creado_el"]

    def __str__(self):
        return f"{self.fecha} - {self.titulo} ({self.usuario})"
