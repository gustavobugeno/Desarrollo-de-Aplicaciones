from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from core.models import Estado
        try:
            # BORRAR todos los estados existentes
            Estado.objects.all().delete()

            # Crear estados correctos con TEMPLATE incluido
            estados = [
                (1, "no_revisada", "No revisada", 1, "no_revisada.html"),
                (2, "revisada", "Revisada por experto", 2, "revisada.html"),
                (3, "asignada", "Experto asignado", 3, "asignada.html"),
                (4, "cotizada", "Cotización generada", 4, "cotizada.html"),
                (5, "enviada", "Cotización enviada", 5, "enviada.html"),
                (6, "aceptada", "Aceptada", 6, "aceptada.html"),
                (7, "pago_inicial", "Pago 50% Inicial", 7, "pago_inicial.html"),
                (8, "en_ejecucion", "En ejecución", 8, "en_ejecucion.html"),
                (9, "completado", "Completado", 9, "completado.html"),
                (16, "pago_final", "Pago Final", 10, "pago_final.html"),
                (10, "pagada", "Pagada", 11, "pagada.html"),
                (11, "rechazada", "Rechazada", 12, "rechazada.html"),
                (17, "finalizado", "Finalizado", 13, "finalizado.html"),
                (12, "mod_creada", "Modificación creada", 100, "mod_creada.html"),
                (13, "mod_en_revision", "Modificación en revisión", 101, "mod_en_revision.html"),
                (14, "mod_aceptada", "Modificación aceptada", 102, "mod_aceptada.html"),
                (15, "mod_rechazada", "Modificación rechazada", 103, "mod_rechazada.html"),
            ]

            # IMPORTANTE: aquí recibimos 5 valores
            for pk, codigo, nombre, orden, template in estados:
                Estado.objects.update_or_create(
                    pk=pk,
                    defaults={
                        "codigo": codigo,
                        "nombre": nombre,
                        "orden": orden,
                        "template": template,
                        "activo": True
                    }
                )
        except Exception:
            pass
