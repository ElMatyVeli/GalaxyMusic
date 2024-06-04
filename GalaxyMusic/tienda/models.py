# En tu archivo models.py

from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    foto = models.ImageField(upload_to='productos/', null=True, blank=True)  # Campo para la foto del producto
    stock = models.IntegerField()
    codigo = models.IntegerField()
    # Otros campos según tus necesidades, como imagen, categoría, etc.
    def __str__(self):
        return self.nombre
