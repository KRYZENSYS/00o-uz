// 00o.uz - i18n + Theme + Search + PWA (Universal)
(function() {
  'use strict';

  // ===== TRANSLATIONS =====
  const T = {
    uz: {
      home: 'Bosh sahifa', startups: 'Startaplar', freelancers: 'Frilanserlar',
      jobs: 'Ish o\'rinlari', premium: 'Premium', profile: 'Profil', contact: 'Aloqa',
      login: 'Kirish', logout: 'Chiqish', start: 'Boshlash', search: 'Qidirish',
      saved: 'Saqlangan', notifications: 'Bildirishnomalar', settings: 'Sozlamalar',
      language: 'Til', theme: 'Mavzu', light: 'Yorug\'', dark: 'Qorong\'i',
      search_placeholder: 'Startap, frilanser, ish qidirish...',
      no_results: 'Hech narsa topilmadi', try_again: 'Boshqacha urinib ko\'ring',
      install_app: 'Ilovani o\'rnatish', later: 'Keyinroq',
      online: 'Onlayn', offline: 'Oflayn', all: 'Hammasi',
      shortcuts: 'Tezkor tugmalar', press: 'Bosish', to_search: 'qidirish uchun',
      toggle_theme: 'Mavzuni almashtirish', change_lang: 'Tilni almashtirish'
    },
    ru: {
      home: 'Главная', startups: 'Стартапы', freelancers: 'Фрилансеры',
      jobs: 'Вакансии', premium: 'Премиум', profile: 'Профиль', contact: 'Контакты',
      login: 'Войти', logout: 'Выйти', start: 'Начать', search: 'Поиск',
      saved: 'Сохранённые', notifications: 'Уведомления', settings: 'Настройки',
      language: 'Язык', theme: 'Тема', light: 'Светлая', dark: 'Тёмная',
      search_placeholder: 'Поиск стартапа, фрилансера, вакансии...',
      no_results: 'Ничего не найдено', try_again: 'Попробуйте иначе',
      install_app: 'Установить приложение', later: 'Позже',
      online: 'Онлайн', offline: 'Оффлайн', all: 'Все',
      shortcuts: 'Горячие клавиши', press: 'Нажмите', to_search: 'для поиска',
      toggle_theme: 'Сменить тему', change_lang: 'Сменить язык'
    },
    en: {
      home: 'Home', startups: 'Startups', freelancers: 'Freelancers',
      jobs: 'Jobs', premium: 'Premium', profile: 'Profile', contact: 'Contact',
      login: 'Login', logout: 'Logout', start: 'Start', search: 'Search',
      saved: 'Saved', notifications: 'Notifications', settings: 'Settings',
      language: 'Language', theme: 'Theme', light: 'Light', dark: 'Dark',
      search_placeholder: 'Search startup, freelancer, job...',
      no_results: 'No results found', try_again: 'Try something else',
      install_app: 'Install App', later: 'Later',
      online: 'Online', offline: 'Offline', all: 'All',
      shortcuts: 'Shortcuts', press: 'Press', to_search: 'to search',
      toggle_theme: 'Toggle theme', change_lang: 'Change language'
    }
  };

  // ===== STATE =====
  const state = {
    lang: localStorage.getItem('00o_lang') || 'uz',
    theme: localStorage.getItem('00o_theme') || 'dark',
    pwaDeferred: null
  };

  // ===== APPLY LANGUAGE =====
  function applyLang() {
    const t = T[state.lang];
    document.documentElement.lang = state.lang;
    
    // Update data-i18n elements
    document.querySelectorAll('[data-i18n]').forEach(el => {
      const key = el.getAttribute('data-i18n');
      if (t[key]) el.textContent = t[key];
    });
    
    // Update specific known patterns
    const navMap = {
      'Bosh sahifa': t.home, 'Startaplar': t.startups, 'Frilanserlar': t.freelancers,
      'Ish o\'rinlari': t.jobs, 'Главная': t.home, 'Стартапы': t.startups,
      'Фрилансеры': t.freelancers, 'Вакансии': t.jobs
    };
    document.querySelectorAll('.nav-links a').forEach(a => {
      if (navMap[a.textContent.trim()]) a.textContent = navMap[a.textContent.trim()];
    });
    
    // Update placeholders
    const searchInputs = document.querySelectorAll('input[type="text"], .search-input');
    searchInputs.forEach(inp => {
      if (inp.placeholder && (inp.placeholder.includes('qidirish') || inp.placeholder.includes('поиск') || inp.placeholder.includes('Search'))) {
        inp.placeholder = t.search_placeholder;
      }
    });
    
    // Save and update switcher
    localStorage.setItem('00o_lang', state.lang);
    updateLangBtn();
  }

  // ===== APPLY THEME =====
  function applyTheme() {
    document.documentElement.setAttribute('data-theme', state.theme);
    localStorage.setItem('00o_theme', state.theme);
    updateThemeBtn();
  }

  // ===== INJECT UI =====
  function injectUI() {
    // Top toolbar (floating)
    if (!document.getElementById('00oToolbar')) {
      const bar = document.createElement('div');
      bar.id = '00oToolbar';
      bar.innerHTML = `
        <button id="00oSearch" class="tbtn" title="Search (Ctrl+K)">🔍</button>
        <button id="00oTheme" class="tbtn" title="Theme">🌙</button>
        <button id="00oLang" class="tbtn tbtn-lang" title="Language">🇺🇿 UZ</button>
      `;
      document.body.appendChild(bar);
      
      // Add styles
      const style = document.createElement('style');
      style.textContent = `
        #00oToolbar { position: fixed; bottom: 24px; right: 24px; display: flex; gap: 8px;
          z-index: 9999; padding: 8px; border-radius: 100px;
          background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(20px);
          border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 10px 40px rgba(0,0,0,0.4); }
        [data-theme="light"] #00oToolbar { background: rgba(255,255,255,0.95); border-color: rgba(0,0,0,0.1); }
        .tbtn { width: 44px; height: 44px; border-radius: 50%; border: none; cursor: pointer;
          background: rgba(255,255,255,0.08); color: white; font-size: 18px;
          display: flex; align-items: center; justify-content: center; transition: 0.3s; }
        [data-theme="light"] .tbtn { background: rgba(0,0,0,0.06); color: #0f172a; }
        .tbtn:hover { background: linear-gradient(135deg, #8b5cf6, #06b6d4); transform: scale(1.1); color: white; }
        .tbtn-lang { width: auto; padding: 0 14px; font-size: 13px; font-weight: 700; }
        
        /* Search Modal */
        #00oSearchModal { display: none; position: fixed; inset: 0;
          background: rgba(0,0,0,0.7); backdrop-filter: blur(8px); z-index: 10000;
          align-items: flex-start; justify-content: center; padding: 100px 20px 20px; }
        #00oSearchModal.open { display: flex; animation: fadeIn 0.2s; }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        .search-box { width: 100%; max-width: 640px;
          background: linear-gradient(135deg, #1e293b, #0f172a);
          border: 1px solid rgba(255,255,255,0.1); border-radius: 16px; overflow: hidden;
          box-shadow: 0 25px 80px rgba(0,0,0,0.5); }
        [data-theme="light"] .search-box { background: white; border-color: rgba(0,0,0,0.1); }
        .search-input-wrap { display: flex; align-items: center; padding: 18px 20px; border-bottom: 1px solid rgba(255,255,255,0.1); }
        [data-theme="light"] .search-input-wrap { border-bottom-color: rgba(0,0,0,0.1); }
        .search-input-wrap span { font-size: 22px; margin-right: 12px; }
        .search-input-wrap input { flex: 1; border: none; background: transparent; color: inherit;
          font-size: 17px; outline: none; font-family: inherit; }
        .search-input-wrap kbd { padding: 4px 8px; background: rgba(255,255,255,0.1); border-radius: 6px;
          font-size: 11px; color: #94a3b8; }
        [data-theme="light"] .search-input-wrap kbd { background: rgba(0,0,0,0.06); color: #64748b; }
        .search-results { max-height: 50vh; overflow-y: auto; padding: 8px; }
        .search-result { padding: 12px 16px; border-radius: 10px; cursor: pointer;
          display: flex; align-items: center; gap: 12px; transition: 0.2s; color: inherit; text-decoration: none; }
        .search-result:hover { background: rgba(139,92,246,0.15); }
        .search-result-icon { width: 40px; height: 40px; border-radius: 10px;
          background: linear-gradient(135deg, #8b5cf6, #06b6d4); display: flex;
          align-items: center; justify-content: center; font-size: 20px; flex-shrink: 0; }
        .search-result-text { flex: 1; min-width: 0; }
        .search-result-title { font-weight: 600; font-size: 14px; }
        .search-result-desc { color: #94a3b8; font-size: 12px; }
        .search-empty { text-align: center; padding: 40px; color: #94a3b8; font-size: 14px; }
        
        /* PWA install banner */
        #00oInstall { display: none; position: fixed; bottom: 90px; right: 24px;
          padding: 16px 20px; border-radius: 16px; z-index: 9999;
          background: linear-gradient(135deg, #8b5cf6, #06b6d4); color: white;
          box-shadow: 0 10px 40px rgba(139,92,246,0.4); max-width: 320px;
          animation: slideUp 0.3s; }
        @keyframes slideUp { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
        #00oInstall button { padding: 8px 16px; border-radius: 8px; border: none;
          font-size: 13px; font-weight: 600; cursor: pointer; margin-top: 8px; margin-right: 6px; }
        #00oInstall .yes { background: white; color: #8b5cf6; }
        #00oInstall .no { background: rgba(255,255,255,0.2); color: white; }
        
        /* Light theme overrides */
        [data-theme="light"] body { background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 50%, #f8fafc 100%) !important; color: #0f172a !important; }
        [data-theme="light"] .nav, [data-theme="light"] nav { background: rgba(255,255,255,0.9) !important; border-bottom-color: rgba(0,0,0,0.1) !important; }
        [data-theme="light"] .nav-links a, [data-theme="light"] .nav a, [data-theme="light"] a { color: #475569; }
        [data-theme="light"] .nav-links a:hover, [data-theme="light"] .nav a.active { color: #8b5cf6; }
        [data-theme="light"] h1, [data-theme="light"] h2, [data-theme="light"] h3, [data-theme="light"] .stat-num, [data-theme="light"] .plan-price, [data-theme="light"] .profile-name { color: #0f172a !important; }
        [data-theme="light"] .feature, [data-theme="light"] .startup-card, [data-theme="light"] .freelancer-card, [data-theme="light"] .job-card,
        [data-theme="light"] .plan, [data-theme="light"] .profile-card, [data-theme="light"] .stat, [data-theme="light"] .stat-card,
        [data-theme="light"] .ai-tool, [data-theme="light"] .activity, [data-theme="light"] .notif, [data-theme="light"] .saved-item,
        [data-theme="light"] .checkout-box, [data-theme="light"] .form-card, [data-theme="light"] .faq-item {
          background: rgba(255,255,255,0.7) !important; border-color: rgba(0,0,0,0.1) !important; color: #0f172a !important; }
        [data-theme="light"] .feature p, [data-theme="light"] .startup-desc, [data-theme="light"] .freelancer-title, [data-theme="light"] .job-company,
        [data-theme="light"] .plan-desc, [data-theme="light"] .profile-bio, [data-theme="light"] .stat-lbl, [data-theme="light"] .activity-time,
        [data-theme="light"] .notif-time, [data-theme="light"] .saved-meta, [data-theme="light"] .plan-period, [data-theme="light"] .faq-a { color: #64748b !important; }
        [data-theme="light"] .search-input, [data-theme="light"] .form-group input, [data-theme="light"] .form-group textarea {
          background: white !important; border-color: rgba(0,0,0,0.15) !important; color: #0f172a !important; }
        [data-theme="light"] .page-hero p, [data-theme="light"] .cta p, [data-theme="light"] .section-title p, [data-theme="light"] footer { color: #64748b !important; }
        [data-theme="light"] footer { border-top-color: rgba(0,0,0,0.1) !important; }
        [data-theme="light"] .tag, [data-theme="light"] .skill { background: rgba(139,92,246,0.1) !important; color: #7c3aed !important; }
        [data-theme="light"] .btn-outline { border-color: rgba(0,0,0,0.2) !important; color: #0f172a !important; }
        [data-theme="light"] .modal-content { background: white !important; color: #0f172a !important; }
        [data-theme="light"] .tabs { background: rgba(0,0,0,0.05) !important; }
        [data-theme="light"] .form-group label { color: #475569 !important; }
      `;
      document.head.appendChild(style);
    }

    // Search modal
    if (!document.getElementById('00oSearchModal')) {
      const modal = document.createElement('div');
      modal.id = '00oSearchModal';
      modal.innerHTML = `
        <div class="search-box" onclick="event.stopPropagation()">
          <div class="search-input-wrap">
            <span>🔍</span>
            <input type="text" id="00oSearchInput" placeholder="${T[state.lang].search_placeholder}" autocomplete="off">
            <kbd>ESC</kbd>
          </div>
          <div class="search-results" id="00oSearchResults"></div>
        </div>
      `;
      document.body.appendChild(modal);
      
      // PWA install banner
      const install = document.createElement('div');
      install.id = '00oInstall';
      install.innerHTML = `
        <div style="font-weight:700;font-size:15px;margin-bottom:4px;">📱 ${T[state.lang].install_app}</div>
        <div style="font-size:12px;opacity:0.9;">00o.uz — tezroq kirish uchun</div>
        <div style="margin-top:8px;">
          <button class="yes" id="00oInstallYes">✓ O'rnatish</button>
          <button class="no" id="00oInstallNo">${T[state.lang].later}</button>
        </div>
      `;
      document.body.appendChild(install);
    }
  }

  // ===== SEARCH DATA =====
  const searchData = [
    { type: 'page', title: 'Bosh sahifa', desc: '00o.uz asosiy sahifa', icon: '🏠', url: 'index.html' },
    { type: 'page', title: 'Startaplar', desc: '12 ta startap', icon: '🚀', url: 'startups.html' },
    { type: 'page', title: 'Frilanserlar', desc: '10 ta mutaxassis', icon: '💼', url: 'freelancers.html' },
    { type: 'page', title: 'Ish o\'rinlari', desc: '12 ta vakansiya', icon: '💎', url: 'jobs.html' },
    { type: 'page', title: 'Premium', desc: 'Pro tariflar', icon: '👑', url: 'premium.html' },
    { type: 'page', title: 'Profil', desc: 'Mening profilim', icon: '👤', url: 'profile.html' },
    { type: 'page', title: 'Aloqa', desc: 'Biz bilan bog\'lanish', icon: '📞', url: 'admin.html' },
    { type: 'startup', title: 'PayUz', desc: '💳 FinTech · $2.5M · 500K+', icon: '💳', url: 'startups.html#payuz' },
    { type: 'startup', title: 'EduPro', desc: '🎓 EdTech · $800K · 120K+', icon: '🎓', url: 'startups.html#edupro' },
    { type: 'startup', title: 'MedLink', desc: '🏥 HealthTech · $1.2M · 85K+', icon: '🏥', url: 'startups.html#medlink' },
    { type: 'startup', title: 'Bozor.uz', desc: '🛒 E-commerce · $5M · 1M+', icon: '🛒', url: 'startups.html#bozor' },
    { type: 'startup', title: 'AgroAI', desc: '🌾 AgriTech · $600K · 45K+', icon: '🌾', url: 'startups.html#agro' },
    { type: 'startup', title: 'TaksiPro', desc: '🚕 Logistika · $3.2M · 300K+', icon: '🚕', url: 'startups.html#taksi' },
    { type: 'freelancer', title: 'Aziz Karimov', desc: 'Full-stack Developer · 25$/soat', icon: '👨‍💻', url: 'freelancers.html#aziz' },
    { type: 'freelancer', title: 'Madina Yusupova', desc: 'UI/UX Designer · 30$/soat', icon: '👩‍🎨', url: 'freelancers.html#madina' },
    { type: 'freelancer', title: 'Bobur Aliyev', desc: 'Digital Marketing · 20$/soat', icon: '👨‍💼', url: 'freelancers.html#bobur' },
    { type: 'job', title: 'Senior Frontend Developer', desc: 'PayUz · 25-40 mln · Remote', icon: '💼', url: 'jobs.html#payuz-fe' },
    { type: 'job', title: 'UI/UX Designer', desc: 'EduPro · 15-25 mln', icon: '🎨', url: 'jobs.html#edu-ux' },
    { type: 'job', title: 'Data Scientist', desc: 'AgroAI · 25-45 mln · Remote', icon: '🤖', url: 'jobs.html#agro-ds' },
  ];

  function doSearch(q) {
    const ql = q.toLowerCase().trim();
    if (!ql) return [];
    return searchData.filter(item => 
      item.title.toLowerCase().includes(ql) || 
      item.desc.toLowerCase().includes(ql) ||
      item.type.includes(ql)
    ).slice(0, 8);
  }

  // ===== SEARCH MODAL =====
  function openSearch() {
    const modal = document.getElementById('00oSearchModal');
    modal.classList.add('open');
    setTimeout(() => document.getElementById('00oSearchInput').focus(), 50);
    renderSearch('');
  }

  function closeSearch() {
    document.getElementById('00oSearchModal').classList.remove('open');
    document.getElementById('00oSearchInput').value = '';
  }

  function renderSearch(q) {
    const results = doSearch(q);
    const t = T[state.lang];
    const el = document.getElementById('00oSearchResults');
    if (results.length === 0) {
      el.innerHTML = `<div class="search-empty">${q ? t.no_results + '. ' + t.try_again + '.' : '🔍 ' + t.search}</div>`;
      return;
    }
    el.innerHTML = results.map(r => `
      <a href="${r.url}" class="search-result">
        <div class="search-result-icon">${r.icon}</div>
        <div class="search-result-text">
          <div class="search-result-title">${r.title}</div>
          <div class="search-result-desc">${r.desc}</div>
        </div>
      </a>
    `).join('');
  }

  // ===== BUTTONS =====
  function updateLangBtn() {
    const flags = { uz: '🇺🇿 UZ', ru: '🇷🇺 RU', en: '🇬🇧 EN' };
    const btn = document.getElementById('00oLang');
    if (btn) btn.textContent = flags[state.lang];
  }

  function updateThemeBtn() {
    const btn = document.getElementById('00oTheme');
    if (btn) btn.textContent = state.theme === 'dark' ? '☀️' : '🌙';
  }

  function toggleLang() {
    const order = ['uz', 'ru', 'en'];
    state.lang = order[(order.indexOf(state.lang) + 1) % 3];
    applyLang();
  }

  function toggleTheme() {
    state.theme = state.theme === 'dark' ? 'light' : 'dark';
    applyTheme();
  }

  // ===== PWA =====
  function setupPWA() {
    // Manifest
    if (!document.querySelector('link[rel="manifest"]')) {
      const link = document.createElement('link');
      link.rel = 'manifest';
      link.href = '/manifest.json';
      document.head.appendChild(link);
    }
    // Theme color
    if (!document.querySelector('meta[name="theme-color"]')) {
      const meta = document.createElement('meta');
      meta.name = 'theme-color';
      meta.content = '#8b5cf6';
      document.head.appendChild(meta);
    }
    // Service worker
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/sw.js').catch(() => {});
    }
    // Install prompt
    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault();
      state.pwaDeferred = e;
      if (!localStorage.getItem('00o_install_dismissed')) {
        setTimeout(() => {
          const banner = document.getElementById('00oInstall');
          if (banner) banner.style.display = 'block';
        }, 5000);
      }
    });
  }

  // ===== EVENTS =====
  function bindEvents() {
    document.getElementById('00oSearch').onclick = openSearch;
    document.getElementById('00oTheme').onclick = toggleTheme;
    document.getElementById('00oLang').onclick = toggleLang;
    
    const modal = document.getElementById('00oSearchModal');
    modal.onclick = (e) => { if (e.target === modal) closeSearch(); };
    
    document.getElementById('00oSearchInput').oninput = (e) => renderSearch(e.target.value);
    
    // ESC + Ctrl+K
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') closeSearch();
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') { e.preventDefault(); openSearch(); }
    });

    // PWA install
    const installYes = document.getElementById('00oInstallYes');
    const installNo = document.getElementById('00oInstallNo');
    if (installYes) installYes.onclick = () => {
      document.getElementById('00oInstall').style.display = 'none';
      if (state.pwaDeferred) { state.pwaDeferred.prompt(); state.pwaDeferred = null; }
    };
    if (installNo) installNo.onclick = () => {
      document.getElementById('00oInstall').style.display = 'none';
      localStorage.setItem('00o_install_dismissed', '1');
    };
  }

  // ===== INIT =====
  function init() {
    injectUI();
    applyTheme();
    applyLang();
    bindEvents();
    setupPWA();
    console.log('%c🌐 00o.uz Global Tools loaded', 'font-size:14px;font-weight:bold;color:#8b5cf6;');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
