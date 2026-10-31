from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import FormularioIngreso, FormularioPerfil, FormularioRegistro


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
            # Se guarda el nombre para mostrarlo en la página de confirmación.
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
def materiales(request):
    return render(request, "cuentas/materiales.html")


@login_required
def practica(request):
    return render(request, "cuentas/practica.html")


@login_required
def fechas(request):
    return render(request, "cuentas/fechas.html")


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
