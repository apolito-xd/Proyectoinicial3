import datetime
import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET, require_POST

from .forms import FormularioIngreso, FormularioPerfil, FormularioRegistro
from .models import NotaCalendario

# Fechas oficiales fijadas por el desarrollador (no editables por los usuarios)
FECHAS_FIJAS_DESARROLLADOR = [
    {
        "id": "fija-paes-verano",
        "fecha": "2026-11-30",
        "titulo": "PAES Verano · 15:00 Hrs",
        "contenido": "Primera prueba PAES M2 (fecha oficial fijada por el desarrollador).",
        "bloqueada": True,
    },
]

MAX_NOTAS_POR_DIA = 20
MAX_LARGO_CONTENIDO = 1000


class IngresarView(LoginView):
    """inicio de secio, cuando termina te redirige al registro"""
    template_name = "cuentas/login.html"
    authentication_form = FormularioIngreso
    redirect_authenticated_user = True


def registro(request):
    if request.user.is_authenticated:
        return redirect("cuentas:inicio")

    if request.method == "POST":
        form = FormularioRegistro(request.POST)
        if form.is_valid():
            usuario = form.save()
            request.session["usuario_creado"] = usuario.username
            return redirect("cuentas:registro_exitoso")
    else:
        form = FormularioRegistro()

    return render(request, "cuentas/registro.html", {"form": form})


def registro_exitoso(request):
    """se confirma la creacion de la cuenta y tiene link para inicio de secion"""
    username = request.session.get("usuario_creado")
    if not username:
        return redirect("cuentas:registro")
    return render(request, "cuentas/registro_exitoso.html", {"username": username})


@login_required
def inicio(request):
    return render(request, "cuentas/inicio.html")


@login_required
def fechas(request):
    return render(request, "cuentas/fechas.html")


@login_required
@require_GET
def api_calendario_eventos(request):
    try:
        anio = int(request.GET.get("year", datetime.date.today().year))
    except (ValueError, TypeError):
        anio = datetime.date.today().year

    if not (1 <= anio <= 9999):
        anio = datetime.date.today().year

    fijas = [f for f in FECHAS_FIJAS_DESARROLLADOR if f["fecha"].startswith(f"{anio:04d}-")]
    notas_qs = NotaCalendario.objects.filter(usuario=request.user, fecha__year=anio)
    notas = [
        {
            "id": n.id,
            "fecha": n.fecha.isoformat(),
            "titulo": n.titulo,
            "contenido": n.contenido,
            "bloqueada": False,
        }
        for n in notas_qs
    ]
    return JsonResponse({"year": anio, "fijas": fijas, "notas": notas})


@login_required
@require_POST
def api_calendario_guardar_nota(request):
    try:
        datos = json.loads(request.body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return JsonResponse({"error": "Formato de datos inválido."}, status=400)

    if not isinstance(datos, dict):
        return JsonResponse({"error": "Formato de datos inválido."}, status=400)

    nota_id = datos.get("id")
    if isinstance(nota_id, str) and nota_id.startswith("fija-"):
        return JsonResponse({"error": "Las fechas oficiales no se pueden editar."}, status=403)

    if nota_id is not None and nota_id != "":
        try:
            nota_id = int(nota_id)
        except (ValueError, TypeError):
            return JsonResponse({"error": "Identificador de nota inválido."}, status=400)
    else:
        nota_id = None

    fecha_str = str(datos.get("fecha") or "").strip()
    titulo = str(datos.get("titulo") or "").strip()
    contenido = str(datos.get("contenido") or "").strip()

    if not titulo:
        return JsonResponse({"error": "Escribe un título para la nota."}, status=400)

    if len(contenido) > MAX_LARGO_CONTENIDO:
        return JsonResponse(
            {"error": f"La nota no puede superar los {MAX_LARGO_CONTENIDO} caracteres."},
            status=400,
        )

    try:
        fecha_obj = datetime.date.fromisoformat(fecha_str)
    except ValueError:
        return JsonResponse({"error": "Fecha inválida."}, status=400)

    if nota_id is not None:
        nota = get_object_or_404(NotaCalendario, pk=nota_id, usuario=request.user)
        nota.titulo = titulo[:120]
        nota.contenido = contenido
        nota.save(update_fields=["titulo", "contenido", "actualizado_el"])
    else:
        total_dia = NotaCalendario.objects.filter(usuario=request.user, fecha=fecha_obj).count()
        if total_dia >= MAX_NOTAS_POR_DIA:
            return JsonResponse(
                {"error": f"Alcanzaste el máximo de {MAX_NOTAS_POR_DIA} notas para este día."},
                status=400,
            )
        nota = NotaCalendario.objects.create(
            usuario=request.user,
            fecha=fecha_obj,
            titulo=titulo[:120],
            contenido=contenido,
        )

    return JsonResponse({
        "nota": {
            "id": nota.id,
            "fecha": nota.fecha.isoformat(),
            "titulo": nota.titulo,
            "contenido": nota.contenido,
            "bloqueada": False,
        }
    })


@login_required
@require_POST
def api_calendario_eliminar_nota(request, pk):
    nota = get_object_or_404(NotaCalendario, pk=pk, usuario=request.user)
    nota.delete()
    return JsonResponse({"ok": True})


@login_required
def creditos(request):
    return render(request, "cuentas/creditos.html")


@login_required
def perfil(request):
    """Ver y editar los datos de la cuenta."""
    if request.method == "POST":
        form = FormularioPerfil(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Tus datos se guardaron.")
            return redirect("cuentas:perfil")
    else:
        form = FormularioPerfil(instance=request.user)

    return render(request, "cuentas/perfil.html", {"form": form})


class CambiarClaveView(PasswordChangeView):
    """SE cambia la contraseña y la secion sigue abierta"""
    template_name = "cuentas/configuracion.html"
    success_url = reverse_lazy("cuentas:configuracion")

    def form_valid(self, form):
        messages.success(self.request, "Tu contraseña se cambió.")
        return super().form_valid(form)
