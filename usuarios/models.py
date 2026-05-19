from djongo import models

class Usuario(models.Model):

    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    

    def __str__(self):
        return f"{self.nombre} {self.apellido}"