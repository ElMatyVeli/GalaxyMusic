from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import Producto, ItemCarrito
from .forms import FormularioRegistro, FormularioEntrar, FormularioPago
import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Inicialización de Firebase Admin SDK con la credencial descargada
cred = credentials.Certificate('tienda\galaxymusic.json')
firebase_admin.initialize_app(cred)

# Función para obtener productos desde Firestore y actualizar en la base de datos local
def obtener_productos_desde_firestore():
    # Inicializa Firestore
    db = firestore.client()

    # Obtiene la colección 'productos' (ajusta según tu colección en Firestore)
    productos_ref = db.collection('productos')

    # Consulta los documentos en la colección
    productos = []
    for doc in productos_ref.stream():
        producto_data = doc.to_dict()
        # Crea o actualiza los productos en tu base de datos local
        producto, created = Producto.objects.update_or_create(
            codigo=producto_data['codigo'],  # Ajusta según tu modelo de Producto
            defaults={
                'nombre': producto_data['nombre'],
                'descripcion': producto_data['descripcion'],
                'precio': producto_data['precio'],
                'foto_url': producto_data['foto_url'],
                'stock': producto_data['stock'],
            }
        )
        productos.append(producto)

    return productos

# Vista principal del sitio web con productos obtenidos desde Firestore
def index(request):
    # Obtener productos desde Firestore
    productos = obtener_productos_desde_firestore()
    return render(request, 'index.html', {'productos': productos})

# Vista para mostrar todos los productos obtenidos desde Firestore
def productos(request):
    # Obtener productos desde Firestore
    productos = obtener_productos_desde_firestore()
    return render(request, 'productos.html', {'productos': productos})

# Vista para mostrar el detalle de un producto específico
def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'detalle_producto.html', {'producto': producto})

# Vista para el carrito
def carrito(request):
    if request.user.is_authenticated:
        items_carrito = ItemCarrito.objects.filter(usuario=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        items_carrito = ItemCarrito.objects.filter(session_key=session_key)

    # Calcular el total para cada item en el carrito
    for item in items_carrito:
        item.total = item.producto.precio * item.cantidad

    context = {
        'items_carrito': items_carrito,
    }
    return render(request, 'carrito.html', context)


from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ItemCarrito, Producto
from .forms import FormularioPago
from datetime import datetime

def realizar_pago(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Debe estar autenticado para realizar el pago.')
        return redirect('mostrar_ingresar')

    items_carrito = ItemCarrito.objects.filter(usuario=request.user)
    total = sum(item.producto.precio * item.cantidad for item in items_carrito)
    boleta = None

    if request.method == 'POST':
        formulario_pago = FormularioPago(request.POST)
        if formulario_pago.is_valid():
            items_para_boleta = list(items_carrito)

            boleta = {
                'usuario': request.user.username,
                'items': [{
                    'codigo': item.producto.codigo,
                    'producto': item.producto,
                    'cantidad': item.cantidad,
                    'descuento': 0  # Puedes agregar lógica para calcular descuentos si es necesario
                } for item in items_para_boleta],
                'total': total,
                'mensaje': 'Pago realizado exitosamente',
                'fecha_emision': datetime.now().strftime('%d/%m/%Y')
            }
            items_carrito.delete()
    else:
        formulario_pago = FormularioPago()

    contexto = {
        'formulario_pago': formulario_pago,
        'boleta': boleta,
        'items_carrito': items_carrito if not boleta else boleta['items'],
        'total': total
    }
    return render(request, 'pago.html', contexto)


def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.user.is_authenticated:
        item_carrito, created = ItemCarrito.objects.get_or_create(usuario=request.user, producto=producto)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        item_carrito, created = ItemCarrito.objects.get_or_create(session_key=session_key, producto=producto)
    if not created:
        item_carrito.cantidad += 1
        item_carrito.save()
    return redirect('carrito')

def eliminar_del_carrito(request, item_id):
    if request.user.is_authenticated:
        item_carrito = get_object_or_404(ItemCarrito, id=item_id, usuario=request.user)
    else:
        session_key = request.session.session_key
        item_carrito = get_object_or_404(ItemCarrito, id=item_id, session_key=session_key)
    item_carrito.delete()
    return redirect('carrito')

def actualizar_cantidad(request, item_id):
    if request.user.is_authenticated:
        item_carrito = get_object_or_404(ItemCarrito, id=item_id, usuario=request.user)
    else:
        session_key = request.session.session_key
        item_carrito = get_object_or_404(ItemCarrito, id=item_id, session_key=session_key)
    if request.method == 'POST':
        cantidad = request.POST.get('cantidad')
        if cantidad:
            item_carrito.cantidad = int(cantidad)
            item_carrito.save()
    return redirect('carrito')

# LOGIN
@csrf_exempt
def mostrar_ingresar(request):
    if request.method == 'GET':
        formulario = FormularioEntrar()
        contexto = {'titulo': 'Ingresar', 'formulario': formulario}
        return render(request, 'ingresar.html', contexto)
    elif request.method == 'POST':
        formulario = FormularioEntrar(data=request.POST)
        if formulario.is_valid():
            usuario = formulario.get_user()
            login(request, usuario)
            return redirect('index')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos')
        contexto = {'titulo': 'Ingresar', 'formulario': formulario}
        return render(request, 'ingresar.html', contexto)

@csrf_exempt
def mostrar_registro(request):
    if request.method == 'POST':
        # Verificar si los datos son JSON
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            formulario = FormularioRegistro(data)
        else:
            formulario = FormularioRegistro(request.POST)
        # Validar el formulario
        if formulario.is_valid():
            nuevo_usuario = formulario.save()
            login(request, nuevo_usuario)
            if request.content_type == 'application/json':
                return JsonResponse({'mensaje': 'Registro exitoso', 'usuario': nuevo_usuario.username})
            else:
                messages.success(request, f'Bienvenido {nuevo_usuario.username}')
                return redirect('index')
        else:
            if request.content_type == 'application/json':
                return JsonResponse({'errors': formulario.errors}, status=400)
            else:
                messages.warning(request, 'Por favor, complete los campos correctamente.')
                contexto = {'titulo': 'Regístrate', 'formulario': formulario}
                return render(request, 'registro.html', contexto)
    else:
        formulario = FormularioRegistro()
        contexto = {'titulo': 'Regístrate', 'formulario': formulario}
        return render(request, 'registro.html', contexto)

def cerrar_sesion(request):
    logout(request)
    return redirect('index')
