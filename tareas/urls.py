from django.urls import path
from . import views

urlpatterns = [
    path('crear/', views.crearTarea, name='crearTarea'),
    path('listar/', views.listarTareas.as_view(), name='listarTareas'),
    path('editar/<str:tareaId>/', views.editarTarea, name='editarTarea'),
    path('eliminar/<str:tareaId>/', views.eliminarTarea, name='eliminarTarea'),
    path('detalle/<str:tareaId>/', views.detalleTarea, name='detalleTarea'),
]