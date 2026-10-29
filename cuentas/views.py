from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from .forms import FormularioIngreso, FormularioRegistro


class IngresarView(LoginView):
    """Inicio de sesión. Al terminar, envía al menú principal (LOGIN_REDIRECT_URL)."""
    template_name = "cuentas/login.html"
    authentication_form = FormularioIngreso
    redirect_authenticated_user = True


def registro(request):
    if request.user.is_authenticated:
        return redirect("cuentas:menu")

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
    """Confirmación de cuenta creada, con enlace para iniciar sesión."""
    username = request.session.get("usuario_creado")
    if not username:
        return redirect("cuentas:registro")
    return render(request, "cuentas/registro_exitoso.html", {"username": username})


@login_required
def menu(request):
    """Prototipo del menú principal."""
    return render(request, "cuentas/menu.html")
