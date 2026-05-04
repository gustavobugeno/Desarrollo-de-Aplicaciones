from django.contrib import admin
from django.utils.html import format_html
from django.conf import settings
from django.core.mail import send_mail

from .models import Servicio, ImagenServicio, SolicitudInformacion, Presupuesto


# ----------------------------
#  INLINE DE PRESUPUESTO
# ----------------------------
class PresupuestoInline(admin.StackedInline):
    model = Presupuesto
    extra = 0
    max_num = 1


@admin.register(Presupuesto)
class PresupuestoAdmin(admin.ModelAdmin):
    list_display = ('solicitud', 'fecha', 'total')


# ----------------------------
#  ADMIN PARA SOLICITUDES
# ----------------------------
@admin.register(SolicitudInformacion)
class SolicitudInformacionAdmin(admin.ModelAdmin):

    inlines = [PresupuestoInline]
    actions = ["enviar_correo_manual"]

    # ---- ESTADO COLOREADO ----
    def estado_coloreado(self, obj):
        colores = {
            'no_revisada': 'orange',
            'revisada': 'blue',
            'asignada': 'purple',
            'cotizada': 'darkblue',
            'enviada': 'teal',
            'aceptada': 'green',
            'rechazada': 'red',
            'pagada': 'darkgreen',
        }
        color = colores.get(obj.estado, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color,
            obj.get_estado_display()
        )
    estado_coloreado.short_description = "Estado"

    # ---- LIST DISPLAY ----
    list_display = (
        'codigo_seguimiento',
        'nombre',
        'email',
        'telefono',
        'servicio',
        'estado_coloreado',
        'fecha_envio'
    )

    search_fields = ('nombre', 'email', 'telefono', 'codigo_seguimiento')
    list_filter = ('estado', 'servicio', 'fecha_envio')
    ordering = ('-fecha_envio',)

    # ---- ENVÍO AUTOMÁTICO AL CAMBIAR ESTADO ----
    def save_model(self, request, obj, form, change):
        estado_cambiado = "estado" in form.changed_data

        super().save_model(request, obj, form, change)

        if estado_cambiado:
            asunto = f"Actualización de su solicitud - {obj.codigo_seguimiento}"
            mensaje = (
                f"Hola {obj.nombre},\n\n"
                f"Su solicitud ha cambiado de estado.\n\n"
                f"Nuevo estado: {obj.get_estado_display()}\n\n"
                f"Puede revisar el detalle en:\n"
                f"https://desarrollo-cbc-eirl.onrender.com/seguimiento/{obj.codigo_seguimiento}/\n\n"
                "Gracias por preferir CBC E.I.R.L."
            )

            send_mail(
                asunto,
                mensaje,
                settings.EMAIL_HOST_USER,
                [obj.email],
                fail_silently=True,
            )

    # ---- ACCIÓN MANUAL PARA ENVIAR CORREO ----
    @admin.action(description="Enviar correo manual al cliente")
    def enviar_correo_manual(self, request, queryset):
        for obj in queryset:
            asunto = f"Mensaje sobre su solicitud {obj.codigo_seguimiento}"
            mensaje = (
                f"Hola {obj.nombre},\n\n"
                f"El administrador desea comunicarse contigo sobre tu solicitud.\n\n"
                f"Revisa tu seguimiento aquí:\n"
                f"https://desarrollo-cbc-eirl.onrender.com/seguimiento/{obj.codigo_seguimiento}/\n\n"
            )

            send_mail(
                asunto,
                mensaje,
                settings.EMAIL_HOST_USER,
                [obj.email],
                fail_silently=True,
            )

        self.message_user(request, "📨 Correos enviados con éxito.")


# ----------------------------
#  ADMIN PARA SERVICIOS
# ----------------------------
class ImagenServicioInline(admin.TabularInline):
    model = ImagenServicio
    extra = 1


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('titulo',)
    inlines = [ImagenServicioInline]