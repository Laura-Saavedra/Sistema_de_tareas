from djongo import models
import random
import string


def generar_codigo():
    """Genera un código de 6 dígitos para verificación de correo."""
    return ''.join(random.choices(string.digits, k=6))


class Usuario(models.Model):

    ROLES = [
        ('profesor', 'Profesor'),
        ('estudiante', 'Estudiante'),
    ]

    # Datos básicos
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    password = models.CharField(max_length=265)

    # Rol del usuario
    rol = models.CharField(max_length=20, choices=ROLES, default='estudiante')

    # Foto de perfil — ruta relativa dentro de MEDIA_ROOT
    foto_perfil = models.CharField(max_length=300, blank=True, default='')

    # Verificación de correo
    verificado = models.BooleanField(default=False)
    codigo_verificacion = models.CharField(max_length=6, blank=True, default='')

    # Estado de la cuenta
    activo = models.BooleanField(default=True)

    # Fecha de registro
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.nombre} {self.apellido} ({self.rol})"

    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"

    def generar_nuevo_codigo(self):
        """Genera y guarda un código de verificación nuevo."""
        self.codigo_verificacion = generar_codigo()
        self.save()
        return self.codigo_verificacion
    
