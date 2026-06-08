import re
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from .models import SolicitudInformacion, Modificacion, Presupuesto

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


class ModificacionForm(forms.ModelForm):
    class Meta:
        model = Modificacion
        fields = [
            'motivo',
            'descripcion',
            'especificaciones',
            'adjunto',
            'contacto_nombre',
            'contacto_email',
            'codigo_seguimiento_cliente',
        ]
        widgets = {
            'motivo': forms.TextInput(attrs={'placeholder': 'Motivo de la modificación (breve)'}),
            'descripcion': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe la modificación que requieres...'}),
            'especificaciones': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Especificaciones técnicas o detalles...'}),
            'contacto_nombre': forms.TextInput(attrs={'placeholder': 'Tu nombre'}),
            'contacto_email': forms.EmailInput(attrs={'placeholder': 'Tu correo'}),
            'codigo_seguimiento_cliente': forms.TextInput(attrs={'readonly': 'readonly'}),
        }


class AgendarVisitaForm(forms.Form):
    nombre = forms.CharField(
        max_length=120,
        label='Nombre completo',
        widget=forms.TextInput(attrs={'placeholder': 'Tu nombre completo', 'class': 'form-control'})
    )
    rut = forms.CharField(
        max_length=12,
        label='RUT',
        validators=[RegexValidator(regex=r'^\d{7,8}-[\dkK]$', message='Ingrese un RUT válido, por ejemplo 12345678-9')],
        widget=forms.TextInput(attrs={'placeholder': '12.345.678-9', 'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'placeholder': 'tu@correo.cl', 'class': 'form-control'})
    )
    fecha_inicio_preferido = forms.DateField(
        label='Fecha de inicio preferida',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    fecha_fin_preferido = forms.DateField(
        label='Fecha de término preferida',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    telefono = forms.CharField(
        max_length=12,
        label='Número telefónico',
        widget=forms.TextInput(attrs={'placeholder': '56912345678', 'class': 'form-control'})
    )


class PesosChilenosWidget(forms.TextInput):
    """Widget que acepta formato de pesos chilenos (300.000, 1.500.000, etc)"""
    
    def __init__(self, attrs=None):
        default_attrs = {'placeholder': 'ej: 300.000 o 1.500.000 o 1.500.000,50'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)


class PesosChilenosField(forms.DecimalField):
    """Campo que acepta números con puntos como separador de miles"""
    
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = PesosChilenosWidget()
        kwargs.setdefault('max_digits', 12)
        kwargs.setdefault('decimal_places', 2)
        super().__init__(*args, **kwargs)
    
    def to_python(self, value):
        """Convierte valores en formato chileno a Decimal.

        - "300.000" => 300000
        - "300000" => 300000
        - "300000.00" => 300000.00
        - "300.000,50" => 300000.50
        """
        if value is None or value == '':
            return None

        if isinstance(value, str):
            value = value.strip()
            if ',' in value:
                last_comma_idx = value.rfind(',')
                value = value[:last_comma_idx].replace('.', '') + ',' + value[last_comma_idx+1:]
                value = value.replace(',', '.')
            elif '.' in value:
                integer_part, decimal_part = value.rsplit('.', 1)
                if len(decimal_part) == 3:
                    # 300.000 -> miles
                    value = value.replace('.', '')
                else:
                    # 300000.00 -> separador decimal
                    value = value.replace(',', '')
            
        return super().to_python(value)


class PresupuestoForm(forms.ModelForm):
    total = PesosChilenosField(required=False, label="Total (ej: 300.000)")
    
    class Meta:
        model = Presupuesto
        fields = '__all__'


class ModificacionAdminForm(forms.ModelForm):
    monto_adicional = PesosChilenosField(required=False, label="Monto Adicional (ej: 50.000)")
    admin_monto_propuesto = PesosChilenosField(required=False, label="Monto Propuesto (ej: 100.000)")
    
    class Meta:
        model = Modificacion
        fields = '__all__'
