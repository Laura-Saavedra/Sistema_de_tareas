from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListarAgendasView.as_view(), name='listar_agendas'),
    path('pendientes/', views.agendarPendientes, name='agendas_pendientes'),
    path('nueva/', views.buscarUsuario, name='buscar_usuario'),
    path('crear/', views.crearAgenda, name='crear_agenda'),
    path('detalle/<str:agenda_id>/', views.detalleAgenda, name='detalle_agenda'),
    path('editar/<str:agenda_id>/', views.editarAgenda, name='editar_agenda'),
    path('eliminar/<str:agenda_id>/', views.eliminarAgenda, name='eliminar_agenda'),
]