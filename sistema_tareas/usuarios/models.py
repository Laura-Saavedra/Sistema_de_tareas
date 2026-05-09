from django.db import models

class Usuario(models.Model):

    nombre = models.CharField(
        max_length=100
    )

    apellido = models.CharField(
        max_length=100
    )

    correo = models.EmailField(
        unique=True
    )

    password = models.CharField(
        max_length=100
    )

    telefono = models.CharField(
        max_length=20
    )

    direccion = models.CharField(
        max_length=200
    )

    ciudad = models.CharField(
        max_length=100
    )

    pais = models.CharField(
        max_length=100
    )

    edad = models.IntegerField()

    activo = models.BooleanField(
        default=True
    )

    fechaRegistro = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return f"{self.nombre} {self.apellido}"
