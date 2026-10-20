/* Buscador: la lupa del menú abre una caja que busca en buscar.json (uno por
   idioma, junto a la página). Sin acentos ni mayúsculas, todas las palabras
   tienen que salir. "/" lo abre desde el teclado. Lo monta buscador.py. */
(function () {
  var b = document.querySelector('.nav-sitio .lupa');
  if (!b) return;
  var datos = null, pide = null, caja, inp, lista, sel = 0, res = [];
  function norm(s) {
    return (s || '').normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase()
      .replace(/[^a-z0-9]+/g, ' ').trim();
  }
  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return {'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;'}[c];
    });
  }
  function cargar() {
    if (pide) return pide;
    return pide = fetch('buscar.json').then(function (r) { return r.json(); }).then(function (d) {
      d.forEach(function (e) {
        e._t = norm(e.t + ' ' + (e.a || ''));
        e._x = norm(e.c + ' ' + e.s + ' ' + (e.x || ''));
      });
      return (datos = d);
    });
  }
  function puntua(e, ps) {
    var p = 0;
    for (var i = 0; i < ps.length; i++) {
      var w = ps[i], enT = e._t.indexOf(w), enX = e._x.indexOf(w);
      if (enT < 0 && enX < 0) return 0;
      if (enT === 0) p += 12; else if (enT > 0) p += (e._t.indexOf(' ' + w) >= 0 ? 8 : 5);
      else p += 1;
    }
    if (e._t === ps.join(' ')) p += 20;
    if (e.c && /^(P[aá]gina|Page|Seite|Pagina)$/.test(e.c)) p += 1;
    return p;
  }
  function pinta() {
    var q = norm(inp.value);
    if (!q) { lista.innerHTML = ''; res = []; return; }
    var ps = q.split(' ');
    res = datos.map(function (e) { return [puntua(e, ps), e]; })
      .filter(function (x) { return x[0] > 0; })
      .sort(function (a, c) { return c[0] - a[0] || a[1].t.length - c[1].t.length; })
      .slice(0, 40).map(function (x) { return x[1]; });
    sel = 0;
    lista.innerHTML = res.length ? res.map(function (e, i) {
      return '<li><a href="' + esc(e.u) + '"' + (i === 0 ? ' class="sel"' : '') + '><i>' + esc(e.c) +
        '</i><b>' + esc(e.t) + '</b>' + (e.s ? '<span>' + esc(e.s) + '</span>' : '') + '</a></li>';
    }).join('') : '<p>' + esc(b.dataset.nada) + '</p>';
  }
  function marca() {
    var as = lista.querySelectorAll('a');
    as.forEach(function (a, i) { a.classList.toggle('sel', i === sel); });
    if (as[sel]) as[sel].scrollIntoView({block: 'nearest'});
  }
  function abre() {
    if (!caja) {
      caja = document.createElement('div');
      caja.className = 'bus';
      caja.innerHTML = '<div class="bus-c" role="dialog" aria-label="' + esc(b.getAttribute('aria-label')) +
        '"><input type="search" autocomplete="off" placeholder="' + esc(b.dataset.ph) + '"><ol></ol></div>';
      document.body.appendChild(caja);
      inp = caja.querySelector('input');
      lista = caja.querySelector('ol');
      caja.addEventListener('click', function (e) {
        if (e.target === caja) cierra();
        if (e.target.closest('a')) cierra();
      });
      inp.addEventListener('input', function () { cargar().then(pinta); });
      inp.addEventListener('keydown', function (e) {
        if (e.key === 'ArrowDown') { sel = Math.min(sel + 1, res.length - 1); marca(); e.preventDefault(); }
        else if (e.key === 'ArrowUp') { sel = Math.max(sel - 1, 0); marca(); e.preventDefault(); }
        else if (e.key === 'Enter' && res[sel]) { cierra(); location.href = res[sel].u; }
      });
    }
    caja.hidden = false;
    inp.focus();
    inp.select();
    cargar();
  }
  function cierra() { if (caja) caja.hidden = true; }
  b.addEventListener('click', abre);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') cierra();
    var t = e.target.tagName;
    if (e.key === '/' && t !== 'INPUT' && t !== 'TEXTAREA' && !e.target.isContentEditable) {
      e.preventDefault(); abre();
    }
  });
  /* Al llegar a un trozo de guía desde el buscador, se marca un momento. */
  function resalta() {
    var el = location.hash && document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (!el || !el.closest('.gu-sec')) return;
    el.classList.add('gu-hit');
    setTimeout(function () { el.classList.remove('gu-hit'); }, 2500);
  }
  window.addEventListener('hashchange', resalta);
  resalta();
})();
