// Command Palette - Ctrl+K - 00o.uz
(function() {
  const style = document.createElement('style');
  style.textContent = `
  .cmdp-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.7); backdrop-filter: blur(8px);
    z-index: 100000; display: flex; align-items: flex-start; justify-content: center; padding-top: 12vh;
    opacity: 0; pointer-events: none; transition: 0.2s; }
  .cmdp-overlay.open { opacity: 1; pointer-events: auto; }
  .cmdp-box { width: 600px; max-width: 92vw; background: linear-gradient(135deg, rgba(30,41,59,0.98), rgba(15,23,42,0.98));
    border: 1px solid rgba(255,255,255,0.1); border-radius: 16px; overflow: hidden;
    transform: scale(0.95) translateY(-10px); transition: 0.2s; box-shadow: 0 20px 80px rgba(0,0,0,0.5); }
  .cmdp-overlay.open .cmdp-box { transform: scale(1) translateY(0); }
  .cmdp-search { width: 100%; padding: 18px 20px; background: transparent; border: none; border-bottom: 1px solid rgba(255,255,255,0.08);
    color: white; font-size: 16px; outline: none; }
  .cmdp-list { max-height: 420px; overflow-y: auto; padding: 8px 0; }
  .cmdp-section { padding: 6px 16px; font-size: 11px; color: #64748b; text-transform: uppercase; font-weight: 700; letter-spacing: 0.5px; }
  .cmdp-item { padding: 10px 16px; display: flex; align-items: center; gap: 12px; cursor: pointer; transition: 0.1s; }
  .cmdp-item:hover, .cmdp-item.active { background: rgba(139,92,246,0.15); }
  .cmdp-icon { font-size: 20px; width: 32px; text-align: center; }
  .cmdp-content { flex: 1; }
  .cmdp-title { font-weight: 600; font-size: 14px; }
  .cmdp-sub { color: #94a3b8; font-size: 12px; }
  .cmdp-shortcut { padding: 3px 8px; background: rgba(255,255,255,0.05); border-radius: 4px; font-size: 11px; color: #94a3b8; }
  .cmdp-empty { padding: 60px 20px; text-align: center; color: #64748b; }
  .cmdp-foot { padding: 10px 16px; border-top: 1px solid rgba(255,255,255,0.05); display: flex; gap: 16px;
    font-size: 11px; color: #64748b; }
  .cmdp-foot kbd { padding: 2px 6px; background: rgba(255,255,255,0.05); border-radius: 3px; font-family: monospace; }
  `;
  document.head.appendChild(style);

  const commands = [
    { icon: '🏠', title: 'Bosh sahifa', sub: 'Asosiy sahifaga o\'tish', action: () => location.href = 'index.html', shortcut: 'G H' },
    { icon: '📊', title: 'Dashboard', sub: 'Statistika va analytics', action: () => location.href = 'dashboard.html', shortcut: 'G D' },
    { icon: '👥', title: 'Community', sub: 'Ijtimoiy tarmoq', action: () => location.href = 'community.html', shortcut: 'G C' },
    { icon: '🏆', title: 'Leaderboard', sub: 'Top foydalanuvchilar', action: () => location.href = 'leaderboard.html', shortcut: 'G L' },
    { icon: '📋', title: 'Kanban Board', sub: 'Loyiha boshqaruvi', action: () => location.href = 'kanban.html', shortcut: 'G B' },
    { icon: '🎖', title: 'Achievements', sub: 'Yutuqlar', action: () => location.href = 'achievements.html' },
    { icon: '🚀', title: 'Startaplar', sub: 'Barcha startaplar', action: () => location.href = 'startups.html' },
    { icon: '💼', title: 'Frilanserlar', sub: 'Mutaxassislar', action: () => location.href = 'freelancers.html' },
    { icon: '💎', title: 'Ish o\'rinlari', sub: 'Vakansiyalar', action: () => location.href = 'jobs.html' },
    { icon: '👑', title: 'Premium', sub: 'Pro tarifga o\'tish', action: () => location.href = 'premium.html' },
    { icon: '📞', title: 'Aloqa', sub: 'Yordam', action: () => location.href = 'admin.html' },
    { icon: '🤖', title: 'AI Chat', sub: 'AI bilan suhbat', action: () => location.href = 'ai-chat.html', shortcut: 'A' },
    { icon: '🌙', title: 'Dark mode', sub: 'Mavzuni almashtirish', action: () => window.darkMode?.toggle() },
    { icon: '🎉', title: 'Confetti', sub: 'Bayram effekti', action: () => window.confetti({count:200}) },
    { icon: '🔔', title: 'Bildirishnomalar', sub: '5 ta yangi', action: () => window.toast?.info('5 ta yangi bildirishnoma', '🔔') },
    { icon: '🎵', title: 'Sound on/off', sub: 'Ovoz effektlari', action: () => window.sfx?.toggle() },
    { icon: '💎', title: 'Kunlik mukofot', sub: 'Spin wheel', action: () => location.href = 'spin-wheel.html' },
    { icon: '📖', title: 'Stories', sub: '24 soatlik hikoyalar', action: () => location.href = 'stories.html' },
    { icon: '🎬', title: 'Reels', sub: 'Qisqa videolar', action: () => location.href = 'reels.html' },
    { icon: '🛍', title: 'Shop', sub: 'Tangalar do\'koni', action: () => location.href = 'shop.html' },
    { icon: '⚔️', title: 'Battle Pass', sub: 'Mavsumiy mukofotlar', action: () => location.href = 'battle-pass.html' },
    { icon: '📅', title: 'Events', sub: 'Tadbirlar', action: () => location.href = 'events.html' },
    { icon: '👥', title: 'Guruhlar', sub: 'Maxsus guruhlar', action: () => location.href = 'groups.html' },
    { icon: '🎓', title: 'Mentorlik', sub: 'Mentor topish', action: () => location.href = 'mentorship.html' },
    { icon: '💬', title: 'Xabarlar', sub: 'Direct messages', action: () => location.href = 'direct-messages.html' },
    { icon: '➕', title: 'Ish e\'lon qilish', sub: 'Yangi vakansiya', action: () => location.href = 'job-create.html' },
    { icon: '⚙️', title: 'Sozlamalar', sub: 'Profil va xavfsizlik', action: () => location.href = 'settings.html' },
    { icon: '🔐', title: '2FA', sub: 'Ikki bosqichli autentifikatsiya', action: () => location.href = '2fa.html' },
    { icon: '📊', title: 'Admin panel', sub: 'Boshqaruv', action: () => location.href = 'admin-dashboard.html' },
    { icon: '🔍', title: 'Global qidiruv', sub: 'Hammasini qidirish', action: () => location.href = 'search.html' },
  ];

  let overlay, input, list, activeIdx = 0, filtered = commands;
  function build() {
    overlay = document.createElement('div');
    overlay.className = 'cmdp-overlay';
    overlay.innerHTML = `
      <div class="cmdp-box">
        <input class="cmdp-search" placeholder="🔍 Buyruq yozing yoki qidiring...">
        <div class="cmdp-list"></div>
        <div class="cmdp-foot">
          <span><kbd>↑</kbd> <kbd>↓</kbd> navigatsiya</span>
          <span><kbd>↵</kbd> tanlash</span>
          <span><kbd>Esc</kbd> yopish</span>
        </div>
      </div>
    `;
    document.body.appendChild(overlay);
    input = overlay.querySelector('.cmdp-search');
    list = overlay.querySelector('.cmdp-list');
    input.addEventListener('input', e => { filter(e.target.value); });
    overlay.addEventListener('click', e => { if (e.target === overlay) close(); });
    document.addEventListener('keydown', e => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') { e.preventDefault(); toggle(); }
      else if (e.key === 'Escape' && overlay.classList.contains('open')) close();
      else if (overlay.classList.contains('open')) {
        if (e.key === 'ArrowDown') { e.preventDefault(); activeIdx = Math.min(filtered.length-1, activeIdx+1); render(); }
        else if (e.key === 'ArrowUp') { e.preventDefault(); activeIdx = Math.max(0, activeIdx-1); render(); }
        else if (e.key === 'Enter' && filtered[activeIdx]) { filtered[activeIdx].action(); close(); }
      }
    });
  }
  function filter(q) {
    q = q.toLowerCase().trim();
    if (!q) { filtered = commands; }
    else {
      filtered = commands.filter(c => c.title.toLowerCase().includes(q) || c.sub?.toLowerCase().includes(q) || c.icon.includes(q));
    }
    activeIdx = 0;
    render();
  }
  function render() {
    if (filtered.length === 0) {
      list.innerHTML = '<div class="cmdp-empty">Hech narsa topilmadi 🤔</div>';
      return;
    }
    const sectionIdx = {};
    list.innerHTML = filtered.map((c, i) => {
      const showSection = i === 0;
      return `
        ${showSection ? '<div class="cmdp-section">⚡ Buyruqlar</div>' : ''}
        <div class="cmdp-item ${i===activeIdx?'active':''}" data-i="${i}">
          <div class="cmdp-icon">${c.icon}</div>
          <div class="cmdp-content">
            <div class="cmdp-title">${c.title}</div>
            <div class="cmdp-sub">${c.sub}</div>
          </div>
          ${c.shortcut ? `<div class="cmdp-shortcut">${c.shortcut}</div>` : ''}
        </div>
      `;
    }).join('');
    list.querySelectorAll('.cmdp-item').forEach((el, i) => {
      el.onclick = () => { filtered[i].action(); close(); };
    });
    const active = list.querySelector('.cmdp-item.active');
    if (active) active.scrollIntoView({ block: 'nearest' });
  }
  function open() {
    overlay.classList.add('open');
    input.value = '';
    filter('');
    setTimeout(() => input.focus(), 50);
  }
  function close() { overlay.classList.remove('open'); }
  function toggle() { overlay.classList.contains('open') ? close() : open(); }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', build);
  else build();

  window.cmdPalette = { open, close, toggle };
})();
