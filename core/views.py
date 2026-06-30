from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import Servicio, SolicitudInformacion, Presupuesto, Visita
from .forms import SolicitarInfoForm, ModificacionForm, AgendarVisitaForm
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from core.models import Estado

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
# VISTA AGENDAR VISITA
# ----------------------------
def agendar_visita(request):
    if request.method == 'POST':
        form = AgendarVisitaForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data
            visita = Visita.objects.create(
                nombre=datos['nombre'],
                rut=datos['rut'],
                email=datos['email'],
                telefono=datos['telefono'],
                fecha_inicio_preferido=datos['fecha_inicio_preferido'],
                fecha_fin_preferido=datos['fecha_fin_preferido'],
            )

            mensaje = (
                f"Nueva solicitud de visita:\n\n"
                f"Código: {visita.codigo}\n"
                f"Nombre: {visita.nombre}\n"
                f"RUT: {visita.rut}\n"
                f"Correo: {visita.email}\n"
                f"Teléfono: {visita.telefono}\n"
                f"Rango preferido: {visita.fecha_inicio_preferido.strftime('%d/%m/%Y')} - "
                f"{visita.fecha_fin_preferido.strftime('%d/%m/%Y')}\n"
            )

            send_mail(
                subject="Agendamiento de visita - CBC E.I.R.L.",
                message=mensaje,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=['cbc_web@hotmail.com'],
                fail_silently=True,
            )

            return redirect('visita_estado', codigo=visita.codigo)
    else:
        form = AgendarVisitaForm()

    return render(request, 'agendar_visita.html', {'form': form})

# ----------------------------
# VISTA ESTADO DE VISITA
# ----------------------------
def visita_estado(request, codigo):
    visita = get_object_or_404(Visita, codigo=codigo)
    return render(request, 'visita_estado.html', {'visita': visita})

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
        form = SolicitarInfoForm()

    return render(request, 'solicitar_info.html', {'form': form, 'servicio': servicio})

# ----------------------------
# VISTA SEGUIMIENTO
# ----------------------------
def seguimiento(request, codigo):
    codigo = codigo.strip()
    solicitud = SolicitudInformacion.objects.filter(
        codigo_seguimiento=codigo
    ).select_related('servicio').prefetch_related('modificaciones').first()

    if solicitud is None:
        return render(request, "seguimiento_no_encontrado.html", {"codigo": codigo}, status=404)

    # ============================
    # MAPEO DE ESTADOS PANEL → CLIENTE
    # ============================
    MAPEO_ESTADOS = {
        "no_revisada": "recibida",
        "revisada": "asignacion_experto",
        "asignada": "experto_asignado",
        "cotizada": "presupuesto_creado",
        "enviada": "enviada",
        "aceptada": "aceptada",
        "pago_inicial": "pago_inicial",
        "en_ejecucion": "en_ejecucion",
        "completado": "completado",
        "pagada": "pagada",
        "rechazada": "rechazada",
        "en_revision": "en_revision",
    }

    # Estado del panel admin
    estado_panel = solicitud.estado_actual.codigo if solicitud.estado_actual else "no_revisada"

    # Estado traducido para el cliente
    estado_codigo = MAPEO_ESTADOS.get(estado_panel, "recibida")

    # ============================
    # MAPEO DE PASOS (1–10)
    # ============================
    estado_map = {
        'recibida': 1,
        'asignacion_experto': 2,
        'experto_asignado': 3,
        'presupuesto_creado': 4,
        'enviada': 5,
        'aceptada': 6,
        'pago_inicial': 7,
        'en_ejecucion': 8,
        'completado': 9,
        'pagada': 10,
        'rechazada': 0,
        'en_revision': 5,
    }

    estado_num = estado_map.get(estado_codigo, 0)

    # ============================
    # ESTADO DEL TRABAJO
    # ============================
    trabajo_estado_map = {
        'recibida': 'Sin trabajo iniciado',
        'asignacion_experto': 'Sin trabajo iniciado',
        'experto_asignado': 'Sin trabajo iniciado',
        'presupuesto_creado': 'Sin trabajo iniciado',
        'enviada': 'Sin trabajo iniciado',
        'aceptada': 'Pendiente de pago inicial',
        'pago_inicial': 'Pago inicial pendiente',
        'en_ejecucion': 'En ejecución',
        'completado': 'Trabajo completado',
        'pagada': 'Pago final completado',
        'rechazada': 'Solicitud rechazada',
        'en_revision': 'Solicitud en revisión',
    }

    estado_trabajo = trabajo_estado_map.get(estado_codigo, 'Sin trabajo iniciado')

    trabajo_comenzado = (
        estado_codigo in ['pago_inicial', 'en_ejecucion', 'completado', 'pagada']
        or solicitud.progreso_trabajo > 0
    )

    # ============================
    # PRESUPUESTO Y MODIFICACIONES
    # ============================
    presupuesto = getattr(solicitud, 'presupuesto', None)
    ultima_modificacion = solicitud.modificaciones.order_by('-creado').first()
    modificaciones = solicitud.modificaciones.order_by('-creado')

    revision_activa = bool(
        ultima_modificacion and ultima_modificacion.estado_mod in ['en_revision', 'mod_en_revision']
    )

    return render(request, "seguimiento.html", {
        "solicitud": solicitud,
        "estado_codigo": estado_codigo,
        "estado_num": estado_num,
        "estado": estado_num,
        "estado_trabajo": estado_trabajo,
        "trabajo_comenzado": trabajo_comenzado,
        "presupuesto": presupuesto,
        "ultima_modificacion": ultima_modificacion,
        "modificaciones": modificaciones,
        "revision_activa": revision_activa,
    })
# ----------------------------
# VISTA INTERMEDIA
# ----------------------------
def seguimiento_base(request):
    codigo = request.GET.get('codigo', '').strip()

    if codigo:
        codigo_normalizado = codigo.upper()
        if codigo_normalizado.startswith('VIS-'):
            return redirect('visita_estado', codigo=codigo_normalizado)
        return redirect('seguimiento', codigo=codigo)

    return redirect('inicio')

# ----------------------------
# SOLICITAR MODIFICACIÓN
# ----------------------------
def solicitar_modificacion(request, codigo):
    solicitud = get_object_or_404(SolicitudInformacion, codigo_seguimiento=codigo)
    presupuesto = getattr(solicitud, 'presupuesto', None)

    if request.method == 'POST':
        form = ModificacionForm(request.POST, request.FILES)
        if form.is_valid():
            mod = form.save(commit=False)
            mod.solicitud = solicitud
            mod.presupuesto = presupuesto
            mod.save()

            solicitud.estado_actual = None  # si quieres manejar estados de modificación
            solicitud.save()

            return redirect('seguimiento', codigo=codigo)
    else:
        form = ModificacionForm(initial={
            'contacto_nombre': solicitud.nombre,
            'contacto_email': solicitud.email,
            'codigo_seguimiento_cliente': solicitud.codigo_seguimiento,
        })

    return render(request, 'solicitud_modificacion.html', {
        'solicitud': solicitud,
        'presupuesto': presupuesto,
        'form': form,
    })

# ----------------------------
# APROBAR / RECHAZAR
# ----------------------------
def aprobar_solicitud(request, codigo):
    solicitud = get_object_or_404(SolicitudInformacion, codigo_seguimiento=codigo)
    solicitud.estado_actual = Estado.objects.get(codigo="aceptada")
    solicitud.save()
    return redirect('pago_inicial', codigo=codigo)

def rechazar_solicitud(request, codigo):
    solicitud = get_object_or_404(SolicitudInformacion, codigo_seguimiento=codigo)
    solicitud.estado_actual = Estado.objects.get(codigo="rechazada")
    solicitud.save()
    return redirect('seguimiento', codigo=codigo)

# ----------------------------
# SOLICITAR CAMBIOS
# ----------------------------
def solicitar_cambios(request, codigo):
    solicitud = get_object_or_404(SolicitudInformacion, codigo_seguimiento=codigo)

    if request.method == "POST":
        comentarios = request.POST.get("comentarios", "")
        solicitud.comentarios_cambios = comentarios
        solicitud.estado_actual = Estado.objects.get(codigo="en_revision")
        solicitud.save()
        return redirect('seguimiento', codigo=codigo)

    return render(request, "solicitar_cambios.html", {"solicitud": solicitud})

# ----------------------------
# PAGO INICIAL
# ----------------------------
def pago_inicial(request, codigo):
    solicitud = get_object_or_404(SolicitudInformacion, codigo_seguimiento=codigo)

    if solicitud.estado_actual.codigo != 'aceptada':
        return redirect('seguimiento', codigo=codigo)

    presupuesto = getattr(solicitud, 'presupuesto', None)
    monto_inicial = presupuesto.total / 2 if presupuesto and presupuesto.total else 0

    return render(request, "pago_inicial.html", {
        "solicitud": solicitud,
        "presupuesto": presupuesto,
        "monto_inicial": monto_inicial
    })

def procesar_pago_inicial(request, codigo):
    solicitud = get_object_or_404(SolicitudInformacion, codigo_seguimiento=codigo)

    if request.method == "POST":
        numero_tarjeta = request.POST.get("numero_tarjeta", "")
        mes_vencimiento = request.POST.get("mes_vencimiento", "")
        ano_vencimiento = request.POST.get("ano_vencimiento", "")
        cvv = request.POST.get("cvv", "")

        if numero_tarjeta and mes_vencimiento and ano_vencimiento and cvv:
            solicitud.estado_actual = Estado.objects.get(codigo="pago_inicial")
            solicitud.save()

            return redirect('pago_completado', codigo=codigo)

    return redirect('pago_inicial', codigo=codigo)

def confirmar_pago_inicial_cliente(request, codigo):
    solicitud = get_object_or_404(SolicitudInformacion, codigo_seguimiento=codigo)
    solicitud.estado_actual = Estado.objects.get(codigo="en_ejecucion")
    solicitud.save()
    return redirect('seguimiento', codigo=codigo)


def pago_completado(request, codigo):  
    solicitud = get_object_or_404(SolicitudInformacion, codigo_seguimiento=codigo)
    presupuesto = getattr(solicitud, 'presupuesto', None)

    monto_inicial = presupuesto.total / 2 if presupuesto and presupuesto.total else 0

    return render(request, "pago_completado.html", {
        "solicitud": solicitud,
        "presupuesto": presupuesto,
        "monto_inicial": monto_inicial
    })

# ----------------------------
# PAGO FINAL
# ----------------------------
def pago_final(request, codigo):
    solicitud = get_object_or_404(SolicitudInformacion, codigo_seguimiento=codigo)

    if solicitud.estado_actual.codigo != 'completado' or solicitud.progreso_trabajo < 100:
        return redirect('seguimiento', codigo=codigo)

    presupuesto = getattr(solicitud, 'presupuesto', None)
    monto_final = presupuesto.total / 2 if presupuesto and presupuesto.total else 0

    return render(request, "pago_final.html", {
        "solicitud": solicitud,
        "presupuesto": presupuesto,
        "monto_final": monto_final
    })

def procesar_pago_final(request, codigo):
    solicitud = get_object_or_404(SolicitudInformacion, codigo_seguimiento=codigo)

    if request.method == "POST":
        numero_tarjeta = request.POST.get("numero_tarjeta", "")
        mes_vencimiento = request.POST.get("mes_vencimiento", "")
        ano_vencimiento = request.POST.get("ano_vencimiento", "")
        cvv = request.POST.get("cvv", "")

        if numero_tarjeta and mes_vencimiento and ano_vencimiento and cvv:
            solicitud.estado_actual = Estado.objects.get(codigo="pagada")
            solicitud.save()
            return redirect('pago_final_completado', codigo=codigo)

    return redirect('pago_final', codigo=codigo)



def pago_final_completado(request, codigo):
    solicitud = get_object_or_404(SolicitudInformacion, codigo_seguimiento=codigo)
    presupuesto = getattr(solicitud, 'presupuesto', None)

    monto_final = presupuesto.total / 2 if presupuesto and presupuesto.total else 0

    return render(request, "pago_final_completado.html", {
        "solicitud": solicitud,
        "presupuesto": presupuesto,
        "monto_final": monto_final
    })

# ----------------------------
# LOGIN / LOGOUT
# ----------------------------
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('admin_dashboard')
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('login')
