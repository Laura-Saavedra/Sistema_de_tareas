from djongo import models


class Tarea(models.Model):

    ESTADOS = [

        ('pendiente', 'Pendiente'),
        ('enProceso', 'En Proceso'),
        ('completada', 'Completada')
    ]

    PRIORIDADES = [

        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta')
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

    prioridad = models.CharField(
        max_length=10,
        choices=PRIORIDADES,
        default='media'
    )

    fechaEntrega = models.DateField()

    usuarioResponsableId = models.IntegerField()

    fechaCreacion = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return self.titulo
        