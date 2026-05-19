from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from .models import Agenda
from .forms import AgendaForm
from . import services
from datetime import date


class ListarAgendasView(View):
    def get(self, request):
        correo = request.session.get('correo')
        if not correo:
            return redirect('/usuarios/login/')
        agendas = Agenda.objects.filter(usuarioCorreo=correo).order_by('fecha')
        return render(request, 'listar_agendas.html', {
            'agendas': agendas,
            'hoy': date.today()
        })


def agendarPendientes(request):
    correo = request.session.get('correo')
    if not correo:
        return redirect('/usuarios/login/')
    agendas = Agenda.objects.filter(usuarioCorreo=correo, estado='pendiente').order_by('fecha')
    return render(request, 'agendas_pendientes.html', {'agendas': agendas})


def crearAgenda(request):
    correo = request.session.get('correo')
    if not correo:
        return redirect('/usuarios/login/')

    tareaId = request.GET.get('tareaId') or request.POST.get('tareaId')

    if not tareaId:
        return redirect('listarTareas')

    tarea = services.obtenerTarea(tareaId)

    if request.method == 'GET':
        formulario = AgendaForm()
        return render(request, 'crear_agenda.html', {
            'formulario': formulario,
            'tarea': tarea,
            'tareaId': tareaId,
        })
    else:
        formulario = AgendaForm(request.POST)
        if formulario.is_valid():
            Agenda.objects.create(
                titulo=formulario.cleaned_data['titulo'],
                descripcion=formulario.cleaned_data['descripcion'],
                fecha=formulario.cleaned_data['fecha'],
                hora=formulario.cleaned_data['hora'],
                prioridad=formulario.cleaned_data['prioridad'],
                estado=formulario.cleaned_data['estado'],
                recordatorioActivo=formulario.cleaned_data['recordatorioActivo'],
                tareaId=tareaId,
                usuarioCorreo=correo,
            )
            return redirect('listar_agendas')
        return render(request, 'crear_agenda.html', {
            'formulario': formulario,
            'tarea': tarea,
            'tareaId': tareaId,
        })


def detalleAgenda(request, agenda_id):
    correo = request.session.get('correo')
    if not correo:
        return redirect('/usuarios/login/')

    try:
        agenda = Agenda.objects.get(id=agenda_id)
    except Agenda.DoesNotExist:
        return HttpResponse("Agenda no encontrada", status=404)

    tarea = services.obtenerTarea(agenda.tareaId) if agenda.tareaId else None
    usuario = services.obtenerUsuario(agenda.usuarioCorreo) if agenda.usuarioCorreo else None

    return render(request, 'detalle_agenda.html', {
        'agenda': agenda,
        'tarea': tarea,
        'usuario': usuario,
    })


def editarAgenda(request, agenda_id):
    correo = request.session.get('correo')
    if not correo:
        return redirect('/usuarios/login/')

    try:
        agenda = Agenda.objects.get(id=agenda_id)
    except Agenda.DoesNotExist:
        return HttpResponse("Agenda no encontrada", status=404)

    if request.method == 'GET':
        formulario = AgendaForm(initial={
            'titulo': agenda.titulo,
            'descripcion': agenda.descripcion,
            'fecha': agenda.fecha,
            'hora': agenda.hora,
            'prioridad': agenda.prioridad,
            'estado': agenda.estado,
            'recordatorioActivo': agenda.recordatorioActivo,
        })
        return render(request, 'editar_agenda.html', {
            'formulario': formulario,
            'agenda': agenda,
        })
    else:
        formulario = AgendaForm(request.POST)
        if formulario.is_valid():
            agenda.titulo = formulario.cleaned_data['titulo']
            agenda.descripcion = formulario.cleaned_data['descripcion']
            agenda.fecha = formulario.cleaned_data['fecha']
            agenda.hora = formulario.cleaned_data['hora']
            agenda.prioridad = formulario.cleaned_data['prioridad']
            agenda.estado = formulario.cleaned_data['estado']
            agenda.recordatorioActivo = formulario.cleaned_data['recordatorioActivo']
            agenda.save()
            return redirect('listar_agendas')
        return render(request, 'editar_agenda.html', {
            'formulario': formulario,
            'agenda': agenda,
        })


def eliminarAgenda(request, agenda_id):
    correo = request.session.get('correo')
    if not correo:
        return redirect('/usuarios/login/')

    try:
        agenda = Agenda.objects.get(id=agenda_id)
    except Agenda.DoesNotExist:
        return HttpResponse("Agenda no encontrada", status=404)

    if request.method == 'POST':
        agenda.delete()
        return redirect('listar_agendas')

    return render(request, 'eliminar_agenda.html', {'agenda': agenda})