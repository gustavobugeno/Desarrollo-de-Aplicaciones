from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required

# MODELOS
from core.models import SolicitudInformacion, Servicio, Estado, Presupuesto

# ============================
# PANEL ADMIN
# ============================

@login_required
def dashboard(request):
    return render(request, "admin_panel/dashboard.html")


@login_required
def ordenar_estados(request):
    return render(request, "admin_panel/ordenar_estados.html")


@login_required
def editar_estado(request):
    return render(request, "admin_panel/estados/editar_estado.html")


@login_required
def eliminar_estado(request):
    return render(request, "admin_panel/estados/eliminar_estado.html")


@login_required
def estado_1(request):
    return render(request, "admin_panel/estados/estado_1.html")


@login_required
def estado_2(request):
    return render(request, "admin_panel/estados/estado_2.html")


# ============================
# CRUD SOLICITUDES
# ============================

@login_required
def admin_solicitudes(request):
    solicitudes = SolicitudInformacion.objects.all().order_by('-fecha_envio')
    return render(request, "admin_panel/solicitudes/listar.html", {
        "solicitudes": solicitudes
    })


@login_required
def admin_solicitud_detalle(request, id):
    solicitud = get_object_or_404(SolicitudInformacion, id=id)
    return render(request, "admin_panel/solicitudes/detalle.html", {
        "solicitud": solicitud
    })


@login_required
def admin_solicitud_editar(request, id):
    solicitud = get_object_or_404(SolicitudInformacion, id=id)
    estados = Estado.objects.filter(activo=True).order_by("orden")

    if request.method == "POST":
        solicitud.nombre = request.POST.get("nombre")
        solicitud.email = request.POST.get("email")
        solicitud.telefono = request.POST.get("telefono")
        solicitud.ubicacion = request.POST.get("ubicacion")
        solicitud.cuando_comenzar = request.POST.get("cuando_comenzar")
        solicitud.requerimientos = request.POST.get("requerimientos")

        nuevo_estado_id = request.POST.get("estado_actual")
        if nuevo_estado_id:
            solicitud.estado_actual = Estado.objects.get(id=nuevo_estado_id)

        solicitud.save()
        return redirect("admin_solicitudes")

    return render(request, "admin_panel/solicitudes/editar.html", {
        "solicitud": solicitud,
        "estados": estados,
    })


@login_required
def admin_solicitud_eliminar(request, id):
    solicitud = get_object_or_404(SolicitudInformacion, id=id)
    solicitud.delete()
    return redirect("admin_solicitudes")


# ============================
# CRUD SERVICIOS
# ============================

@login_required
def admin_servicios(request):
    servicios = Servicio.objects.all()
    return render(request, "admin_panel/servicios/listar.html", {
        "servicios": servicios
    })


@login_required
def crear_servicio(request):
    if request.method == "POST":
        Servicio.objects.create(
            titulo=request.POST.get("titulo"),
            descripcion=request.POST.get("descripcion"),
        )
        return redirect("admin_servicios")

    return render(request, "admin_panel/servicios/crear.html")


@login_required
def editar_servicio(request, id):
    servicio = get_object_or_404(Servicio, id=id)

    if request.method == "POST":
        servicio.titulo = request.POST.get("titulo")
        servicio.descripcion = request.POST.get("descripcion")
        servicio.save()
        return redirect("admin_servicios")

    return render(request, "admin_panel/servicios/editar.html", {
        "servicio": servicio
    })


@login_required
def eliminar_servicio(request, id):
    servicio = get_object_or_404(Servicio, id=id)
    servicio.delete()
    return redirect("admin_servicios")


# ============================
# CREAR ADMIN
# ============================

def create_admin(request):
    if User.objects.filter(username="admin").exists():
        return HttpResponse("El superusuario ya existe.")

    User.objects.create_superuser(
        username="admin",
        password="Admin1234!",
        email="admin@example.com"
    )
    return HttpResponse("Superusuario creado correctamente.")

# ============================
# FLUJO DE ESTADOS
# ============================

@login_required
def flujo_solicitud(request, id):
    solicitud = get_object_or_404(SolicitudInformacion, id=id)
    estado = solicitud.estado_actual

    # Si no hay estado asignado, toma el primero activo
    if not estado:
        estado = Estado.objects.filter(activo=True).order_by('orden').first()
        solicitud.estado_actual = estado
        solicitud.save()

    # Si el estado no tiene template definido, usa uno por defecto
    template = estado.template if estado and estado.template else "estado_default.html"

    return render(request, f"estados/{template}", {
        "solicitud": solicitud,
        "estado": estado
    })

# ============================
# AVANZAR ESTADO (CORREGIDO)
# ============================

@login_required
def avanzar_estado(request, id):
    solicitud = get_object_or_404(SolicitudInformacion, id=id)
    estado = solicitud.estado_actual.codigo

    # 6 — CLIENTE SUBE PAGO INICIAL
    if estado == "aceptada":
        solicitud.estado_actual = Estado.objects.get(codigo="pago_inicial")
        solicitud.save()
        return redirect("flujo_solicitud", id=id)

    # 7 — ADMIN CONFIRMA PAGO INICIAL
    if estado == "pago_inicial":
        solicitud.estado_actual = Estado.objects.get(codigo="en_ejecucion")
        solicitud.save()
        return redirect("flujo_solicitud", id=id)

    # 8 — ADMIN CONFIRMA ENTREGA
    if estado == "en_ejecucion":
        solicitud.estado_actual = Estado.objects.get(codigo="completado")
        solicitud.save()
        return redirect("flujo_solicitud", id=id)

    # 9 — ADMIN SOLICITA PAGO FINAL
    if estado == "completado":
        return redirect("flujo_solicitud", id=id)

    # 10 — CLIENTE SUBE PAGO FINAL
    if estado == "pago_final":
        solicitud.estado_actual = Estado.objects.get(codigo="pagada")
        solicitud.save()
        return redirect("flujo_solicitud", id=id)

    # 11 — ADMIN CONFIRMA PAGO FINAL
    if estado == "pagada":
        solicitud.estado_actual = Estado.objects.get(codigo="finalizado")
        solicitud.save()
        return redirect("flujo_solicitud", id=id)

    # AVANCE NORMAL
    estado_actual = solicitud.estado_actual
    siguiente = Estado.objects.filter(
        orden__gt=estado_actual.orden,
        activo=True
    ).order_by('orden').first()

    if siguiente:
        solicitud.estado_actual = siguiente
        solicitud.save()

    if siguiente and siguiente.codigo == "asignada":
        return redirect("subir_cotizacion", id=id)

    if siguiente and siguiente.codigo == "enviada":
        return redirect("esperar_respuesta_cliente", id=id)

    return redirect("flujo_solicitud", id=id)


# ============================
# RETROCEDER ESTADO
# ============================

@login_required
def retroceder_estado(request, id):
    solicitud = get_object_or_404(SolicitudInformacion, id=id)
    estado_actual = solicitud.estado_actual

    anterior = Estado.objects.filter(
        orden__lt=estado_actual.orden,
        activo=True
    ).order_by('-orden').first()

    if anterior:
        solicitud.estado_actual = anterior
        solicitud.save()

    return redirect("flujo_solicitud", id=id)


# ============================
# ESTADO 2 — ASIGNAR EXPERTO
# ============================

@login_required
def asignar_experto(request, id):
    solicitud = get_object_or_404(SolicitudInformacion, id=id)

    if request.method == "POST":
        solicitud.experto_nombre = request.POST.get("experto_nombre")
        solicitud.experto_email = request.POST.get("experto_email")
        solicitud.experto_telefono = request.POST.get("experto_telefono")

        siguiente = Estado.objects.filter(
            orden__gt=solicitud.estado_actual.orden,
            activo=True
        ).order_by('orden').first()

        if siguiente:
            solicitud.estado_actual = siguiente

        solicitud.save()
        return redirect("flujo_solicitud", id=id)

    return render(request, "estados/revisada.html", {"solicitud": solicitud})


# ============================
# ESTADO 3 — SUBIR COTIZACIÓN
# ============================

@login_required
def subir_cotizacion(request, id):
    solicitud = get_object_or_404(SolicitudInformacion, id=id)

    if request.method == "POST":
        archivo = request.FILES.get("cotizacion_pdf")
        monto = request.POST.get("monto")
        tiempo = request.POST.get("tiempo_estimado")

        presupuesto, _ = Presupuesto.objects.get_or_create(solicitud=solicitud)
        presupuesto.archivo = archivo
        presupuesto.total = monto
        presupuesto.save()

        solicitud.tiempo_estimado = tiempo

        siguiente = Estado.objects.filter(
            orden__gt=solicitud.estado_actual.orden,
            activo=True
        ).order_by('orden').first()

        if siguiente:
            solicitud.estado_actual = siguiente

        solicitud.save()
        return redirect("flujo_solicitud", id=id)

    return render(request, "estados/asignada.html", {"solicitud": solicitud})


# ============================
# ESTADO 4 — ENVIAR COTIZACIÓN
# ============================

@login_required
def enviar_cotizacion(request, id):
    solicitud = get_object_or_404(SolicitudInformacion, id=id)

    if request.method == "POST":
        siguiente = Estado.objects.filter(
            orden__gt=solicitud.estado_actual.orden,
            activo=True
        ).order_by('orden').first()

        if siguiente:
            solicitud.estado_actual = siguiente
            solicitud.save()

        return redirect("flujo_solicitud", id=id)

    return render(request, "estados/cotizada.html", {"solicitud": solicitud})


# ============================
# ESTADO 5 — RESPUESTA CLIENTE
# ============================

@login_required
def esperar_respuesta_cliente(request, id):
    solicitud = get_object_or_404(SolicitudInformacion, id=id)
    return render(request, "estados/enviada.html", {"solicitud": solicitud})


def aceptar_cotizacion(request, id):
    solicitud = get_object_or_404(SolicitudInformacion, id=id)
    solicitud.estado_actual = Estado.objects.get(codigo="aceptada")
    solicitud.save()
    return redirect("flujo_solicitud", id=id)


def rechazar_cotizacion(request, id):
    solicitud = get_object_or_404(SolicitudInformacion, id=id)
    solicitud.estado_actual = Estado.objects.get(codigo="rechazada")
    solicitud.save()
    return redirect("flujo_solicitud", id=id)


# ============================
# ESTADO 6 — PAGO INICIAL
# ============================

@login_required
def pago_inicial(request, id):
    solicitud = get_object_or_404(SolicitudInformacion, id=id)

    if request.method == "POST":
        solicitud.pago_inicial_archivo = request.FILES.get("pago_inicial")
        solicitud.pago_inicial_monto = request.POST.get("monto_pagado")
        solicitud.save()
        return redirect("avanzar_estado", id=id)

    return render(request, "estados/aceptada.html", {"solicitud": solicitud})


# ============================
# ESTADO 7 — CONFIRMAR PAGO INICIAL
# ============================

@login_required
def confirmar_pago_inicial(request, id):
    return redirect("avanzar_estado", id=id)


# ============================
# ESTADO 8 — EN EJECUCIÓN
# ============================

@login_required
def en_ejecucion(request, id):
    solicitud = get_object_or_404(SolicitudInformacion, id=id)

    if request.method == "POST":
        solicitud.avance_archivo = request.FILES.get("avance")
        solicitud.avance_comentarios = request.POST.get("comentarios")
        solicitud.save()

    return render(request, "estados/en_ejecucion.html", {"solicitud": solicitud})


# ============================
# ESTADO 9 — ENTREGA
# ============================

@login_required
def confirmar_entrega(request, id):
    return redirect("avanzar_estado", id=id)


# ============================
# ESTADO 10 — PAGO FINAL
# ============================

@login_required
def pago_final(request, id):
    solicitud = get_object_or_404(SolicitudInformacion, id=id)

    # Si el cliente entra a pagar, cambiar estado a "pago_final"
    if solicitud.estado_actual.codigo == "completado":
        solicitud.estado_actual = Estado.objects.get(codigo="pago_final")
        solicitud.save()

    if request.method == "POST":
        solicitud.pago_final_archivo = request.FILES.get("pago_final")
        solicitud.pago_final_monto = request.POST.get("monto_final")
        solicitud.save()
        return redirect("avanzar_estado", id=id)

    return render(request, "estados/pagada.html", {"solicitud": solicitud})

@login_required
def pago_final_cliente(request, codigo):
    solicitud = get_object_or_404(SolicitudInformacion, codigo_seguimiento=codigo)

    if solicitud.estado_actual.codigo == "completado":
        solicitud.estado_actual = Estado.objects.get(codigo="pago_final")
        solicitud.save()

    if request.method == "POST":
        solicitud.pago_final_archivo = request.FILES.get("pago_final")
        solicitud.pago_final_monto = request.POST.get("monto_final")
        solicitud.estado_actual = Estado.objects.get(codigo="pagada")
        solicitud.save()
        # 🔁 Redirige al seguimiento del cliente
        return redirect("seguimiento", codigo=codigo)

    # Solo muestra el formulario si aún no se ha pagado
    return render(request, "estados/pago_final_cliente.html", {"solicitud": solicitud})

@login_required
def finalizar_solicitud(request, id):
    solicitud = get_object_or_404(SolicitudInformacion, id=id)
    solicitud.estado_actual = Estado.objects.get(codigo="finalizado")
    solicitud.save()
    return redirect("admin_solicitudes")