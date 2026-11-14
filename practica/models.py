from django.db import models

from django.conf import settings
from django.db import models


class Ensayo(models.Model):
    MATERIAS = [
        ("m1", "Matemática M1"),
        ("m2", "Matemática M2"),
        ("lectora", "Comprensión Lectora"),
        ("historia", "Historia y Cs. Sociales"),
        ("ciencias", "Ciencias"),
    ]

    titulo = models.CharField(max_length=150)
    materia = models.CharField(max_length=20, choices=MATERIAS)
    descripcion = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.titulo


class Pregunta(models.Model):
    ALTERNATIVAS = [("A", "A"), ("B", "B"), ("C", "C"), ("D", "D")]

    ensayo = models.ForeignKey(Ensayo, on_delete=models.CASCADE, related_name="preguntas")
    enunciado = models.TextField()
    alt_a = models.CharField(max_length=250)
    alt_b = models.CharField(max_length=250)
    alt_c = models.CharField(max_length=250)
    alt_d = models.CharField(max_length=250)
    correcta = models.CharField(max_length=1, choices=ALTERNATIVAS)
    explicacion = models.TextField(blank=True)

    def __str__(self):
        return self.enunciado[:60]


class Resultado(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ensayo = models.ForeignKey(Ensayo, on_delete=models.CASCADE)
    puntaje = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha"]
