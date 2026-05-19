from django.shortcuts import render, redirect
from django.views.generic import ListView
from .models import Tarea


class listarTareas(ListView):
    model = Tarea
    template_name = 'tareas/listar.html'
    context_object_name = 'tareas'

    def get_queryset(self):
        correo = self.request.session.get('correo')
        if not correo:
            return Tarea.objects.none()
        return Tarea.objects.filter(usuarioCorreo=correo)


def crearTarea(request):
    if request.method == 'POST':
        correo = request.session.get('correo')
        if not correo:
            return redirect('/usuarios/login/')

        titulo = request.POST['titulo']
        descripcion = request.POST['descripcion']
        estadoTarea = request.POST['estadoTarea']

        tarea = Tarea(
            titulo=titulo,
            descripcion=descripcion,
            estadoTarea=estadoTarea,
            usuarioCorreo=correo
        )
        tarea.save()
        return redirect('/tareas/listar/')

    return render(request, 'tareas/crear.html')


def editarTarea(request, tareaId):
    correo = request.session.get('correo')
    if not correo:
        return redirect('/usuarios/login/')

    tarea = Tarea.objects.get(id=tareaId)

    if request.method == 'POST':
        tarea.titulo = request.POST['titulo']
        tarea.descripcion = request.POST['descripcion']
        tarea.estadoTarea = request.POST['estadoTarea']
        tarea.save()
        return redirect('/tareas/listar/')

    return render(request, 'tareas/editar.html', {
        'tarea': tarea
    })


def eliminarTarea(request, tareaId):
    correo = request.session.get('correo')
    if not correo:
        return redirect('/usuarios/login/')

    tarea = Tarea.objects.get(id=tareaId)
    tarea.delete()
    return redirect('/tareas/listar/')


def detalleTarea(request, tareaId):
    correo = request.session.get('correo')
    if not correo:
        return redirect('/usuarios/login/')

    tarea = Tarea.objects.get(id=tareaId)
    return render(request, 'tareas/detalle.html', {
        'tarea': tarea
    })