from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
import sweetify
from sweetify import success,warning
from .forms import ProductoForm, FormularioRegistro, FormularioEntrar
from django.contrib.auth import authenticate, login, logout
from django.db import DatabaseError

# VISTA DE PAGINAS

def index(request):
    try:
        productos = Producto.objects.all()
        return render(request, 'index.html', {'productos': productos})
    except DatabaseError:
        # Redirigir a una página de error específica o renderizar una plantilla con un mensaje de error
        return render(request, 'error.html', {'message': 'Error: No se pudo conectar a la base de datos. Por favor, inténtelo de nuevo más tarde.'})

def productos(request):
    productos = Producto.objects.all()
    return render(request, 'Producto/productos.html', {'productos': productos})

def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    return render(request, 'Producto/detalle_producto.html', {'producto': producto})

# FUNCIONES CREAR ELIMINAR

def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirige al usuario al index después de crear exitosamente un nuevo producto
    else:
        form = ProductoForm()
    return render(request, 'Producto/crear_producto.html', {'form': form})

def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        # Redirige a la página de productos después de eliminar
        return redirect('productos')

# LOGIN

def mostrar_ingresar(request):
    if request.method == 'GET':
        formulario = FormularioEntrar()
        contexto = {'titulo': 'Bienvenido', 'formulario': formulario}
        return render(request, 'Login/ingresar.html', contexto)
    elif request.method == 'POST':
        formulario = FormularioEntrar(data=request.POST)
        if formulario.is_valid():
            username = formulario.cleaned_data['usuario']
            password = formulario.cleaned_data['contrasenia_usuario']
            usuario = authenticate(username=username, password=password)
            if usuario is not None:
                login(request, usuario)
                success(request, f'Bienvenido {usuario.username}')
                return redirect('index')
        warning(request, 'Usuario y/o contraseña incorrectos')
        contexto = {'titulo': 'Bienvenido', 'formulario': formulario}
        return render(request, 'Login/ingresar.html', contexto)

def mostrar_registro(request):
    if request.method == 'GET':
        formulario = FormularioRegistro()
        contexto = {'formulario': formulario}
        return render(request, 'Login/registro.html', contexto)
    elif request.method == 'POST':
        formulario_usuario = FormularioRegistro(request.POST)
        if formulario_usuario.is_valid():
            formulario_usuario.save()
            success(request, 'Bienvenido, gracias por registrarte')
            return redirect('mostrar_ingresar')
        else:
            warning(request, 'Por favor, completa los campos correctamente.')
            contexto = {'formulario': formulario_usuario}
            return render(request, 'Login/registro.html', contexto)


def cerrar_sesion(request):
    if request.user.is_authenticated:
        logout(request)
        success(request, 'Hasta pronto :)')
    return redirect('index')
