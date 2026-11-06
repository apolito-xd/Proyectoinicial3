import logging
from smtplib import SMTPException

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .forms import FormularioIngreso, FormularioPerfil, FormularioRegistro

User = get_user_model()
logger = logging.getLogger(__name__)


class IngresarView(LoginView):
    """inicio de secio, cuando termina te redirige al registro"""
    template_name = "cuentas/login.html"
    authentication_form = FormularioIngreso
    redirect_authenticated_user = True


def enviar_correo_activacion(request, usuario):
    """Manda al correo del usuario el enlace para activar su cuenta."""
    uid = urlsafe_base64_encode(force_bytes(usuario.pk))
    token = default_token_generator.make_token(usuario)
    enlace = request.build_absolute_uri(reverse("cuentas:activar", args=[uid, token]))
    mensaje = render_to_string("cuentas/correo_activacion.txt", {"usuario": usuario, "enlace": enlace})
    send_mail("Confirma tu cuenta en Preu-Fast", mensaje, None, [usuario.email])


def registro(request):
    if request.user.is_authenticated:
        return redirect("cuentas:inicio")

    if request.method == "POST":
        form = FormularioRegistro(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.is_active = False  # se activa al abrir el enlace del correo
            usuario.save()
            try:
                enviar_correo_activacion(request, usuario)
            except (SMTPException, OSError):
                logger.exception("No se pudo enviar el correo de activación")
                usuario.delete()
                form.add_error("email", "No pudimos enviar el correo de confirmación. Revisa la dirección e inténtalo de nuevo.")
            else:
                request.session["usuario_creado"] = usuario.username
                request.session["correo_creado"] = usuario.email
                return redirect("cuentas:registro_exitoso")
    else:
        form = FormularioRegistro()

    return render(request, "cuentas/registro.html", {"form": form})


def registro_exitoso(request):
    """se confirma la creacion de la cuenta y tiene link para inicio de secion"""
    username = request.session.get("usuario_creado")
    if not username:
        return redirect("cuentas:registro")
    contexto = {"username": username, "correo": request.session.get("correo_creado")}
    return render(request, "cuentas/registro_exitoso.html", contexto)


def activar(request, uidb64, token):
    """Abre el enlace del correo: si es válido, deja la cuenta activa."""
    try:
        usuario = User.objects.get(pk=urlsafe_base64_decode(uidb64).decode())
    except (ValueError, TypeError, OverflowError, User.DoesNotExist):
        usuario = None

    valido = usuario is not None and default_token_generator.check_token(usuario, token)
    if valido:
        usuario.is_active = True
        usuario.save()
    return render(request, "cuentas/activacion.html", {"valido": valido})


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
