// 00o.uz - Global utilities (must be loaded first)
(function(){
  'use strict';
  try {
  // ===== TOAST =====
  function ensureToastHost(){
    var h = document.getElementById('__oo_toast_host');
    if (!h) {
      h = document.createElement('div');
      h.id = '__oo_toast_host';
      h.style.cssText = 'position:fixed;top:20px;right:20px;left:20px;z-index:99999;display:flex;flex-direction:column;gap:8px;pointer-events:none;align-items:flex-end;';
      document.body.appendChild(h);
    }
    return h;
  }
  function showToast(msg, type, emoji){
    try {
      var h = ensureToastHost();
      var t = document.createElement('div');
      t.style.cssText = 'background:rgba(15,20,35,0.95);backdrop-filter:blur(20px);color:white;padding:12px 18px;border-radius:12px;font-size:14px;font-weight:600;box-shadow:0 8px 32px rgba(0,0,0,0.4);border:1px solid rgba(255,255,255,0.1);animation:ooToastIn 0.3s ease;pointer-events:auto;display:flex;align-items:center;gap:8px;max-width:90%;';
      if (type==='success') t.style.borderColor = 'rgba(34,197,94,0.5)';
      if (type==='error') t.style.borderColor = 'rgba(239,68,68,0.5)';
      t.innerHTML = (emoji || (type==='success' ? '✅' : type==='error' ? '❌' : 'ℹ️')) + ' ' + msg;
      h.appendChild(t);
      setTimeout(function(){ t.style.animation='ooToastOut 0.3s ease'; setTimeout(function(){ if(t.parentNode) t.remove(); }, 300); }, 2500);
    } catch(e) { console.log('Toast:', msg); }
  }
  var style = document.createElement('style');
  style.textContent = '@keyframes ooToastIn{from{opacity:0;transform:translateX(100%)}to{opacity:1;transform:translateX(0)}}@keyframes ooToastOut{from{opacity:1}to{opacity:0;transform:translateX(100%)}}';
  document.head.appendChild(style);
  window.toast = {
    success: function(m, e) { showToast(m, 'success', e); },
    error: function(m, e) { showToast(m, 'error', e); },
    info: function(m, e) { showToast(m, 'info', e); }
  };

  // ===== CONFETTI =====
  window.confetti = function(opts){
    opts = opts || {};
    var count = opts.count || 30;
    var colors = ['#8b5cf6','#ec4899','#06b6d4','#22c55e','#fbbf24','#ef4444'];
    var host = document.getElementById('__oo_confetti_host');
    if (!host) {
      host = document.createElement('div');
      host.id = '__oo_confetti_host';
      host.style.cssText = 'position:fixed;inset:0;pointer-events:none;z-index:99998;overflow:hidden;';
      document.body.appendChild(host);
    }
    for (var i = 0; i < count; i++) {
      var p = document.createElement('div');
      var c = colors[Math.floor(Math.random()*colors.length)];
      p.style.cssText = 'position:absolute;width:8px;height:8px;background:'+c+';top:-10px;left:'+Math.random()*100+'%;border-radius:'+(Math.random()>0.5?'50%':'0')+';animation:ooFall '+(2+Math.random()*2)+'s linear forwards;';
      host.appendChild(p);
    }
    setTimeout(function(){ if(host) host.innerHTML=''; }, 4000);
  };
  var cstyle = document.createElement('style');
  cstyle.textContent = '@keyframes ooFall{to{transform:translateY(110vh) rotate(720deg);opacity:0}}';
  document.head.appendChild(cstyle);

  // ===== STORAGE (localStorage with JSON) =====
  function _ls(){
    try { return window.localStorage; } catch(e){ return null; }
  }
  window.oo = {
    save: function(key, val){
      try { _ls().setItem('oo-'+key, JSON.stringify(val)); } catch(e){}
    },
    load: function(key, def){
      try {
        var v = _ls().getItem('oo-'+key);
        return v === null ? def : JSON.parse(v);
      } catch(e){ return def; }
    },
    del: function(key){
      try { _ls().removeItem('oo-'+key); } catch(e){}
    }
  };

  // ===== HAPTIC (vibration) =====
  window.vibrate = function(p){ try { if(navigator.vibrate) navigator.vibrate(p || 50); } catch(e){} };

  // ===== SHARE =====
  window.shareData = function(data){
    if (navigator.share) {
      navigator.share(data).catch(function(){});
    } else {
      try { navigator.clipboard.writeText(data.url || data.text || ''); toast.success('Nusxalandi!'); } catch(e){}
    }
  };
  } catch(err){ console.error('global.js init:', err); }
})();
