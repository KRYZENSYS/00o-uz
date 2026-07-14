// Confetti effect - 00o.uz
(function() {
  const canvas = document.createElement('canvas');
  canvas.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;z-index:99999';
  document.body.appendChild(canvas);
  const ctx = canvas.getContext('2d');
  let particles = [];
  let animating = false;
  const colors = ['#8b5cf6','#06b6d4','#ec4899','#f59e0b','#22c55e','#3b82f6','#ef4444'];

  function resize() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
  resize();
  window.addEventListener('resize', resize);

  class Particle {
    constructor(x, y) {
      this.x = x; this.y = y;
      this.size = Math.random() * 8 + 4;
      this.color = colors[Math.floor(Math.random() * colors.length)];
      this.vx = (Math.random() - 0.5) * 12;
      this.vy = Math.random() * -15 - 5;
      this.gravity = 0.4;
      this.rotation = Math.random() * 360;
      this.rotationSpeed = (Math.random() - 0.5) * 10;
      this.opacity = 1;
      this.shape = Math.random() > 0.5 ? 'rect' : 'circle';
    }
    update() {
      this.x += this.vx; this.y += this.vy;
      this.vy += this.gravity; this.vx *= 0.99;
      this.rotation += this.rotationSpeed;
      if (this.y > canvas.height) this.opacity -= 0.02;
    }
    draw() {
      ctx.save();
      ctx.globalAlpha = this.opacity;
      ctx.translate(this.x, this.y);
      ctx.rotate(this.rotation * Math.PI / 180);
      ctx.fillStyle = this.color;
      if (this.shape === 'rect') {
        ctx.fillRect(-this.size/2, -this.size/2, this.size, this.size/2);
      } else {
        ctx.beginPath();
        ctx.arc(0, 0, this.size/2, 0, Math.PI * 2);
        ctx.fill();
      }
      ctx.restore();
    }
  }

  function loop() {
    if (!animating) return;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    particles = particles.filter(p => p.opacity > 0);
    particles.forEach(p => { p.update(); p.draw(); });
    if (particles.length > 0) requestAnimationFrame(loop);
    else animating = false;
  }

  window.confetti = function(opts = {}) {
    const { count = 150, x = canvas.width/2, y = canvas.height/3 } = opts;
    for (let i = 0; i < count; i++) {
      particles.push(new Particle(x, y));
    }
    if (!animating) { animating = true; loop(); }
  };

  window.fireworks = function() {
    for (let i = 0; i < 5; i++) {
      setTimeout(() => {
        const x = Math.random() * canvas.width;
        const y = Math.random() * canvas.height * 0.5;
        window.confetti({ count: 80, x, y });
      }, i * 300);
    }
  };
})();
