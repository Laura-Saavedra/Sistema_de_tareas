from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError



class Reporte(models.Model):
    """
    Modelo que representa los reportes generados por el sistema.
    Guarda métricas y estadísticas relacionadas con usuarios y tareas.
    """

    # Identificador único del reporte
    # unique=True evita IDs repetidos
    reporteId = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="ID del reporte"
    )

    # Nombre principal del reporte
    nombreReporte = models.CharField(
        max_length=200,
        verbose_name="Nombre del reporte"
    )

    # Descripción opcional del reporte
    # blank=True permite dejar el campo vacío en formularios
    # null=True permite guardar NULL en la base de datos
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descripción"
    )

    # Fecha automática de creación del reporte
    # auto_now_add=True guarda la fecha solo al crear el registro
    fechaGeneracion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de generación"
    )

    # Total de usuarios registrados en el reporte
    # PositiveIntegerField evita números negativos
    totalUsuarios = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Total usuarios"
    )

    # Total de tareas registradas
    totalTareas = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Total tareas"
    )

    # Cantidad de tareas completadas
    tareasCompletadas = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Tareas completadas"
    )

    # Porcentaje de eficiencia del sistema
    # max_digits=5 permite valores como 100.00
    # decimal_places=2 limita a 2 decimales
    eficiencia = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100)
        ],
        verbose_name="Eficiencia (%)"
    )

    # Estado del reporte
    # True = activo / False = inactivo
    activo = models.BooleanField(
        default=True,
        verbose_name="Reporte activo"
    )

    # Campo flexible para almacenar métricas dinámicas en formato JSON
    # default=dict crea un diccionario vacío por defecto
    metricas = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Métricas adicionales"
    )

    # Fecha automática de actualización
    # auto_now=True se actualiza cada vez que el registro cambia
    fechaActualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de actualización"
    )

    class Meta:
        """
        Configuración adicional del modelo
        """

        # Nombre real de la tabla en la base de datos
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