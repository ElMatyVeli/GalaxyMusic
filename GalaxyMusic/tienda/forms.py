from django import forms
from .models import Producto
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.forms import (
    Form,
    CharField,
    PasswordInput,
    EmailField,
    EmailInput,
    CheckboxInput,
    BooleanField,
    TextInput
)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class FormularioRegistro(UserCreationForm):
    def __init__(self, *args,**kargs):
        super().__init__(*args,**kargs)
        # Le aplicamos las clases forzadamente a los campos
        # password1 y password2
        self.fields['password1'].widget.attrs = { 'class': 'form-control'}
        self.fields['password2'].widget.attrs = { 'class': 'form-control'}
    class Meta:
        # Registramos este formulario para el modelo User
        model = User
        fields = [
            'username',
            'password1',
            'password2',
            'first_name',
            'last_name',
            'email'
        ]
        # Le reemplazamos los estilos por defecto a los campos del modelo Usuario
        # completar los campos que faltan para poder terminar los estilos
        widgets = {
            'username': TextInput( attrs = { 'class' : 'form-control'} ),
            'first_name': TextInput( attrs = { 'class' : 'form-control'} ),
            'last_name': TextInput( attrs = { 'class' : 'form-control'} ),
            'email': EmailInput( attrs = { 'class' : 'form-control'} ),
        }

class FormularioEntrar(Form):
    usuario = CharField(
        min_length=1,
        max_length=18,
        required = True,
        label = 'Ingrese su usuario',
        widget = TextInput(
            attrs = {
                'class':'form-control'
            }
        )
    )
    contrasenia_usuario = CharField(
        required = True,
        min_length = 4,
        max_length = 16,
        label = 'Ingrese su contraseña',
        widget = PasswordInput(
            attrs = {
                'class':'form-control',
                'placeholder':'Password'
            }
        )
    )
    recuerdame = BooleanField(
        required = False,
        label = 'Recordarme',
        widget = CheckboxInput(

        )
    )
# FIN FORMULARIO USUARIO

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio','descripcion', 'foto','stock','codigo']  # Asegúrate de incluir 'foto' en los campos del formulario

    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        self.fields['foto'].widget.attrs.update({'accept': 'image/*'})  # Para limitar los tipos de archivos a imágenes

class EliminarProductoForm(forms.Form):
    confirmacion = forms.BooleanField(required=True, label='Confirmar eliminación')


