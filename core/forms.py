import re
from django import forms
from django.core.exceptions import ValidationError
from .models import SolicitudInformacion

class SolicitarInfoForm(forms.ModelForm):

    requerimientos = forms.CharField(
        label="Requerimientos (habitaciones, metros cuadrados, especificaciones técnicas, etc.)",
        widget=forms.Textarea
    )

    class Meta:
        model = SolicitudInformacion
        fields = [
            'nombre',
            'email',
            'telefono',
            'tienes_terreno',
            'ubicacion',
            'cuando_comenzar',
            'requerimientos'
        ]

        widgets = {
            'tienes_terreno': forms.Select(choices=[
                ('si', 'Sí'),
                ('no', 'No'),
            ]),

            'cuando_comenzar': forms.Select(choices=[
                ('inmediato', 'Inmediato'),
                ('1_mes', 'En un mes'),
                ('3_meses', 'En tres meses'),
                ('otro', 'Otro'),
            ]),
        }

    def clean_requerimientos(self):
        data = self.cleaned_data.get('requerimientos', '')
        pattern = r"(select|insert|update|delete|drop|;|--|\bunion\b)"
        if re.search(pattern, data, re.IGNORECASE):
            raise ValidationError("El texto contiene caracteres o palabras no permitidas.")
        return data
