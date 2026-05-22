# tareas/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('',                              views.listarTareas,  name='listarTareas'),
    path('listar/',                       views.listarTareas,  name='listarTareas'),
    path('crear/',                        views.crearTarea,    name='crearTarea'),
    path('detalle/<str:tareaId>/',        views.detalleTarea,  name='detalleTarea'),
    path('editar/<str:tareaId>/',         views.editarTarea,   name='editarTarea'),
    path('eliminar/<str:tareaId>/',       views.eliminarTarea, name='eliminarTarea'),
    path('estado/<str:tareaId>/',         views.cambiarEstado, name='cambiarEstado'),
    path('calificar/<str:tareaId>/',      views.calificarTarea, name='calificarTarea'),
]