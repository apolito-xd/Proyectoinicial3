Esta rama "unir-proyectos" se usara solo momentareamente para probar el login sin tener dos proyectos separados, cuando se haya testeado correctamente, se fusionara a main

<<<<<<< HEAD


Esta hecho el subido de material funcionalidad corazon, ahora, si quieren trabajar:
***git switch unir-proyectos
=======
requisito: Crear venv con django instalado
Con el vinculo del repositorio, clonenlo en su pc mediante la terminal (git clone "url")
si quieren trabajar:
git switch unir-proyectos
>>>>>>> 15402bd0f75d1857266c06ff45d93487db8e507e
git pull
git manage.py migrate***

<<<<<<< HEAD
Para subir material: "link/admin" los pdfs que suban son de prueba y no finales, obviamente no veran lo que subo yo ni yo vere lo que suban ustedes, son archivos locales

&#x20;

Para iniciar correctamente el servidor, deberan hacer los pasos de siempre e instalar el dns que sirve como blockeo a gmails no existentes

con el . venv activado van a la carpeta del branch y escriben en el cmd ***pip install dnspython***

despues antes de iniciar el server escriben

***$env:EMAIL\_HOST\_USER="anedblancog2@gmail.com"***

***$env:EMAIL\_HOST\_PASSWORD="rcojfyiqkwzkopkq"***

***python manage.py runserver***

esto permite que a partir de la aplicacion que registre con mi cuenta gmail se verifique la existencia de otras cuentas gmail

DEspues le dan a python manage.py runserver
=======
y para tener el server: 
git manage.py runserver

Para subir material: Crear un superuser con git createsuperuser,
luego entrar en el navegador: "url"/admin" los pdfs que suban son de prueba y no finales, obviamente no veran lo que subo yo ni yo vere lo que suban ustedes, son archivos locales

>>>>>>> 15402bd0f75d1857266c06ff45d93487db8e507e

