# tareas/models.py
from djongo import models


class Tarea(models.Model):

    ESTADOS = [
        ('pendiente',  'Pendiente'),
        ('enProceso',  'En Proceso'),
        ('entregada',  'Entregada'),
        ('revisada',   'Revisada'),
        ('completada', 'Completada'),
        ('vencida',    'Vencida'),
    ]

    PRIORIDADES = [
        ('baja',    'Baja'),
        ('media',   'Media'),
        ('alta',    'Alta'),
        ('urgente', 'Urgente'),
    ]

    titulo          = models.CharField(max_length=200)
    descripcion     = models.TextField(blank=True, default='')
    estadoTarea     = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    prioridad       = models.CharField(max_length=20, choices=PRIORIDADES, default='media')
    fechaEntrega    = models.DateField(null=True, blank=True)

    # Quién la creó (correo del profesor)
    usuarioCorreo   = models.CharField(max_length=200)

    # Estudiante asignado (correo)
    estudianteCorreo = models.CharField(max_length=200, blank=True, default='')

    # Adjuntos: lista de nombres de archivo (guardados en media/tareas_adjuntos/)
    adjuntos        = models.JSONField(default=list, blank=True)

    fechaCreacion   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class Comentario(models.Model):
    tarea       = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='comentarios')
    autorCorreo = models.CharField(max_length=200)
    autorNombre = models.CharField(max_length=200)
    autorRol    = models.CharField(max_length=20)   # 'profesor' | 'estudiante'
    texto       = models.TextField()
    fecha       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.autorRol}] {self.autorNombre}: {self.texto[:40]}"


class HistorialCambio(models.Model):
    tarea       = models.ForeignKey(Tarea, on_delete=models.CASCADE, related_name='historial')
    accion      = models.CharField(max_length=300)
    usuarioCorreo = models.CharField(max_length=200)
    usuarioNombre = models.CharField(max_length=200)
    fecha       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.accion} — {self.usuarioNombre}"


class Calificacion(models.Model):
    tarea           = models.OneToOneField(Tarea, on_delete=models.CASCADE, related_name='calificacion')
    nota            = models.FloatField()          # 0.0 – 5.0
    observaciones   = models.TextField(blank=True, default='')
    profesorCorreo  = models.CharField(max_length=200)
    profesorNombre  = models.CharField(max_length=200)
    fecha           = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Nota {self.nota} — {self.tarea.titulo}"