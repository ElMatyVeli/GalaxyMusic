from django.db import models

class Producto(models.Model):
    # Definición de campos para el modelo Producto
    nombre = models.CharField(max_length=100)  # Campo para el nombre del producto
    descripcion = models.TextField()  # Campo para la descripción del producto
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # Campo para el precio del producto con dos decimales
    foto = models.ImageField(upload_to='productos/', null=True, blank=True)  # Campo para la foto del producto, opcional
    stock = models.IntegerField()  # Campo para el stock disponible del producto
    codigo = models.IntegerField()  # Campo para el código del producto

    # Método que define la representación en cadena de un objeto Producto
    def __str__(self):
        return self.nombre  # Devuelve el nombre del producto
