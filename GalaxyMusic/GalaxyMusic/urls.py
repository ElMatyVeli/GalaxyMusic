"""
URL configuration for GalaxyMusic project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from tienda import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('crear-producto/', views.crear_producto, name='crear_producto'),
    path('productos/', views.productos, name='productos'),
    path('producto/<int:pk>/eliminar/', views.eliminar_producto, name='eliminar_producto'),
    path('ingresar/',views.mostrar_ingresar,name='mostrar_ingresar'),
    path('registrar/',views.mostrar_registro, name='mostrar_registro'),
    path('salir/', views.cerrar_sesion, name='cerrar_sesion'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



