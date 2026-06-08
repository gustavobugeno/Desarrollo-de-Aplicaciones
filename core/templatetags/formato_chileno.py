from django import template
from decimal import Decimal, InvalidOperation

register = template.Library()


def normalize_chilean_number(value):
    if isinstance(value, str):
        value = value.strip()
        if ',' in value:
            if '.' in value:
                # 1.500.000,50 -> 1500000.50
                value = value.replace('.', '').replace(',', '.')
            else:
                # 150000,50 -> 150000.50
                value = value.replace(',', '.')
        elif '.' in value:
            integer_part, decimal_part = value.rsplit('.', 1)
            if len(decimal_part) == 3:
                # 300.000 -> 300000
                value = value.replace('.', '')
        return value
    return value


@register.filter
def pesos_chilenos(value):
    """Formatea un número como pesos chilenos (CLP)"""
    if value is None or value == '':
        return '$0'

    try:
        if isinstance(value, str):
            value = normalize_chilean_number(value)
        value = Decimal(value)

        if value == value.to_integral_value():
            formatted = f"{int(value):,}".replace(',', '.')
            return f"${formatted}"

        quantized = value.quantize(Decimal('0.01'))
        integer_part, decimal_part = f"{quantized:.2f}".split('.')
        integer_part = f"{int(integer_part):,}".replace(',', '.')
        return f"${integer_part},{decimal_part}"
    except (InvalidOperation, ValueError, TypeError):
        return value
