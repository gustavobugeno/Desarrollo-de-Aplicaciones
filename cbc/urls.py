from django.contrib import admin
from django.urls import path
from core import views, views_admin
from django.conf import settings
from django.conf.urls.static import static
from core.views import login_view, logout_view, test_storage
from core.views import confirmar_pago_inicial_cliente

# IMPORTANTE: agregar esta línea
from core.views_admin import enviar_cotizacion

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # Autenticación
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    # Página pública
    path('', views.inicio, name='inicio'),
    path('servicios/', views.servicios, name='servicios'),
    path('contacto/', views.contacto, name='contacto'),
    path('agendar-visita/', views.agendar_visita, name='agendar_visita'),
    path('visita/<str:codigo>/', views.visita_estado, name='visita_estado'),

    # Solicitudes públicas
    path('solicitar-info/<int:servicio_id>/', views.solicitar_info, name='solicitar_info'),
    path('gracias/', views.gracias, name='gracias'),

    # ============================
    # PANEL ADMIN - SOLICITUDES
    # ============================

    path("panel/solicitudes/", views_admin.admin_solicitudes, name="admin_solicitudes"),
    path("panel/solicitudes/<int:id>/", views_admin.admin_solicitud_detalle, name="admin_solicitud_detalle"),
    path("panel/solicitudes/<int:id>/editar/", views_admin.admin_solicitud_editar, name="admin_solicitud_editar"),
    path("panel/solicitudes/<int:id>/eliminar/", views_admin.admin_solicitud_eliminar, name="admin_solicitud_eliminar"),

    # ============================
    # FLUJO DE ESTADOS
    # ============================

    path("panel/solicitudes/<int:id>/flujo/", views_admin.flujo_solicitud, name="flujo_solicitud"),
    path("panel/solicitudes/<int:id>/avanzar/", views_admin.avanzar_estado, name="avanzar_estado"),
    path("panel/solicitudes/<int:id>/retroceder/", views_admin.retroceder_estado, name="retroceder_estado"),

    # ESTADO 2 — Asignar experto
    path("panel/solicitudes/<int:id>/asignar-experto/", views_admin.asignar_experto, name="asignar_experto"),

    # ESTADO 3 — Subir cotización
    path("panel/solicitudes/<int:id>/subir-cotizacion/", views_admin.subir_cotizacion, name="subir_cotizacion"),

    # ESTADO 4 — Enviar cotización (corregido)
    path("panel/solicitudes/<int:id>/enviar-cotizacion/", enviar_cotizacion, name="enviar_cotizacion"),

    # ESTADO 5 — Respuesta del cliente
    path("panel/solicitudes/<int:id>/respuesta/", views_admin.esperar_respuesta_cliente, name="esperar_respuesta_cliente"),
    path("panel/solicitudes/<int:id>/aceptar/", views_admin.aceptar_cotizacion, name="aceptar_cotizacion"),
    path("panel/solicitudes/<int:id>/rechazar/", views_admin.rechazar_cotizacion, name="rechazar_cotizacion"),

    # ESTADO 6 — Pago inicial
    path("panel/solicitudes/<int:id>/pago-inicial/", views_admin.pago_inicial, name="pago_inicial"),
    path("panel/solicitudes/<int:id>/confirmar-pago-inicial/", views_admin.confirmar_pago_inicial, name="confirmar_pago_inicial"),
    path('seguimiento/<str:codigo>/confirmar-pago-inicial/', confirmar_pago_inicial_cliente, name='confirmar_pago_inicial_cliente'),

    # ESTADO 8 — En ejecución
    path("panel/solicitudes/<int:id>/ejecucion/", views_admin.en_ejecucion, name="en_ejecucion"),

    # ESTADO 9 — Confirmar entrega
    path("panel/solicitudes/<int:id>/confirmar-entrega/", views_admin.confirmar_entrega, name="confirmar_entrega"),

    # ESTADO 10 — Pago final
    path("panel/solicitudes/<int:id>/pago-final/", views_admin.pago_final, name="pago_final"),
    path("seguimiento/<str:codigo>/pago-final/", views_admin.pago_final_cliente, name="pago_final_cliente"),
    path("panel/solicitudes/<int:id>/finalizar/",views_admin.finalizar_solicitud,name="finalizar_solicitud"),
    # ============================
    # SEGUIMIENTO CLIENTE (NO ADMIN)
    # ============================

    path("seguimiento/", views.seguimiento_base, name="seguimiento_base"),
    path("seguimiento/<str:codigo>/", views.seguimiento, name="seguimiento"),

    path('seguimiento/<str:codigo>/aprobar/', views.aprobar_solicitud, name='aprobar_solicitud'),
    path('seguimiento/<str:codigo>/rechazar/', views.rechazar_solicitud, name='rechazar_solicitud'),
    path('seguimiento/<str:codigo>/cambios/', views.solicitar_cambios, name='solicitar_cambios'),
    path('seguimiento/<str:codigo>/pago-inicial/', views.pago_inicial, name='pago_inicial'),
    path('seguimiento/<str:codigo>/solicitar-modificacion/', views.solicitar_modificacion, name='solicitar_modificacion'),
    path('seguimiento/<str:codigo>/procesar-pago/', views.procesar_pago_inicial, name='procesar_pago'),
    path('seguimiento/<str:codigo>/pago-completado/', views.pago_completado, name='pago_completado'),
    path('seguimiento/<str:codigo>/pago-final/', views.pago_final, name='pago_final'),
    path('seguimiento/<str:codigo>/procesar-pago-final/', views.procesar_pago_final, name='procesar_pago_final'),
    path('seguimiento/<str:codigo>/pago-final-completado/', views.pago_final_completado, name='pago_final_completado'),
    path( "panel/solicitudes/<int:id>/finalizar/", views_admin.finalizar_solicitud,name="finalizar_solicitud"),

    # ============================
    # PANEL ADMIN - CONFIG
    # ============================

    path("create-admin/", views_admin.create_admin, name="create_admin"),

    path('panel/dashboard/', views_admin.dashboard, name='admin_dashboard'),
    path('panel/ordenar-estados/', views_admin.ordenar_estados, name='admin_ordenar_estados'),
    path('panel/editar-estado/', views_admin.editar_estado, name='admin_editar_estado'),
    path('panel/eliminar-estado/', views_admin.eliminar_estado, name='admin_eliminar_estado'),
    path('panel/estado-1/', views_admin.estado_1, name='admin_estado_1'),
    path('panel/estado-2/', views_admin.estado_2, name='admin_estado_2'),

    # Test storage
    path("test-storage/", test_storage),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
