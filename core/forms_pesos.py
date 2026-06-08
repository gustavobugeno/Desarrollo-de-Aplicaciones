from django import forms

# -----------------------------------
# WIDGET Y FIELD PARA PESOS CHILENOS
# -----------------------------------
class PesosChilenosWidget(forms.TextInput):
    """Widget que acepta formato de pesos chilenos (300.000, 1.500.000, etc) y lo convierte a número decimal"""
    
    def __init__(self, attrs=None):
        default_attrs = {'placeholder': 'ej: 300.000 o 1.500.000 o 1.500.000,50'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)


class PesosChilenosField(forms.DecimalField):
    """Campo que acepta números con puntos como separador de miles (300.000, 1.500.000, etc)"""
    
    def __init__(self, *args, **kwargs):
        kwargs['widget'] = PesosChilenosWidget()
        # Asegurar que acepta números grandes (hasta 9.999.999.999,99)
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
                    value = value.replace('.', '')
                else:
                    value = value.replace(',', '')

        return super().to_python(value)
