#para poder iniciar secion con django

1. tienes que crear el entorno y lo instalas:
   python -m venv venv
   venv\Scripts\activate        (en windows)
   pip install -r requirements.txt (para que funcione)
2. se crea la base de datoss:
   python manage.py migrate
3. (Opcional) se puede o no crear un administrador:
   python manage.py createsuperuser
4. se inicia y se entra en  http://127.0.0.1:8000/
   python manage.py runserver

algunas rutas: /ingresar/ · /registro/ · /registro/listo/ (confirmación) · /menu/ (protegida) · /salir/ (POST) · /admin/

esto no esta hecho con ia:)
