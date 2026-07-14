// 00o.uz — Global utilities (must be loaded first)
(function(){
  'use strict';

  // ===== TOAST =====
  function ensureToastHost(){
    let h = document.getElementById('__oo_toast_host');
    if (!h) {
      h = document.createElement('div');
      h.id = '__oo_toast_host';
      h.style.cssText = 'position:fixed;top:20px;right:20px;z-index:99999;display:flex;flex-direction:column;gap:8px;pointer-events:none;';
      document.body.appendChild(h);
    }
    return h;
  }
  function showToast(msg, type, emoji){
    try {
      const h = ensureToastHost();
      const t = document.createElement('div');
      t.style.cssText = 'background:rgba(15,20,35,0.95);backdrop-filter:blur(20px);color:white;padding:12px 18px;border-radius:12px;font-size:14px;font-weight:600;box-shadow:0 8px 32px rgba(0,0,0,0.4);border:1px solid rgba(255,255,255,0.1);animation:ooToastIn 0.3s ease;pointer-events:auto;display:flex;align-items:center;gap:8px;';
      if (type==='success') t.style.borderColor = 'rgba(34,197,94,0.5)';
      if (type==='error') t.style.borderColor = 'rgba(239,68,68,0.5)';
      t.innerHTML = (emoji || (type==='success' ? '✅' : type==='error' ? '❌' : 'ℹ️')) + ' ' + msg;
      h.appendChild(t);
      setTimeout(() => { t.style.animation='ooToastOut 0.3s ease'; setTimeout(()=>t.remove(), 300); }, 2500);
    } catch(e) { console.log('Toast:', msg); }
  }
  const style = document.createElement('style');
  style.textContent = '@keyframes ooToastIn{from{opacity:0;transform:translateX(100%)}to{opacity:1;transform:translateX(0)}}@keyframes ooToastOut{from{opacity:1}to{opacity:0;transform:translateX(100%)}}';
  document.head.appendChild(style);
  window.toast = {
    success: (m, e) => showToast(m, 'success', e),
    error: (m, e) => showToast(m, 'error', e),
    info: (m, e) => showToast(m, 'info', e)
  };

  // ===== CONFETTI =====
  window.confetti = function(opts){
    opts = opts || {};
    const count = opts.count || 30;
    const colors = ['#8b5cf6','#ec4899','#06b6d4','#22c55e','#fbbf24','#ef4444'];
    let host = document.getElementById('__oo_confetti_host');
    if (!host) {
      host = document.createElement('div');
      host.id = '__oo_confetti_host';
      host.style.cssText = 'position:fixed;inset:0;pointer-events:none;z-index:99998;overflow:hidden;';
      document.body.appendChild(host);
    }
    for (let i = 0; i < count; i++) {
      const p = document.createElement('div');
      const size = 6 + Math.random() * 8;
      p.style.cssText = `position:absolute;width:${size}px;height:${size}px;background:${colors[Math.floor(Math.random()*colors.length)]};left:${Math.random()*100}%;top:-20px;border-radius:2px;`;
      host.appendChild(p);
      const duration = 1500 + Math.random() * 1500;
      const drift = (Math.random() - 0.5) * 200;
      p.animate([
        { transform: `translate(0,0) rotate(0deg)`, opacity: 1 },
        { transform: `translate(${drift}px, ${window.innerHeight + 50}px) rotate(${360 + Math.random()*360}deg)`, opacity: 0 }
      ], { duration, easing: 'cubic-bezier(0.2, 0.8, 0.4, 1)' });
      setTimeout(()=>p.remove(), duration);
    }
  };

  // ===== PWA SERVICE WORKER =====
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/sw.js').catch(()=>{});
    });
  }

  // ===== MOBILE MENU HELPER (optional for pages) =====
  window.ooBack = function(label){
    const a = document.createElement('a');
    a.href = '/index.html';
    a.innerHTML = '← ' + (label || 'Bosh sahifa');
    a.style.cssText = 'position:fixed;top:12px;left:12px;z-index:9999;padding:8px 14px;background:rgba(0,0,0,0.6);backdrop-filter:blur(20px);color:white;text-decoration:none;border-radius:100px;font-size:13px;font-weight:600;border:1px solid rgba(255,255,255,0.1);display:flex;align-items:center;gap:4px;';
    return a;
  };

  // ===== UTILS =====
  window.oo = {
    fmt(n) { try { return Number(n).toLocaleString('uz-UZ'); } catch(e) { return n; } },
    save(k, v) { try { localStorage.setItem('oo-' + k, JSON.stringify(v)); } catch(e){} },
    load(k, d) { try { return JSON.parse(localStorage.getItem('oo-' + k)) || d; } catch(e) { return d; } },
    today() { return new Date().toDateString(); }
  };

  // Auto-add back button if not on home and no other fixed top elements
  document.addEventListener('DOMContentLoaded', function(){
    if (location.pathname !== '/' && location.pathname !== '/index.html' && !document.getElementById('__oo_back')) {
      const back = window.ooBack();
      back.id = '__oo_back';
      document.body.appendChild(back);
    }
  });

  console.log('🚀 00o.uz ready');
})();
