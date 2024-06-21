@echo off

REM Iniciar json-server en segundo plano
start /B json-server --watch db.json --port 4000

REM Iniciar servidor de Django en segundo plano
start /B python manage.py runserver

REM Mantener la ventana abierta hasta que se cierren los servidores
pause
