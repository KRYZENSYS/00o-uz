// PWA install + offline - 00o.uz
(function() {
  const style = document.createElement('style');
  style.textContent = `
  .pwa-banner { position: fixed; bottom: 80px; right: 20px; z-index: 9999;
    background: linear-gradient(135deg, #8b5cf6, #06b6d4); color: white;
    padding: 16px 20px; border-radius: 16px; box-shadow: 0 10px 40px rgba(139,92,246,0.4);
    max-width: 320px; display: flex; align-items: center; gap: 12px;
    animation: pwaSlide 0.5s cubic-bezier(0.16, 1, 0.3, 1); }
  .pwa-banner.hide { animation: pwaSlideOut 0.4s ease-out forwards; }
  .pwa-icon { font-size: 32px; }
  .pwa-content { flex: 1; }
  .pwa-title { font-weight: 700; font-size: 14px; }
  .pwa-sub { font-size: 12px; opacity: 0.9; }
  .pwa-actions { display: flex; flex-direction: column; gap: 4px; }
  .pwa-btn { padding: 6px 12px; border-radius: 8px; border: none; font-size: 11px; font-weight: 600; cursor: pointer; }
  .pwa-install { background: white; color: #8b5cf6; }
  .pwa-close { background: rgba(255,255,255,0.2); color: white; }
  @keyframes pwaSlide { from { transform: translateX(120%); } to { transform: translateX(0); } }
  @keyframes pwaSlideOut { to { transform: translateX(120%); opacity: 0; } }
  .pwa-status { position: fixed; top: 80px; left: 20px; z-index: 9999;
    padding: 8px 14px; border-radius: 100px; font-size: 12px; font-weight: 600;
    background: rgba(15,23,42,0.9); backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.1); color: white;
    display: flex; align-items: center; gap: 6px; opacity: 0; transition: 0.3s; }
  .pwa-status.show { opacity: 1; }
  .pwa-dot { width: 8px; height: 8px; border-radius: 50%; background: #22c55e; }
  .pwa-dot.offline { background: #ef4444; }
  `;
  document.head.appendChild(style);

  let deferredPrompt = null;
  window.addEventListener('beforeinstallprompt', e => {
    e.preventDefault();
    deferredPrompt = e;
    if (!localStorage.getItem('pwa-dismissed')) showBanner();
  });

  function showBanner() {
    const b = document.createElement('div');
    b.className = 'pwa-banner';
    b.innerHTML = `
      <div class="pwa-icon">📱</div>
      <div class="pwa-content">
        <div class="pwa-title">00o.uz ni o'rnating</div>
        <div class="pwa-sub">Tezroq, offline, to'liq ekran</div>
      </div>
      <div class="pwa-actions">
        <button class="pwa-btn pwa-install">O'rnatish</button>
        <button class="pwa-btn pwa-close">Keyin</button>
      </div>
    `;
    document.body.appendChild(b);
    b.querySelector('.pwa-install').onclick = async () => {
      if (deferredPrompt) {
        deferredPrompt.prompt();
        await deferredPrompt.userChoice;
        deferredPrompt = null;
        b.classList.add('hide');
        setTimeout(() => b.remove(), 400);
      }
    };
    b.querySelector('.pwa-close').onclick = () => {
      b.classList.add('hide');
      localStorage.setItem('pwa-dismissed', '1');
      setTimeout(() => b.remove(), 400);
    };
  }

  function showStatus(online) {
    let s = document.querySelector('.pwa-status');
    if (!s) {
      s = document.createElement('div');
      s.className = 'pwa-status';
      document.body.appendChild(s);
    }
    s.innerHTML = `<div class="pwa-dot ${online ? '' : 'offline'}"></div>${online ? '🌐 Onlayn' : '📴 Oflayn rejim'}`;
    s.classList.add('show');
    clearTimeout(s._timer);
    s._timer = setTimeout(() => s.classList.remove('show'), 3000);
  }

  window.addEventListener('online', () => showStatus(true));
  window.addEventListener('offline', () => showStatus(false));
  setTimeout(() => showStatus(navigator.onLine), 2000);
})();
