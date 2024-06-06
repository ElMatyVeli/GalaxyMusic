from django import forms
from .models import Producto
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import Form, CharField, PasswordInput, EmailField, EmailInput, CheckboxInput, BooleanField, TextInput

# Formulario de Registro de Usuario
class FormularioRegistro(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        required=True,
        label='Nombre de usuario',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        max_length=30,
        required=True,
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        max_length=30,
        required=True,
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label='Nombre',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label='Apellido',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        max_length=254,
        required=True,
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Añade la clase 'form-control' a todos los campos del formulario
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

# Formulario de Inicio de Sesión
class FormularioEntrar(Form):
    usuario = CharField(
        min_length=1,
        max_length=18,
        required=True,
        label='Ingrese su usuario',
        widget=TextInput(attrs={'class': 'form-control'})
    )
    contrasenia_usuario = CharField(
        required=True,
        min_length=4,
        max_length=16,
        label='Ingrese su contraseña',
        widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    recuerdame = BooleanField(
        required=False,
        label='Recordarme',
        widget=CheckboxInput()
    )

# Formulario de Producto
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'descripcion', 'foto', 'stock', 'codigo']  # Incluye 'foto' en los campos del formulario

    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        # Limita los tipos de archivos aceptados a imágenes
        self.fields['foto'].widget.attrs.update({'accept': 'image/*'})

# Formulario para Confirmar Eliminación de Producto
class EliminarProductoForm(forms.Form):
    confirmacion = forms.BooleanField(required=True, label='Confirmar eliminación')
