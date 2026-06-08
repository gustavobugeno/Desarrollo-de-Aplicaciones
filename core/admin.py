from django.contrib import admin
from django.utils.html import format_html
from django.conf import settings
from django.core.mail import send_mail
from decimal import Decimal

from .models import Servicio, ImagenServicio, SolicitudInformacion, Presupuesto, Modificacion, Visita
from .forms import PresupuestoForm, ModificacionAdminForm
from django.utils import timezone


# ----------------------------
#  INLINE DE PRESUPUESTO
# ----------------------------
class PresupuestoInline(admin.StackedInline):
    model = Presupuesto
    form = PresupuestoForm
    extra = 0
    max_num = 1


@admin.register(Presupuesto)
class PresupuestoAdmin(admin.ModelAdmin):
    form = PresupuestoForm
    list_display = ('solicitud', 'fecha', 'total')


# ----------------------------
#  ADMIN PARA SOLICITUDES
# ----------------------------
@admin.register(SolicitudInformacion)
class SolicitudInformacionAdmin(admin.ModelAdmin):

    inlines = [PresupuestoInline]
    actions = ["enviar_correo_manual", "marcar_completado"]

    # ---- ESTADO COLOREADO ----
    def estado_coloreado(self, obj):
        colores = {
            'no_revisada': 'orange',
            'revisada': 'blue',
            'asignada': 'purple',
            'cotizada': 'darkblue',
            'enviada': 'teal',
            'aceptada': 'green',
            'pago_inicial': '#ff8c00',
            'en_ejecucion': '#008080',
            'completado': '#0b75ad',
            'pagada': 'darkgreen',
            'rechazada': 'red',
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
        'progreso_trabajo',
        'fecha_estimado_finalizacion',
        'fecha_envio'
    )

    search_fields = ('nombre', 'email', 'telefono', 'codigo_seguimiento')
    list_filter = ('estado', 'servicio', 'fecha_envio')
    ordering = ('-fecha_envio',)

    # ---- FIELDSETS ----
    fieldsets = (
        ('Información del Cliente', {
            'fields': ('nombre', 'email', 'telefono', 'servicio')
        }),
        ('Detalles del Proyecto', {
            'fields': ('ubicacion', 'cuando_comenzar', 'tienes_terreno', 'requerimientos')
        }),
        ('Estado y Seguimiento', {
            'fields': ('estado', 'codigo_seguimiento', 'comentarios_cambios', 'fecha_estimado_finalizacion')
        }),
        ('Progreso del Trabajo', {
            'fields': ('progreso_trabajo',),
            'description': 'Actualiza el porcentaje de progreso cuando la solicitud esté en ejecución (0-100%).'
        }),
    )

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
    @admin.action(description="Marcar solicitudes como completadas")
    def marcar_completado(self, request, queryset):
        updated = queryset.update(estado='completado', progreso_trabajo=100)
        self.message_user(request, f"✅ {updated} solicitud(es) marcadas como completadas.")

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


@admin.register(Modificacion)
class ModificacionAdmin(admin.ModelAdmin):
    form = ModificacionAdminForm
    list_display = ('solicitud', 'descripcion_short', 'motivo', 'estado_mod', 'monto_adicional', 'admin_monto_propuesto', 'aceptada', 'creado')
    list_filter = ('estado_mod', 'aceptada', 'creado')
    actions = ['marcar_en_revision', 'aceptar_modificacion', 'rechazar_modificacion']
    list_editable = ('admin_monto_propuesto', 'estado_mod')
    readonly_fields = ('creado', 'fecha_aceptacion')
    fieldsets = (
        (None, {'fields': ('solicitud', 'presupuesto', 'motivo', 'descripcion', 'especificaciones', 'adjunto', 'monto_adicional', 'estado_mod')}),
        ('Propuesta del Admin', {'fields': ('admin_monto_propuesto', 'admin_observaciones', 'fecha_aceptacion')}),
    )

    def descripcion_short(self, obj):
        return (obj.descripcion[:60] + '...') if len(obj.descripcion) > 60 else obj.descripcion
    descripcion_short.short_description = 'Descripción'

    @admin.action(description='Aceptar modificación y actualizar presupuesto')
    def aceptar_modificacion(self, request, queryset):
        updated = 0
        skipped = 0
        for mod in queryset:
            if mod.aceptada:
                skipped += 1
                continue
            pres = mod.presupuesto
            if pres and mod.admin_monto_propuesto is not None:
                # Aplicar el monto propuesto por el admin como aumento (sumarlo al total)
                if pres.total:
                    pres.total = pres.total + mod.admin_monto_propuesto
                else:
                    pres.total = mod.admin_monto_propuesto
                pres.save()
                mod.aceptada = True
                mod.estado_mod = 'aceptada'
                mod.fecha_aceptacion = timezone.now()
                mod.save()
                # actualizar estado de la solicitud principal
                solicitud = mod.solicitud
                solicitud.estado = 'mod_aceptada'
                solicitud.save()
                updated += 1
            else:
                skipped += 1

        self.message_user(request, f"✅ {updated} modificación(es) aceptada(s). {skipped} omitida(s) (sin monto propuesto o ya aceptadas).")

    @admin.action(description='Marcar modificación como En Revisión')
    def marcar_en_revision(self, request, queryset):
        updated = 0
        for mod in queryset:
            if mod.estado_mod != 'en_revision':
                mod.estado_mod = 'en_revision'
                mod.save()
                # actualizar solicitud
                solicitud = mod.solicitud
                solicitud.estado = 'mod_en_revision'
                solicitud.save()
                updated += 1
        self.message_user(request, f"ℹ️ {updated} modificación(es) marcadas como en revisión.")

    @admin.action(description='Rechazar modificación')
    def rechazar_modificacion(self, request, queryset):
        updated = 0
        for mod in queryset:
            if mod.estado_mod != 'rechazada':
                mod.estado_mod = 'rechazada'
                mod.aceptada = False
                mod.fecha_aceptacion = None
                mod.save()
                solicitud = mod.solicitud
                solicitud.estado = 'mod_rechazada'
                solicitud.save()
                updated += 1
        self.message_user(request, f"❌ {updated} modificación(es) rechazadas.")

    def save_model(self, request, obj, form, change):
        estado_cambiado = 'estado_mod' in form.changed_data
        admin_monto_cambiado = 'admin_monto_propuesto' in form.changed_data

        old_admin_monto = None
        old_aceptada = False
        if change:
            try:
                old_obj = Modificacion.objects.get(pk=obj.pk)
                old_admin_monto = old_obj.admin_monto_propuesto
                old_aceptada = old_obj.estado_mod == 'aceptada'
            except Modificacion.DoesNotExist:
                old_admin_monto = None
                old_aceptada = False

        new_aceptada = obj.estado_mod == 'aceptada'
        obj.aceptada = new_aceptada
        if new_aceptada and not old_aceptada:
            obj.fecha_aceptacion = timezone.now()
        elif not new_aceptada:
            obj.fecha_aceptacion = None

        super().save_model(request, obj, form, change)

        if obj.presupuesto and obj.admin_monto_propuesto is not None:
            pres = obj.presupuesto
            current_total = pres.total or Decimal('0')
            new_admin_monto = obj.admin_monto_propuesto or Decimal('0')
            old_admin_monto = old_admin_monto or Decimal('0')

            if change and not old_aceptada and new_aceptada:
                # La modificación se aceptó ahora: sumar el monto total de la modificación
                pres.total = current_total + new_admin_monto
                pres.save()
            elif change and old_aceptada and not new_aceptada:
                # La modificación dejó de estar aceptada: restar el monto anterior
                pres.total = current_total - old_admin_monto
                pres.save()
            elif change and admin_monto_cambiado and new_admin_monto != old_admin_monto:
                # El precio de la modificación cambió: ajustar la diferencia
                pres.total = current_total + (new_admin_monto - old_admin_monto)
                pres.save()

        if estado_cambiado:
            mapping = {
                'creada': 'mod_creada',
                'en_revision': 'mod_en_revision',
                'aceptada': 'mod_aceptada',
                'rechazada': 'mod_rechazada',
            }
            nuevo = mapping.get(obj.estado_mod)
            if nuevo:
                solicitud = obj.solicitud
                solicitud.estado = nuevo
                solicitud.save()


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('titulo',)
    inlines = [ImagenServicioInline]


@admin.register(Visita)
class VisitaAdmin(admin.ModelAdmin):
    list_display = (
        'codigo',
        'nombre',
        'email',
        'telefono',
        'estado',
        'fecha_inicio_preferido',
        'fecha_fin_preferido',
        'fecha_inicio_propuesta',
        'fecha_fin_propuesta',
    )
    list_filter = ('estado', 'creado')
    search_fields = ('codigo', 'nombre', 'email', 'rut', 'telefono')
    readonly_fields = ('codigo', 'creado')
    fieldsets = (
        ('Información del cliente', {
            'fields': ('codigo', 'nombre', 'rut', 'email', 'telefono')
        }),
        ('Rango preferido para la visita', {
            'fields': ('fecha_inicio_preferido', 'fecha_fin_preferido')
        }),
        ('Propuesta del admin', {
            'fields': ('estado', 'fecha_inicio_propuesta', 'fecha_fin_propuesta', 'observaciones')
        }),
    )
