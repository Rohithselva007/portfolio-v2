
    // Cursor
    const cur = document.getElementById('cursor'), ring = document.getElementById('cursor-ring');
    let mx = 0, my = 0, rx = 0, ry = 0;
    document.addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; cur.style.left = mx + 'px'; cur.style.top = my + 'px'; });
    (function animRing() { rx += (mx - rx) * .12; ry += (my - ry) * .12; ring.style.left = rx + 'px'; ring.style.top = ry + 'px'; requestAnimationFrame(animRing); })();

    // Canvas
    const canvas = document.getElementById('bg-canvas'), ctx = canvas.getContext('2d');
    let W, H, dots = [];
    function resize() { W = canvas.width = window.innerWidth; H = canvas.height = window.innerHeight; }
    resize(); window.addEventListener('resize', resize);
    for (let i = 0; i < 80; i++)dots.push({ x: Math.random() * 1920, y: Math.random() * 1080, vx: (Math.random() - .5) * .3, vy: (Math.random() - .5) * .3, r: Math.random() * 1.5 + .5 });
    function drawCanvas() {
      ctx.clearRect(0, 0, W, H);
      dots.forEach(d => { d.x += d.vx; d.y += d.vy; if (d.x < 0) d.x = W; if (d.x > W) d.x = 0; if (d.y < 0) d.y = H; if (d.y > H) d.y = 0; ctx.beginPath(); ctx.arc(d.x, d.y, d.r, 0, Math.PI * 2); ctx.fillStyle = 'rgba(127,119,221,.6)'; ctx.fill(); });
      dots.forEach((a, i) => dots.slice(i + 1).forEach(b => { const dist = Math.hypot(a.x - b.x, a.y - b.y); if (dist < 120) { ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.strokeStyle = `rgba(127,119,221,${.15 * (1 - dist / 120)})`; ctx.lineWidth = .5; ctx.stroke(); } }));
      requestAnimationFrame(drawCanvas);
    }
    drawCanvas();

    // Scroll reveal
    const obs = new IntersectionObserver(entries => entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); }), { threshold: .1 });
    document.querySelectorAll('section').forEach(s => obs.observe(s));

    // Skill bars
    const skillObs = new IntersectionObserver(entries => entries.forEach(e => { if (e.isIntersecting) e.target.querySelectorAll('.skill-fill').forEach(b => b.style.width = b.dataset.w + '%'); }), { threshold: .2 });
    document.querySelectorAll('#skills').forEach(s => skillObs.observe(s));

    // Project view tracking
    document.querySelectorAll('.proj-card[data-slug]').forEach(card => {
      card.addEventListener('click', () => {
        const slug = card.dataset.slug;
        fetch(`/api/project/${slug}/view/`, { method: 'POST', headers: { 'X-CSRFToken': getCookie('csrftoken') } })
          .then(r => r.json()).then(d => {
            const el = document.getElementById('views-' + slug);
            if (el) el.textContent = d.views + ' views';
          }).catch(() => { });
      });
    });

    // Contact form
    document.getElementById('contact-form').addEventListener('submit', async e => {
      e.preventDefault();
      const form = e.target, btn = form.querySelector('button[type=submit]'), msg = document.getElementById('form-msg');
      btn.textContent = 'Sending...'; btn.disabled = true;
      const data = new FormData(form);
      try {
        const res = await fetch('/contact/', { method: 'POST', body: data, headers: { 'X-CSRFToken': getCookie('csrftoken') } });
        const json = await res.json();
        if (json.ok) { msg.textContent = "Message sent! I'll get back to you soon."; msg.className = 'form-msg success'; form.reset(); }
        else { msg.textContent = json.errors.join(' '); msg.className = 'form-msg error'; }
      } catch (err) { msg.textContent = 'Something went wrong. Please email me directly.'; msg.className = 'form-msg error'; }
      btn.textContent = 'Send message →'; btn.disabled = false;
    });

    function getCookie(name) {
      const val = `; ${document.cookie}`;
      const parts = val.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(';').shift();
    }