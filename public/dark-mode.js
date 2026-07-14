// Dark/Light mode + themes - 00o.uz
(function() {
  const style = document.createElement('style');
  style.textContent = `
  [data-theme="light"] { --bg: #f8fafc; --bg-soft: #ffffff; --text: #0f172a; --text-soft: #475569; --border: rgba(0,0,0,0.08); }
  [data-theme="synth"] { --accent: #f72585; }
  [data-theme="ocean"] { --accent: #06b6d4; }
  [data-theme="sunset"] { --accent: #f97316; }
  [data-theme="forest"] { --accent: #22c55e; }
  [data-theme="royal"] { --accent: #fbbf24; }
  .theme-switcher { position: fixed; bottom: 20px; left: 20px; z-index: 9998;
    background: rgba(15,23,42,0.9); backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.1); border-radius: 100px; padding: 6px;
    display: flex; gap: 4px; box-shadow: 0 10px 40px rgba(0,0,0,0.3); }
  .theme-btn { width: 32px; height: 32px; border-radius: 50%; border: 2px solid transparent;
    cursor: pointer; transition: 0.2s; font-size: 14px;
    display: flex; align-items: center; justify-content: center; background: transparent; color: white; }
  .theme-btn:hover { transform: scale(1.15); }
  .theme-btn.active { border-color: white; }
  `;
  document.head.appendChild(style);

  const themes = [
    { id: 'dark', icon: '🌙', color: '#0a0e1a' },
    { id: 'light', icon: '☀️', color: '#f8fafc' },
    { id: 'synth', icon: '🌸', color: '#f72585' },
    { id: 'ocean', icon: '🌊', color: '#06b6d4' },
    { id: 'sunset', icon: '🌅', color: '#f97316' },
    { id: 'forest', icon: '🌲', color: '#22c55e' },
    { id: 'royal', icon: '👑', color: '#fbbf24' },
  ];

  let currentTheme = localStorage.getItem('oo-theme') || 'dark';

  function apply(theme) {
    currentTheme = theme;
    localStorage.setItem('oo-theme', theme);
    if (theme === 'light') {
      document.documentElement.setAttribute('data-theme', 'light');
      document.body.style.background = 'linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #f8fafc 100%)';
      document.body.style.color = '#0f172a';
      document.documentElement.style.setProperty('--text', '#0f172a');
      document.documentElement.style.setProperty('--text-soft', '#475569');
    } else {
      document.documentElement.removeAttribute('data-theme');
      document.body.style.background = '';
      document.body.style.color = '';
    }
    document.documentElement.setAttribute('data-theme-style', theme);
    updateButtons();
  }

  function updateButtons() {
    document.querySelectorAll('.theme-btn').forEach(b => {
      b.classList.toggle('active', b.dataset.theme === currentTheme);
    });
  }

  function build() {
    const wrap = document.createElement('div');
    wrap.className = 'theme-switcher';
    wrap.innerHTML = themes.map(t => `<button class="theme-btn" data-theme="${t.id}" title="${t.id}">${t.icon}</button>`).join('');
    document.body.appendChild(wrap);
    wrap.querySelectorAll('.theme-btn').forEach(b => {
      b.onclick = () => apply(b.dataset.theme);
    });
    updateButtons();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => { build(); apply(currentTheme); });
  else { build(); apply(currentTheme); }

  window.darkMode = { apply, toggle: () => apply(currentTheme === 'dark' ? 'light' : 'dark'), current: () => currentTheme };
})();
