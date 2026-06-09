import random
import string
from django.db import models
from django.core.validators import RegexValidator



def generar_codigo():
    año = "2025"
    numero = ''.join(random.choices(string.digits, k=5))
    return f"CBC-{año}-{numero}"


class Servicio(models.Model):
    titulo = models.CharField("Nombre del Servicio", max_length=100)
    descripcion = models.TextField("Descripción", blank=True, null=True)

    imagen = models.ImageField(
    upload_to='servicios/imagenes_extra/'
)

    def __str__(self):
        return self.titulo


class SolicitudInformacion(models.Model):
    ESTADOS = [
        ('no_revisada', 'Pendiente de revisión'),
        ('revisada', 'En revisión'),
        ('aceptada', 'Aceptada'),
        ('en_ejecucion', 'En ejecución'),
        ('rechazada', 'Rechazada'),
        ('asignada', 'Experto asignado'),
        ('cotizada', 'Cotización generada'),
        ('enviada', 'Cotización enviada'),
        ('mod_creada', 'Modificación: Creada'),
        ('mod_en_revision', 'Modificación: En revisión'),
        ('mod_aceptada', 'Modificación: Aceptada'),
        ('mod_rechazada', 'Modificación: Rechazada'),
        ('pago_inicial', 'Pago 50% Inicial'),
        ('completado', 'Completado'),
        ('pagada', 'Pagada'),
    ]

    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.CASCADE,
        related_name="solicitudes",
        null=True,
        blank=True,
    )

    nombre = models.CharField(max_length=100)
    email = models.EmailField()

    telefono = models.CharField(
        max_length=12,
        validators=[
            RegexValidator(
                regex=r'^569\d{8}$',
                message="El teléfono debe tener el formato 569XXXXXXXX",
            ),
        ],
    )

    tienes_terreno = models.CharField(
        max_length=10,
        choices=[('si', 'Sí'), ('no', 'No')],
        default='no'
    )

    ubicacion = models.CharField(max_length=255)
    cuando_comenzar = models.CharField(max_length=20)
    requerimientos = models.TextField()

    estado = models.CharField(max_length=20, choices=ESTADOS, default='no_revisada')
    fecha_envio = models.DateTimeField(auto_now_add=True)

    codigo_seguimiento = models.CharField(max_length=30, unique=True, blank=True)
    comentarios_cambios = models.TextField(blank=True, null=True)
    progreso_trabajo = models.IntegerField(default=0, help_text="Porcentaje de progreso (0-100)")
    fecha_estimado_finalizacion = models.DateField(blank=True, null=True, help_text="Fecha estimada de finalización del proyecto")

    def save(self, *args, **kwargs):
        if not self.codigo_seguimiento:
            self.codigo_seguimiento = generar_codigo()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} - {self.codigo_seguimiento}"


class ImagenServicio(models.Model):
    servicio = models.ForeignKey(
        Servicio, related_name='imagenes_extra', on_delete=models.CASCADE
    )
    imagen = models.ImageField(
    upload_to='servicios/imagenes_extra/'
)

    def __str__(self):
        return f"Imagen de {self.servicio.titulo}"


class Presupuesto(models.Model):
    solicitud = models.OneToOneField(
        SolicitudInformacion,
        on_delete=models.CASCADE,
        related_name='presupuesto'
    )

    archivo = models.FileField(
    upload_to='presupuestos/'
)

    fecha = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Presupuesto de {self.solicitud.codigo_seguimiento}"


class Visita(models.Model):
    ESTADOS_VISITA = [
        ('pendiente', 'Solicitud creada'),
        ('propuesta', 'En revisión'),
        ('confirmada', 'Aceptada'),
        ('rechazada', 'Solicitud rechazada'),
    ]

    codigo = models.CharField(max_length=30, unique=True, blank=True)
    nombre = models.CharField(max_length=120)
    rut = models.CharField(max_length=12)
    email = models.EmailField()
    telefono = models.CharField(max_length=12)
    fecha_inicio_preferido = models.DateField()
    fecha_fin_preferido = models.DateField()
    fecha_inicio_propuesta = models.DateField(blank=True, null=True)
    fecha_fin_propuesta = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_VISITA, default='pendiente')
    evidencia = models.ImageField(upload_to='visitas/evidencias/', blank=True, null=True)
    evidencia_observaciones = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = self._generar_codigo_visita()
        super().save(*args, **kwargs)

    def _generar_codigo_visita(self):
        prefijo = 'VIS'
        numero = ''.join(random.choices(string.digits, k=5))
        return f"{prefijo}-{numero}"

    def __str__(self):
        return f"Visita {self.codigo} - {self.nombre}"

    @property
    def estado_publico(self):
        return {
            'pendiente': 'Solicitud creada',
            'propuesta': 'En revisión',
            'confirmada': 'Aceptada',
            'rechazada': 'Solicitud rechazada',
        }.get(self.estado, 'Solicitud creada')

    @property
    def paso_estado(self):
        return {
            'pendiente': 1,
            'propuesta': 2,
            'confirmada': 3,
            'rechazada': 0,
        }.get(self.estado, 1)

    @property
    def fecha_reflejada(self):
        return bool(self.fecha_inicio_propuesta and self.fecha_fin_propuesta)


class Modificacion(models.Model):
    solicitud = models.ForeignKey(
        SolicitudInformacion,
        on_delete=models.CASCADE,
        related_name='modificaciones'
    )
    presupuesto = models.ForeignKey(
        Presupuesto,
        on_delete=models.CASCADE,
        related_name='modificaciones',
        null=True,
        blank=True,
    )
    motivo = models.CharField(max_length=150, blank=True, null=True)
    descripcion = models.TextField()
    especificaciones = models.TextField(blank=True, null=True)
    contacto_nombre = models.CharField(max_length=120, blank=True, null=True)
    contacto_email = models.EmailField(blank=True, null=True)
    codigo_seguimiento_cliente = models.CharField(max_length=50, blank=True, null=True)
    monto_adicional = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    # Campos adicionales para la solicitud del cliente
    adjunto = models.FileField(upload_to='modificaciones/', null=True, blank=True)
    adjunto = models.FileField(upload_to='modificaciones/', null=True, blank=True)
    # El administrador propondrá el monto a aplicar (precio en moneda del presupuesto)
    admin_monto_propuesto = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    ESTADO_MOD_CHOICES = [
        ('creada', 'Creada'),
        ('en_revision', 'En revisión'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
    ]
    estado_mod = models.CharField(max_length=20, choices=ESTADO_MOD_CHOICES, default='creada')
    creado = models.DateTimeField(auto_now_add=True)
    aceptada = models.BooleanField(default=False)
    fecha_aceptacion = models.DateTimeField(null=True, blank=True)
    admin_observaciones = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Modificación {self.id} - {self.solicitud.codigo_seguimiento}"
