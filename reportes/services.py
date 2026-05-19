from .models import Reporte
from datetime import datetime, time
#Importa manejo de zonas horarias.
import pytz

# Cada usuario solo puede tener máximo 3 reportes guardados
LIMITE_HISTORIAL = 3

def obtenerTareasPorUsuario(usuarioCorreo, fechaInicio=None, fechaFin=None):

    try:
        from tareas.models import Tarea
        #Busca todas las tareas del usuario.
        tareas = Tarea.objects.filter(usuarioCorreo=usuarioCorreo)
        #Solo generar información si las dos fechas existen
        if fechaInicio and fechaFin:
            bogota = pytz.timezone('America/Bogota')
            inicio = bogota.localize(datetime.combine(fechaInicio, time.min))
            fin = bogota.localize(datetime.combine(fechaFin, time.max))
            tareas = tareas.filter(
                fechaCreacion__gte=inicio,
                fechaCreacion__lte=fin
            )

        return list(tareas)

    except Exception as e:
        print("Error tareas:", e)
        return []


def obtenerAgendasPorUsuario(usuarioCorreo, fechaInicio=None, fechaFin=None):

    try:
        from agenda.models import Agenda

        agendas = Agenda.objects.filter(usuarioCorreo=usuarioCorreo)

        if fechaInicio and fechaFin:
            agendas = agendas.filter(
                fecha__gte=fechaInicio,
                fecha__lte=fechaFin
            )

        return list(agendas)

    except Exception as e:
        print("Error agendas:", e)
        return []

#len() retorna la cantidad de elementos de una lista.

def calcularResumenTareas(tareas):
     # Crear diccionario inicial
    resumen = {
        'total': len(tareas),
        'pendientes': 0,
        'enProceso': 0,
        'completadas': 0
    }
    # Recorrer cada agenda
    for t in tareas:
        if t.estadoTarea == 'pendiente':
            resumen['pendientes'] += 1
        elif t.estadoTarea == 'enProceso':
            resumen['enProceso'] += 1
        elif t.estadoTarea == 'completada':
            resumen['completadas'] += 1
    #Devolver resultado
    return resumen


def calcularResumenAgendas(agendas):
    resumen = {
        'total': len(agendas),
        'pendientes': 0,
        'completadas': 0,
        'canceladas': 0,
        'alta': 0
    }
    
    for a in agendas:
        if a.estado == 'pendiente':
            resumen['pendientes'] += 1
        elif a.estado == 'completada':
            resumen['completadas'] += 1
        elif a.estado == 'cancelada':
            resumen['canceladas'] += 1
        
        if a.prioridad == 'alta':
            resumen['alta'] += 1
    
    return resumen

#Compara tareas vs agendas
def calcularCruceDatos(tareas, agendas):
    #set se usa porque evita valores repetidos automáticamente: Si 3 agendas pertenecen a la misma tarea (tareaId=1), el set las cuenta como 1 sola tarea:
    tareasAgendadasIds = set()

    for agenda in agendas:
        ## Guarda el ID de la tarea relacionada
        tareasAgendadasIds.add(agenda.tareaId)

    tareasAgendadas = len(tareasAgendadasIds)
    tareasSinAgendar = len(tareas) - tareasAgendadas

    return {
        'tareasAgendadas': tareasAgendadas,
        'tareasSinAgendar': tareasSinAgendar
    }


def obtenerReporteUsuario(usuarioCorreo, fechaInicio=None, fechaFin=None):

    tareas = obtenerTareasPorUsuario(usuarioCorreo, fechaInicio, fechaFin)
    agendas = obtenerAgendasPorUsuario(usuarioCorreo, fechaInicio, fechaFin)

    resumenTareas = calcularResumenTareas(tareas)
    resumenAgendas = calcularResumenAgendas(agendas)
    cruce = calcularCruceDatos(tareas, agendas)

    return {
        'usuarioCorreo': usuarioCorreo,
        'fechaInicio': fechaInicio,
        'fechaFin': fechaFin,
        'resumenTareas': resumenTareas,
        'resumenAgendas': resumenAgendas,
        'cruce': cruce
    }


def guardarReporte(usuarioCorreo, resumenTareas, resumenAgendas, cruce, tipoReporte='mensual'):

    productividad = 0

    if resumenTareas['total'] > 0:
        productividad = round(
            (resumenTareas['completadas'] / resumenTareas['total']) * 100, 2
        )

    Reporte.objects.create(
        usuarioCorreo=usuarioCorreo,
        tipoReporte=tipoReporte,
        totalTareas=resumenTareas['total'],
        tareasPendientes=resumenTareas['pendientes'],
        tareasEnProceso=resumenTareas['enProceso'],
        tareasCompletadas=resumenTareas['completadas'],
        totalAgendas=resumenAgendas['total'],
        agendasPendientes=resumenAgendas['pendientes'],
        agendasCompletadas=resumenAgendas['completadas'],
        agendasCanceladas=resumenAgendas['canceladas'],
        agendasAltaPrioridad=resumenAgendas['alta'],
        tareasAgendadas=cruce['tareasAgendadas'],
        tareasSinAgendar=cruce['tareasSinAgendar'],
        productividad=productividad
    )

    reportes = Reporte.objects.filter(
        usuarioCorreo=usuarioCorreo
    ).order_by('-fechaGeneracion')

    if reportes.count() > LIMITE_HISTORIAL:
        ids_eliminar = reportes[LIMITE_HISTORIAL:]
        for r in ids_eliminar:
            r.delete()


def obtenerHistorialReportes(usuarioCorreo):

    return list(
        Reporte.objects.filter(
            usuarioCorreo=usuarioCorreo
        ).order_by('-fechaGeneracion')[:LIMITE_HISTORIAL]
    )