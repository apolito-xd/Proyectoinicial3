import os

from django.contrib.auth.decorators import login_required
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, render

from .models import Material


@login_required
def lista(request):
    materiales = Material.objects.all()
    materia = request.GET.get("materia")
    if materia:
        materiales = materiales.filter(materia=materia)
    return render(request, "cuentas/materiales.html", {
        "materiales": materiales,
        "materias": Material.MATERIAS,
        "materia_actual": materia,
        "actual": "materiales",
    })


@login_required
def descargar(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if not material.archivo:
        raise Http404("El archivo PDF no se encuentra disponible.")

    try:
        archivo_abierto = material.archivo.open("rb")
    except (FileNotFoundError, OSError):
        raise Http404("El archivo PDF no se encuentra disponible en el servidor.")

    return FileResponse(
        archivo_abierto,
        as_attachment=True,
        content_type="application/pdf",
        filename=os.path.basename(material.archivo.name),
    )
