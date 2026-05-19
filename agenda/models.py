from djongo import models
from .validators import validarFecha

class Agenda(models.Model):

    PRIORIDAD_CHOICES = [
        ('alta', 'Alta'),
        ('media', 'Media'),
        ('baja', 'Baja'),
    ]

    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]

    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    fecha = models.DateField(validators=[validarFecha])     
    hora = models.TimeField()
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='media')
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='pendiente')
    recordatorioActivo = models.BooleanField(default=False)
    tareaId = models.CharField(max_length=100)
    usuarioCorreo = models.CharField(max_length=200)
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

    class Meta:
        app_label = 'agenda'