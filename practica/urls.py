from django.urls import path
from . import views

app_name = "practica"

urlpatterns = [
    path("", views.lista, name="lista"),
    path("<int:pk>/", views.ensayo, name="ensayo"),
]