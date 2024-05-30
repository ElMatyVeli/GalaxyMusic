from django.shortcuts import render, redirect
# Usuario 
from django.contrib.auth import authenticate, login, logout
from .forms import FormularioEntrar, FormularioRegistro
from sweetify import success, warning, info, error

# Usuario
# Create your views here.
# Usuario
def mostrar_entrar(request):
    if request.method == 'GET':
        contexto = {
            'titulo': 'Bienvenido',
            'formulario':FormularioEntrar()
        }
        return render(request,'login/entrar.html',contexto)
    if request.method == 'POST':
        datos_usuario = FormularioEntrar(data=request.POST)
        es_valido = datos_usuario.is_valid()
        if es_valido:
            username = datos_usuario.cleaned_data['usuario']
            password = datos_usuario.cleaned_data['contrasenia_usuario']
            usuario = authenticate(username=username,password=password)
            if usuario is not None:
                login(request, usuario)
                success(request, f'Bienvenido {usuario.username}')
                return redirect('mostrar_principal')
        contexto = {
            'titulo': 'Bienvenido',
            'formulario': datos_usuario
        }
        warning(request,'Usuario y contraseña incorrectos')
        return render(request,'login/entrar.html',contexto)

def mostrar_registro(request):
    # Usamos el nuevo formulario para mostrar los elementos con clases
    if request.method == 'GET':
        contexto = {
            'formulario': FormularioRegistro()
        }
        return render(request, 'login/registro.html', contexto)
    elif request.method == 'POST':
        formulario_usuario = FormularioRegistro(request.POST)
        es_valido = formulario_usuario.is_valid() # True Valido, False Invalido 
        if es_valido:
            formulario_usuario.save()
            success(request,'Bienvenido, gracias por registrarte')
            return redirect('mostrar_entrar')
        contexto = {
            'formulario': formulario_usuario
        }
        warning(request, 'Ups... complete los campos correctamente')
        return render(request, 'registro.html', contexto)


        
def cerrar_sesion(request):
    if request.user.is_authenticated:
        logout(request)
        success(request,'Hasta pronto :)')
    return redirect('mostrar_principal')
# Usuario
    
def mostrar_carrito(request):
    contexto={
        ""
    }
    return render(request,'',contexto)