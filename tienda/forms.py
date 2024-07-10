from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from datetime import date

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

class FormularioEntrar(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        label='Nombre de usuario',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        required=True,
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError("Nombre de usuario o contraseña incorrectos.")
            elif not self.user_cache.is_active:
                raise forms.ValidationError("Esta cuenta está inactiva.")
        return self.cleaned_data

    def get_user(self):
        return self.user_cache

class FormularioPago(forms.Form):
    numero_tarjeta = forms.IntegerField(
        label='Número de Tarjeta', 
        min_value=1000000000000000,  # Valor mínimo para una tarjeta de 16 dígitos
        max_value=9999999999999999,  # Valor máximo para una tarjeta de 16 dígitos
        required=True,
        widget=forms.NumberInput(attrs={'placeholder': 'XXXX XXXX XXXX XXXX', 'class': 'form-control'})
    )
    fecha_vencimiento = forms.DateField(
        label='Fecha de Vencimiento', 
        required=True,
        input_formats=['%m/%y'],
        widget=forms.DateInput(attrs={'placeholder': 'MM/YY', 'class': 'form-control'}, format='%m/%y')
    )
    codigo_seguridad = forms.IntegerField(
        label='Código de Seguridad', 
        min_value=100,  # Valor mínimo para un código de 3 dígitos
        max_value=999,  # Valor máximo para un código de 3 dígitos
        required=True,
        widget=forms.NumberInput(attrs={'placeholder': 'XXX', 'class': 'form-control'})
    )

    def clean_fecha_vencimiento(self):
        fecha_vencimiento = self.cleaned_data.get('fecha_vencimiento')
        if fecha_vencimiento < date.today():
            raise forms.ValidationError("La fecha de vencimiento no puede ser en el pasado.")
        return fecha_vencimiento
