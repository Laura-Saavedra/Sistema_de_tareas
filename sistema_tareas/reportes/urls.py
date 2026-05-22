from django.urls import path
from . import views 

from .views import (
    ListaReportesView,
    CrearReporteView
)

urlpatterns = [

    path(
        '',
        ListaReportesView.as_view(),
        name='lista_reportes'
    ),

    path(
        'crear/',
        CrearReporteView.as_view(),
        name='crear_reporte'
    ),

    path(
        'generar/',
        views.generacion_automatica,
        name='generar_reporte'
    ),
    path(
        '<str:reporte_id>/',
        views.detalle_reporte,
        name='detalle_reporte'
    ),
    path(
    'editar/<str:reporte_id>/',
    views.editar_reporte,
    name='editar_reporte'
    ),

    path(
    'eliminar/<str:reporte_id>/',
    views.eliminar_reporte,
    name='eliminar_reporte'
    ),
]