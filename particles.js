(function () {
  const canvas = document.createElement('canvas');
  canvas.id = 'bg-canvas';
  document.body.prepend(canvas);

  const ctx = canvas.getContext('2d');

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }

  resize();
  window.addEventListener('resize', resize);

  const PARTICLE_COUNT = 10;
  const particles = [];

  function getContentRect() {
    var el = document.querySelector('main');
    if (!el) return null;
    return el.getBoundingClientRect();
  }

  function spawnOnPerimeter(rect) {
    var perimeter = 2 * (rect.width + rect.height);
    var t = Math.random() * perimeter;
    var x, y;

    if (t < rect.width) {
      x = rect.left + t;
      y = rect.top;
    } else if (t < rect.width + rect.height) {
      x = rect.right;
      y = rect.top + (t - rect.width);
    } else if (t < 2 * rect.width + rect.height) {
      x = rect.right - (t - rect.width - rect.height);
      y = rect.bottom;
    } else {
      x = rect.left;
      y = rect.bottom - (t - 2 * rect.width - rect.height);
    }

    return { x: x, y: y };
  }

  function Particle(stagger) {
    this.reset(stagger);
  }

  Particle.prototype.reset = function (stagger) {
    var rect = getContentRect();

    var cx, cy, spawnX, spawnY;

    if (rect) {
      cx = rect.left + rect.width / 2;
      cy = rect.top + rect.height / 2;
      var pt = spawnOnPerimeter(rect);
      spawnX = pt.x;
      spawnY = pt.y;
    } else {
      cx = canvas.width / 2;
      cy = canvas.height / 2;
      var angle0 = Math.random() * Math.PI * 2;
      spawnX = cx + Math.cos(angle0) * 200;
      spawnY = cy + Math.sin(angle0) * 200;
    }

    var dx = spawnX - cx;
    var dy = spawnY - cy;
    var len = Math.sqrt(dx * dx + dy * dy) || 1;
    var speed = 0.4 + Math.random() * 0.6;
    this.vx = (dx / len) * speed;
    this.vy = (dy / len) * speed;
    this.size = 3 + Math.random() * 4;
    this.maxLife = 400 + Math.random() * 400;

    if (stagger) {
      var t2 = Math.random() * this.maxLife;
      this.life = t2;
      this.x = spawnX + this.vx * t2;
      this.y = spawnY + this.vy * t2;
    } else {
      this.life = 0;
      this.x = spawnX;
      this.y = spawnY;
    }
  };

  Particle.prototype.update = function () {
    this.x += this.vx;
    this.y += this.vy;
    this.life++;

    if (
      this.life >= this.maxLife ||
      this.x < -80 || this.x > canvas.width + 80 ||
      this.y < -80 || this.y > canvas.height + 80
    ) {
      this.reset(false);
    }
  };

  Particle.prototype.draw = function () {
    var progress = this.life / this.maxLife;
    var alpha = progress < 0.15
      ? (progress / 0.15) * 0.4
      : (1 - progress) * 0.4;

    ctx.save();
    ctx.translate(this.x, this.y);
    ctx.strokeStyle = 'rgba(140, 140, 140, ' + alpha + ')';
    ctx.lineWidth = 0.75;
    ctx.lineCap = 'round';

    for (var i = 0; i < 6; i++) {
      ctx.save();
      ctx.rotate((i * Math.PI) / 3);
      ctx.beginPath();
      ctx.moveTo(0, 0);
      ctx.lineTo(0, this.size);
      var bh = this.size * 0.55;
      var bw = this.size * 0.3;
      ctx.moveTo(0, bh);
      ctx.lineTo(bw, bh - bw);
      ctx.moveTo(0, bh);
      ctx.lineTo(-bw, bh - bw);
      ctx.stroke();
      ctx.restore();
    }

    ctx.restore();
  };

  for (var i = 0; i < PARTICLE_COUNT; i++) {
    particles.push(new Particle(true));
  }

  function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (var i = 0; i < particles.length; i++) {
      particles[i].update();
      particles[i].draw();
    }
    requestAnimationFrame(animate);
  }

  animate();
})();
