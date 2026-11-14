from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import Ensayo, Resultado


@login_required
def lista(request):
    ensayos = Ensayo.objects.all()
    materia = request.GET.get("materia")
    if materia:
        ensayos = ensayos.filter(materia=materia)
    print("ENSAYOS:", ensayos.count(), "FILTRO:", materia)
    return render(request, "cuentas/practica.html", {
        "ensayos": ensayos,
        "materias": Ensayo.MATERIAS,
        "actual": "practica",
    })


@login_required
def ensayo(request, pk):
    ensayo = get_object_or_404(Ensayo, pk=pk)
    preguntas = list(ensayo.preguntas.all())

    # Armamos las alternativas de cada pregunta para usarlas en la plantilla
    for p in preguntas:
        p.opciones = [("A", p.alt_a), ("B", p.alt_b), ("C", p.alt_c), ("D", p.alt_d)]

    if request.method == "POST":
        puntaje = 0
        revision = []
        for p in preguntas:
            elegida = request.POST.get(f"p{p.pk}")
            acierto = elegida == p.correcta
            if acierto:
                puntaje += 1
            revision.append({"pregunta": p, "elegida": elegida, "acierto": acierto})

        Resultado.objects.create(
            usuario=request.user,
            ensayo=ensayo,
            puntaje=puntaje,
            total=len(preguntas),
        )
        return render(request, "practica/resultado.html", {
            "ensayo": ensayo,
            "revision": revision,
            "puntaje": puntaje,
            "total": len(preguntas),
            "actual": "practica",
        })

    return render(request, "practica/ensayo.html", {
        "ensayo": ensayo,
        "preguntas": preguntas,
        "actual": "practica",
    })


