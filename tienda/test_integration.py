import pytest
from django.urls import reverse
from tienda.models import Producto, ItemCarrito, User
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import datetime
from django.core import mail
from unittest.mock import patch

@pytest.mark.django_db
def test_login_and_add_to_cart(client):
    user = User.objects.create_user(username='testuser', password='12345')
    producto = Producto.objects.create(nombre='Test Producto', descripcion='Descripción', precio=100, stock=10, codigo='TEST1')

    # Iniciar sesión
    response = client.post(reverse('mostrar_ingresar'), {
        'username': 'testuser',
        'password': '12345'
    })
    assert response.status_code == 302  # Redirige al index
    assert response.wsgi_request.user.is_authenticated

    # Agregar producto al carrito
    response = client.post(reverse('agregar_al_carrito', args=[producto.id]))
    assert response.status_code == 302  # Redirige al carrito

    # Verificar que el producto está en el carrito
    response = client.get(reverse('carrito'))
    assert response.status_code == 200
    assert len(response.context['items_carrito']) == 1
    item_carrito = response.context['items_carrito'][0]
    assert item_carrito.producto == producto
    assert item_carrito.cantidad == 1

@pytest.mark.django_db
def test_apply_discount(client):
    user = User.objects.create_user(username='testuser', password='12345')
    client.login(username='testuser', password='12345')
    producto = Producto.objects.create(nombre='Test Producto', descripcion='Descripción', precio=100, stock=10, codigo='TEST1')

    # Agregar producto al carrito
    client.post(reverse('agregar_al_carrito', args=[producto.id]))

    # Aplicar descuento
    response = client.post(reverse('aplicar_descuento'), {'codigo_descuento': 'INVIERNO2024'})
    assert response.status_code == 302  # Redirige al carrito
    assert client.session['descuento'] == 30

    # Verificar el total con descuento
    response = client.get(reverse('carrito'))
    assert response.status_code == 200
    assert response.context['total_con_descuento'] == Decimal('70.00')  # 30% de descuento en 100

@pytest.mark.django_db
def test_update_cart_item_quantity(client):
    # Crear un usuario de prueba y hacer login
    user = User.objects.create_user(username='testuser', password='12345')
    client.login(username='testuser', password='12345')
    
    # Crear un producto de prueba
    producto = Producto.objects.create(nombre='Test Producto', descripcion='Descripción', precio=100, stock=10, codigo='TEST1')

    # Agregar producto al carrito
    response_agregar = client.post(reverse('agregar_al_carrito', args=[producto.id]))
    assert response_agregar.status_code == 302  # Verificar que se haya redirigido correctamente

    # Actualizar cantidad en el carrito
    item_carrito = ItemCarrito.objects.get(producto=producto, usuario=user)
    assert item_carrito.cantidad == 1  # Verificar que la cantidad inicial sea 1

    response_actualizar = client.post(reverse('actualizar_cantidad', args=[item_carrito.id]), {'cantidad': 2})
    assert response_actualizar.status_code == 302  # Verificar redirección después de actualizar

    # Verificar la cantidad actualizada en el carrito
    response_carrito = client.get(reverse('carrito'))
    assert response_carrito.status_code == 200
    items_carrito = response_carrito.context['items_carrito']
    assert len(items_carrito) == 1
    assert items_carrito[0].cantidad == 2  # Verificar que la cantidad se haya actualizado correctamente

@pytest.mark.django_db
def test_complete_payment_process(client):
    # Crear un usuario de prueba y hacer login
    user = User.objects.create_user(username='testuser', password='12345')
    client.login(username='testuser', password='12345')

    # Crear un producto de prueba
    producto = Producto.objects.create(nombre='Test Producto', descripcion='Descripción', precio=100, stock=10, codigo='TEST1')

    # Agregar producto al carrito
    response_agregar = client.post(reverse('agregar_al_carrito', args=[producto.id]))
    assert response_agregar.status_code == 302  # Verificar que se haya redirigido correctamente

    # Actualizar cantidad en el carrito
    item_carrito = ItemCarrito.objects.get(producto=producto, usuario=user)
    assert item_carrito.cantidad == 1  # Verificar que la cantidad inicial sea 1

    response_actualizar = client.post(reverse('actualizar_cantidad', args=[item_carrito.id]), {'cantidad': 2})
    assert response_actualizar.status_code == 302  # Verificar redirección después de actualizar

    # Verificar la cantidad actualizada en el carrito
    response_carrito = client.get(reverse('carrito'))
    assert response_carrito.status_code == 200
    items_carrito = response_carrito.context['items_carrito']
    assert len(items_carrito) == 1
    assert items_carrito[0].cantidad == 2  # Verificar que la cantidad se haya actualizado correctamente

    # Proceso de pago
    response_pago = client.post(reverse('realizar_pago'), {'metodo_pago': 'tarjeta', 'direccion_envio': 'Calle Ejemplo 123'})
    
    # Verificar que después del pago, se renderice la plantilla correcta
    assert response_pago.status_code == 200  # La vista renderiza la plantilla pago.html

@pytest.mark.django_db
@patch('django.core.mail.send_mail')
def test_email_notification_on_purchase(mock_send_mail, client):
    # Envío de correo electrónico
    mock_send_mail.return_value = 1

    # Crear un usuario de prueba y autenticarlo
    user = User.objects.create_user(username='testuser', password='12345')
    client.login(username='testuser', password='12345')

    # Crear un producto de prueba
    producto = Producto.objects.create(nombre='Test Producto', descripcion='Descripción', precio=100, stock=10, codigo='TEST1')

    # Agregar el producto al carrito
    response_carrito = client.post(reverse('agregar_al_carrito', args=[producto.id]))

    # Verificar que se agregó correctamente al carrito
    assert response_carrito.status_code == 302  # Verifica el código de redirección después de agregar al carrito

    # Realizar el proceso de pago
    response_pago = client.post(reverse('realizar_pago'), {'metodo_pago': 'tarjeta', 'direccion_envio': 'Calle Ejemplo 123'})

    # Verificar que el pago se realizó correctamente
    assert response_pago.status_code == 200

    # Verificar que se envió un correo electrónico
    assert mock_send_mail.return_value == 1
