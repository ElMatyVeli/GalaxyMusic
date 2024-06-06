from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
import sweetify
from sweetify import success, warning
from .forms import ProductoForm, FormularioRegistro, FormularioEntrar
from django.contrib.auth import authenticate, login, logout
from django.db import DatabaseError
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

# VISTAS DE PÁGINAS

# Vista principal del sitio web
def index(request):
    try:
        # Recupera todos los productos de la base de datos
        productos = Producto.objects.all()
        # Renderiza la plantilla 'index.html' con la lista de productos
        return render(request, 'index.html', {'productos': productos})
    except DatabaseError:
        # En caso de error de conexión a la base de datos, renderiza una plantilla de error
        return render(request, 'error.html', {'message': 'Error: No se pudo conectar a la base de datos. Por favor, inténtelo de nuevo más tarde.'})

# Vista para mostrar todos los productos
def productos(request):
    # Recupera todos los productos de la base de datos
    productos = Producto.objects.all()
    # Renderiza la plantilla 'productos.html' con la lista de productos
    return render(request, 'Producto/productos.html', {'productos': productos})

# Vista para mostrar el detalle de un producto específico
def detalle_producto(request, producto_id):
    # Recupera un producto específico o lanza un error 404 si no se encuentra
    producto = get_object_or_404(Producto, pk=producto_id)
    # Renderiza la plantilla 'detalle_producto.html' con el producto específico
    return render(request, 'Producto/detalle_producto.html', {'producto': producto})

# FUNCIONES PARA CREAR Y ELIMINAR PRODUCTOS

# Vista para crear un nuevo producto
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            # Guarda el nuevo producto en la base de datos
            form.save()
            # Redirige al usuario al índice después de crear exitosamente un nuevo producto
            return redirect('index')
    else:
        form = ProductoForm()
    # Renderiza la plantilla 'crear_producto.html' con el formulario de creación de producto
    return render(request, 'Producto/crear_producto.html', {'form': form})

# Vista para eliminar un producto existente
def eliminar_producto(request, pk):
    # Recupera un producto específico o lanza un error 404 si no se encuentra
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        # Elimina el producto de la base de datos
        producto.delete()
        # Redirige a la página de productos después de eliminar
        return redirect('productos')

# LOGIN

# Vista para mostrar y manejar el formulario de inicio de sesión

@csrf_exempt
def mostrar_ingresar(request):
    if request.method == 'GET':
        formulario = FormularioEntrar()
        contexto = {'titulo': 'Bienvenido', 'formulario': formulario}
        return render(request, 'Login/ingresar.html', contexto)
    
    elif request.method == 'POST':
        if request.headers.get('Content-Type') == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST

        formulario = FormularioEntrar(data=data)
        if formulario.is_valid():
            username = formulario.cleaned_data['usuario']
            password = formulario.cleaned_data['contrasenia_usuario']
            usuario = authenticate(username=username, password=password)
            if usuario is not None:
                login(request, usuario)
                if request.headers.get('Content-Type') == 'application/json':
                    return JsonResponse({'usuario': usuario.username, 'contrasenia_usuario': password})
                else:
                    sweetify.success(request, f'Bienvenido {usuario.username}')
                    return redirect('index')
            else:
                if request.headers.get('Content-Type') == 'application/json':
                    return JsonResponse({'error': 'Usuario y/o contraseña incorrectos'}, status=400)
                else:
                    sweetify.warning(request, 'Usuario y/o contraseña incorrectos')
                    contexto = {'titulo': 'Bienvenido', 'formulario': formulario}
                    return render(request, 'Login/ingresar.html', contexto)
        else:
            if request.headers.get('Content-Type') == 'application/json':
                return JsonResponse({'errors': formulario.errors}, status=400)
            else:
                sweetify.warning(request, 'Por favor, complete los campos correctamente.')
                contexto = {'titulo': 'Bienvenido', 'formulario': formulario}
                return render(request, 'Login/ingresar.html', contexto)
    else:
        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({'error': 'Método HTTP no permitido'}, status=405)
        else:
            return render(request, 'Login/ingresar.html', {'titulo': 'Bienvenido', 'formulario': FormularioEntrar()})
# Vista para mostrar y manejar el formulario de registro de usuarios
def mostrar_registro(request):
    if request.method == 'GET':
        formulario = FormularioRegistro()
        contexto = {'formulario': formulario}
        # Renderiza la plantilla 'registro.html' con el formulario de registro
        return render(request, 'Login/registro.html', contexto)
    elif request.method == 'POST':
        formulario_usuario = FormularioRegistro(request.POST)
        if formulario_usuario.is_valid():
            # Guarda el nuevo usuario en la base de datos
            formulario_usuario.save()
            success(request, 'Bienvenido, gracias por registrarte')
            # Redirige al usuario a la página de inicio de sesión después de registrarse
            return redirect('mostrar_ingresar')
        else:
            for field, errors in formulario_usuario.errors.items():
                for error in errors:
                    messages.error(request, f"{formulario_usuario.fields[field].label}: {error}")
            warning(request, 'Por favor, completa los campos correctamente.')
            contexto = {'formulario': formulario_usuario}
            # Renderiza nuevamente la plantilla 'registro.html' si el formulario no es válido
            return render(request, 'Login/registro.html', contexto)
# Vista para cerrar sesión del usuario
def cerrar_sesion(request):
    if request.user.is_authenticated:
        # Cierra sesión del usuario
        logout(request)
        success(request, 'Hasta pronto :)')
    # Redirige al usuario a la página principal después de cerrar sesión
    return redirect('index')
