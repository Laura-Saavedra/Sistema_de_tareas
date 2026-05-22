# tareas/views.py
import os
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.utils import timezone

from usuarios.decoradores import login_requerido, rol_requerido
from usuarios.models import Usuario
from .models import Tarea, Comentario, HistorialCambio, Calificacion
from .forms import TareaForm, EditarTareaForm, ComentarioForm, CalificacionForm


# ──────────────────────────────────────────────────────
# Helpers internos
# ──────────────────────────────────────────────────────

def _registrar_historial(tarea, accion, request):
    HistorialCambio.objects.create(
        tarea=tarea,
        accion=accion,
        usuarioCorreo=request.session.get('correo', ''),
        usuarioNombre=request.session.get('nombre', ''),
    )


def _guardar_adjuntos(tarea, archivos):
    """Guarda archivos en media/tareas_adjuntos/ y actualiza tarea.adjuntos."""
    carpeta = os.path.join(settings.MEDIA_ROOT, 'tareas_adjuntos')
    os.makedirs(carpeta, exist_ok=True)
    nombres = list(tarea.adjuntos or [])
    for f in archivos:
        ext = os.path.splitext(f.name)[1].lower()
        nombre = f"{uuid.uuid4().hex}{ext}"
        with open(os.path.join(carpeta, nombre), 'wb+') as dest:
            for chunk in f.chunks():
                dest.write(chunk)
        nombres.append({'original': f.name, 'guardado': nombre})
    tarea.adjuntos = nombres
    tarea.save()


# ──────────────────────────────────────────────────────
# LISTAR — Profesor ve todas; Estudiante ve las suyas
# ──────────────────────────────────────────────────────

@login_requerido
def listarTareas(request):
    correo = request.session.get('correo')
    rol    = request.session.get('rol')

    if rol == 'profesor':
        qs = Tarea.objects.filter(usuarioCorreo=correo)
    else:
        qs = Tarea.objects.filter(estudianteCorreo=correo)

    # ── Filtros GET ──
    estado    = request.GET.get('estado', '')
    prioridad = request.GET.get('prioridad', '')
    fecha     = request.GET.get('fecha', '')
    busqueda  = request.GET.get('q', '')
    usuario_f = request.GET.get('usuario', '')   # solo profesor

    if estado:
        qs = qs.filter(estadoTarea=estado)
    if prioridad:
        qs = qs.filter(prioridad=prioridad)
    if fecha:
        qs = qs.filter(fechaEntrega=fecha)
    if busqueda:
        qs = qs.filter(titulo__icontains=busqueda)
    if usuario_f and rol == 'profesor':
        qs = qs.filter(estudianteCorreo=usuario_f)

    # Estadísticas
    todas = (Tarea.objects.filter(usuarioCorreo=correo)
             if rol == 'profesor'
             else Tarea.objects.filter(estudianteCorreo=correo))

    estadisticas = {
        'total':      todas.count(),
        'pendientes': todas.filter(estadoTarea='pendiente').count(),
        'completadas': todas.filter(estadoTarea='completada').count(),
    }

    # Promedio académico (estudiante)
    notas = []
    if rol == 'estudiante':
        for t in todas:
            try:
                notas.append(t.calificacion.nota)
            except Calificacion.DoesNotExist:
                pass
        estadisticas['promedio'] = round(sum(notas) / len(notas), 2) if notas else None

    # Lista de estudiantes para filtro (profesor)
    estudiantes = []
    if rol == 'profesor':
        estudiantes = list(
            Usuario.objects.filter(rol='estudiante').values('correo', 'nombre', 'apellido')
        )

    contexto = {
        'tareas':      list(qs.order_by('-fechaCreacion')),
        'estadisticas': estadisticas,
        'estudiantes': estudiantes,
        'filtros': {
            'estado': estado, 'prioridad': prioridad,
            'fecha': fecha, 'q': busqueda, 'usuario': usuario_f,
        },
        'estados':     Tarea.ESTADOS,
        'prioridades': Tarea.PRIORIDADES,
    }
    return render(request, 'tareas/listar.html', contexto)


# ──────────────────────────────────────────────────────
# CREAR — solo profesor
# ──────────────────────────────────────────────────────

@rol_requerido('profesor')
def crearTarea(request):
    correo = request.session.get('correo')
    estudiantes = list(
        Usuario.objects.filter(rol='estudiante').values('correo', 'nombre', 'apellido')
    )

    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.usuarioCorreo = correo
            tarea.save()

            # Adjuntos
            archivos = request.FILES.getlist('adjuntos')
            if archivos:
                _guardar_adjuntos(tarea, archivos)

            _registrar_historial(tarea, 'Tarea creada', request)
            return redirect('listarTareas')
    else:
        form = TareaForm()

    return render(request, 'tareas/crear.html', {
        'form': form,
        'estudiantes': estudiantes,
    })


# ──────────────────────────────────────────────────────
# DETALLE + COMENTARIOS + CAMBIO DE ESTADO (estudiante)
# ──────────────────────────────────────────────────────

@login_requerido
def detalleTarea(request, tareaId):
    correo = request.session.get('correo')
    rol    = request.session.get('rol')
    tarea  = get_object_or_404(Tarea, id=tareaId)

    # Control de acceso: solo el profesor creador o el estudiante asignado
    if rol == 'profesor' and tarea.usuarioCorreo != correo:
        return redirect('listarTareas')
    if rol == 'estudiante' and tarea.estudianteCorreo != correo:
        return redirect('listarTareas')

    comentarios  = tarea.comentarios.order_by('fecha')
    historial    = tarea.historial.order_by('-fecha')
    try:
        calificacion = tarea.calificacion
    except Calificacion.DoesNotExist:
        calificacion = None

    # Cambio de estado desde estudiante
    if request.method == 'POST' and 'cambiar_estado' in request.POST:
        nuevo_estado = request.POST.get('nuevo_estado')
        opciones_estudiante = ['enProceso', 'entregada']
        if rol == 'estudiante' and nuevo_estado in opciones_estudiante:
            estado_anterior = tarea.get_estadoTarea_display()
            tarea.estadoTarea = nuevo_estado
            tarea.save()
            _registrar_historial(
                tarea,
                f'Estado cambiado de "{estado_anterior}" a "{tarea.get_estadoTarea_display()}"',
                request
            )
            return redirect('detalleTarea', tareaId=tareaId)

    # Comentario nuevo
    form_comentario = ComentarioForm()
    if request.method == 'POST' and 'enviar_comentario' in request.POST:
        form_comentario = ComentarioForm(request.POST)
        if form_comentario.is_valid():
            c = form_comentario.save(commit=False)
            c.tarea       = tarea
            c.autorCorreo = correo
            c.autorNombre = request.session.get('nombre', '')
            c.autorRol    = rol
            c.save()
            return redirect('detalleTarea', tareaId=tareaId)

    return render(request, 'tareas/detalle.html', {
        'tarea':          tarea,
        'comentarios':    comentarios,
        'historial':      historial,
        'calificacion':   calificacion,
        'form_comentario': form_comentario,
        'rol':            rol,
    })


# ──────────────────────────────────────────────────────
# EDITAR — solo profesor
# ──────────────────────────────────────────────────────

@rol_requerido('profesor')
def editarTarea(request, tareaId):
    correo = request.session.get('correo')
    tarea  = get_object_or_404(Tarea, id=tareaId, usuarioCorreo=correo)
    estudiantes = list(
        Usuario.objects.filter(rol='estudiante').values('correo', 'nombre', 'apellido')
    )

    if request.method == 'POST':
        estado_anterior = tarea.get_estadoTarea_display()
        form = EditarTareaForm(request.POST, instance=tarea)
        if form.is_valid():
            tarea_guardada = form.save()
            archivos = request.FILES.getlist('adjuntos')
            if archivos:
                _guardar_adjuntos(tarea_guardada, archivos)
            nuevo_estado = tarea_guardada.get_estadoTarea_display()
            if estado_anterior != nuevo_estado:
                _registrar_historial(
                    tarea_guardada,
                    f'Estado cambiado de "{estado_anterior}" a "{nuevo_estado}"',
                    request
                )
            else:
                _registrar_historial(tarea_guardada, 'Tarea editada', request)
            return redirect('detalleTarea', tareaId=tareaId)
    else:
        form = EditarTareaForm(instance=tarea)

    return render(request, 'tareas/editar.html', {
        'form': form,
        'tarea': tarea,
        'estudiantes': estudiantes,
    })


# ──────────────────────────────────────────────────────
# CAMBIAR ESTADO — solo profesor (desde detalle)
# ──────────────────────────────────────────────────────

@rol_requerido('profesor')
def cambiarEstado(request, tareaId):
    correo = request.session.get('correo')
    tarea  = get_object_or_404(Tarea, id=tareaId, usuarioCorreo=correo)

    if request.method == 'POST':
        nuevo = request.POST.get('estado')
        estados_validos = [e[0] for e in Tarea.ESTADOS]
        if nuevo in estados_validos:
            anterior = tarea.get_estadoTarea_display()
            tarea.estadoTarea = nuevo
            tarea.save()
            _registrar_historial(
                tarea,
                f'Estado cambiado de "{anterior}" a "{tarea.get_estadoTarea_display()}"',
                request
            )
    return redirect('detalleTarea', tareaId=tareaId)


# ──────────────────────────────────────────────────────
# CALIFICAR — solo profesor
# ──────────────────────────────────────────────────────

@rol_requerido('profesor')
def calificarTarea(request, tareaId):
    correo = request.session.get('correo')
    tarea  = get_object_or_404(Tarea, id=tareaId, usuarioCorreo=correo)

    try:
        calificacion = tarea.calificacion
    except Calificacion.DoesNotExist:
        calificacion = None

    if request.method == 'POST':
        form = CalificacionForm(request.POST, instance=calificacion)
        if form.is_valid():
            cal = form.save(commit=False)
            cal.tarea          = tarea
            cal.profesorCorreo = correo
            cal.profesorNombre = request.session.get('nombre', '')
            cal.save()
            # Marcar como completada automáticamente
            if tarea.estadoTarea != 'completada':
                tarea.estadoTarea = 'completada'
                tarea.save()
                _registrar_historial(tarea, f'Calificada con nota {cal.nota}', request)
            return redirect('detalleTarea', tareaId=tareaId)
    else:
        form = CalificacionForm(instance=calificacion)

    return render(request, 'tareas/calificar.html', {
        'form': form,
        'tarea': tarea,
        'calificacion': calificacion,
    })


# ──────────────────────────────────────────────────────
# ELIMINAR — solo profesor
# ──────────────────────────────────────────────────────

@rol_requerido('profesor')
def eliminarTarea(request, tareaId):
    correo = request.session.get('correo')
    tarea  = get_object_or_404(Tarea, id=tareaId, usuarioCorreo=correo)
    if request.method == 'POST':
        tarea.delete()
        return redirect('listarTareas')
    return render(request, 'tareas/eliminar.html', {'tarea': tarea})