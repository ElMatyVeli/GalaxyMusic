import pytest
from django.test import Client
from django.urls import reverse
from tienda.models import Producto, ItemCarrito
from django.contrib.auth.models import User

@pytest.mark.django_db
def test_index_view_with_firestore():
    client = Client()
    response = client.get(reverse('index'))
    assert response.status_code == 200
    productos_renderizados = response.context['productos']
    assert productos_renderizados is not None
    assert isinstance(productos_renderizados, list)
    assert all(isinstance(producto, Producto) for producto in productos_renderizados)
    assert 'index.html' in [template.name for template in response.templates]

@pytest.mark.django_db
def test_productos_view_with_firestore():
    client = Client()
    response = client.get(reverse('productos'))
    assert response.status_code == 200
    productos_renderizados = response.context['productos']
    assert productos_renderizados is not None
    assert isinstance(productos_renderizados, list)
    assert all(isinstance(producto, Producto) for producto in productos_renderizados)
    assert 'productos.html' in [template.name for template in response.templates]

@pytest.mark.django_db
def test_detalle_producto_view():
    producto = Producto.objects.create(nombre='Test Producto', descripcion='Descripción', precio=100, stock=10, codigo='TEST1')
    client = Client()
    response = client.get(reverse('detalle_producto', args=[producto.id]))
    assert response.status_code == 200
    assert response.context['producto'] == producto
    assert 'detalle_producto.html' in [template.name for template in response.templates]


@pytest.mark.django_db
def test_navbar_links():
    client = Client()
    # Probar el enlace a la página de inicio
    response_inicio = client.get(reverse('index'))
    assert response_inicio.status_code == 200

    # Probar el enlace a la página de productos
    response_productos = client.get(reverse('productos'))
    assert response_productos.status_code == 200

    # Probar el enlace a la página del carrito
    response_carrito = client.get(reverse('carrito'))
    assert response_carrito.status_code == 200

@pytest.mark.django_db
def test_navbar_links1():
    client = Client()

    # Si el usuario no está autenticado, probar el enlace a la página de ingresar
    response_ingresar = client.get(reverse('mostrar_ingresar'))
    assert response_ingresar.status_code == 200

    # Si el usuario no está autenticado, probar el enlace a la página de registro
    response_registro = client.get(reverse('mostrar_registro'))
    assert response_registro.status_code == 200
    


@pytest.mark.django_db
def test_registrar_usuario_view():
    client = Client()
    response = client.get(reverse('mostrar_registro'))
    assert response.status_code == 200
    assert 'registro.html' in [template.name for template in response.templates]

@pytest.mark.django_db
def test_salir_view():
    client = Client()
    response = client.get(reverse('cerrar_sesion'))
    assert response.status_code == 302  # Redirige al index

@pytest.mark.django_db
def test_carrito_view():
    client = Client()
    response = client.get(reverse('carrito'))
    assert response.status_code == 200
    assert 'carrito.html' in [template.name for template in response.templates]

@pytest.mark.django_db
def test_aplicar_descuento():
    client = Client()
    session = client.session
    session.create()
    session.save()
    response = client.post(reverse('aplicar_descuento'), {'codigo_descuento': 'INVIERNO2024'})
    assert response.status_code == 302  # Redirige al carrito
    assert client.session['descuento'] == 30


@pytest.mark.django_db
def test_mostrar_ingresar():
    user = User.objects.create_user(username='testuser', password='12345')
    client = Client()
    response = client.post(reverse('mostrar_ingresar'), {
        'username': 'testuser',
        'password': '12345'
    })
    assert response.status_code == 302  # Redirige al index
    assert response.wsgi_request.user.is_authenticated
