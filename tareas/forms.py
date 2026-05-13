from django import forms
from .models import Tarea


class TareaForm(forms.ModelForm):

    class Meta:

        model = Tarea

        fields = [
            'titulo',
            'descripcion',
            'estado',
            'prioridad',
            'categoria',
            'fechaEntrega',
            'usuarioId'
        ]

        widgets = {

            'fechaEntrega': forms.DateInput(
                attrs={'type': 'date'}
            )
        }