import json

from django.http import JsonResponse
from django.shortcuts import render
from .models import Usuario


def obtener_usuarios(request):

    usuarios = Usuario.objects.all()
    data = []

    for usuario in usuarios:

        data.append({
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
            correo = request.POST.get('correo')
            password = request.POST.get('password')
            telefono = request.POST.get('telefono')
            direccion = request.POST.get('direccion')
            ciudad = request.POST.get('ciudad')
            pais = request.POST.get('pais')
            edad = request.POST.get('edad')

            Usuario.objects.create(
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

                return JsonResponse({
                    "mensaje": "Login exitoso",
                    "usuario": {
                        "id": usuario.id,
                        "nombre": usuario.nombre,
                        "correo": usuario.correo
                    }
                })

            else:

                return JsonResponse({
                    "error": "Credenciales incorrectas"
                }, status=401)

        except Exception as e:

            return JsonResponse({
                "error": str(e)
            }, status=500)

    return render(request, 'login.html')
