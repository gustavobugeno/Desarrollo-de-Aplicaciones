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

  const progressSection = document.querySelector('.progress-section');
  const isProjectComplete = progressSection && progressSection.classList.contains('project-complete');

  if (isProjectComplete) {
    progressSteps.forEach((step) => {
      const indicator = step.querySelector('.step-indicator');
      const connector = step.querySelector('.step-connector');
      const content = step.querySelector('.step-content');
      const title = step.querySelector('.step-title');
      const description = step.querySelector('.step-description');

      step.classList.remove('active');
      step.classList.add('completed');
      step.style.opacity = '1';

      if (indicator) {
        indicator.style.background = 'linear-gradient(135deg, #2a2aff 0%, #5f4bff 100%)';
        indicator.style.borderColor = '#2a2aff';
        indicator.style.color = '#ffffff';
        indicator.style.boxShadow = '0 16px 36px rgba(42, 42, 255, 0.22)';
      }

      if (connector) {
        connector.style.background = 'linear-gradient(180deg, #2a2aff 0%, #5f4bff 100%)';
      }

      if (content) {
        content.style.background = 'linear-gradient(135deg, #f5f7ff 0%, #eef2ff 100%)';
        content.style.borderColor = 'rgba(42, 42, 255, 0.2)';
        content.style.boxShadow = '0 16px 40px rgba(42, 42, 255, 0.12)';
      }

      if (title) {
        title.style.color = '#171c35';
      }

      if (description) {
        description.style.color = '#4b5563';
      }
    });
  }

  const animateOnScroll = () => {
    const trackingHeader = document.querySelector('.tracking-header');
    const clientInfo = document.querySelector('.client-info');

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
