// AI Chat widget - 00o.uz
(function() {
  const style = document.createElement('style');
  style.textContent = `
  .ai-bubble { position: fixed; bottom: 20px; right: 90px; z-index: 9998;
    width: 60px; height: 60px; border-radius: 50%;
    background: linear-gradient(135deg, #8b5cf6, #ec4899); border: none; color: white;
    font-size: 28px; cursor: pointer; box-shadow: 0 10px 30px rgba(139,92,246,0.5);
    animation: aiPulse 3s ease-in-out infinite; }
  @keyframes aiPulse { 0%, 100% { box-shadow: 0 10px 30px rgba(139,92,246,0.5); } 50% { box-shadow: 0 10px 50px rgba(139,92,246,0.8), 0 0 0 10px rgba(139,92,246,0.1); } }
  .ai-panel { position: fixed; bottom: 90px; right: 20px; z-index: 9999;
    width: 380px; max-width: calc(100vw - 40px); height: 560px; max-height: calc(100vh - 120px);
    background: linear-gradient(135deg, rgba(30,41,59,0.98), rgba(15,23,42,0.98));
    backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px; display: flex; flex-direction: column;
    box-shadow: 0 20px 80px rgba(0,0,0,0.5); transform: scale(0.8) translateY(20px);
    opacity: 0; pointer-events: none; transition: 0.3s cubic-bezier(0.16, 1, 0.3, 1); transform-origin: bottom right; }
  .ai-panel.open { transform: scale(1) translateY(0); opacity: 1; pointer-events: auto; }
  .ai-head { padding: 16px; border-bottom: 1px solid rgba(255,255,255,0.05);
    display: flex; align-items: center; gap: 12px; }
  .ai-avatar { width: 40px; height: 40px; border-radius: 50%;
    background: linear-gradient(135deg, #8b5cf6, #ec4899); display: flex; align-items: center; justify-content: center; font-size: 20px; }
  .ai-info { flex: 1; }
  .ai-name { font-weight: 700; }
  .ai-status { color: #22c55e; font-size: 12px; display: flex; align-items: center; gap: 4px; }
  .ai-status::before { content: ''; width: 6px; height: 6px; background: #22c55e; border-radius: 50%; }
  .ai-close { background: rgba(255,255,255,0.05); border: none; color: white; width: 30px; height: 30px;
    border-radius: 50%; cursor: pointer; }
  .ai-msgs { flex: 1; overflow-y: auto; padding: 16px; display: flex; flex-direction: column; gap: 12px; }
  .ai-msg { max-width: 85%; padding: 10px 14px; border-radius: 14px; font-size: 14px; line-height: 1.4; }
  .ai-msg.bot { background: rgba(139,92,246,0.15); border: 1px solid rgba(139,92,246,0.2); align-self: flex-start; }
  .ai-msg.user { background: linear-gradient(135deg, #8b5cf6, #06b6d4); align-self: flex-end; }
  .ai-msg.tool { background: rgba(34,197,94,0.1); border: 1px solid rgba(34,197,94,0.2); align-self: flex-start; font-size: 13px; }
  .ai-tools { padding: 8px 12px; border-top: 1px solid rgba(255,255,255,0.05);
    display: flex; gap: 6px; overflow-x: auto; }
  .ai-tool-btn { padding: 6px 10px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.08);
    border-radius: 100px; color: white; font-size: 11px; font-weight: 600; cursor: pointer; white-space: nowrap; }
  .ai-tool-btn:hover { background: linear-gradient(135deg, #8b5cf6, #06b6d4); border-color: transparent; }
  .ai-input { padding: 12px; border-top: 1px solid rgba(255,255,255,0.05);
    display: flex; gap: 8px; }
  .ai-input input { flex: 1; padding: 10px 14px; background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1); border-radius: 100px; color: white; font-size: 13px; outline: none; }
  .ai-input input:focus { border-color: #8b5cf6; }
  .ai-send { padding: 0 16px; background: linear-gradient(135deg, #8b5cf6, #06b6d4);
    border: none; color: white; border-radius: 100px; font-weight: 600; cursor: pointer; font-size: 14px; }
  .ai-typing { display: inline-flex; gap: 4px; }
  .ai-typing span { width: 6px; height: 6px; background: #8b5cf6; border-radius: 50%;
    animation: aiTyping 1.4s infinite; }
  .ai-typing span:nth-child(2) { animation-delay: 0.2s; }
  .ai-typing span:nth-child(3) { animation-delay: 0.4s; }
  @keyframes aiTyping { 0%, 60%, 100% { transform: translateY(0); opacity: 0.5; } 30% { transform: translateY(-8px); opacity: 1; } }
  `;
  document.head.appendChild(style);

  const responses = {
    greeting: ['Salom! 👋 Men 00o AI yordamchisiman. 30 ta vosita bilan yordam bera olaman!', 'Qalaysiz? Bugun qanday yordam kerak? 😊', 'Assalomu alaykum! 🚀 Qanday savol bor?'],
    startup: ['🚀 Startap g\'oyangiz qanday? AI sizga 3 ta mos investor topadi!', 'Biznes rejani yaratish uchun 5 ta savol beraymi?', 'MVP yaratish uchun mo\'ljallangan tool bor — kod kerakmi?'],
    job: ['💼 Qaysi sohada ish izlayapsiz? IT, dizayn, marketing?', '500+ vakansiya bor — filter qilib ko\'rsataymi?', 'CV yaratish uchun AI tool bor — ishlatib ko\'rdingizmi?'],
    default: ['Qiziqarli savol! Buni chuqurroq o\'rganaymi? 🤖', 'Bu haqida batafsil ma\'lumot bera olaman. Davom etamizmi?', 'Yaxshi fikr! Bu haqida hujjat tayyorlayman 📄']
  };

  const bubble = document.createElement('button');
  bubble.className = 'ai-bubble';
  bubble.innerHTML = '🤖';
  const panel = document.createElement('div');
  panel.className = 'ai-panel';
  panel.innerHTML = `
    <div class="ai-head">
      <div class="ai-avatar">🤖</div>
      <div class="ai-info">
        <div class="ai-name">00o AI</div>
        <div class="ai-status">onlayn · 30 ta vosita</div>
      </div>
      <button class="ai-close">×</button>
    </div>
    <div class="ai-msgs"></div>
    <div class="ai-tools">
      <button class="ai-tool-btn" data-t="startup">🚀 Startap</button>
      <button class="ai-tool-btn" data-t="job">💼 Ish</button>
      <button class="ai-tool-btn" data-t="code">💻 Kod</button>
      <button class="ai-tool-btn" data-t="design">🎨 Dizayn</button>
      <button class="ai-tool-btn" data-t="translate">🌍 Tarjima</button>
      <button class="ai-tool-btn" data-t="idea">💡 G\'oya</button>
    </div>
    <div class="ai-input">
      <input placeholder="Xabar yozing...">
      <button class="ai-send">➤</button>
    </div>
  `;
  document.body.appendChild(bubble);
  document.body.appendChild(panel);

  const msgs = panel.querySelector('.ai-msgs');
  const input = panel.querySelector('input');
  const send = panel.querySelector('.ai-send');
  const close = panel.querySelector('.ai-close');
  bubble.onclick = () => panel.classList.toggle('open');
  close.onclick = () => panel.classList.remove('open');

  function addMsg(text, type='bot') {
    const m = document.createElement('div');
    m.className = 'ai-msg ' + type;
    m.textContent = text;
    msgs.appendChild(m);
    msgs.scrollTop = msgs.scrollHeight;
  }
  function typing() {
    const t = document.createElement('div');
    t.className = 'ai-msg bot';
    t.innerHTML = '<div class="ai-typing"><span></span><span></span><span></span></div>';
    msgs.appendChild(t);
    msgs.scrollTop = msgs.scrollHeight;
    return t;
  }
  function respond(text) {
    const t = typing();
    setTimeout(() => {
      t.remove();
      const lower = text.toLowerCase();
      let arr = responses.default;
      if (lower.match(/salom|qalay|assalom/)) arr = responses.greeting;
      else if (lower.match(/startap|biznes|kompaniya/)) arr = responses.startup;
      else if (lower.match(/ish|vakansiya|cv/)) arr = responses.job;
      addMsg(arr[Math.floor(Math.random() * arr.length)]);
      window.sfx?.notification();
    }, 800 + Math.random() * 800);
  }
  function send_() {
    const t = input.value.trim();
    if (!t) return;
    addMsg(t, 'user');
    input.value = '';
    respond(t);
  }
  send.onclick = send_;
  input.onkeydown = e => { if (e.key === 'Enter') send_(); };
  panel.querySelectorAll('.ai-tool-btn').forEach(b => b.onclick = () => {
    const t = b.dataset.t;
    addMsg(b.textContent, 'user');
    setTimeout(() => addMsg('Bu vosiha tayyor! Batafsil: ai-chat.html', 'tool'), 600);
  });
  setTimeout(() => {
    addMsg(responses.greeting[0]);
  }, 1000);
})();
