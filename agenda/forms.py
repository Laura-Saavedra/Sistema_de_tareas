from django import forms
from .models import Agenda
from .validators import validarFecha


class AgendaForm(forms.Form):
    titulo = forms.CharField(label="Título", max_length=200)
    descripcion = forms.CharField(label="Descripción", widget=forms.Textarea)
    fecha = forms.DateField(
        label="Fecha",
        widget=forms.DateInput(attrs={'type': 'date'}),
        validators=[validarFecha]
    )
    hora = forms.TimeField(
        label="Hora",
        widget=forms.TimeInput(attrs={'type': 'time'})
    )
    prioridad = forms.ChoiceField(
        label="Prioridad",
        choices=Agenda.PRIORIDAD_CHOICES
    )
    estado = forms.ChoiceField(
        label="Estado",
        choices=Agenda.ESTADO_CHOICES
    )
    recordatorioActivo = forms.BooleanField(
        label="Recordatorio activo",
        required=False
    )