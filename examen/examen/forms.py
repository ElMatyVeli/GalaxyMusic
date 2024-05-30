from django import forms
from django.forms import TextInput, URLInput
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ('nombre', 'precio', 'stars', 'foto')