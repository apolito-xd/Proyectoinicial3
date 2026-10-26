from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = "cuentas"

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="cuentas:menu"), name="inicio"),
    path("ingresar/", views.IngresarView.as_view(), name="login"),
    path("salir/", LogoutView.as_view(), name="logout"),
    path("registro/", views.registro, name="registro"),
    path("registro/listo/", views.registro_exitoso, name="registro_exitoso"),
    path("menu/", views.menu, name="menu"),
]
