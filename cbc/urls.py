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

    path('solicitar-info/<int:servicio_id>/', views.solicitar_info, name='solicitar_info'),
    path('gracias/', views.gracias, name='gracias'),

    # Seguimiento
    path("seguimiento/", views.seguimiento_base, name="seguimiento_base"),
    path("seguimiento/<str:codigo>/", views.seguimiento, name="seguimiento"),

    path('seguimiento/<str:codigo>/aprobar/', views.aprobar_solicitud, name='aprobar_solicitud'),
    path('seguimiento/<str:codigo>/rechazar/', views.rechazar_solicitud, name='rechazar_solicitud'),
    path('seguimiento/<str:codigo>/cambios/', views.solicitar_cambios, name='solicitar_cambios'),

    # Admin custom
    path("create-admin/", create_admin, name="create_admin"),

    # Test storage
    path("test-storage/", test_storage),
]

# 👇 SOLO EN DESARROLLO (imágenes locales)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)