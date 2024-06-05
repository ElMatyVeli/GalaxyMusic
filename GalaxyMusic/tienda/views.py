from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from sweetify import success, warning
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
        contexto = {
            'titulo': 'Bienvenido',
            'formulario': FormularioEntrar()
        }
        return render(request, 'Login/ingresar.html', contexto)
    if request.method == 'POST':
        datos_usuario = FormularioEntrar(data=request.POST)
        es_valido = datos_usuario.is_valid()
        if es_valido:
            username = datos_usuario.cleaned_data['usuario']
            password = datos_usuario.cleaned_data['contrasenia_usuario']
            usuario = authenticate(username=username, password=password)
            if usuario is not None:
                login(request, usuario)
                success(request, f'Bienvenido {usuario.username}')
                return redirect('index')
        contexto = {
            'titulo': 'Bienvenido',
            'formulario': datos_usuario
        }
        warning(request, 'Usuario y contraseña incorrectos')
        return render(request, 'Login/ingresar.html', contexto)

def mostrar_registro(request):
    # Usamos el nuevo formulario para mostrar los elementos con clases
    if request.method == 'GET':
        contexto = {
            'formulario': FormularioRegistro()
        }
        return render(request, 'Login/registro.html', contexto)
    elif request.method == 'POST':
        formulario_usuario = FormularioRegistro(request.POST)
        es_valido = formulario_usuario.is_valid()  # True Valido, False Invalido 
        if es_valido:
            formulario_usuario.save()
            success(request, 'Bienvenido, gracias por registrarte')
            return redirect('mostrar_entrar')
        contexto = {
            'formulario': formulario_usuario
        }
        warning(request, 'Ups... complete los campos correctamente')
        return render(request, 'Login/registro.html', contexto)

def cerrar_sesion(request):
    if request.user.is_authenticated:
        logout(request)
        success(request, 'Hasta pronto :)')
    return redirect('index')
