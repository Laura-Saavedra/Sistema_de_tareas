from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Agenda
from .forms import AgendaForm, BuscarUsuarioForm
from . import services
from django.views import View

class ListarAgendasView(View):
    def get(self, request):
        cedula = request.session.get('cedula')
        if not cedula:
            return redirect('/usuarios/login/')
        agendas = Agenda.objects.filter(usuarioId=str(cedula))
        return render(request, 'listar_agendas.html', {
            'agendas': agendas,
            'cedula': cedula
        })

def agendarPendientes(request):
    agendas = Agenda.objects.filter(estado='pendiente').order_by('fecha')
    return render(request, 'agendas_pendientes.html', {'agendas': agendas})


def buscarUsuario(request):
    if request.method == 'GET':
        formulario = BuscarUsuarioForm()
        return render(request, 'buscar_usuario.html', {'formulario': formulario})
    else:
        formulario = BuscarUsuarioForm(request.POST)
        if formulario.is_valid():
            usuarioId = formulario.cleaned_data['usuarioId']
            tareas = services.obtenerTareasPorUsuario(usuarioId)
            return render(request, 'seleccionar_tarea.html', {
                'tareas': tareas,
                'usuarioId': usuarioId,
                'formulario': formulario,
            })
        return render(request, 'buscar_usuario.html', {'formulario': formulario})


def crearAgenda(request):
    tareaId = request.GET.get('tareaId') or request.POST.get('tareaId')
    cedula = request.GET.get('cedula') or request.POST.get('cedula')

    if not tareaId or not cedula:
        return redirect('buscar_usuario')

    tarea = services.obtenerTarea(tareaId)

    if request.method == 'GET':
        formulario = AgendaForm()
        return render(request, 'crear_agenda.html', {
            'formulario': formulario,
            'tarea': tarea,
            'tareaId': tareaId,
            'usuarioId': usuarioId,
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
                usuarioId=usuarioId,
            )
            return redirect('listar_agendas')
        return render(request, 'crear_agenda.html', {
            'formulario': formulario,
            'tarea': tarea,
            'tareaId': tareaId,
            'usuarioId': usuarioId,
        })


def detalleAgenda(request, agenda_id):
    try:
        agenda = Agenda.objects.get(id=agenda_id)
    except Agenda.DoesNotExist:
        return HttpResponse("Agenda no encontrada", status=404)

    tarea = services.obtenerTarea(agenda.tareaId) if agenda.tareaId else None
    usuario = services.obtenerUsuario(agenda.usuarioId) if agenda.usuarioId else None

    return render(request, 'detalle_agenda.html', {
        'agenda': agenda,
        'tarea': tarea,
        'usuario': usuario,
    })


def editarAgenda(request, agenda_id):
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
    try:
        agenda = Agenda.objects.get(id=agenda_id)
    except Agenda.DoesNotExist:
        return HttpResponse("Agenda no encontrada", status=404)

    if request.method == 'POST':
        agenda.delete()
        return redirect('listar_agendas')

    return render(request, 'eliminar_agenda.html', {'agenda': agenda})