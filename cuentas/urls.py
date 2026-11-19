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

    # Menú principal
    path("inicio/", views.inicio, name="inicio"),
    path("materiales/", RedirectView.as_view(pattern_name="material:lista"), name="materiales"),
    path("fechas/", views.fechas, name="fechas"),
    path("creditos/", views.creditos, name="creditos"),

    # API JSON del calendario interactivo
    path("fechas/api/eventos/", views.api_calendario_eventos, name="api_calendario_eventos"),
    path("fechas/api/notas/", views.api_calendario_guardar_nota, name="api_calendario_guardar_nota"),
    path("fechas/api/notas/<int:pk>/eliminar/", views.api_calendario_eliminar_nota, name="api_calendario_eliminar_nota"),

    # Cuenta
    path("perfil/", views.perfil, name="perfil"),
    path("configuracion/", views.CambiarClaveView.as_view(), name="configuracion"),
]
