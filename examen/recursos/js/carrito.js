// Variables globales
var carrito = []; // Almacena los productos en el carrito de compras
var totalAntiguo = 0; // Almacena el total sin descuento
var totalNuevo = 0; // Almacena el total con descuento
var descuento = 0; // Almacena el monto de descuento aplicado


function agregarAlCarrito(nombre, precio, foto) {
  const producto = { nombre, precio: parseFloat(precio), foto };
  carrito.push(producto);
  guardarCarrito(carrito);
  alert(`${nombre} se ha agregado al carrito`);
  mostrarCarrito();
}

// Muestra los productos en el carrito de compras.
function mostrarCarrito() {
  var carritoBody = document.getElementById('carrito-body');
  carritoBody.innerHTML = '';
  totalAntiguo = 0;
  totalNuevo = 0;
  descuento = 0;

  for (var i = 0; i < carrito.length; i++) {
    var producto = carrito[i];

    var fila = document.createElement('tr');
    var celdaNombre = document.createElement('td');
    var celdaPrecio = document.createElement('td');

    var imagenProducto = document.createElement('img');
    imagenProducto.src = producto.foto;
    imagenProducto.classList.add('producto-imagen');

    var nombreProducto = document.createElement('span');
    nombreProducto.textContent = producto.nombre;

    celdaNombre.classList.add('producto-nombre');
    celdaNombre.appendChild(imagenProducto);
    celdaNombre.appendChild(nombreProducto);

    if (typeof producto.precio === 'number') {
      celdaPrecio.textContent = '$' + producto.precio.toFixed(3);
      totalAntiguo += producto.precio;
      totalNuevo += producto.precio;
    } else {
      celdaPrecio.textContent = 'Precio inválido';
    }

    fila.appendChild(celdaNombre);
    fila.appendChild(celdaPrecio);
    carritoBody.appendChild(fila);
  }

  var totalAntiguoElement = document.getElementById('total-antiguo');
  totalAntiguoElement.textContent = '$' + totalAntiguo.toFixed(3);

  var codigoDescuentoInput = document.getElementById('codigo-descuento');
  var aplicarDescuentoButton = document.getElementById('aplicar-descuento');

  aplicarDescuentoButton.addEventListener('click', function() {
    var codigo = codigoDescuentoInput.value;
    if (codigo === 'INVIERNO2023') { // Código de descuento válido
      descuento = totalAntiguo * 0.1;
      totalNuevo = totalAntiguo - descuento;
      alert('Código de descuento ingresado con éxito');
    } else { // Código de descuento inválido
      descuento = 0;
      totalNuevo = totalAntiguo;
      alert('Código de descuento invalido');
    }
    mostrarTotalNuevo(totalNuevo);
  });

  mostrarTotalNuevo(totalNuevo);
}


// Muestra el nuevo total a pagar en el carrito de compras
function mostrarTotalNuevo(totalNuevo) {
  var totalNuevoElement = document.getElementById('total-nuevo');
  totalNuevoElement.textContent = '$' + totalNuevo.toFixed(3);
}

//Guarda el carrito de compras en el javascript
function guardarCarrito(carrito) {
  localStorage.setItem('carrito', JSON.stringify(carrito));
}


//Carga el carrito de compras desde el almacenamiento local.
 //Si existe un carrito guardado, lo carga y muestra los productos.

function cargarCarrito() {
  var carritoGuardado = localStorage.getItem('carrito');
  if (carritoGuardado) {
    carrito = JSON.parse(carritoGuardado);
    mostrarCarrito();
  }
}


//Borra todos los productos del carrito de compras, luego, guarda el carrito vacío en el almacenamiento local y muestra un mensaje de alerta.
function borrarCarrito() {
  carrito = [];
  guardarCarrito(carrito);
  mostrarCarrito();
  alert('El carrito se ha borrado');
}


// Carga el carrito al cargar la página
cargarCarrito();


//Muestra el formulario de modificación para un producto específico.
function mostrarFormulario(productoId) {
  var formulario = document.getElementById('formulario-' + productoId);
  formulario.style.display = 'block';
}


//Genera la boleta de compra con los productos del carrito. Calcula el total a pagar y lo muestra en la boleta.
function generarBoleta() {
  var boletaContainer = document.getElementById('boleta');
  var productosBoleta = document.getElementById('productos-boleta');
  productosBoleta.innerHTML = ''; // Limpiar contenido anterior de los productos

  var totalPagar = 0; // Variable para calcular el total a pagar

  for (var i = 0; i < carrito.length; i++) {
    var producto = carrito[i];

    var nombre = producto.nombre;
    var precio = producto.precio;
    var cantidad = 1; // Supongamos que siempre es una unidad por producto

    var itemBoleta = document.createElement('div');
    itemBoleta.classList.add('item-boleta');

    var nombreProducto = document.createElement('p');
    nombreProducto.textContent = nombre;

    var precioProducto = document.createElement('p');
    precioProducto.textContent = '$' + precio.toFixed(3);

    var cantidadProducto = document.createElement('p');
    cantidadProducto.textContent = cantidad;

    itemBoleta.appendChild(nombreProducto);
    itemBoleta.appendChild(precioProducto);
    itemBoleta.appendChild(cantidadProducto);

    productosBoleta.appendChild(itemBoleta);

    // Agregar separador (línea horizontal o margen superior)
    if (i < carrito.length - 1) {
      var separador = document.createElement('hr');
      productosBoleta.appendChild(separador);
    }

    totalPagar += precio; // Sumar el precio al total a pagar
  }

  var totalPagarElement = document.getElementById('total-pagar');
  totalPagarElement.textContent = '$' + totalPagar.toFixed(3);
}
// Evento de clic en el botón "Pagar"
var pagarButton = document.getElementById('pagar');
pagarButton.addEventListener('click', function() {
  generarBoleta();
});


 // Función para abrir el modal
 function openModal() {
  var modal = document.getElementById("myModal");
  modal.style.display = "block";
}

// Función para cerrar el modal
function closeModal() {
  var modal = document.getElementById("myModal");
  modal.style.display = "none";
}