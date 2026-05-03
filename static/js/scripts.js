// ============================================
// FUNCIONES DE ANIMACIÓN Y DINAMISMO
// ============================================

/**
 * Anima elementos cuando entran en el viewport (Intersection Observer)
 */
function initScrollAnimations() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
  });

  // Animar tarjetas
  document.querySelectorAll('.card').forEach(card => {
    card.classList.add('fade-in');
    observer.observe(card);
  });

  // Animar títulos
  document.querySelectorAll('h2, h3').forEach(title => {
    title.style.animationDelay = '0.2s';
    observer.observe(title);
  });

  // Animar listas
  document.querySelectorAll('.list-unstyled li').forEach((li, index) => {
    li.style.animationDelay = `${index * 0.1}s`;
    observer.observe(li);
  });
}

/**
 * Anima elementos de lista individualmente
 */
function animateListItems() {
  document.querySelectorAll('.list-unstyled li').forEach((li, index) => {
    li.style.opacity = '0';
    li.style.animation = `fadeInUp 0.5s ease forwards`;
    li.style.animationDelay = `${index * 0.1}s`;
  });
}

/**
 * Agrega efectos de hover a las tarjetas
 */
function addCardHoverEffects() {
  const cards = document.querySelectorAll('.card');
  
  cards.forEach(card => {
    card.addEventListener('mouseenter', function() {
      this.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
      this.style.transform = 'translateY(-8px) scale(1.02)';
    });

    card.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0) scale(1)';
    });

    // Efecto de luz en movimiento del mouse
    card.addEventListener('mousemove', function(e) {
      const rect = this.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      const centerX = rect.width / 2;
      const centerY = rect.height / 2;

      const rotateX = (y - centerY) * 0.05;
      const rotateY = (centerX - x) * 0.05;

      // Aplicar una rotación sutil (3D effect)
      this.style.transform = `
        translateY(-8px) 
        scale(1.02) 
        rotateX(${rotateX}deg) 
        rotateY(${rotateY}deg)
      `;
    });

    card.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0) scale(1) rotateX(0) rotateY(0)';
    });
  });
}

/**
 * Valida el formulario de seguimiento
 */
function initFormValidation() {
  const form = document.querySelector('form');
  if (!form) return;

  const input = form.querySelector('input[name="codigo"]');
  const button = form.querySelector('button[type="submit"]');

  if (input && button) {
    // Validar en tiempo real
    input.addEventListener('input', function() {
      const value = this.value.trim();
      
      if (value.length > 0) {
        button.disabled = false;
        button.style.opacity = '1';
        button.style.cursor = 'pointer';
      } else {
        button.disabled = true;
        button.style.opacity = '0.6';
        button.style.cursor = 'not-allowed';
      }
    });

    // Efectos visuales al focus
    input.addEventListener('focus', function() {
      this.parentElement.style.boxShadow = '0 0 15px rgba(85, 85, 255, 0.3)';
      this.style.borderColor = '#5555ff';
    });

    input.addEventListener('blur', function() {
      this.parentElement.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
      this.style.borderColor = '#ddd';
    });

    // Prevenir envío por defecto y agregar feedback visual
    form.addEventListener('submit', function(e) {
      e.preventDefault();
      
      if (input.value.trim().length > 0) {
        // Animación de envío
        button.innerHTML = 'Buscando...';
        button.disabled = true;

        // Simular búsqueda
        setTimeout(() => {
          button.innerHTML = 'Revisar';
          button.disabled = false;
          input.value = '';
          
          // Mostrar mensaje de éxito
          showSuccessMessage('Búsqueda completada');
        }, 1500);
      }
    });
  }
}

/**
 * Muestra un mensaje de éxito temporal
 */
function showSuccessMessage(message) {
  const messageDiv = document.createElement('div');
  messageDiv.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: linear-gradient(135deg, #5555ff, #1a1a4d);
    color: white;
    padding: 1rem 1.5rem;
    border-radius: 6px;
    box-shadow: 0 4px 12px rgba(85, 85, 255, 0.4);
    z-index: 1000;
    animation: slideInLeft 0.3s ease;
    font-weight: 500;
  `;
  messageDiv.textContent = message;

  document.body.appendChild(messageDiv);

  setTimeout(() => {
    messageDiv.style.animation = 'slideInLeft 0.3s ease reverse';
    setTimeout(() => {
      messageDiv.remove();
    }, 300);
  }, 2000);
}

/**
 * Agrega efecto de ripple a los botones
 */
function addRippleEffect() {
  const buttons = document.querySelectorAll('.btn');
  
  buttons.forEach(button => {
    button.addEventListener('click', function(e) {
      const ripple = document.createElement('span');
      const rect = this.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      const x = e.clientX - rect.left - size / 2;
      const y = e.clientY - rect.top - size / 2;

      ripple.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        background: rgba(255, 255, 255, 0.5);
        border-radius: 50%;
        left: ${x}px;
        top: ${y}px;
        pointer-events: none;
        animation: ripple-animation 0.6s ease-out;
      `;

      // Agregar animación de ripple si no existe
      if (!document.querySelector('style[data-ripple]')) {
        const style = document.createElement('style');
        style.setAttribute('data-ripple', 'true');
        style.textContent = `
          @keyframes ripple-animation {
            to {
              transform: scale(4);
              opacity: 0;
            }
          }
        `;
        document.head.appendChild(style);
      }

      this.style.position = 'relative';
      this.style.overflow = 'hidden';
      this.appendChild(ripple);

      setTimeout(() => {
        ripple.remove();
      }, 600);
    });
  });
}

/**
 * Anima números en contadores (si existen)
 */
function animateCounters() {
  const counters = document.querySelectorAll('.counter');
  
  counters.forEach(counter => {
    const target = parseInt(counter.textContent);
    const increment = target / 50;
    let current = 0;

    const updateCounter = () => {
      current += increment;
      if (current < target) {
        counter.textContent = Math.floor(current);
        requestAnimationFrame(updateCounter);
      } else {
        counter.textContent = target;
      }
    };

    updateCounter();
  });
}

/**
 * Agrega efecto parallax suave en scroll
 */
function addParallaxEffect() {
  window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const parallaxElements = document.querySelectorAll('[data-parallax]');

    parallaxElements.forEach(element => {
      const speed = element.dataset.parallax || 0.5;
      element.style.transform = `translateY(${scrolled * speed}px)`;
    });
  });
}

/**
 * Agrega navegación suave
 */
function addSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const href = this.getAttribute('href');
      if (href !== '#') {
        e.preventDefault();
        const target = document.querySelector(href);
        if (target) {
          target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
          });
        }
      }
    });
  });
}

/**
 * Aplica animaciones a los checkmarks
 */
function animateCheckmarks() {
  const items = document.querySelectorAll('.list-unstyled li');
  
  items.forEach((item, index) => {
    if (item.textContent.includes('✔')) {
      item.style.animation = `fadeInUp 0.6s ease forwards`;
      item.style.animationDelay = `${index * 0.1}s`;
    }
  });
}

/**
 * Inicializa navbar activa en scroll
 */
function initNavbarActive() {
  const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
  
  window.addEventListener('scroll', () => {
    let current = '';
    const sections = document.querySelectorAll('section, [id]');

    sections.forEach(section => {
      const sectionTop = section.offsetTop;
      const sectionHeight = section.clientHeight;
      if (pageYOffset >= sectionTop - 200) {
        current = section.getAttribute('id');
      }
    });

    navLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === `#${current}`) {
        link.classList.add('active');
      }
    });
  });
}

/**
 * Efecto de escritura en textos
 */
function typewriterEffect(element, speed = 50) {
  if (!element) return;

  const text = element.textContent;
  element.textContent = '';
  let index = 0;

  const type = () => {
    if (index < text.length) {
      element.textContent += text.charAt(index);
      index++;
      setTimeout(type, speed);
    }
  };

  type();
}

/**
 * Maneja el seguimiento de códigos
 */
function handleTracking(event) {
  event.preventDefault();
  const codigo = event.target.querySelector('input[name="codigo"]').value;
  if (codigo.trim()) {
    showSuccessMessage('Código de seguimiento: ' + codigo);
    event.target.reset();
  }
}

/**
 * Inicialización principal
 */
document.addEventListener('DOMContentLoaded', function() {
  console.log('✨ Inicializando dinamismos CBC E.I.R.L');

  // Ejecutar todas las funciones de dinamismo
  initScrollAnimations();
  addCardHoverEffects();
  initFormValidation();
  addRippleEffect();
  animateCheckmarks();
  addSmoothScroll();
  
  // Agregar atributos de datos para parallax (opcional)
  // addParallaxEffect();

  // Animaciones específicas
  setTimeout(() => {
    animateListItems();
  }, 300);

  // Feedback de carga completada
  console.log('✨ Dinamismos aplicados correctamente');
});

// Ejecutar funciones cuando el DOM está listo
window.addEventListener('load', () => {
  // Asegurar que todas las animaciones estén listas
  document.querySelectorAll('.card').forEach(card => {
    card.style.visibility = 'visible';
  });
});

// Exportar funciones para uso externo si es necesario
window.cbcFunctions = {
  showSuccessMessage,
  typewriterEffect,
  animateCounters
};
