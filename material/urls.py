from django.urls import path
from . import views

app_name = "material"

urlpatterns = [
    path("", views.lista, name="lista"),
    path("<int:pk>/descargar/", views.descargar, name="descargar"),
]