from django.urls import path
from . import views

urlpatterns = [
    path('generar/', views.generarReporte, name='generarReporte'),
    path('historial/', views.HistorialReportesView.as_view(), name='historialReportes'),
]