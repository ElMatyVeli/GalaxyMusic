import pytest
from django.test import Client
from django.urls import reverse
from tienda.models import Producto
from tienda.views import index

@pytest.mark.django_db
def test_index_view_with_firestore():
    # Configurar el cliente de prueba
    client = Client()

    # Hacer la solicitud GET a la vista index
    response = client.get(reverse('index'))

    # Verificar que la vista responde correctamente (código 200)
    assert response.status_code == 200

    # Verificar que los productos se pasan al contexto de la plantilla
    productos_renderizados = response.context['productos']
    assert productos_renderizados is not None
    assert isinstance(productos_renderizados, list)
    assert all(isinstance(producto, Producto) for producto in productos_renderizados)

    # Verificar que la plantilla usada es la correcta
    assert 'index.html' in [template.name for template in response.templates]

@pytest.mark.django_db
def test_productos_view_with_firestore():
    # Configurar el cliente de prueba
    client = Client()

    # Hacer la solicitud GET a la vista productos
    response = client.get(reverse('productos'))

    # Verificar que la vista responde correctamente (código 200)
    assert response.status_code == 200

    # Verificar que los productos se pasan al contexto de la plantilla
    productos_renderizados = response.context['productos']
    assert productos_renderizados is not None
    assert isinstance(productos_renderizados, list)
    assert all(isinstance(producto, Producto) for producto in productos_renderizados)

    # Verificar que la plantilla usada es la correcta
    assert 'productos.html' in [template.name for template in response.templates]
