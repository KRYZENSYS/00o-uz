// Skeleton loader - 00o.uz
(function() {
  const style = document.createElement('style');
  style.textContent = `
  @keyframes shimmer { 0% { background-position: -200% 0; } 100% { background-position: 200% 0; } }
  .skeleton { background: linear-gradient(90deg, rgba(255,255,255,0.03) 0%, rgba(255,255,255,0.08) 50%, rgba(255,255,255,0.03) 100%);
    background-size: 200% 100%; animation: shimmer 1.5s infinite; border-radius: 8px; }
  .sk-text { height: 14px; margin: 8px 0; }
  .sk-title { height: 24px; width: 60%; margin: 12px 0; }
  .sk-avatar { width: 40px; height: 40px; border-radius: 50%; }
  .sk-card { padding: 20px; border-radius: 12px;
    background: linear-gradient(135deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01));
    border: 1px solid rgba(255,255,255,0.06); margin-bottom: 12px; }
  `;
  document.head.appendChild(style);

  window.skeleton = {
    card: () => `<div class="sk-card">
      <div style="display:flex;gap:12px;align-items:center;margin-bottom:16px">
        <div class="skeleton sk-avatar"></div>
        <div style="flex:1"><div class="skeleton sk-title"></div><div class="skeleton sk-text" style="width:40%"></div></div>
      </div>
      <div class="skeleton sk-text"></div>
      <div class="skeleton sk-text"></div>
      <div class="skeleton sk-text" style="width:80%"></div>
    </div>`,
    text: (w=100) => `<div class="skeleton sk-text" style="width:${w}%"></div>`
  };
})();
