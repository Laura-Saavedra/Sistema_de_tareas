from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic import ListView
from django.views.generic import CreateView


from django.urls import reverse_lazy
from .models import Reporte
from .forms import ReporteForm

# Vista basada en clase para listar reportes
class ListaReportesView(ListView):

    model = Reporte

    template_name = 'reportes/lista.html'

    context_object_name = 'reportes'

def detalle_reporte(request, reporte_id):
    """
    Muestra el detalle de un reporte
    """

    reporte = get_object_or_404(
        Reporte,
        reporteId=reporte_id
    )

    return render(request, 'reportes/detalle.html', {
        'reporte': reporte
    })


class CrearReporteView(CreateView):

    model = Reporte
    form_class = ReporteForm
    template_name = 'reportes/crear.html'

    # Redirección después de guardar
    success_url = reverse_lazy('lista_reportes')


def generar_reporte(request):
    """
    Vista preparada para futura integración
    con Usuarios, Tareas y Agenda.
    """

    contexto = {

        'mensaje':
        'Pendiente integración con otras aplicaciones'
    }

    return render(
        request,
        'reportes/generar.html',
        contexto
    )
def editar_reporte(request, reporte_id):
    """
    Edita un reporte existente
    """

    reporte = get_object_or_404(
        Reporte,
        reporteId=reporte_id
    )

    if request.method == 'POST':

        form = ReporteForm(
            request.POST,
            instance=reporte
        )

        if form.is_valid():

            form.save()

            return redirect(
                'detalle_reporte',
                reporte_id=reporte.reporteId
            )

    else:

        form = ReporteForm(instance=reporte)

    return render(
        request,
        'reportes/editar.html',
        {
            'form': form,
            'reporte': reporte
        }
    )

def eliminar_reporte(request, reporte_id):
    """
    Elimina un reporte
    """

    reporte = get_object_or_404(
        Reporte,
        reporteId=reporte_id
    )

    if request.method == 'POST':

        reporte.delete()

        return redirect('lista_reportes')

    return render(
        request,
        'reportes/eliminar.html',
        {
            'reporte': reporte
        }
    )

"""
def lista_reportes(request):
    
    # Obtiene todos los reportes
    reportes = Reporte.objects.all()

    return render(request, 'reportes/lista.html', {
        'reportes': reportes
    })


def crear_reporte(request):
    
    # Verifica si el formulario fue enviado
    if request.method == 'POST':

        # Carga datos del formulario
        form = ReporteForm(request.POST)

        # Valida los datos
        if form.is_valid():

            # Guarda el reporte
            form.save()

            # Redirecciona a la lista
            return redirect('lista_reportes')

    else:

        # Muestra formulario vacío
        form = ReporteForm()

    return render(request, 'reportes/crear.html', {
        'form': form
    })
"""