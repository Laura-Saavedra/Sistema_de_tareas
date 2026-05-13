from django.shortcuts import render, redirect
from django.views.generic import ListView

from .models import Tarea
from usuarios.views import obtenerUsuarios


class listarTareas(ListView):

    model = Tarea

    template_name = 'tareas/listar.html'

    context_object_name = 'tareas'


def crearTarea(request):
    error_cedula = None

    if request.method == 'POST':
        titulo = request.POST['titulo']
        descripcion = request.POST['descripcion']
        estadoTarea = request.POST['estadoTarea']
        prioridad = request.POST['prioridad']
        fechaEntrega = request.POST['fechaEntrega']
        usuarioResponsableId = request.POST['usuarioResponsableId']

        # Validar que exista un usuario con esa cédula
        from usuarios.services import obtenerUsuarioPorCedula
        usuario = obtenerUsuarioPorCedula(usuarioResponsableId)

        if usuario is None:
            error_cedula = 'No existe un usuario con esa cédula.'
        else:
            tarea = Tarea(
                titulo=titulo,
                descripcion=descripcion,
                estadoTarea=estadoTarea,
                prioridad=prioridad,
                fechaEntrega=fechaEntrega,
                usuarioResponsableId=usuarioResponsableId
            )
            tarea.save()
            return redirect('/tareas/listar/')

    return render(request, 'tareas/crear.html', {
        'error_cedula': error_cedula
    })

def editarTarea(request, tareaId):
    tarea = Tarea.objects.get(id=tareaId)
    error_cedula = None

    if request.method == 'POST':
        tarea.titulo = request.POST['titulo']
        tarea.descripcion = request.POST['descripcion']
        tarea.estadoTarea = request.POST['estadoTarea']
        tarea.prioridad = request.POST['prioridad']
        tarea.fechaEntrega = request.POST['fechaEntrega']
        usuarioResponsableId = request.POST['usuarioResponsableId']

        from usuarios.services import obtenerUsuarioPorCedula
        usuario = obtenerUsuarioPorCedula(usuarioResponsableId)

        if usuario is None:
            error_cedula = 'No existe un usuario con esa cédula.'
        else:
            tarea.usuarioResponsableId = usuarioResponsableId
            tarea.save()
            return redirect('/tareas/listar/')

    return render(request, 'tareas/editar.html', {
        'tarea': tarea,
        'error_cedula': error_cedula
    })

def eliminarTarea(request, tareaId):

    tarea = Tarea.objects.get(id=tareaId)

    tarea.delete()

    return redirect('/tareas/listar/')


def detalleTarea(request, tareaId):

    tarea = Tarea.objects.get(id=tareaId)

    return render(request, 'tareas/detalle.html', {

        'tarea': tarea
    })