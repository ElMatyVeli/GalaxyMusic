from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import Producto, ItemCarrito
from .forms import FormularioRegistro, FormularioEntrar, FormularioPago
import json
import os
from django.conf import settings
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
from decimal import Decimal
from django.db.models import Q
import logging
from django.core.mail import send_mail
 
# Inicialización de Firebase Admin SDK con la credencial descargada
cred_path = os.path.join(settings.BASE_DIR, 'tienda', 'galaxymusic-6c651-firebase-adminsdk-9ika2-641ef26708.json')
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)
 
# Configuración del logger
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
 
 
@csrf_exempt
@require_http_methods(["POST"])
def validacion_stock(request):
    try:
        data = json.loads(request.body)
        nombre_producto = data.get('nombre')
        cantidad_comprada = data.get('cantidad')
 
        if not nombre_producto or not cantidad_comprada:
            return JsonResponse({'error': 'Datos incompletos'}, status=400)
 
        db = firestore.client()
 
        producto_ref = db.collection('productos').where('nombre', '==', nombre_producto).limit(1).stream()
        for doc in producto_ref:
            producto_data = doc.to_dict()
            nuevo_stock = producto_data['stock'] - cantidad_comprada
            if nuevo_stock < 0:
                return JsonResponse({'error': 'Stock insuficiente'}, status=400)
 
            producto = Producto.objects.get(codigo=producto_data['codigo'])
            producto.stock = nuevo_stock
            producto.save()
 
            return JsonResponse({'mensaje': 'Stock suficiente'}, status=200)
 
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)
 
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
 
 
# Función para obtener productos desde Firestore y actualizar en la base de datos local
def obtener_productos_desde_firestore():
    db = firestore.client()
    productos_ref = db.collection('productos')
    productos = []
    for doc in productos_ref.stream():
        producto_data = doc.to_dict()
        producto, created = Producto.objects.update_or_create(
            codigo=producto_data['codigo'],
            defaults={
                'nombre': producto_data['nombre'],
                'descripcion': producto_data.get('descripcion', ''),  # Asegurando que la descripción sea opcional
                'precio': producto_data['precio'],
                'foto_url': producto_data['foto_url'],
                'stock': producto_data['stock'],
            }
        )
        productos.append(producto)
    return productos
 
 
# Vista principal del sitio web con productos obtenidos desde Firestore
def index(request):
    productos = obtener_productos_desde_firestore()
    return render(request, 'index.html', {'productos': productos})
 
 
# Vista para mostrar todos los productos obtenidos desde Firestore
def productos(request):
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
 
    for item in items_carrito:
        item.total = item.producto.precio * item.cantidad
 
    total_carrito = sum(item.total for item in items_carrito)
    total_con_descuento = total_carrito
    descuento = request.session.get('descuento', 0)
    total_con_descuento = total_carrito * (Decimal('1.0') - (Decimal(descuento) / Decimal('100.0')))
 
    context = {
        'items_carrito': items_carrito,
        'total_con_descuento': total_con_descuento,
        'total_carrito': total_carrito,
    }
    return render(request, 'carrito.html', context)
 
 
 
# Aplicar descuento al carrito
def aplicar_descuento(request):
    if request.method == 'POST':
        codigo_descuento = request.POST.get('codigo_descuento')
        if codigo_descuento == 'INVIERNO2024':
            request.session['descuento'] = 30
            messages.success(request, 'Descuento aplicado exitosamente.', extra_tags='descuento')
        else:
            request.session['descuento'] = 0
            messages.error(request, 'Código de descuento no válido.', extra_tags='descuento')
    return redirect('carrito')
 
def realizar_pago(request):
    boleta = {}
    if not request.user.is_authenticated:
        messages.error(request, 'Debe estar autenticado para realizar el pago.', extra_tags='autenticado')
        return redirect('mostrar_ingresar')
 
    items_carrito = ItemCarrito.objects.filter(usuario=request.user)
    for item in items_carrito:
        if item.cantidad > item.producto.stock:
            messages.error(request, f"No hay suficiente stock disponible para '{item.producto.nombre}'. Por favor, actualiza la cantidad en tu carrito.")
            return redirect('carrito')
 
    descuento = request.session.get('descuento', 0)
    total = sum(item.producto.precio * item.cantidad for item in items_carrito)
    total_con_descuento = total * (Decimal('1.0') - (Decimal(descuento) / Decimal('100.0')))
 
    if request.method == 'POST':
        formulario_pago = FormularioPago(request.POST)
        if formulario_pago.is_valid():
            items_para_boleta = list(items_carrito)
 
            boleta = {
                'usuario': request.user.username,
                'items': [{
                    'codigo': item.producto.codigo,
                    'producto': item.producto,
                    'cantidad': item.cantidad
                } for item in items_para_boleta],
                'total': total_con_descuento,
                'mensaje': 'Pago realizado exitosamente',
                'fecha_emision': datetime.now().strftime('%d/%m/%Y')
            }
 
            db = firestore.client()
            errores = []
 
            for item in items_para_boleta:
                try:
                    producto_ref = db.collection('productos').where('nombre', '==', item.producto.nombre).limit(1).stream()
                    for doc in producto_ref:
                        nuevo_stock = doc.to_dict()['stock'] - item.cantidad
                        if nuevo_stock < 0:
                            errores.append(f'Stock insuficiente para {item.producto.nombre}')
                        else:
                            doc.reference.update({'stock': nuevo_stock})
                except Exception as e:
                    errores.append(f'Error al actualizar el stock para {item.producto.nombre}: {str(e)}')
 
            if errores:
                for error in errores:
                    messages.error(request, error)
 
            items_carrito.delete()
            messages.success(request, 'Pago realizado exitosamente')
                
            # Enviar correo electrónico con la boleta
            subject = 'Boleta de compra - GalaxyMusic'
            message = f"""
            Hola {request.user.username},
 
                Gracias por tu compra en GalaxyMusic. Aquí tienes los detalles de tu boleta:
 
                Fecha de emisión: {boleta['fecha_emision']}
                Total: ${boleta['total']}
 
                Detalles de los productos:
                """
            for item in boleta['items']:
                message += f"\n- {item['producto'].nombre} (Código: {item['codigo']}), Cantidad: {item['cantidad']}"
            message += "\n\nGracias por comprar con nosotros."
            from_email = 'galaxymusic2024@gmail.com'
            recipient_list = [request.user.email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
 
    else:
        formulario_pago = FormularioPago()
 
    contexto = {
        'formulario_pago': formulario_pago,
        'boleta': boleta,
        'items_carrito': items_carrito if not boleta else boleta['items'],
        'total': total_con_descuento,
        'subtotal': total,
    }
    return render(request, 'pago.html', contexto)
 
 
# Agregar producto al carrito
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    session_key = request.session.session_key
    if request.user.is_authenticated:
        item_carrito, created = ItemCarrito.objects.get_or_create(usuario=request.user, producto=producto)
    else:
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        item_carrito, created = ItemCarrito.objects.get_or_create(session_key=session_key, producto=producto)
    if not created:
        item_carrito.cantidad += 1
        item_carrito.save()
    return redirect('carrito')
 
 
# Eliminar producto del carrito
def eliminar_del_carrito(request, item_id):
    if request.user.is_authenticated:
        item_carrito = get_object_or_404(ItemCarrito, id=item_id, usuario=request.user)
    else:
        session_key = request.session.session_key
        item_carrito = get_object_or_404(ItemCarrito, id=item_id, session_key=session_key)
    item_carrito.delete()
    return redirect('carrito')
 
 
# Actualizar cantidad de producto en el carrito
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
 
 
# Vista para mostrar formulario de inicio de sesión
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
 
 
# Vista para mostrar formulario de registro
@csrf_exempt
def mostrar_registro(request):
    if request.method == 'POST':
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            formulario = FormularioRegistro(data)
        else:
            formulario = FormularioRegistro(request.POST)
        if formulario.is_valid():
            nuevo_usuario = formulario.save()
            login(request, nuevo_usuario)
            
            # Enviar correo electrónico con código de descuento
            subject = '¡Bienvenido a GalaxyMusic! Código de Descuento'
            message = 'Gracias por registrarte en GalaxyMusic. Usa el código INVIERNO2024 para obtener un 30% de descuento en tus próximos productos.'
            from_email = 'galaxymusic2024@gmail.com'
            recipient_list = [nuevo_usuario.email]
            
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
 
            if request.content_type == 'application/json':
                return JsonResponse({'mensaje': 'Registro exitoso', 'usuario': nuevo_usuario.username})
            else:
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
 
 
# Función para cerrar sesión
def cerrar_sesion(request):
    logout(request)
    return redirect('index')