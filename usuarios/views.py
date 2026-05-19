import json

from django.http import JsonResponse
from django.shortcuts import redirect, render
from .models import Usuario
from django.views.generic import ListView


def obtenerUsuarios(request):
    usuarios = Usuario.objects.all()
    data = []
    for usuario in usuarios:
        data.append({
            "nombre": usuario.nombre,
            "correo": usuario.correo,
        })
    return JsonResponse(data, safe=False)


def crearUsuario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        correo = request.POST.get('correo')
        password = request.POST.get('password')

        if not nombre:
            return render(request, 'usuarios.html', {'error': 'El nombre es obligatorio'})

        if not apellido:
            return render(request, 'usuarios.html', {'error': 'El apellido es obligatorio'})

        if not correo:
            return render(request, 'usuarios.html', {'error': 'El correo es obligatorio'})

        if not password:
            return render(request, 'usuarios.html', {'error': 'La contraseña es obligatoria'})

        usuarioExiste = Usuario.objects.filter(correo=correo).first()

        if usuarioExiste:
            return render(request, 'usuarios.html', {'error': 'El correo ya está registrado'})

        try:
            Usuario.objects.create(
                nombre=nombre,
                apellido=apellido,
                correo=correo,
                password=password,
            )
            request.session['mensaje'] = 'Usuario creado correctamente'
            return redirect('/usuarios/login/')

        except Exception as e:
            print('ERROR:', e)
            return render(request, 'usuarios.html', {'error': 'Ocurrió un error al crear el usuario'})

    return render(request, 'usuarios.html')


def loginUsuario(request):
    mensaje = request.session.pop('mensaje', None)

    if request.method == "POST":
        try:
            correo = request.POST.get("correo")
            password = request.POST.get("password")

            usuario = Usuario.objects.filter(correo=correo).first()

            if usuario and usuario.password == password:
                request.session['nombre'] = usuario.nombre
                request.session['correo'] = usuario.correo
                return redirect('/usuarios/dashboard/')
            else:
                return render(request, 'login.html', {'error': 'Credenciales incorrectas'})

        except Exception as e:
            return render(request, 'login.html', {'error': str(e)})

    return render(request, 'login.html', {'mensaje': mensaje})


def dashboard(request):
    if not request.session.get('correo'):
        return redirect('/usuarios/login/')
    return render(request, 'dashboard.html', {'nombre': request.session.get('nombre')})


def logoutUsuario(request):
    request.session.flush()
    return redirect('/usuarios/login/')


class perfilUsuarioView(ListView):
    model = Usuario
    template_name = 'perfilUsuario.html'
    context_object_name = 'usuarios'

    def dispatch(self, request, *args, **kwargs):
        if not request.session.get('correo'):
            return redirect('/usuarios/login/')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        correo = self.request.session.get('correo')
        return Usuario.objects.filter(correo=correo)


def editarUsuario(request):
    if not request.session.get('correo'):
        return redirect('/usuarios/login/')
    correo = request.session.get('correo')
    usuario = Usuario.objects.get(correo=correo)
    if request.method == 'POST':
        usuario.nombre = request.POST.get('nombre')
        usuario.apellido = request.POST.get('apellido')
        usuario.correo = request.POST.get('correo')
        usuario.save()
        request.session['correo'] = usuario.correo
        return redirect('/usuarios/perfilUsuario/')
    return render(request, 'editarUsuario.html', {'usuario': usuario})