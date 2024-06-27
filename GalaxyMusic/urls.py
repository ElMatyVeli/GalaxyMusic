from django.contrib import admin
from django.urls import path
from tienda import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('agregar-al-carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('eliminar-del-carrito/<int:item_id>/', views.eliminar_del_carrito, name='eliminar_del_carrito'),
    path('actualizar-cantidad/<int:item_id>/', views.actualizar_cantidad, name='actualizar_cantidad'),
    path('realizar_pago/', views.realizar_pago, name='realizar_pago'),
    path('productos/', views.productos, name='productos'),
    path('carrito/', views.carrito, name='carrito'),
    path('ingresar/', views.mostrar_ingresar, name='mostrar_ingresar'),
    path('registrar/', views.mostrar_registro, name='mostrar_registro'),
    path('salir/', views.cerrar_sesion, name='cerrar_sesion'),
]
