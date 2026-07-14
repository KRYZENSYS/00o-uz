// Scroll animations - 00o.uz
(function() {
  const style = document.createElement('style');
  style.textContent = `
  .oo-anim { opacity: 0; transition: opacity 0.8s ease, transform 0.8s cubic-bezier(0.16, 1, 0.3, 1); }
  .oo-anim.fade-up { transform: translateY(40px); }
  .oo-anim.fade-down { transform: translateY(-40px); }
  .oo-anim.fade-left { transform: translateX(-40px); }
  .oo-anim.fade-right { transform: translateX(40px); }
  .oo-anim.scale { transform: scale(0.9); }
  .oo-anim.visible { opacity: 1; transform: none; }
  .oo-stagger > * { transition-delay: calc(var(--i, 0) * 0.08s); }
  @media (prefers-reduced-motion: reduce) { .oo-anim { transition: none; opacity: 1; transform: none; } }
  `;
  document.head.appendChild(style);

  function init() {
    document.querySelectorAll('.oo-anim').forEach((el, i) => {
      el.style.setProperty('--i', i % 10);
      observer.observe(el);
    });
  }

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
