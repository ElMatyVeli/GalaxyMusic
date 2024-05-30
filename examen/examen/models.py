from django.db import models

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stars = models.CharField(max_length=20)
    foto = models.URLField(max_length=300)

    def __str__(self):
        return self.nombre