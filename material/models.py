from django.db import models
from django.core.validators import FileExtensionValidator




class Material(models.Model):
    MATERIAS = [
        ("m1", "Matemática M1"),
        ("m2", "Matemática M2"),
        ("lectora", "Comprensión Lectora"),
        ("historia", "Historia y Cs. Sociales"),
        ("ciencias", "Ciencias"),
    ]
    titulo = models.CharField(max_length=150)
    descripcion = models.CharField(max_length=250, blank= True)
    materia = models.CharField(max_length=20, choices=MATERIAS)
    archivo = models.FileField(
        upload_to="material/",
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
    )
    subido_el = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ["-subido_el"]
    
    def __str__(self):
        return self.titulo