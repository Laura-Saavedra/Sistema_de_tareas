from django import forms
from .models import Reporte


class ReporteForm(forms.ModelForm):

    class Meta:

        # Modelo que utilizará el formulario
        model = Reporte

        # Incluye todos los campos del modelo
        fields = '__all__'

        # Personalización visual de los campos
        widgets = {

            # Campo de texto para el ID
            'reporteId': forms.TextInput(
                attrs={
                    'placeholder': 'REP001'
                }
            ),

            # Campo de texto para el nombre
            'nombreReporte': forms.TextInput(
                attrs={
                    'placeholder':
                    'Ingrese nombre del reporte'
                }
            ),

            # Área de texto para descripción
            'descripcion': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder':
                    'Descripción del reporte'
                }
            ),

            # Campo numérico total usuarios
            'totalUsuarios': forms.NumberInput(
                attrs={
                    'placeholder': '0'
                }
            ),

            # Campo numérico total tareas
            'totalTareas': forms.NumberInput(
                attrs={
                    'placeholder': '0'
                }
            ),

            # Campo numérico tareas completadas
            'tareasCompletadas': forms.NumberInput(
                attrs={
                    'placeholder': '0'
                }
            ),

            # Campo numérico eficiencia
            'eficiencia': forms.NumberInput(
                attrs={
                    'placeholder': '0.00'
                }
            ),

            # Campo JSON de métricas adicionales
            'metricas': forms.Textarea(
                attrs={
                    'rows': 5,
                    'placeholder':
                    '{"usuarios_activos": 10}'
                }
            )
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

        self.fields['metricas'].initial = ''