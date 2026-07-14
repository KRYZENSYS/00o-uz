// Toast notification system - 00o.uz
(function() {
  const styles = `
  .oo-toast-container { position: fixed; top: 80px; right: 20px; z-index: 9999; display: flex; flex-direction: column; gap: 10px; pointer-events: none; max-width: 380px; }
  .oo-toast { background: linear-gradient(135deg, rgba(30,41,59,0.98), rgba(15,23,42,0.98)); backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.1); border-radius: 14px; padding: 14px 18px;
    display: flex; align-items: center; gap: 12px; min-width: 280px; box-shadow: 0 10px 40px rgba(0,0,0,0.4);
    color: white; font-size: 14px; pointer-events: auto; animation: oo-slide-in 0.4s cubic-bezier(0.16, 1, 0.3, 1); position: relative; overflow: hidden; }
  .oo-toast.removing { animation: oo-slide-out 0.3s ease-out forwards; }
  .oo-toast::before { content: ''; position: absolute; left: 0; top: 0; bottom: 0; width: 4px; }
  .oo-toast.success::before { background: linear-gradient(180deg, #22c55e, #06b6d4); }
  .oo-toast.error::before { background: linear-gradient(180deg, #ef4444, #f59e0b); }
  .oo-toast.info::before { background: linear-gradient(180deg, #06b6d4, #8b5cf6); }
  .oo-toast.warning::before { background: linear-gradient(180deg, #f59e0b, #ef4444); }
  .oo-toast.achievement::before { background: linear-gradient(180deg, #fbbf24, #f59e0b); }
  .oo-toast-icon { font-size: 24px; flex-shrink: 0; }
  .oo-toast-content { flex: 1; }
  .oo-toast-title { font-weight: 700; margin-bottom: 2px; }
  .oo-toast-msg { color: #94a3b8; font-size: 12px; }
  .oo-toast-close { background: rgba(255,255,255,0.05); border: none; color: #94a3b8;
    width: 24px; height: 24px; border-radius: 50%; cursor: pointer; font-size: 14px; flex-shrink: 0; }
  .oo-toast-close:hover { background: rgba(255,255,255,0.1); color: white; }
  .oo-toast-progress { position: absolute; bottom: 0; left: 0; height: 3px; background: linear-gradient(90deg, #8b5cf6, #06b6d4);
    width: 100%; transform-origin: left; animation: oo-progress 4s linear forwards; }
  @keyframes oo-slide-in { from { transform: translateX(120%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
  @keyframes oo-slide-out { to { transform: translateX(120%); opacity: 0; } }
  @keyframes oo-progress { from { transform: scaleX(1); } to { transform: scaleX(0); } }
  @media (max-width: 480px) { .oo-toast-container { right: 10px; left: 10px; max-width: none; } }
  `;
  const styleEl = document.createElement('style');
  styleEl.textContent = styles;
  document.head.appendChild(styleEl);

  let container = null;
  function ensureContainer() {
    if (!container) {
      container = document.createElement('div');
      container.className = 'oo-toast-container';
      document.body.appendChild(container);
    }
    return container;
  }

  window.toast = function(opts) {
    const cfg = typeof opts === 'string' ? { message: opts } : opts;
    const { title, message, type = 'info', icon, duration = 4000 } = cfg;
    const icons = { success: '✅', error: '❌', info: 'ℹ️', warning: '⚠️', achievement: '🏆' };
    const el = document.createElement('div');
    el.className = 'oo-toast ' + type;
    el.innerHTML = `
      <div class="oo-toast-icon">${icon || icons[type] || '📢'}</div>
      <div class="oo-toast-content">
        ${title ? `<div class="oo-toast-title">${title}</div>` : ''}
        <div class="oo-toast-msg">${message || ''}</div>
      </div>
      <button class="oo-toast-close">×</button>
      <div class="oo-toast-progress"></div>`;
    el.querySelector('.oo-toast-close').onclick = () => remove(el);
    ensureContainer().appendChild(el);
    if (duration > 0) {
      setTimeout(() => remove(el), duration);
    }
    return el;
  };

  function remove(el) {
    if (!el.parentNode) return;
    el.classList.add('removing');
    setTimeout(() => el.remove(), 300);
  }

  window.toast.success = (m, t) => window.toast({ message: m, title: t, type: 'success' });
  window.toast.error = (m, t) => window.toast({ message: m, title: t, type: 'error' });
  window.toast.info = (m, t) => window.toast({ message: m, title: t, type: 'info' });
  window.toast.warning = (m, t) => window.toast({ message: m, title: t, type: 'warning' });
  window.toast.achievement = (m, t) => window.toast({ message: m, title: t, type: 'achievement', icon: '🏆', duration: 6000 });
})();
