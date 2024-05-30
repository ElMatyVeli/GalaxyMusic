from django.urls import path
from .views import (
    mostrar_entrar,
mostrar_registro,
cerrar_sesion
)
urlpatterns = [path('entrar/',mostrar_entrar,name='mostrar_entrar'),
    path('registrar/',mostrar_registro, name='mostrar_registro'),
    path('salir/', cerrar_sesion, name='cerrar_sesion'),
    ]