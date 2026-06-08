document.addEventListener('DOMContentLoaded', () => {
  const btnSolicitarCambios = document.getElementById('btn-solicitar-cambios');
  const formCambios = document.getElementById('form-cambios');

  if (btnSolicitarCambios && formCambios) {
    btnSolicitarCambios.addEventListener('click', () => {
      const isHidden = formCambios.style.display === 'none';
      if (isHidden) {
        formCambios.style.display = 'block';
        btnSolicitarCambios.textContent = 'Cancelar cambios';
        btnSolicitarCambios.classList.add('btn-secondary');
        btnSolicitarCambios.classList.remove('btn-warning');
      } else {
        formCambios.style.display = 'none';
        btnSolicitarCambios.textContent = 'Solicitar cambios';
        btnSolicitarCambios.classList.remove('btn-secondary');
        btnSolicitarCambios.classList.add('btn-warning');
      }
    });
  }

  const progressSteps = document.querySelectorAll('[data-paso]');
  progressSteps.forEach((step, index) => {
    const paso = parseInt(step.getAttribute('data-paso'), 10);
    const estado = parseInt(step.getAttribute('data-estado'), 10);

    if (paso < estado) {
      step.classList.add('completed');
    } else if (paso === estado) {
      step.classList.add('active');
    }
  });

  const animateOnScroll = () => {
    const trackingHeader = document.querySelector('.tracking-header');
    const clientInfo = document.querySelector('.client-info');
    const progressSection = document.querySelector('.progress-section');

    if (trackingHeader) {
      trackingHeader.style.opacity = '1';
      trackingHeader.style.transform = 'translateY(0)';
    }

    const delay = (element, ms) => {
      if (element) {
        setTimeout(() => {
          element.style.opacity = '1';
          element.style.transform = 'translateY(0)';
        }, ms);
      }
    };

    delay(clientInfo, 150);
    delay(progressSection, 300);
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', animateOnScroll);
  } else {
    animateOnScroll();
  }
});
