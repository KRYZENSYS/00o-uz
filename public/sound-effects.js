// Sound effects - 00o.uz
(function() {
  const ctx = new (window.AudioContext || window.webkitAudioContext)();
  let enabled = localStorage.getItem('oo-sfx') !== '0';
  function play(freq, dur, type='sine', vol=0.1) {
    if (!enabled) return;
    try {
      const o = ctx.createOscillator();
      const g = ctx.createGain();
      o.frequency.value = freq;
      o.type = type;
      g.gain.value = vol;
      g.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + dur);
      o.connect(g);
      g.connect(ctx.destination);
      o.start();
      o.stop(ctx.currentTime + dur);
    } catch(e) {}
  }
  const sfx = {
    click: () => play(800, 0.05, 'square', 0.05),
    success: () => { play(523, 0.1); setTimeout(() => play(659, 0.1), 80); setTimeout(() => play(784, 0.15), 160); },
    error: () => play(220, 0.15, 'sawtooth', 0.1),
    notification: () => { play(1200, 0.08); setTimeout(() => play(1600, 0.1), 60); },
    levelup: () => { [523, 659, 784, 1047].forEach((f, i) => setTimeout(() => play(f, 0.15, 'sine', 0.1), i*100)); },
    coin: () => play(1500, 0.08, 'triangle', 0.08),
    achievement: () => { [659, 784, 988, 1319].forEach((f, i) => setTimeout(() => play(f, 0.2, 'triangle', 0.08), i*80)); }
  };
  document.addEventListener('click', e => {
    const btn = e.target.closest('button, a');
    if (btn) sfx.click();
  });
  window.sfx = { ...sfx, toggle: () => { enabled = !enabled; localStorage.setItem('oo-sfx', enabled ? '1' : '0'); return enabled; }, enabled: () => enabled };
})();
