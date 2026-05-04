from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import Servicio, SolicitudInformacion, Presupuesto
from .forms import SolicitarInfoForm
from django.http import HttpResponse

def test_storage(request):
    return HttpResponse(settings.DEFAULT_FILE_STORAGE)
# ----------------------------
# VISTA INICIO
# ----------------------------
def inicio(request):
    return render(request, 'inicio.html')

# ----------------------------
# VISTA SERVICIOS
# ----------------------------
def servicios(request):
    servicios = Servicio.objects.all()
    return render(request, 'servicios.html', {'servicios': servicios})


# ----------------------------
# VISTA CONTACTO
# ----------------------------
def contacto(request):
    return render(request, 'contacto.html')


# ----------------------------
# VISTA GRACIAS
# ----------------------------
def gracias(request):
    return render(request, 'gracias.html')


# ----------------------------
# VISTA SOLICITAR INFORMACION
# ----------------------------
def solicitar_info(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)

    if request.method == 'POST':
        form = SolicitarInfoForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.servicio = servicio
            solicitud.save()

            mensaje = (
                f"Nueva solicitud de información:\n\n"
                f"Servicio: {servicio.titulo}\n"
                f"Nombre: {solicitud.nombre}\n"
                f"Email: {solicitud.email}\n"
                f"Teléfono: {solicitud.telefono}\n"
                f"¿Tiene terreno?: {solicitud.tienes_terreno}\n"
                f"Ubicación: {solicitud.ubicacion}\n"
                f"¿Cuándo quiere comenzar?: {solicitud.cuando_comenzar}\n\n"
                f"Requerimientos:\n{solicitud.requerimientos}"
            )

            send_mail(
                subject="Solicitud de Cotización - CBC E.I.R.L.",
                message=mensaje,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=['cbc_web@hotmail.com'],
                fail_silently=True,
            )

            return redirect('seguimiento', codigo=solicitud.codigo_seguimiento)
        else:
            print("Errores del formulario:", form.errors)
    else:
        form = SolicitarInfoForm()

    return render(request, 'solicitar_info.html', {
        'form': form,
        'servicio': servicio
    })


# ----------------------------
# VISTA SEGUIMIENTO (por código)
# ----------------------------
def seguimiento(request, codigo):
    solicitud = get_object_or_404(SolicitudInformacion, codigo_seguimiento=codigo)

    estado_map = {
        'no_revisada': 1,
        'revisada': 2,
        'cotizacion_creada': 3,
        'enviada': 4,
        'aceptada': 5,
        'pago_final': 6
    }
    estado_num = estado_map.get(solicitud.estado, 0)

    presupuesto = getattr(solicitud, 'presupuesto', None)  # None si no existe

    return render(request, "seguimiento.html", {
        "solicitud": solicitud,
        "estado": estado_num,
        "presupuesto": presupuesto
    })


# ----------------------------
# VISTA INTERMEDIA PARA FORMULARIO DE SEGUIMIENTO
# ----------------------------
def seguimiento_base(request):
    """
    Recibe el código del formulario de inicio y redirige a la URL de seguimiento con código.
    """
    codigo = request.GET.get('codigo')
    if codigo:
        return redirect('seguimiento', codigo=codigo)
    return redirect('inicio')
def aprobar_solicitud(request, codigo):
    solicitud = get_object_or_404(SolicitudInformacion, codigo_seguimiento=codigo)
    solicitud.estado = 'aceptada'
    solicitud.save()
    return redirect('seguimiento', codigo=codigo)

def rechazar_solicitud(request, codigo):
    solicitud = get_object_or_404(SolicitudInformacion, codigo_seguimiento=codigo)
    solicitud.estado = 'rechazada'
    solicitud.save()
    return redirect('seguimiento', codigo=codigo)

def solicitar_cambios(request, codigo):
    solicitud = get_object_or_404(SolicitudInformacion, codigo_seguimiento=codigo)

    if request.method == "POST":
        comentarios = request.POST.get("comentarios", "")
        solicitud.comentarios_cambios = comentarios
        solicitud.estado = 'en_revision'  # Nuevo estado
        solicitud.save()
        return redirect('seguimiento', codigo=codigo)

    return render(request, "solicitar_cambios.html", {"solicitud": solicitud})
