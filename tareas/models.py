from djongo import models


class Tarea(models.Model):

    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('enProceso', 'En Proceso'),
        ('completada', 'Completada')
    ]

    titulo = models.CharField(
        max_length=100
    )

    descripcion = models.TextField()

    estadoTarea = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default='pendiente'
    )

    usuarioCorreo = models.CharField(
        max_length=200
    )

    fechaCreacion = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.titulo