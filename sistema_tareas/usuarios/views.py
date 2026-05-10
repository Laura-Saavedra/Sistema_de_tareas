import json

from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import Usuario
from django.views.generic import ListView


def obtener_usuarios(request):

    usuarios = Usuario.objects.all()
    data = []

    for usuario in usuarios:

        data.append({
            "cedula": usuario.cedula,
            "id": usuario.id,
            "nombre": usuario.nombre,
            "correo": usuario.correo,
            "edad": usuario.edad,
            "activo": usuario.activo
        })

    return JsonResponse(data, safe=False)


def crear_usuario(request):

    if request.method == 'POST':

        try:

            nombre = request.POST.get('nombre')
            apellido = request.POST.get('apellido')
            cedula = request.POST.get('cedula')
            correo = request.POST.get('correo')
            password = request.POST.get('password')
            telefono = request.POST.get('telefono')
            direccion = request.POST.get('direccion')
            ciudad = request.POST.get('ciudad')
            pais = request.POST.get('pais')
            edad = request.POST.get('edad')
            

            Usuario.objects.create(
                cedula=cedula,
                nombre=nombre,
                apellido=apellido,
                correo=correo,
                password=password,
                telefono=telefono,
                direccion=direccion,
                ciudad=ciudad,
                pais=pais,
                edad=int(edad)
            )

            return JsonResponse({
                'mensaje': 'Usuario creado correctamente'
            })

        except Exception as e:

            return JsonResponse({
                'error': repr(e)
            })

    return render(request, 'usuarios.html')


def login_usuario(request):

    if request.method == "POST":

        try:

            correo = request.POST.get("correo")
            password = request.POST.get("password")

            usuario = Usuario.objects.filter(
                correo=correo,
                password=password
            ).first()

            if usuario:

                return redirect('/dashboard/')

            else:

                return render(request, 'login.html', {
                    'error': 'Credenciales incorrectas'
                })

        except Exception as e:

            return render(request, 'login.html', {
                'error': str(e)
            })

    return render(request, 'login.html')

def dashboard(request):

    return render(request, 'dashboard.html')

class ListaUsuariosView(ListView):

    model = Usuario
    template_name = 'lista-usuarios.html'
    context_object_name = 'usuarios'
