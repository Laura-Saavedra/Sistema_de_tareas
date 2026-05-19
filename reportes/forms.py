from django import forms

class GenerarReporteForm(forms.Form):

    fechaInicio = forms.DateField(
        label='Fecha inicio',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    fechaFin = forms.DateField(
        label='Fecha fin',
        widget=forms.DateInput(attrs={'type': 'date'})
    )