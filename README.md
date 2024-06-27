# GalaxyMusic APP

Este repositorio contiene la aplicación GalaxyMusic, desarrollada como parte del proyecto de integración de plataformas.

## Requisitos

- Python 3.12

## Instalación y Configuración

1. Clona este repositorio:

git clone https://github.com/ElMatyVeli/GalaxyMusic.git
cd GalaxyMusic

2. Crea y activa un entorno virtual:

py -m venv entorno
cd entorno
Scripts\activate.bat # Windows

ó

source bin/activate # Mac/Linux
cd ..

3. Instala las dependencias:

pip install -r requeriments.txt

4. Crea archivos de migración

py manage.py makemigrations

5. Ejecuta las migraciones:

python manage.py migrate

6. Inicia el servidor de desarrollo:

python manage.py runserver

7. Accede a la aplicación en tu navegador web:

http://localhost:PUERTO/

## Notas adicionales

- Para cualquier problema o consulta, contacta al equipo de desarrollo.
Este texto te proporciona todos los pasos necesarios para instalar, configurar y ejecutar la aplicación GalaxyMusic desde el repositorio proporcionado.
