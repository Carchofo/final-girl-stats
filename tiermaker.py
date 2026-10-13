#!/usr/bin/env python3
"""Página "Crea tu tier list": arrastrar películas, killers o localizaciones a
filas S-D, descargar la imagen y compartir un enlace que la reproduce.

Todo en el navegador, sin servidor: el estado viaja en el #hash del enlace
(modo + índices por fila) y la imagen se dibuja en un <canvas> con las
portadas, que son del mismo dominio y no ensucian el canvas.

En el móvil arrastrar con el dedo es torpe, así que además de arrastrar se
puede tocar una foto y luego tocar la fila donde va.
"""
import json

import paginas as P
import tops

T = {
 "es": {"anadir": "Añadir fila", "quitar": "Quitar fila", "title": "Crea tu tier list de Final Girl: películas, killers y localizaciones",
        "desc": "Haz tu propia tier list de Final Girl arrastrando las cajas, los killers o los mapas. Descárgala como imagen o compártela con un enlace.",
        "eb": "Tier list maker · gratis, sin registro", "h1": "Crea tu<span class=\"roja\">tier list</span>",
        "dek": "Arrastra cada foto a su fila (en el móvil: toca la foto y luego la fila). Cuando acabes, descárgala como imagen o comparte el enlace.",
        "modos": ["Películas", "Killers", "Localizaciones"], "sin": "Sin colocar", "bajar": "Descargar imagen",
        "comp": "Copiar enlace", "copiado": "¡Enlace copiado!", "reset": "Empezar de nuevo",
        "tit_def": "Mi tier list de Final Girl", "tit_lbl": "Título", "datos": "¿Y según los datos? Mira la tier list de dificultad →"},
 "en": {"anadir": "Add row", "quitar": "Remove row", "title": "Final Girl tier list maker: rank movies, killers and locations",
        "desc": "Make your own Final Girl tier list by dragging boxes, killers or maps. Download it as an image or share it with a link. Free, no sign-up.",
        "eb": "Tier list maker · free, no sign-up", "h1": "Final Girl<span class=\"roja\">tier list maker</span>",
        "dek": "Drag each picture to its row (on mobile: tap the picture, then the row). When you're done, download it as an image or share the link.",
        "modos": ["Movies", "Killers", "Locations"], "sin": "Unranked", "bajar": "Download image",
        "comp": "Copy link", "copiado": "Link copied!", "reset": "Start over",
        "tit_def": "My Final Girl tier list", "tit_lbl": "Title", "datos": "What does the data say? See the difficulty tier list →"},
 "fr": {"anadir": "Ajouter une ligne", "quitar": "Supprimer la ligne", "title": "Créer sa tier list Final Girl : films, killers et lieux",
        "desc": "Faites votre propre tier list Final Girl en glissant les boîtes, les killers ou les lieux. Téléchargez l'image ou partagez le lien.",
        "eb": "Tier list maker · gratuit, sans inscription", "h1": "Créez votre<span class=\"roja\">tier list</span>",
        "dek": "Glissez chaque image dans sa ligne (sur mobile : touchez l'image puis la ligne). Ensuite, téléchargez l'image ou partagez le lien.",
        "modos": ["Films", "Killers", "Lieux"], "sin": "Non classés", "bajar": "Télécharger l'image",
        "comp": "Copier le lien", "copiado": "Lien copié !", "reset": "Recommencer",
        "tit_def": "Ma tier list Final Girl", "tit_lbl": "Titre", "datos": "Et selon les données ? Voir la tier list de difficulté →"},
 "de": {"anadir": "Reihe hinzufügen", "quitar": "Reihe entfernen", "title": "Final Girl Tier-List-Maker: Filme, Killer und Schauplätze",
        "desc": "Erstelle deine eigene Final-Girl-Tier-List: Boxen, Killer oder Schauplätze per Drag-and-drop. Als Bild herunterladen oder per Link teilen.",
        "eb": "Tier-List-Maker · gratis, ohne Anmeldung", "h1": "Erstelle deine<span class=\"roja\">Tier List</span>",
        "dek": "Zieh jedes Bild in seine Reihe (am Handy: Bild antippen, dann die Reihe). Danach als Bild herunterladen oder den Link teilen.",
        "modos": ["Filme", "Killer", "Schauplätze"], "sin": "Nicht eingeordnet", "bajar": "Bild herunterladen",
        "comp": "Link kopieren", "copiado": "Link kopiert!", "reset": "Neu anfangen",
        "tit_def": "Meine Final-Girl-Tier-List", "tit_lbl": "Titel", "datos": "Was sagen die Daten? Zur Schwierigkeits-Tier-List →"},
 "it": {"anadir": "Aggiungi riga", "quitar": "Rimuovi riga", "title": "Crea la tua tier list di Final Girl: film, killer e ambientazioni",
        "desc": "Crea la tua tier list di Final Girl trascinando scatole, killer o mappe. Scaricala come immagine o condividila con un link.",
        "eb": "Tier list maker · gratis, senza registrazione", "h1": "Crea la tua<span class=\"roja\">tier list</span>",
        "dek": "Trascina ogni immagine nella sua riga (da mobile: tocca l'immagine e poi la riga). Alla fine scaricala come immagine o condividi il link.",
        "modos": ["Film", "Killer", "Ambientazioni"], "sin": "Non classificati", "bajar": "Scarica immagine",
        "comp": "Copia link", "copiado": "Link copiato!", "reset": "Ricomincia",
        "tit_def": "La mia tier list di Final Girl", "tit_lbl": "Titolo", "datos": "E secondo i dati? Guarda la tier list di difficoltà →"},
}

FILAS = [("S", "#b3122a"), ("A", "#c8452c"), ("B", "#b8862b"), ("C", "#5f8a3a"), ("D", "#2f7a6b")]


def _items():
    img = tops._imagenes()
    D = P.D
    cajas = sorted(f["film"] for f in D["films"])
    killers = sorted(k for k in P.KILLERS)
    locs = sorted({f["loc"] for f in D["films"]})
    return [[(n, img.get(n, "")) for n in grupo] for grupo in (cajas, killers, locs)]


def pagina(lang):
    t = T[lang]
    pre = "" if lang == "es" else "../"
    grupos = [[(n, pre + i if i else "") for n, i in g] for g in _items()]
    cfg = {"g": grupos, "f": FILAS, "t": t, "lang": lang}
    pres = ' aria-pressed="true"'
    modos = "".join(f'<button type="button" data-m="{i}"{pres if i == 0 else ""}>{m}</button>'
                    for i, m in enumerate(t["modos"]))
    h = f'''<p class="eyebrow">{t["eb"]}</p>
<h1>{t["h1"]}</h1>
<p class="dek">{t["dek"]}</p></header>
<div class="tm-bar">
  <div class="tm-modos" role="tablist">{modos}</div>
  <label class="tm-tit">{t["tit_lbl"]} <input id="tm-titulo" maxlength="60" value="{t["tit_def"]}"></label>
</div>
<div id="tm-filas" class="tm-filas"></div>
<p class="sub tm-sinl">{t["sin"]}</p>
<div id="tm-pool" class="tm-pool tm-zona" data-fila="-1"></div>
<div class="tm-acc">
  <button type="button" id="tm-bajar" class="tm-prim">{t["bajar"]}</button>
  <button type="button" id="tm-comp">{t["comp"]}</button>
  <button type="button" id="tm-reset" class="tm-sec">{t["reset"]}</button>
</div>
<p><a href="tops.html#tier">{t["datos"]}</a></p>
<style>
  .tm-bar {{ display:flex; flex-wrap:wrap; gap:12px 20px; align-items:center; justify-content:space-between; margin:6px 0 14px; }}
  .tm-modos button {{ font:inherit; font-size:13px; font-weight:600; padding:7px 14px; border:1px solid var(--line); background:var(--surface);
                      color:var(--muted); cursor:pointer; border-radius:3px; margin-right:6px; }}
  .tm-modos button[aria-pressed="true"] {{ background:var(--blood); color:#fff; border-color:var(--blood); }}
  .tm-tit {{ font-size:13px; color:var(--muted); display:flex; gap:8px; align-items:center; }}
  .tm-tit input {{ font:inherit; font-size:14px; padding:6px 8px; background:var(--sunk); color:var(--ink); border:1px solid var(--line); border-radius:3px; width:240px; max-width:60vw; }}
  .tm-filas {{ border:1px solid var(--line); border-radius:3px; overflow:hidden; }}
  .tm-fila {{ display:flex; border-top:1px solid var(--line); background:var(--surface); }}
  .tm-fila:first-child {{ border-top:0; }}
  .tm-l {{ flex:none; width:64px; display:flex; align-items:center; justify-content:center; font-weight:800; font-size:24px; color:#fff; }}
  .tm-l input {{ width:100%; background:none; border:0; color:#fff; font:inherit; text-align:center; }}
  .tm-fila {{ position:relative; }}
  .tm-del {{ flex:none; width:30px; border:0; background:var(--sunk); color:var(--muted); font-size:18px; cursor:pointer; }}
  .tm-del:hover {{ color:#fff; background:var(--blood); }}
  .tm-add {{ display:block; width:100%; padding:8px; border:0; border-top:1px dashed var(--line); background:var(--sunk);
             color:var(--muted); font:inherit; font-size:13px; font-weight:600; cursor:pointer; }}
  .tm-add:hover {{ color:var(--ink); }}
  .tm-zona {{ display:flex; flex-wrap:wrap; gap:6px; padding:6px; min-height:84px; flex:1; }}
  .tm-zona.sobre {{ background:color-mix(in srgb,var(--blood) 12%,transparent); }}
  .tm-pool {{ border:1px dashed var(--line); border-radius:3px; background:var(--sunk); }}
  .tm-sinl {{ margin:14px 0 6px; }}
  .tm-it {{ position:relative; width:76px; height:76px; border-radius:3px; overflow:hidden; background:#222; cursor:grab; flex:none;
            touch-action:none; user-select:none; -webkit-user-select:none; }}
  .tm-it img {{ width:100%; height:100%; object-fit:cover; object-position:center 62%; pointer-events:none; display:block; }}
  .tm-it img[src*="art/"] {{ object-position:center 25%; }}
  .tm-it img[src*="loc/"] {{ object-fit:contain; background:#0d0a0b; padding:6px 4px 20px; box-sizing:border-box; }}
  .tm-it span {{ position:absolute; left:0; right:0; bottom:0; padding:12px 3px 3px; font-size:9.5px; line-height:1.15; font-weight:600;
                 color:#fff; background:linear-gradient(transparent,rgba(0,0,0,.9)); pointer-events:none; }}
  .tm-it.sel {{ outline:3px solid var(--blood); outline-offset:-3px; }}
  .tm-it.drag {{ position:fixed; z-index:99; pointer-events:none; opacity:.9; box-shadow:0 8px 24px rgba(0,0,0,.6); }}
  .tm-acc {{ display:flex; flex-wrap:wrap; gap:10px; margin:18px 0; }}
  .tm-acc button {{ font:inherit; font-size:14px; font-weight:600; padding:10px 18px; border-radius:3px; cursor:pointer;
                    border:1px solid var(--blood); background:none; color:var(--blood); }}
  .tm-acc .tm-prim {{ background:var(--blood); color:#fff; }}
  .tm-acc .tm-sec {{ border-color:var(--line); color:var(--muted); }}
  @media (max-width:560px) {{ .tm-l {{ width:44px; font-size:18px; }} .tm-it {{ width:60px; height:60px; }} .tm-zona {{ min-height:68px; }} }}
</style>
<script>
(function () {{
  var C = {json.dumps(cfg, ensure_ascii=False)};
  var filasEl = document.getElementById('tm-filas'), pool = document.getElementById('tm-pool');
  // Filas variables: se pueden añadir y quitar. Colores en ciclo.
  var PAL = C.f.map(function (f) {{ return f[1]; }}).concat(['#2f5f8a', '#5a3f8a', '#7a7a7a', '#8a2f6b']);
  var BASE = ['S', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'];
  function color(k) {{ return PAL[k % PAL.length]; }}
  var modo = 0, estado = null, etiquetas = C.f.map(function (f) {{ return f[0]; }}), sel = null;
  function esc(s) {{ return String(s).replace(/[&<>"]/g, function (c) {{ return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]; }}); }}
  function vacio() {{ return {{ filas: etiquetas.map(function () {{ return []; }}), pool: C.g[modo].map(function (_, i) {{ return i; }}) }}; }}

  // --- enlace: #m=0&t=Título&e=S,A,..&r=3.5.7|2|... (índices en base 36)
  function aHash() {{
    var p = 'm=' + modo + '&t=' + encodeURIComponent(document.getElementById('tm-titulo').value) +
      '&e=' + encodeURIComponent(etiquetas.join(',')) +
      '&r=' + estado.filas.map(function (f) {{ return f.map(function (i) {{ return i.toString(36); }}).join('.'); }}).join('|');
    history.replaceState(null, '', '#' + p);
  }}
  function deHash() {{
    var h = location.hash.slice(1); if (h.indexOf('m=') < 0) return false;
    var q = {{}}; h.split('&').forEach(function (kv) {{ var i = kv.indexOf('='); q[kv.slice(0, i)] = decodeURIComponent(kv.slice(i + 1)); }});
    modo = Math.min(2, +q.m || 0);
    if (q.t) document.getElementById('tm-titulo').value = q.t;
    if (q.e) {{ var e = q.e.split(','); if (e.length >= 1 && e.length <= 12) etiquetas = e; }}
    estado = vacio();
    (q.r || '').split('|').forEach(function (f, k) {{
      if (k >= etiquetas.length || !f) return;
      f.split('.').forEach(function (x) {{
        var i = parseInt(x, 36), j = estado.pool.indexOf(i);
        if (j >= 0) {{ estado.pool.splice(j, 1); estado.filas[k].push(i); }}
      }});
    }});
    return true;
  }}

  function ficha(i) {{
    var it = C.g[modo][i];
    return '<div class="tm-it" data-i="' + i + '" title="' + esc(it[0]) + '">' + (it[1] ? '<img src="' + it[1] + '" alt="">' : '') +
      '<span>' + esc(it[0]) + '</span></div>';
  }}
  function pintar() {{
    filasEl.innerHTML = etiquetas.map(function (et, k) {{
      return '<div class="tm-fila"><div class="tm-l" style="background:' + color(k) + '"><input value="' + esc(et) + '" data-k="' + k + '" maxlength="6"></div>' +
        '<div class="tm-zona" data-fila="' + k + '">' + estado.filas[k].map(ficha).join('') + '</div>' +
        (etiquetas.length > 1 ? '<button type="button" class="tm-del" data-k="' + k + '" aria-label="' + esc(C.t.quitar) + '" title="' + esc(C.t.quitar) + '">×</button>' : '') + '</div>';
    }}).join('') + '<button type="button" class="tm-add">+ ' + esc(C.t.anadir) + '</button>';
    filasEl.querySelectorAll('.tm-del').forEach(function (b) {{
      b.onclick = function () {{
        var k = +b.getAttribute('data-k');
        estado.pool = estado.pool.concat(estado.filas[k]); estado.filas.splice(k, 1); etiquetas.splice(k, 1); sel = null; pintar();
      }};
    }});
    filasEl.querySelector('.tm-add').onclick = function () {{
      if (etiquetas.length >= 12) return;
      etiquetas.push(BASE[etiquetas.length] || String(etiquetas.length + 1)); estado.filas.push([]); pintar();
    }};
    pool.innerHTML = estado.pool.map(ficha).join('');
    document.querySelectorAll('.tm-modos button').forEach(function (b) {{ b.setAttribute('aria-pressed', +b.getAttribute('data-m') === modo); }});
    filasEl.querySelectorAll('.tm-l input').forEach(function (inp) {{ inp.oninput = function () {{ etiquetas[+inp.getAttribute('data-k')] = inp.value; aHash(); }}; }});
    aHash();
  }}
  function mover(i, destino, antesDe) {{
    [estado.pool].concat(estado.filas).forEach(function (l) {{ var j = l.indexOf(i); if (j >= 0) l.splice(j, 1); }});
    var lista = destino < 0 ? estado.pool : estado.filas[destino];
    var pos = antesDe == null ? -1 : lista.indexOf(antesDe);
    if (pos < 0) lista.push(i); else lista.splice(pos, 0, i);
    pintar();
  }}

  // --- arrastrar (ratón y dedo con Pointer Events) o tocar y tocar
  var arr = null;
  document.addEventListener('pointerdown', function (e) {{
    var it = e.target.closest('.tm-it'); if (!it || !it.closest('#tm-filas, #tm-pool')) return;
    arr = {{ i: +it.getAttribute('data-i'), el: it, x: e.clientX, y: e.clientY, mov: false, clon: null }};
  }});
  document.addEventListener('pointermove', function (e) {{
    if (!arr) return;
    if (!arr.mov && Math.abs(e.clientX - arr.x) + Math.abs(e.clientY - arr.y) < 8) return;
    if (!arr.mov) {{ arr.mov = true; arr.clon = arr.el.cloneNode(true); arr.clon.classList.add('drag'); document.body.appendChild(arr.clon); arr.el.style.opacity = '.3'; }}
    var w = arr.clon.offsetWidth;
    arr.clon.style.left = (e.clientX - w / 2) + 'px'; arr.clon.style.top = (e.clientY - w / 2) + 'px';
    document.querySelectorAll('.tm-zona.sobre').forEach(function (z) {{ z.classList.remove('sobre'); }});
    var z = document.elementFromPoint(e.clientX, e.clientY); z = z && z.closest('.tm-zona'); if (z) z.classList.add('sobre');
    e.preventDefault();
  }}, {{ passive: false }});
  document.addEventListener('pointerup', function (e) {{
    if (!arr) return;
    var a = arr; arr = null;
    document.querySelectorAll('.tm-zona.sobre').forEach(function (z) {{ z.classList.remove('sobre'); }});
    if (a.mov) {{
      a.clon.remove();
      var bajo = document.elementFromPoint(e.clientX, e.clientY), z = bajo && bajo.closest('.tm-zona'), otro = bajo && bajo.closest('.tm-it');
      if (z) mover(a.i, +z.getAttribute('data-fila'), otro && +otro.getAttribute('data-i') !== a.i ? +otro.getAttribute('data-i') : null);
      else a.el.style.opacity = '';
      sel = null; return;
    }}
    // Toque sin arrastre: seleccionar, o colocar el seleccionado.
    if (sel === a.i) {{ sel = null; a.el.classList.remove('sel'); return; }}
    if (sel == null) {{ sel = a.i; a.el.classList.add('sel'); return; }}
    var dest = a.el.closest('.tm-zona'); var i = sel; sel = null; mover(i, +dest.getAttribute('data-fila'), a.i);
  }});
  document.addEventListener('click', function (e) {{
    if (sel == null || e.target.closest('.tm-it, .tm-l input')) return;
    var z = e.target.closest('.tm-zona, .tm-fila'); if (!z) return;
    if (z.classList.contains('tm-fila')) z = z.querySelector('.tm-zona');
    var i = sel; sel = null; mover(i, +z.getAttribute('data-fila'), null);
  }});

  document.querySelectorAll('.tm-modos button').forEach(function (b) {{
    b.onclick = function () {{ modo = +b.getAttribute('data-m'); estado = vacio(); sel = null; pintar(); }};
  }});
  document.getElementById('tm-titulo').oninput = aHash;
  document.getElementById('tm-reset').onclick = function () {{ etiquetas = C.f.map(function (f) {{ return f[0]; }}); estado = vacio(); sel = null; pintar(); }};
  document.getElementById('tm-comp').onclick = function () {{
    var b = this, url = location.href;
    if (navigator.share && /Mobi|Android/i.test(navigator.userAgent)) {{ navigator.share({{ title: document.getElementById('tm-titulo').value, url: url }}).catch(function () {{}}); return; }}
    (navigator.clipboard ? navigator.clipboard.writeText(url) : Promise.reject()).then(function () {{ b.textContent = C.t.copiado; setTimeout(function () {{ b.textContent = C.t.comp; }}, 2500); }},
      function () {{ window.prompt(C.t.comp, url); }});
  }};

  // --- imagen: se dibuja en un canvas y se descarga como PNG
  function cargar(src) {{ return new Promise(function (ok) {{ if (!src) return ok(null); var im = new Image(); im.onload = function () {{ ok(im); }}; im.onerror = function () {{ ok(null); }}; im.src = src; }}); }}
  document.getElementById('tm-bajar').onclick = function () {{
    var S = 96, G = 6, L = 90, POR = 9, W = L + G + POR * (S + G) + G, cab = 64, pie = 34;
    var alturas = estado.filas.map(function (f) {{ return Math.max(1, Math.ceil(f.length / POR)) * (S + G) + G; }});
    var H = cab + alturas.reduce(function (a, b) {{ return a + b; }}, 0) + pie;
    var cv = document.createElement('canvas'); cv.width = W * 2; cv.height = H * 2;
    var x = cv.getContext('2d'); x.scale(2, 2);
    var todos = [].concat.apply([], estado.filas);
    Promise.all(todos.map(function (i) {{ return cargar(C.g[modo][i][1]); }})).then(function (ims) {{
      var mapa = {{}}; todos.forEach(function (i, k) {{ mapa[i] = ims[k]; }});
      x.fillStyle = '#0d0a0b'; x.fillRect(0, 0, W, H);
      x.fillStyle = '#fff'; x.font = '800 26px system-ui, sans-serif'; x.fillText(document.getElementById('tm-titulo').value, 16, 42);
      var y = cab;
      estado.filas.forEach(function (f, k) {{
        var h = alturas[k];
        x.fillStyle = color(k); x.fillRect(0, y, L, h - 2);
        x.fillStyle = '#fff'; x.font = '800 30px system-ui, sans-serif'; x.textAlign = 'center'; x.textBaseline = 'middle';
        x.fillText(etiquetas[k], L / 2, y + h / 2); x.textAlign = 'left'; x.textBaseline = 'alphabetic';
        x.fillStyle = '#1a1416'; x.fillRect(L, y, W - L, h - 2);
        f.forEach(function (i, n) {{
          var cx = L + G + (n % POR) * (S + G), cy = y + G + Math.floor(n / POR) * (S + G), im = mapa[i];
          x.fillStyle = '#2a2224'; x.fillRect(cx, cy, S, S);
          if (im) {{
            if (/loc\\//.test(C.g[modo][i][1])) {{
              // Logo: entero, centrado, sin recortar.
              var k2 = Math.min((S - 8) / im.width, (S - 30) / im.height), w2 = im.width * k2, h2 = im.height * k2;
              x.fillStyle = '#0d0a0b'; x.fillRect(cx, cy, S, S); x.drawImage(im, cx + (S - w2) / 2, cy + 4 + (S - 30 - h2) / 2, w2, h2);
            }} else {{
            var art = /art\\//.test(C.g[modo][i][1]), lado = Math.min(im.width, im.height);
            var sx = (im.width - lado) / 2, sy = art ? (im.height - lado) * 0.25 : (im.height - lado) * 0.62;
            x.drawImage(im, sx, sy, lado, lado, cx, cy, S, S);
            }}
          }}
          x.fillStyle = 'rgba(0,0,0,.75)'; x.fillRect(cx, cy + S - 22, S, 22);
          x.fillStyle = '#fff'; x.font = '600 10px system-ui, sans-serif';
          var nom = C.g[modo][i][0]; while (x.measureText(nom).width > S - 6 && nom.length > 3) nom = nom.slice(0, -2) + '…';
          x.fillText(nom, cx + 3, cy + S - 8);
        }});
        y += h;
      }});
      x.fillStyle = '#e03b48'; x.font = '700 14px system-ui, sans-serif'; x.textAlign = 'right';
      x.fillText('finalgirlstats.com', W - 14, H - 12);
      var a = document.createElement('a'); a.download = 'final-girl-tier-list.png'; a.href = cv.toDataURL('image/png'); a.click();
    }});
  }};

  if (!deHash()) estado = vacio();
  pintar();
}})();
</script>'''
    return t["title"], t["desc"][:158], h
