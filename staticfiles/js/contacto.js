document.addEventListener('DOMContentLoaded', () => {
  const copyCards = document.querySelectorAll('.copy-card');
  const toast = document.getElementById('copy-toast');
  const backButton = document.getElementById('contact-back');

  const showToast = (message) => {
    if (!toast) return;
    toast.textContent = message;
    toast.classList.remove('hidden');
    toast.classList.add('visible');
    window.setTimeout(() => {
      toast.classList.remove('visible');
      toast.classList.add('hidden');
    }, 1900);
  };

  copyCards.forEach((card) => {
    card.addEventListener('click', async () => {
      const copyText = card.dataset.copy;
      try {
        await navigator.clipboard.writeText(copyText);
        copyCards.forEach((item) => item.classList.remove('copied'));
        card.classList.add('copied');
        showToast(`Copiado: ${copyText}`);
      } catch (error) {
        showToast('No se pudo copiar. Intenta de nuevo.');
      }
    });
  });

  if (backButton) {
    backButton.addEventListener('click', () => {
      window.location.href = '/';
    });
  }

  const cardContainer = document.querySelector('.contact-card');
  if (cardContainer) {
    cardContainer.classList.add('fade-in-contact');
  }
});
