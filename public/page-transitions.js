// Page transitions + bottom sheet - 00o.uz
(function() {
  const style = document.createElement('style');
  style.textContent = 'body{opacity:0;animation:pageIn .5s ease-out forwards}@keyframes pageIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}.bs-backdrop{position:fixed;inset:0;background:rgba(0,0,0,0.5);z-index:10000;opacity:0;pointer-events:none;transition:.3s}.bs-backdrop.open{opacity:1;pointer-events:auto}.bottom-sheet{position:fixed;left:0;right:0;bottom:0;z-index:10001;background:linear-gradient(180deg,rgba(30,41,59,0.98),rgba(15,23,42,0.98));backdrop-filter:blur(20px);border-top:1px solid rgba(255,255,255,0.1);border-radius:24px 24px 0 0;max-height:80vh;padding:12px 20px 24px;transform:translateY(100%);transition:.4s cubic-bezier(0.16,1,0.3,1)}.bottom-sheet.open{transform:translateY(0)}.bs-handle{width:40px;height:4px;background:rgba(255,255,255,0.2);border-radius:2px;margin:0 auto 16px}.bs-title{font-size:18px;font-weight:700;margin-bottom:16px}';
  document.head.appendChild(style);
  window.bottomSheet = function(title, content) {
    const back = document.createElement('div');
    back.className = 'bs-backdrop';
    const sheet = document.createElement('div');
    sheet.className = 'bottom-sheet';
    sheet.innerHTML = `<div class="bs-handle"></div><div class="bs-title">${title}</div><div class="bs-content">${content}</div>`;
    document.body.appendChild(back);
    document.body.appendChild(sheet);
    requestAnimationFrame(() => { back.classList.add('open'); sheet.classList.add('open'); });
    const close = () => { back.classList.remove('open'); sheet.classList.remove('open'); setTimeout(() => { back.remove(); sheet.remove(); }, 400); };
    back.onclick = close;
    return { close, sheet };
  };
})();
