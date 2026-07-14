// Floating action button - 00o.uz
(function() {
  const style = document.createElement('style');
  style.textContent = `
  .oo-fab { position: fixed; bottom: 80px; right: 20px; z-index: 9998;
    width: 56px; height: 56px; border-radius: 50%;
    background: linear-gradient(135deg, #8b5cf6, #06b6d4); border: none; color: white;
    font-size: 24px; cursor: pointer; box-shadow: 0 10px 30px rgba(139,92,246,0.4);
    display: flex; align-items: center; justify-content: center;
    transition: 0.3s; }
  .oo-fab:hover { transform: scale(1.1) rotate(90deg); }
  .oo-fab-menu { position: fixed; bottom: 150px; right: 20px; z-index: 9997;
    display: flex; flex-direction: column; gap: 12px; align-items: flex-end;
    opacity: 0; pointer-events: none; transition: 0.3s; transform: translateY(20px); }
  .oo-fab-menu.open { opacity: 1; pointer-events: auto; transform: translateY(0); }
  .oo-fab-item { padding: 10px 16px; background: rgba(15,23,42,0.95); backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.1); border-radius: 100px; color: white;
    font-size: 13px; font-weight: 500; cursor: pointer; display: flex; align-items: center; gap: 8px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3); transition: 0.2s; }
  .oo-fab-item:hover { background: linear-gradient(135deg, #8b5cf6, #06b6d4); transform: translateX(-4px); }
  `;
  document.head.appendChild(style);

  const items = [
    { icon: '➕', label: 'Post yozish', action: () => location.href = 'community.html' },
    { icon: '🚀', label: 'Yangi startap', action: () => location.href = 'startups.html' },
    { icon: '💼', label: 'Ish e\'lon qilish', action: () => location.href = 'job-create.html' },
    { icon: '🤖', label: 'AI Chat', action: () => location.href = 'ai-chat.html' },
  ];

  const fab = document.createElement('button');
  fab.className = 'oo-fab';
  fab.innerHTML = '➕';
  const menu = document.createElement('div');
  menu.className = 'oo-fab-menu';
  menu.innerHTML = items.map(i => `<div class="oo-fab-item">${i.icon} ${i.label}</div>`).join('');
  document.body.appendChild(fab);
  document.body.appendChild(menu);
  menu.querySelectorAll('.oo-fab-item').forEach((el, i) => el.onclick = () => { items[i].action(); fab.click(); });
  fab.onclick = () => menu.classList.toggle('open');
})();
