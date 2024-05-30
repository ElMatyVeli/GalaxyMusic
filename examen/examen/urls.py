"""
URL configuration for examen project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import (mostrar_principal, mostrar_productos, mostrar_carrito, agregar_producto, eliminar_producto,guardar_cambios
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', mostrar_principal, name='mostrar_principal'),
    path('productos/', mostrar_productos, name='mostrar_productos'),
    path('carrito/', mostrar_carrito, name='mostrar_carrito'),
    path('usuarios/', include('m_user.urls')),
    path('gestiones/', agregar_producto, name='agregar_producto'),
    path('eliminar_producto/<int:producto_id>/',eliminar_producto, name='eliminar_producto'),
    path('guardar_cambios/<int:producto_id>/', guardar_cambios, name='guardar_cambios'),
]