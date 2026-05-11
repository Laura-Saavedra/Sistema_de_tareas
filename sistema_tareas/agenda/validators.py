from django.core.exceptions import ValidationError
from django.utils import timezone

def validarFecha(value):
    hoy = timezone.now().date()
    if value < hoy:
        raise ValidationError("La fecha no puede ser anterior al día de hoy.")