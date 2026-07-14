// 00o.uz — Per-page safe wrapper (use this in all app pages)
(function(){
  'use strict';
  // Make sure toast/confetti exist even if global.js failed
  if (!window.toast) {
    window.toast = {
      success: function(m){ try { alert('✅ ' + m); } catch(e){} },
      error: function(m){ try { alert('❌ ' + m); } catch(e){} },
      info: function(m){ try { alert('ℹ️ ' + m); } catch(e){} }
    };
  }
  if (!window.confetti) {
    window.confetti = function(){ /* noop */ };
  }
  // Safe storage wrapper
  window.oo = window.oo || {
    fmt: function(n){ try { return Number(n).toLocaleString('uz-UZ'); } catch(e) { return String(n); } },
    save: function(k, v){ try { localStorage.setItem('oo-' + k, JSON.stringify(v)); } catch(e){ console.warn('save err', e); } },
    load: function(k, d){ try { var v = localStorage.getItem('oo-' + k); return v ? JSON.parse(v) : d; } catch(e) { return d; } },
    today: function(){ return new Date().toDateString(); }
  };
})();
