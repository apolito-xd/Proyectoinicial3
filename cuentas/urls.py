from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "cuentas"

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="cuentas:inicio"), name="raiz"),
    path("ingresar/", views.IngresarView.as_view(), name="login"),
    path("salir/", LogoutView.as_view(), name="logout"),
    path("registro/", views.registro, name="registro"),
    path("registro/listo/", views.registro_exitoso, name="registro_exitoso"),
    path("activar/<uidb64>/<token>/", views.activar, name="activar"),

    # Menú principal
    path("inicio/", views.inicio, name="inicio"),
    path("materiales/", views.materiales, name="materiales"),
    path("practica/", views.practica, name="practica"),
    path("fechas/", views.fechas, name="fechas"),
    path("creditos/", views.creditos, name="creditos"),

    # Cuenta
    path("perfil/", views.perfil, name="perfil"),
    path("configuracion/", views.CambiarClaveView.as_view(), name="configuracion"),
]
