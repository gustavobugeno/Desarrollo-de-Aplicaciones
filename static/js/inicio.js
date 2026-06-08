const initInicioPage = () => {
  const observerOptions = {
    threshold: 0.15,
  };

  const revealElements = document.querySelectorAll('.inicio-fade');

  const revealItem = (entry) => {
    if (!entry.isIntersecting) return;
    const element = entry.target;
    const delay = parseFloat(element.dataset.delay || '0');

    window.setTimeout(() => {
      element.classList.add('visible');
    }, delay * 1000);
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => revealItem(entry));
  }, observerOptions);

  revealElements.forEach((element) => observer.observe(element));

  const codigoInput = document.getElementById('codigo');
  const storageKey = 'cbc-seguimiento-codigo';

  if (codigoInput) {
    const savedCodigo = window.localStorage.getItem(storageKey);
    if (savedCodigo) {
      codigoInput.value = savedCodigo;
    }

    codigoInput.addEventListener('input', () => {
      window.localStorage.setItem(storageKey, codigoInput.value.trim());
    });
  }
};

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initInicioPage);
} else {
  initInicioPage();
}
