# tareas/admin.py
from django.contrib import admin
from .models import Tarea, Comentario, HistorialCambio, Calificacion

admin.site.register(Tarea)
admin.site.register(Comentario)
admin.site.register(HistorialCambio)
admin.site.register(Calificacion)