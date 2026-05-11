from django.urls import path
from . import views

urlpatterns = [

    path('crear/', views.crearTarea),

    path('listar/', views.listarTareas),

    path('editar/<int:tareaId>/', views.editarTarea),

    path('eliminar/<int:tareaId>/', views.eliminarTarea),

    path('detalle/<int:tareaId>/', views.detalleTarea),
]