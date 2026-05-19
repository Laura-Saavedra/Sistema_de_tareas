from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from .forms import GenerarReporteForm
from .services import (
    obtenerReporteUsuario,
    guardarReporte,
    obtenerHistorialReportes
)

def generarReporte(request):

    if not request.session.get('correo'):
        return redirect('/usuarios/login/')
    reporte = None

    # Verifica si es formulario fue enviado
    if request.method == 'POST':
        #Crea formularios -- request.POST contiene los inputs del formulario.
        form = GenerarReporteForm(request.POST)

        if form.is_valid():

            usuarioCorreo = request.session.get('correo')
            fechaInicio = form.cleaned_data['fechaInicio']
            fechaFin = form.cleaned_data['fechaFin']
            #Llama la función que genera el reporte.
            reporte = obtenerReporteUsuario(
                usuarioCorreo,
                fechaInicio,
                fechaFin
            )

            if (
                reporte['resumenTareas']['total'] == 0 and
                reporte['resumenAgendas']['total'] == 0
            ):
                return render(request, 'reportes/reporteUsuario.html', {
                    'form': form,
                    'reporte': None,
                    'sin_datos': True
                })
            else:
                # Guardar solo si hay datos
                guardarReporte(
                    usuarioCorreo=usuarioCorreo,
                    resumenTareas=reporte['resumenTareas'],
                    resumenAgendas=reporte['resumenAgendas'],
                    cruce=reporte['cruce']
                )

    else:
        form = GenerarReporteForm()

    return render(
        request,
        'reportes/reporteUsuario.html',
        {
            'form': form,
            'reporte': reporte
        }
    )

class HistorialReportesView(View):
    #Obtener el historial de reportes del usuario que actualmente tiene la sesión iniciada
    def get(self, request):

        if not request.session.get('correo'):
            return redirect('/usuarios/login/')

        usuarioCorreo = request.session.get('correo')
        #Busca historial de reportes del usuario.
        historial = obtenerHistorialReportes(usuarioCorreo)

        return render(
            request,
            'reportes/historialReportes.html',
            {
                'historial': historial
            }
        )