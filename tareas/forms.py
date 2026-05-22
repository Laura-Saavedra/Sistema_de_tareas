# tareas/forms.py
from django import forms
from .models import Tarea, Comentario, Calificacion


class TareaForm(forms.ModelForm):
    class Meta:
        model  = Tarea
        fields = ['titulo', 'descripcion', 'prioridad', 'fechaEntrega', 'estudianteCorreo']
        widgets = {
            'fechaEntrega': forms.DateInput(attrs={'type': 'date'}),
            'descripcion':  forms.Textarea(attrs={'rows': 4}),
        }


class EditarTareaForm(forms.ModelForm):
    """Para editar, el profesor puede también cambiar el estado."""
    class Meta:
        model  = Tarea
        fields = ['titulo', 'descripcion', 'prioridad', 'fechaEntrega',
                  'estudianteCorreo', 'estadoTarea']
        widgets = {
            'fechaEntrega': forms.DateInput(attrs={'type': 'date'}),
            'descripcion':  forms.Textarea(attrs={'rows': 4}),
        }


class ComentarioForm(forms.ModelForm):
    class Meta:
        model  = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escribe un comentario...'}),
        }


class CalificacionForm(forms.ModelForm):
    class Meta:
        model  = Calificacion
        fields = ['nota', 'observaciones']
        widgets = {
            'nota':          forms.NumberInput(attrs={'min': 0, 'max': 5, 'step': '0.1'}),
            'observaciones': forms.Textarea(attrs={'rows': 3}),
        }