// 00o.uz - Mobile Nav Helper
(function() {
  if (document.getElementById('oo-mobile-nav')) return;
  const style = document.createElement('style');
  style.textContent = `
    .oo-menu-btn{display:none;width:40px;height:40px;border-radius:10px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);color:white;font-size:18px;cursor:pointer;align-items:center;justify-content:center;flex-shrink:0}
    .oo-mobile-menu{display:none;position:fixed;top:60px;left:0;right:0;background:rgba(10,14,26,0.98);backdrop-filter:blur(20px);border-bottom:1px solid rgba(255,255,255,0.05);padding:12px;z-index:99;flex-direction:column;gap:2px;max-height:calc(100vh - 60px);overflow-y:auto;animation:slideDown 0.3s ease}
    .oo-mobile-menu.open{display:flex}
    .oo-mobile-menu a{color:white;text-decoration:none;padding:12px 16px;border-radius:10px;font-size:15px;font-weight:600;display:flex;align-items:center;gap:12px;transition:0.2s}
    .oo-mobile-menu a:hover,.oo-mobile-menu a.active{background:rgba(139,92,246,0.15);color:#c4b5fd}
    @keyframes slideDown{from{opacity:0;transform:translateY(-10px)}to{opacity:1;transform:translateY(0)}}
    @media (max-width:767px){.oo-menu-btn{display:flex}.nav-links,.desktop-nav{display:none!important}}
  `;
  document.head.appendChild(style);
  // Wait for nav to exist
  function init() {
    const nav = document.querySelector('nav');
    if (!nav) return;
    const navInner = nav.querySelector('.nav-inner,.container') || nav.firstElementChild;
    if (!navInner) return;
    const navLinks = navInner.querySelector('.nav-links');
    if (!navLinks) return;
    // Get all links
    const links = Array.from(navLinks.querySelectorAll('a')).map(a => ({
      href: a.getAttribute('href'),
      text: a.textContent.trim(),
      active: a.classList.contains('active')
    }));
    // Create mobile menu
    const mobileMenu = document.createElement('div');
    mobileMenu.className = 'oo-mobile-menu';
    mobileMenu.innerHTML = links.map(l => `<a href="${l.href}" class="${l.active?'active':''}">${l.text}</a>`).join('');
    document.body.appendChild(mobileMenu);
    // Create hamburger button
    const btn = document.createElement('button');
    btn.className = 'oo-menu-btn';
    btn.innerHTML = '☰';
    btn.setAttribute('aria-label', 'Menu');
    // Insert after logo
    const logo = navInner.querySelector('.logo,a');
    if (logo && logo.nextSibling) {
      navInner.insertBefore(btn, logo.nextSibling);
    } else {
      navInner.appendChild(btn);
    }
    btn.onclick = (e) => {
      e.stopPropagation();
      mobileMenu.classList.toggle('open');
      btn.innerHTML = mobileMenu.classList.contains('open') ? '✕' : '☰';
    };
    // Close on outside click
    document.addEventListener('click', e => {
      if (!mobileMenu.contains(e.target) && e.target !== btn) {
        mobileMenu.classList.remove('open');
        btn.innerHTML = '☰';
      }
    });
    // Close on link click
    mobileMenu.querySelectorAll('a').forEach(a => a.onclick = () => {
      mobileMenu.classList.remove('open');
      btn.innerHTML = '☰';
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
