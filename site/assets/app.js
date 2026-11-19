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

  // Sanft einblenden
  var rvs = [].slice.call(document.querySelectorAll('.rv'));
  if ('IntersectionObserver' in window && !still) {
    var rio = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); rio.unobserve(e.target); } });
    }, { threshold: 0.15 });
    rvs.forEach(function (r) { rio.observe(r); });
  } else rvs.forEach(function (r) { r.classList.add('in'); });

  // Speisekarte
  var box = document.querySelector('[data-menu]');
  if (box && window.NANIWA_MENU) {
    var data = window.NANIWA_MENU[box.dataset.menu], cats = box.querySelector('.cats'), list = box.querySelector('.dishes');
    function esc(s) { return String(s || '').replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
    function show(i) {
      [].forEach.call(cats.children, function (b, j) { b.setAttribute('aria-selected', j === i ? 'true' : 'false'); });
      list.innerHTML = data[i].g.map(function (g) {
        return '<div class="dish">' + (g.b ? '<img class="ph" loading="lazy" alt="' + esc(g.n) + '" src="' + esc(g.b) + '">' : '<span class="noph" lang="ja" aria-hidden="true">なにわ</span>') +
          '<span class="nm"><small>' + esc(g.nr) + '</small>' + esc(g.n) + '</span><span class="pr">' + esc(g.p) + '</span>' +
          (g.jp ? '<span class="jpn" lang="ja">' + esc(g.jp) + '</span>' : '') + (g.t ? '<span class="ds">' + esc(g.t) + '</span>' : '') + '</div>';
      }).join('');
    }
    data.forEach(function (c, i) {
      var b = document.createElement('button');
      b.type = 'button'; b.setAttribute('role', 'tab'); b.textContent = c.k;
      b.addEventListener('click', function () { show(i); });
      cats.appendChild(b);
    });
    show(box.dataset.menu === 'noodles' ? 1 : 0);
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
