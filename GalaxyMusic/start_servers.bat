@echo off

REM Iniciar json-server
start cmd /k "json-server --watch db.json --port 4000"

REM Iniciar servidor de Django
python manage.py runserver

REM Mantener la ventana abierta
pause
