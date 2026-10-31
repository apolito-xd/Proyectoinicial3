from django.contrib.auth.decorators import login_required
from django.http import FileResponse
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
def descargar(request,pk):
    material = get_object_or_404(Material, pk=pk)
    return FileResponse(
        material.archivo.open("rb"),
        as_attachment=True,
        filename=material.archivo.name.split("/")[-1],
    )