# Inicio de sesión con Django (versión sin humanizar)

1. Crear entorno e instalar:
   python -m venv venv
   venv\Scripts\activate        (Windows)   |   source venv/bin/activate  (Mac/Linux)
   pip install -r requirements.txt
2. Crear la base de datos:
   python manage.py migrate
3. (Opcional) Crear un administrador:
   python manage.py createsuperuser
4. Iniciar el servidor y abrir http://127.0.0.1:8000/
   python manage.py runserver

Rutas: /ingresar/ · /registro/ · /registro/listo/ · /inicio/ · /materiales/ · /practica/ ·
/fechas/ · /creditos/ · /perfil/ · /configuracion/ · /salir/ (POST) · /admin/
