from django.contrib import admin
from django.urls import path
from core import views
from django.conf import settings
from django.conf.urls.static import static

# 👇 IMPORTANTE (esto faltaba)
from core.views_admin import create_admin
from core.views import test_storage

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.inicio, name='inicio'),
    path('servicios/', views.servicios, name='servicios'),
    path('contacto/', views.contacto, name='contacto'),
    path('agendar-visita/', views.agendar_visita, name='agendar_visita'),
    path('visita/<str:codigo>/', views.visita_estado, name='visita_estado'),

    path('solicitar-info/<int:servicio_id>/', views.solicitar_info, name='solicitar_info'),
    path('gracias/', views.gracias, name='gracias'),

    # Seguimiento
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

    # Admin custom
    path("create-admin/", create_admin, name="create_admin"),

    # Test storage
    path("test-storage/", test_storage),
]

# 👇 SOLO EN DESARROLLO (imágenes locales)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)