from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from core.models import Estado
        try:
            if Estado.objects.count() == 0:
                estados = [
                    (1, "no_revisada", "No revisada", 1),
                    (2, "revisada", "Revisada por experto", 2),
                    (3, "asignada", "Experto asignado", 3),
                    (4, "cotizada", "Cotización generada", 4),
                    (5, "enviada", "Cotización enviada", 5),
                    (6, "aceptada", "Aceptada", 6),
                    (7, "pago_inicial", "Pago 50% Inicial", 7),
                    (8, "en_ejecucion", "En ejecución", 8),
                    (9, "completado", "Completado", 9),
                    (16, "pago_final", "Pago Final", 10),
                    (10, "pagada", "Pagada", 11),
                    (11, "rechazada", "Rechazada", 12),
                    (17, "finalizado", "Finalizado", 13),
                    (12, "mod_creada", "Modificación creada", 100),
                    (13, "mod_en_revision", "Modificación en revisión", 101),
                    (14, "mod_aceptada", "Modificación aceptada", 102),
                    (15, "mod_rechazada", "Modificación rechazada", 103),
                ]

                for pk, codigo, nombre, orden in estados:
                    Estado.objects.update_or_create(
                        pk=pk,
                        defaults={
                            "codigo": codigo,
                            "nombre": nombre,
                            "orden": orden,
                            "activo": True
                        }
                    )
        except Exception:
            pass
