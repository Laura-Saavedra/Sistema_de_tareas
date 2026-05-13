from django.contrib import admin
from .models import Reporte


@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):

    list_display = (
        'reporteId',
        'nombreReporte',
        'totalUsuarios',
        'totalTareas',
        'tareasCompletadas',
        'eficiencia',
        'activo'
    )

    search_fields = (
        'reporteId',
        'nombreReporte'
    )

    list_filter = (
        'activo',
        'fechaGeneracion'
    )