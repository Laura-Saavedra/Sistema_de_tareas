from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('agenda/', include('agenda.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('tareas/', include('tareas.urls')),
    path('reportes/', include('reportes.urls')),
]