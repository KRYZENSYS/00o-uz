// 00o.uz Global Bundle - barcha sahifalarga avtomatik ulanadi
(function() {
  // === DARK MODE & THEMES ===
  const dmStyle = document.createElement('style');
  dmStyle.textContent = `.theme-switcher{position:fixed;bottom:20px;left:20px;z-index:99998;background:rgba(15,23,42,0.9);backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,0.1);border-radius:100px;padding:6px;display:flex;gap:4px;box-shadow:0 10px 40px rgba(0,0,0,0.3)}.theme-btn{width:32px;height:32px;border-radius:50%;border:2px solid transparent;cursor:pointer;transition:0.2s;font-size:14px;display:flex;align-items:center;justify-content:center;background:transparent;color:white}.theme-btn:hover{transform:scale(1.15)}.theme-btn.active{border-color:white}`;
  document.head.appendChild(dmStyle);
  const themes = [
    {id:'dark',icon:'🌙'},{id:'light',icon:'☀️'},{id:'synth',icon:'🌸'},
    {id:'ocean',icon:'🌊'},{id:'sunset',icon:'🌅'},{id:'forest',icon:'🌲'},{id:'royal',icon:'👑'}
  ];
  let curTheme = localStorage.getItem('oo-theme') || 'dark';
  const ts = document.createElement('div');
  ts.className = 'theme-switcher';
  ts.innerHTML = themes.map(t => `<button class="theme-btn ${t.id===curTheme?'active':''}" data-t="${t.id}" title="${t.id}">${t.icon}</button>`).join('');
  document.body.appendChild(ts);
  ts.querySelectorAll('.theme-btn').forEach(b => b.onclick = () => {
    curTheme = b.dataset.t;
    localStorage.setItem('oo-theme', curTheme);
    if (curTheme === 'light') {
      document.body.style.background = 'linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #f8fafc 100%)';
      document.body.style.color = '#0f172a';
    } else {
      document.body.style.background = '';
      document.body.style.color = '';
    }
    ts.querySelectorAll('.theme-btn').forEach(x => x.classList.toggle('active', x.dataset.t === curTheme));
  });

  // === AI CHAT BUBBLE ===
  const aiStyle = document.createElement('style');
  aiStyle.textContent = `.ai-bubble{position:fixed;bottom:20px;right:90px;z-index:99998;width:60px;height:60px;border-radius:50%;background:linear-gradient(135deg,#8b5cf6,#ec4899);border:none;color:white;font-size:28px;cursor:pointer;box-shadow:0 10px 30px rgba(139,92,246,0.5);animation:aiPulse 3s ease-in-out infinite}@keyframes aiPulse{0%,100%{box-shadow:0 10px 30px rgba(139,92,246,0.5)}50%{box-shadow:0 10px 50px rgba(139,92,246,0.8),0 0 0 10px rgba(139,92,246,0.1)}}.ai-panel{position:fixed;bottom:90px;right:20px;z-index:99999;width:380px;max-width:calc(100vw - 40px);height:540px;max-height:calc(100vh - 120px);background:linear-gradient(135deg,rgba(30,41,59,0.98),rgba(15,23,42,0.98));backdrop-filter:blur(20px);border:1px solid rgba(255,255,255,0.1);border-radius:20px;display:none;flex-direction:column;box-shadow:0 20px 80px rgba(0,0,0,0.5);transform:scale(0.8) translateY(20px);opacity:0;transition:0.3s cubic-bezier(0.16,1,0.3,1);transform-origin:bottom right}.ai-panel.open{display:flex;transform:scale(1) translateY(0);opacity:1}.ai-head{padding:16px;border-bottom:1px solid rgba(255,255,255,0.05);display:flex;align-items:center;gap:12px}.ai-av{width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,#8b5cf6,#ec4899);display:flex;align-items:center;justify-content:center;font-size:20px}.ai-name{font-weight:700}.ai-st{color:#22c55e;font-size:12px}.ai-close{margin-left:auto;background:rgba(255,255,255,0.05);border:none;color:white;width:30px;height:30px;border-radius:50%;cursor:pointer}.ai-msgs{flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:12px}.ai-msg{max-width:85%;padding:10px 14px;border-radius:14px;font-size:14px;line-height:1.4}.ai-msg.bot{background:rgba(139,92,246,0.15);border:1px solid rgba(139,92,246,0.2);align-self:flex-start}.ai-msg.user{background:linear-gradient(135deg,#8b5cf6,#06b6d4);align-self:flex-end}.ai-input{padding:12px;border-top:1px solid rgba(255,255,255,0.05);display:flex;gap:8px}.ai-input input{flex:1;padding:10px 14px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:100px;color:white;font-size:13px;outline:none}.ai-send{padding:0 16px;background:linear-gradient(135deg,#8b5cf6,#ec4899);border:none;color:white;border-radius:100px;font-weight:600;cursor:pointer}`;
  document.head.appendChild(aiStyle);
  const aiB = document.createElement('button');
  aiB.className = 'ai-bubble';
  aiB.innerHTML = '🤖';
  const aiP = document.createElement('div');
  aiP.className = 'ai-panel';
  aiP.innerHTML = `<div class="ai-head"><div class="ai-av">🤖</div><div><div class="ai-name">00o AI</div><div class="ai-st">onlayn</div></div><button class="ai-close">×</button></div><div class="ai-msgs" id="aiMsgs"></div><div class="ai-input"><input id="aiIn" placeholder="Xabar yozing..."><button class="ai-send">➤</button></div>`;
  document.body.appendChild(aiB);
  document.body.appendChild(aiP);
  const aiMsgs = document.getElementById('aiMsgs');
  const aiIn = document.getElementById('aiIn');
  aiB.onclick = () => aiP.classList.toggle('open');
  aiP.querySelector('.ai-close').onclick = () => aiP.classList.remove('open');
  function aiAdd(t, type) {
    const m = document.createElement('div');
    m.className = 'ai-msg ' + type;
    m.textContent = t;
    aiMsgs.appendChild(m);
    aiMsgs.scrollTop = aiMsgs.scrollHeight;
  }
  function aiSend() {
    const t = aiIn.value.trim();
    if (!t) return;
    aiAdd(t, 'user');
    aiIn.value = '';
    setTimeout(() => {
      const lower = t.toLowerCase();
      let r = 'Qiziqarli savol! AI yordam berishga tayyor 🤖';
      if (lower.match(/salom|qalay/)) r = 'Salom! 👋 30 ta AI vositam bor. Qaysi biri kerak?';
      else if (lower.match(/startap/)) r = '💡 3 ta startap g\'oyasi:\n1. AI tutor (EdTech)\n2. Local delivery\n3. Crypto edu';
      else if (lower.match(/ish|vakansiya/)) r = '💼 500+ vakansiya bor! IT, dizayn, marketing';
      else if (lower.match(/cv/)) r = '📄 CV yaratish uchun ai-chat.html ga o\'ting';
      else if (lower.match(/kod|code/)) r = '💻 Qaysi til? React, Python, Java?';
      aiAdd(r, 'bot');
    }, 700);
  }
  aiP.querySelector('.ai-send').onclick = aiSend;
  aiIn.onkeydown = e => { if (e.key === 'Enter') aiSend(); };
  setTimeout(() => aiAdd('Salom! 👋 Men 00o AI yordamchisiman. 30 ta vosita bilan ishlayman.', 'bot'), 1500);

  // === COMMAND PALETTE (Ctrl+K) ===
  const cmds = [
    {i:'🏠',t:'Bosh sahifa',a:'index.html'},{i:'📊',t:'Dashboard',a:'dashboard.html'},
    {i:'👥',t:'Community',a:'community.html'},{i:'🏆',t:'Leaderboard',a:'leaderboard.html'},
    {i:'📋',t:'Kanban',a:'kanban.html'},{i:'🎖',t:'Achievements',a:'achievements.html'},
    {i:'🚀',t:'Startaplar',a:'startups.html'},{i:'💼',t:'Frilanserlar',a:'freelancers.html'},
    {i:'💎',t:'Ish',a:'jobs.html'},{i:'🤖',t:'AI Chat',a:'ai-chat.html'},
    {i:'📖',t:'Stories',a:'stories.html'},{i:'🎬',t:'Reels',a:'reels.html'},
    {i:'🛍',t:'Shop',a:'shop.html'},{i:'⚔️',t:'Battle Pass',a:'battle-pass.html'},
    {i:'🎰',t:'Spin Wheel',a:'spin-wheel.html'},{i:'📅',t:'Events',a:'events.html'},
    {i:'👥',t:'Guruhlar',a:'groups.html'},{i:'🎓',t:'Mentorlik',a:'mentorship.html'},
    {i:'➕',t:'Ish e\'lon qilish',a:'job-create.html'},{i:'🛡',t:'Admin',a:'admin-dashboard.html'},
    {i:'👤',t:'Profil',a:'profile.html'},{i:'⚙️',t:'Sozlamalar',a:'settings.html'},
    {i:'🔐',t:'Login',a:'login.html'},
  ];
  const cStyle = document.createElement('style');
  cStyle.textContent = `.cmdp{position:fixed;inset:0;background:rgba(0,0,0,0.7);backdrop-filter:blur(8px);z-index:100000;display:none;align-items:flex-start;justify-content:center;padding-top:12vh}.cmdp.open{display:flex}.cmdp-box{width:600px;max-width:92vw;background:linear-gradient(135deg,rgba(30,41,59,0.98),rgba(15,23,42,0.98));border:1px solid rgba(255,255,255,0.1);border-radius:16px;overflow:hidden;box-shadow:0 20px 80px rgba(0,0,0,0.5)}.cmdp-search{width:100%;padding:18px 20px;background:transparent;border:none;border-bottom:1px solid rgba(255,255,255,0.08);color:white;font-size:16px;outline:none}.cmdp-list{max-height:420px;overflow-y:auto;padding:8px 0}.cmdp-item{padding:10px 16px;display:flex;align-items:center;gap:12px;cursor:pointer;transition:0.1s}.cmdp-item:hover,.cmdp-item.active{background:rgba(139,92,246,0.15)}.cmdp-i{font-size:20px;width:32px;text-align:center}.cmdp-n{flex:1;font-weight:600;font-size:14px}`;
  document.head.appendChild(cStyle);
  const cp = document.createElement('div');
  cp.className = 'cmdp';
  cp.innerHTML = `<div class="cmdp-box"><input class="cmdp-search" placeholder="🔍 Buyruq yozing... (Ctrl+K)"><div class="cmdp-list" id="cmdpList"></div></div>`;
  document.body.appendChild(cp);
  const cpIn = cp.querySelector('.cmdp-search');
  const cpList = document.getElementById('cmdpList');
  function renderCmds(filter='') {
    const f = cmds.filter(c => !filter || c.t.toLowerCase().includes(filter.toLowerCase()));
    cpList.innerHTML = f.map((c, i) => `<div class="cmdp-item ${i===0?'active':''}" data-a="${c.a}"><div class="cmdp-i">${c.i}</div><div class="cmdp-n">${c.t}</div></div>`).join('');
    cpList.querySelectorAll('.cmdp-item').forEach(el => el.onclick = () => location.href = el.dataset.a);
  }
  cp.onclick = e => { if (e.target === cp) cp.classList.remove('open'); };
  cpIn.oninput = e => renderCmds(e.target.value);
  document.addEventListener('keydown', e => {
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
      e.preventDefault();
      cp.classList.toggle('open');
      setTimeout(() => cpIn.focus(), 50);
      renderCmds();
    } else if (e.key === 'Escape') cp.classList.remove('open');
  });
  renderCmds();
  window.cmdPalette = { toggle: () => cp.classList.toggle('open') };
})();
