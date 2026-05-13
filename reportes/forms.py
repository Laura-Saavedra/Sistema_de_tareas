from django import forms
from .models import Reporte


class ReporteForm(forms.ModelForm):

    class Meta:
        model = Reporte


        fields = '__all__'

        widgets = {

            'reporteId': forms.TextInput(
                attrs={
                    'placeholder': 'REP001'
                }
            ),

            'nombreReporte': forms.TextInput(
                attrs={
                    'placeholder':
                    'Ingrese nombre del reporte'
                }
            ),

            'descripcion': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder':
                    'Descripción del reporte'
                }
            ),


            'totalUsuarios': forms.NumberInput(
                attrs={
                    'placeholder': '0'
                }
            ),

            'totalTareas': forms.NumberInput(
                attrs={
                    'placeholder': '0'
                }
            ),

            'tareasCompletadas': forms.NumberInput(
                attrs={
                    'placeholder': '0'
                }
            ),

            'eficiencia': forms.NumberInput(
                attrs={
                    'placeholder': '0.00'
                }
            ),
        }

    # Permite modificar valores iniciales
    def __init__(self, *args, **kwargs):

        # Inicializa correctamente la clase padre
        super().__init__(*args, **kwargs)

        # 0 y {}
        self.fields['totalUsuarios'].initial = ''
        self.fields['totalTareas'].initial = ''
        self.fields['tareasCompletadas'].initial = ''
        self.fields['eficiencia'].initial = ''