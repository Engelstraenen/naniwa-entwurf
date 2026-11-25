/* NANIWA – Design-Entwurf. Öffnungszeiten, Videos, Speisekarte. */
(function () {
  // Öffnungszeiten: Index 0 = Sonntag … 6 = Samstag, Zeiten in Minuten ab Mitternacht (Europe/Berlin)
  var H = {
    noodles: [[[690, 1290]], [], [[690, 1290]], [[690, 1290]], [], [[690, 1290]], [[690, 1290]]],
    sushi: [[], [[690, 870], [1020, 1290]], [[690, 870], [1020, 1290]], [], [[690, 870], [1020, 1290]], [[690, 870], [1020, 1290]], [[690, 930], [1020, 1290]]]
  };
  var TAGE = ['Sonntag', 'Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag'];

  function berlin() {
    var p = new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/Berlin', weekday: 'short', hour: '2-digit', minute: '2-digit', hour12: false }).formatToParts(new Date());
    var o = {};
    p.forEach(function (x) { o[x.type] = x.value; });
    return { d: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].indexOf(o.weekday), m: (+o.hour % 24) * 60 + +o.minute };
  }
  function hm(m) { return ('0' + Math.floor(m / 60)).slice(-2) + ':' + ('0' + (m % 60)).slice(-2); }
  function status(shop) {
    var n = berlin(), today = H[shop][n.d], i;
    for (i = 0; i < today.length; i++) if (n.m >= today[i][0] && n.m < today[i][1]) return { open: true, text: 'Jetzt geöffnet · bis ' + hm(today[i][1]) };
    for (i = 0; i < today.length; i++) if (n.m < today[i][0]) return { open: false, text: 'Öffnet heute um ' + hm(today[i][0]) };
    for (var k = 1; k <= 7; k++) {
      var d = (n.d + k) % 7;
      if (H[shop][d].length) return { open: false, text: 'Öffnet ' + (k === 1 ? 'morgen' : TAGE[d]) + ' um ' + hm(H[shop][d][0][0]) };
    }
    return { open: false, text: 'Geschlossen' };
  }
  document.querySelectorAll('[data-status]').forEach(function (el) {
    var s = status(el.dataset.status);
    el.textContent = s.text;
    el.classList.toggle('zu', !s.open);
  });
  document.querySelectorAll('table.hours[data-shop]').forEach(function (t) {
    var shop = t.dataset.shop, n = berlin(), html = '';
    [1, 2, 3, 4, 5, 6, 0].forEach(function (d) {
      var z = H[shop][d];
      html += '<tr class="' + (d === n.d ? 'heute ' : '') + (z.length ? '' : 'ruhe') + '"><td>' + TAGE[d] + '</td><td>' +
        (z.length ? z.map(function (r) { return hm(r[0]) + ' – ' + hm(r[1]); }).join(' · ') : 'Ruhetag') + '</td></tr>';
    });
    t.innerHTML = html;
  });

  // Videos: nur abspielen, wenn sichtbar; Pause-Knopf; weniger Bewegung respektieren
  var still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var vids = [].slice.call(document.querySelectorAll('video[data-bg]'));
  if (window.matchMedia('(max-width:820px) and (orientation:portrait)').matches) {
    vids.forEach(function (v) { if (v.dataset.m) v.src = v.dataset.m; });
  }
  if ('IntersectionObserver' in window) {
    var vio = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        var v = e.target;
        if (e.isIntersecting && !still && !v.dataset.userPaused) { var p = v.play(); if (p && p.catch) p.catch(function () {}); }
        else v.pause();
      });
    }, { threshold: 0.2 });
    vids.forEach(function (v) { vio.observe(v); });
  }
  document.querySelectorAll('.pause').forEach(function (b) {
    b.addEventListener('click', function () {
      var v = b.parentElement.querySelector('video');
      if (!v) return;
      if (v.paused) { delete v.dataset.userPaused; v.play(); b.setAttribute('aria-pressed', 'false'); b.setAttribute('aria-label', 'Video anhalten'); }
      else { v.dataset.userPaused = '1'; v.pause(); b.setAttribute('aria-pressed', 'true'); b.setAttribute('aria-label', 'Video abspielen'); }
    });
  });

  // Kopfzeile auf hellen Bereichen dunkel schalten
  var hell = [].slice.call(document.querySelectorAll('.menu,.reviews,.visit,.faq,.quote'));
  if (hell.length) {
    var tick = false;
    var check = function () {
      tick = false;
      var y = 60, on = hell.some(function (h) { var r = h.getBoundingClientRect(); return r.top <= y && r.bottom > y; });
      document.body.classList.toggle('hell', on);
    };
    window.addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(check); } }, { passive: true });
    check();
  }

  // Gäste-Stimmen: ruhiges Überblenden (Desktop 3 Karten, Handy 1 Karte)
  var vbox = document.querySelector('[data-voices]');
  if (vbox) {
    var texts = JSON.parse(vbox.dataset.voices), mq = window.matchMedia('(max-width:820px)'), timer = null;
    var build = function () {
      var n = mq.matches ? 1 : 3, slots = [], html = '';
      vbox.style.setProperty('--n', n);
      for (var i = 0; i < n; i++) slots.push([]);
      texts.forEach(function (t, i) { slots[i % n].push(t); });
      vbox.innerHTML = slots.map(function (sl) {
        return '<div class="vslot">' + sl.map(function (t, k) {
          return '<figure class="voice' + (k === 0 ? ' on' : '') + '"><p>' + t.replace(/[<>&]/g, '') + '</p><span class="tag">Beispiel · noch keine echte Bewertung</span></figure>';
        }).join('') + '</div>';
      }).join('');
      if (timer) clearInterval(timer);
      if (still) return;
      var tick = 0, pos = slots.map(function () { return 0; });
      // ruhig: pro Takt wechselt nur eine Karte, reihum
      timer = setInterval(function () {
        var si = tick % n, slot = vbox.children[si], c = slot.children;
        if (c.length > 1) { c[pos[si]].classList.remove('on'); pos[si] = (pos[si] + 1) % c.length; var nx = c[pos[si]]; setTimeout(function () { nx.classList.add('on'); }, 900); }
        tick++;
      }, n > 1 ? 6000 : 8000);
    };
    build();
    if (mq.addEventListener) mq.addEventListener('change', build);
  }

  // Zahlen hochzählen, sobald sichtbar (Bewertungen)
  var nums = [].slice.call(document.querySelectorAll('[data-to]'));
  function fmt(v, dec) { return dec ? v.toFixed(dec).replace('.', ',') : Math.round(v).toLocaleString('de-DE'); }
  function count(el) {
    var to = parseFloat(el.dataset.to), dec = +(el.dataset.dec || 0), t0 = null, dur = 1700;
    function step(t) { if (!t0) t0 = t; var k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 3); el.textContent = fmt(to * e, dec); if (k < 1) requestAnimationFrame(step); }
    requestAnimationFrame(step);
  }
  if (nums.length && 'IntersectionObserver' in window && !still) {
    nums.forEach(function (el) { el.textContent = fmt(0, +(el.dataset.dec || 0)); });
    var nio = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { count(e.target); nio.unobserve(e.target); } });
    }, { threshold: 0.6 });
    nums.forEach(function (el) { nio.observe(el); });
  }

  // Sanft einblenden
  var rvs = [].slice.call(document.querySelectorAll('.rv'));
  if ('IntersectionObserver' in window && !still) {
    var rio = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('vis'); rio.unobserve(e.target); } });
    }, { threshold: 0.15 });
    rvs.forEach(function (r) { rio.observe(r); });
  } else rvs.forEach(function (r) { r.classList.add('vis'); });

  // Speisekarte
  var box = document.querySelector('[data-menu]');
  if (box && window.NANIWA_MENU) {
    var data = window.NANIWA_MENU[box.dataset.menu], cats = box.querySelector('.cats'), list = box.querySelector('.dishes');
    function esc(s) { return String(s || '').replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
    var leg = window.NANIWA_MENU.leg || { al: {}, zs: {} }, ic = '../assets/img/allergene/';
    // Symbole wie auf der echten Karte: Zusatzstoffe als Hochzahl, Allergene als kleine Kreise, Schwein, vegetarisch
    function zs(z) {
      return z && z.length ? '<sup class="zs" title="' + esc(z.map(function (n) { return n + ' ' + (leg.zs[n] || ''); }).join(', ')) + '">' + z.join(',') + '</sup>' : '';
    }
    function sy(g) {
      if (!(g.al && g.al.length) && !g.sw && !g.veg) return '';
      return '<div class="sy">' + (g.al || []).map(function (k) {
        return '<img src="' + ic + k + '.png" width="20" height="20" alt="' + esc(leg.al[k] || k) + '" title="' + esc(leg.al[k] || k) + '">';
      }).join('') +
        (g.sw ? '<span class="sw" role="img" aria-label="mit Schweinefleisch' + (g.sw > 1 ? ', doppelte Menge' : '') + '" title="Schwein' + (g.sw > 1 ? ' ×2' : '') + '"><i></i>' + (g.sw > 1 ? '<b>×2</b>' : '') + '</span>' : '') +
        (g.veg ? '<span class="veg">auch komplett vegetarisch</span>' : '') + '</div>';
    }
    function legende() {
      var al = Object.keys(leg.al);
      if (!al.length || box.dataset.menu !== 'noodles') return;
      var d = document.createElement('details');
      d.className = 'leg';
      d.innerHTML = '<summary>Allergene &amp; Zusatzstoffe</summary><div class="lg">' +
        al.map(function (k) { return '<span><img src="' + ic + k + '.png" width="20" height="20" alt="">' + esc(leg.al[k]) + '</span>'; }).join('') +
        '<span><span class="sw"><i></i></span>Schwein (×2 = doppelt Chashu)</span>' +
        '<span><span class="veg">veg.</span>auch komplett vegetarisch erhältlich</span></div><div class="lg zl">' +
        Object.keys(leg.zs).map(function (n) { return '<span><b>' + n + '</b>' + esc(leg.zs[n]) + '</span>'; }).join('') +
        '</div><p>Angaben laut Naniwa-Speisekarte. Bei Allergien bitte im Restaurant nachfragen.</p>';
      list.parentNode.insertBefore(d, list.nextSibling);
    }
    function show(i) {
      [].forEach.call(cats.children, function (b, j) { b.setAttribute('aria-selected', j === i ? 'true' : 'false'); });
      list.innerHTML = data[i].g.map(function (g) {
        return '<article class="dish">' + (g.nr || g.jp ? '<div class="tp"><small>' + esc(g.nr) + '</small>' + (g.jp ? '<span lang="ja">' + esc(g.jp) + '</span>' : '') + '</div>' : '') +
          (g.b ? '<img class="ph" loading="lazy" decoding="async" width="1200" height="800" alt="' + esc(g.n) + '" src="' + esc(g.b) + '">' : '') +
          '<div class="rw"><h3 class="nm">' + esc(g.n) + zs(g.zs) + '</h3><span class="pr">' + esc(g.p) + '</span></div>' +
          (g.t ? '<p class="ds">' + esc(g.t) + '</p>' : '') + sy(g) + '</article>';
      }).join('');
    }
    data.forEach(function (c, i) {
      var b = document.createElement('button');
      b.type = 'button'; b.setAttribute('role', 'tab'); b.textContent = c.k;
      b.addEventListener('click', function () { show(i); });
      cats.appendChild(b);
    });
    show(box.dataset.menu === 'noodles' ? 1 : 0);
    legende();
    var z = document.createElement('div');
    z.className = 'zoom'; z.innerHTML = '<img alt=""><p></p>';
    document.body.appendChild(z);
    z.addEventListener('click', function () { z.classList.remove('on'); });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') z.classList.remove('on'); });
    list.addEventListener('click', function (e) {
      if (!e.target.classList.contains('ph')) return;
      z.firstChild.src = e.target.src; z.lastChild.textContent = e.target.alt; z.classList.add('on');
    });
  }
})();
