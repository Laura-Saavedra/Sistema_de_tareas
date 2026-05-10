from django.shortcuts import render, redirect
from .models import Tarea
from usuarios.services import obtenerUsuarios

def crearTarea(request):

    if request.method == 'POST':

        titulo = request.POST['titulo']

        descripcion = request.POST['descripcion']

        estadoTarea = request.POST['estadoTarea']

        prioridad = request.POST['prioridad']

        fechaEntrega = request.POST['fechaEntrega']

        usuarioResponsableId = request.POST['usuarioResponsableId']

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

    return render(request, 'tareas/crear.html')


def listarTareas(request):

    tareas = Tarea.objects.all()

    return render(request, 'tareas/listar.html', {

        'tareas': tareas
    })

def editarTarea(request, tareaId):

    tarea = Tarea.objects.get(id=tareaId)

    usuarios = obtenerUsuarios()

    if request.method == 'POST':

        tarea.titulo = request.POST['titulo']

        tarea.descripcion = request.POST['descripcion']

        tarea.estadoTarea = request.POST['estadoTarea']

        tarea.prioridad = request.POST['prioridad']

        tarea.fechaEntrega = request.POST['fechaEntrega']

        tarea.usuarioResponsableId = request.POST['usuarioResponsableId']

        tarea.save()

        return redirect('/tareas/listar/')

    return render(request, 'tareas/editar.html', {

        'tarea': tarea,
        'usuarios': usuarios
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