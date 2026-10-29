from django.contrib import admin
from django.urls import include, path
##este archivo es el que se encarga de enrutar las urls de la aplicacion principal
##en este caso la aplicacion principal es cuentas, por lo que se importa el archivo urls.py de la aplicacion cuentas
## y se incluye en el archivo urls.py del proyecto principal.
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("cuentas.urls")),
]
