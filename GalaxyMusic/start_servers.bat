@echo off

REM Comando para detener el proceso que usa el puerto 4000 (json-server)
for /f "tokens=5" %%a in ('netstat -aon ^| find ":4000" ^| find "LISTENING"') do taskkill /f /pid %%a

REM Comando para detener el proceso que usa el puerto 8000 (Django)
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8000" ^| find "LISTENING"') do taskkill /f /pid %%a

REM Ejecutar migraciones de Django
cmd /c "python manage.py migrate"
if errorlevel 1 (
    echo Error al ejecutar las migraciones de Django. Saliendo...
    exit /b 1
)

REM Iniciar json-server en segundo plano
start /B cmd /c "json-server --watch db.json --port 4000"

REM Esperar un momento para que json-server se inicie completamente
timeout /t 5

REM Iniciar el servidor de Django en segundo plano
start /B cmd /c "python manage.py runserver"

REM Mantener la ventana abierta hasta que se cierre cualquiera de los servidores
pause