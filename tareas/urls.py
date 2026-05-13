from django.urls import path
from . import views

urlpatterns = [

    path('crear/', views.crearTarea, name='crearTareas'),

    path('listar/', views.listarTareas.as_view(), name='listarTareas'),

    path('editar/<int:tareaId>/', views.editarTarea),

    path('eliminar/<int:tareaId>/', views.eliminarTarea),

    path('detalle/<int:tareaId>/', views.detalleTarea),
]