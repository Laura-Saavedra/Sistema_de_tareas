from djongo import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError



class Reporte(models.Model):

    reporteId = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="ID del reporte"
    )


    nombreReporte = models.CharField(
        max_length=200,
        verbose_name="Nombre del reporte"
    )


    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción"
    )

    fechaGeneracion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de generación"
    )


    totalUsuarios = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Total usuarios"
    )

    totalTareas = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Total tareas"
    )


    tareasCompletadas = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Tareas completadas"
    )

    eficiencia = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ],
        verbose_name="Eficiencia (%)"
    )

    activo = models.BooleanField(
        default=True,
        verbose_name="Reporte activo"
    )
    
    fechaActualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de actualización"
    )

    class Meta:
        """
        Configuración adicional del modelo
        """
        db_table = "reportes"

        # Nombre singular mostrado en Django Admin
        verbose_name = "Reporte"

        # Nombre plural mostrado en Django Admin
        verbose_name_plural = "Reportes"

        # Ordena los reportes del más reciente al más antiguo
        ordering = ['-fechaGeneracion']

    def clean(self):
        """
        Validación personalizada del modelo.
        Evita que las tareas completadas sean mayores
        al total de tareas.
        """

        if self.tareasCompletadas > self.totalTareas:
            raise ValidationError(
                "Las tareas completadas no pueden ser mayores al total de tareas."
            )

    def __str__(self):
        """
        Representación en texto del objeto.
        Se muestra en Django Admin y consultas.
        """

        return f"{self.reporteId} - {self.nombreReporte}"