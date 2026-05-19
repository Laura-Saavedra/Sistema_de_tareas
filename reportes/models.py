from djongo import models
class Reporte(models.Model):

    usuarioCorreo = models.CharField(max_length=200)
    fechaGeneracion = models.DateTimeField(auto_now_add=True)
    tipoReporte = models.CharField(max_length=20, default='mensual')

    totalTareas = models.IntegerField(default=0)
    tareasPendientes = models.IntegerField(default=0)
    tareasEnProceso = models.IntegerField(default=0)
    tareasCompletadas = models.IntegerField(default=0)

    totalAgendas = models.IntegerField(default=0)
    agendasPendientes = models.IntegerField(default=0)
    agendasCompletadas = models.IntegerField(default=0)
    agendasCanceladas = models.IntegerField(default=0)
    agendasAltaPrioridad = models.IntegerField(default=0)

    tareasAgendadas = models.IntegerField(default=0)
    tareasSinAgendar = models.IntegerField(default=0)
    productividad = models.FloatField(default=0)

    def __str__(self):
        return f"{self.usuarioCorreo} - {self.fechaGeneracion}"