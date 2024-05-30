from django.shortcuts import render, redirect, get_object_or_404
from .productos import productos 
from .forms import ProductoForm
from .models import Producto
from sweetify import success, warning
from .productosdestacados import productosdestacados
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test


def mostrar_principal(request):
    context =   {
        'titulo':'Zapatillas',
        'lista': productosdestacados,
    }
    return render(request,'principal.html',context)
from .models import Producto

def mostrar_productos(request):
    productos_bd = Producto.objects.all()
    context = {
        'titulo': 'Zapatillas',
        'productos_lista': productos,
        'productos_bd_lista': productos_bd,
    }
    return render(request, 'productos.html', context)

def mostrar_carrito(request):
    return render(request,'carrito.html')



@user_passes_test(lambda u: u.is_superuser)
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto agregado')
            return redirect('mostrar_productos')
    else:
        form = ProductoForm()
    return render(request, 'gestiones.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    return redirect('mostrar_productos')

def guardar_cambios(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cambios guardados')
            return redirect('mostrar_productos')
    else:
        form = ProductoForm(instance=producto)
    
    context = {
        'form': form,
        'producto': producto,
    }
    
    return render(request, 'productos.html', context)



