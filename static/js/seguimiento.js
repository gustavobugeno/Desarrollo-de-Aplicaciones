document.addEventListener('DOMContentLoaded', () => {
  const btnSolicitarCambios = document.getElementById('btn-solicitar-cambios');
  const formCambios = document.getElementById('form-cambios');

  if (btnSolicitarCambios && formCambios) {
    btnSolicitarCambios.addEventListener('click', () => {
      const isHidden = formCambios.style.display === 'none';
      if (isHidden) {
        formCambios.style.display = 'block';
        btnSolicitarCambios.textContent = 'Cancelar cambios';
      } else {
        formCambios.style.display = 'none';
        btnSolicitarCambios.textContent = 'Solicitar cambios';
      }
    });
  }

  // ============================
  // MARCAR PASOS ACTIVE / COMPLETED
  // ============================

  const progressSteps = document.querySelectorAll('[data-paso]');
  if (!progressSteps.length) return;

  // tomo el estado desde el primer paso (todos tienen el mismo estado_codigo)
  const estadoActual = progressSteps[0].getAttribute('data-estado');

  const ordenEstados = [
    "recibida",
    "asignacion_experto",
    "experto_asignado",
    "presupuesto_creado",
    "enviada",
    "aceptada",
    "pago_inicial",
    "en_ejecucion",
    "completado",
    "pagada"
  ];

  const pasoActual = ordenEstados.indexOf(estadoActual) + 1;

  progressSteps.forEach(step => {
    const paso = parseInt(step.getAttribute('data-paso'), 10);

    if (paso < pasoActual) {
      step.classList.add('completed');
    } else if (paso === pasoActual) {
      step.classList.add('active');
    }
  });
});
// ============================
// SINCRONIZAR COLOR CON ESTADO
// ============================

document.addEventListener('DOMContentLoaded', () => {
  const progressSteps = document.querySelectorAll('.progress-step');
  const estadoActual = "{{ estado_codigo }}"; // viene del template

  progressSteps.forEach(step => {
    const paso = parseInt(step.getAttribute('data-paso'), 10);
    const ordenEstados = [
      "recibida",
      "asignacion_experto",
      "experto_asignado",
      "presupuesto_creado",
      "enviada",
      "aceptada",
      "pago_inicial",
      "en_ejecucion",
      "completado",
      "pagada"
    ];

    const pasoActual = ordenEstados.indexOf(estadoActual) + 1;

    // Actualiza el atributo data-estado dinámicamente
    step.setAttribute('data-estado', estadoActual);

    // Aplica clases visuales
    if (paso < pasoActual) {
      step.classList.add('completed');
    } else if (paso === pasoActual) {
      step.classList.add('active');
    }
  });
});
