#!/usr/bin/env python3
"""Pestaña "Tops de la comunidad": votación y ranking, todo dentro de la web.

El voto viaja a un formulario de Google (de la cuenta del sitio) con un POST
desde el navegador; el visitante nunca ve el formulario. Los resultados se
leen de la hoja de respuestas, compartida en solo lectura, por la API de
visualización de Google en modo JSONP (no necesita CORS).

Un voto por navegador (se recuerda en localStorage). No es infalible y no
pretende serlo: si alguien hace trampas, se filtran filas en la hoja.

Las opciones salen de tops_opciones.json, que se generó desde los mismos
datos que el resto de la web, y son exactamente las del formulario.
"""
import json
import pathlib

AQUI = pathlib.Path(__file__).parent

FORM = "https://docs.google.com/forms/d/e/1FAIpQLSeMu7wzCoW5v_4VNMMvg2HARI5c0rTgZUsahPcBv1C-IUiBqQ/formResponse"
HOJA = "1HcwE8UFDByRGln_h4_RZk1ds-Xo3xPIrWfeXV7brwVM"
ENTRADAS = {"easiest_box": "1037940783", "hardest_box": "990824240", "most_immersive_box": "959760338",
            "worst_box": "1386136466", "best_killer": "1501686861", "best_location": "1356803176",
            "best_setup": "674130540", "best_series": "414320778", "best_final_girl": "589723174",
            "simplest_killer": "1967221705", "most_complex_killer": "2122986646"}
# Orden de las columnas en la hoja (después de Timestamp), igual que el formulario.
COLUMNAS = list(ENTRADAS)

T = {
 "es": {"tab": "Tops", "h2": "Tops de la comunidad",
        "sub": "Lo que dice la gente, no los datos. Vota lo tuyo: todas las preguntas son opcionales y puedes dejar las que no sepas.",
        "votar": "Votar", "gracias": "¡Gracias! Tu voto ya cuenta.", "ya": "Ya has votado desde este navegador. Así va la cosa:",
        "nada": "—", "votos": "votos", "voto": "voto", "sin": "Aún no hay votos. Sé el primero.",
        "error": "No se han podido cargar los resultados ahora mismo.", "enviando": "Enviando…",
        "q": {"easiest_box": "Caja más fácil", "hardest_box": "Caja más difícil", "most_immersive_box": "Caja más inmersiva",
              "worst_box": "Peor caja", "best_killer": "Mejor killer", "best_location": "Mejor localización",
              "best_setup": "Mejor Setup", "best_series": "Mejor temporada", "best_final_girl": "Mejor Final Girl",
              "simplest_killer": "Killer más sencillo de reglas", "most_complex_killer": "Killer más complejo de reglas"}},
 "en": {"tab": "Tops", "h2": "Community tops",
        "sub": "What players think, not what the data says. Cast your vote: every question is optional, skip the ones you don't know.",
        "votar": "Vote", "gracias": "Thanks! Your vote counts.", "ya": "You've already voted from this browser. Here's how it stands:",
        "nada": "—", "votos": "votes", "voto": "vote", "sin": "No votes yet. Be the first.",
        "error": "Results couldn't be loaded right now.", "enviando": "Sending…",
        "q": {"easiest_box": "Easiest box", "hardest_box": "Hardest box", "most_immersive_box": "Most immersive box",
              "worst_box": "Worst box", "best_killer": "Best killer", "best_location": "Best location",
              "best_setup": "Best Setup", "best_series": "Best series", "best_final_girl": "Best Final Girl",
              "simplest_killer": "Simplest killer (rules)", "most_complex_killer": "Most complex killer (rules)"}},
 "fr": {"tab": "Tops", "h2": "Tops de la communauté",
        "sub": "L'avis des joueurs, pas celui des chiffres. Votez : toutes les questions sont facultatives.",
        "votar": "Voter", "gracias": "Merci ! Votre vote compte.", "ya": "Vous avez déjà voté depuis ce navigateur. Voici les résultats :",
        "nada": "—", "votos": "votes", "voto": "vote", "sin": "Pas encore de votes. Soyez le premier.",
        "error": "Impossible de charger les résultats pour le moment.", "enviando": "Envoi…",
        "q": {"easiest_box": "Boîte la plus facile", "hardest_box": "Boîte la plus difficile", "most_immersive_box": "Boîte la plus immersive",
              "worst_box": "Pire boîte", "best_killer": "Meilleur killer", "best_location": "Meilleur lieu",
              "best_setup": "Meilleur Setup", "best_series": "Meilleure saison", "best_final_girl": "Meilleure Final Girl",
              "simplest_killer": "Killer aux règles les plus simples", "most_complex_killer": "Killer aux règles les plus complexes"}},
 "de": {"tab": "Tops", "h2": "Community-Tops",
        "sub": "Was die Spieler denken, nicht was die Daten sagen. Stimm ab: Jede Frage ist optional.",
        "votar": "Abstimmen", "gracias": "Danke! Deine Stimme zählt.", "ya": "Du hast in diesem Browser schon abgestimmt. So sieht es aus:",
        "nada": "—", "votos": "Stimmen", "voto": "Stimme", "sin": "Noch keine Stimmen. Sei die erste Stimme.",
        "error": "Die Ergebnisse konnten gerade nicht geladen werden.", "enviando": "Wird gesendet…",
        "q": {"easiest_box": "Leichteste Box", "hardest_box": "Schwerste Box", "most_immersive_box": "Atmosphärischste Box",
              "worst_box": "Schlechteste Box", "best_killer": "Bester Killer", "best_location": "Bester Schauplatz",
              "best_setup": "Bestes Setup", "best_series": "Beste Staffel", "best_final_girl": "Bestes Final Girl",
              "simplest_killer": "Killer mit den einfachsten Regeln", "most_complex_killer": "Killer mit den komplexesten Regeln"}},
 "it": {"tab": "Top", "h2": "Top della community",
        "sub": "Cosa pensano i giocatori, non cosa dicono i dati. Vota: ogni domanda è facoltativa.",
        "votar": "Vota", "gracias": "Grazie! Il tuo voto conta.", "ya": "Hai già votato da questo browser. Ecco come va:",
        "nada": "—", "votos": "voti", "voto": "voto", "sin": "Ancora nessun voto. Sii il primo.",
        "error": "Non è stato possibile caricare i risultati ora.", "enviando": "Invio…",
        "q": {"easiest_box": "Scatola più facile", "hardest_box": "Scatola più difficile", "most_immersive_box": "Scatola più immersiva",
              "worst_box": "Scatola peggiore", "best_killer": "Miglior killer", "best_location": "Miglior ambientazione",
              "best_setup": "Miglior Setup", "best_series": "Miglior stagione", "best_final_girl": "Miglior Final Girl",
              "simplest_killer": "Killer con le regole più semplici", "most_complex_killer": "Killer con le regole più complesse"}},
}


def _opciones():
    return json.loads((AQUI / "tops_opciones.json").read_text(encoding="utf-8"))


def seccion(lang):
    t = T[lang]
    cfg = {"form": FORM, "hoja": HOJA, "e": ENTRADAS, "cols": COLUMNAS, "o": _opciones(), "t": t}
    return f'''
<section id="v-tops" hidden>
  <h2>{t["h2"]}</h2>
  <p class="sub">{t["sub"]}</p>
  <form id="ct-form" class="ct-form"></form>
  <p id="ct-msg" class="sub" aria-live="polite"></p>
  <div id="ct-res" class="ct-res"></div>
</section>
<style>
  .ct-form {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(230px,1fr)); gap:10px 14px; margin:14px 0 6px; }}
  .ct-form label {{ display:flex; flex-direction:column; gap:4px; font-family:var(--f-mono); font-size:10.5px;
                    letter-spacing:.08em; text-transform:uppercase; color:var(--muted); }}
  .ct-form select {{ font:inherit; font-family:var(--f-sans, inherit); text-transform:none; letter-spacing:0; font-size:14px;
                     padding:8px; background:var(--sunk); color:var(--ink); border:1px solid var(--line); border-radius:3px; }}
  .ct-form button {{ grid-column:1/-1; justify-self:start; background:var(--blood); color:#fff; border:0; border-radius:3px;
                     padding:10px 22px; font:inherit; font-weight:600; letter-spacing:.04em; cursor:pointer; }}
  .ct-form button[disabled] {{ opacity:.6; cursor:default; }}
  .ct-res {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:14px; margin-top:16px; }}
  .ct-card {{ background:var(--surface); border:1px solid var(--line); border-top:2px solid var(--blood); border-radius:3px; padding:12px 14px; }}
  .ct-card h3 {{ margin:0 0 8px; font-size:15px; }}
  .ct-row {{ position:relative; display:flex; justify-content:space-between; gap:8px; padding:5px 6px; font-size:13.5px; }}
  .ct-row .b {{ position:absolute; inset:0 auto 0 0; background:color-mix(in srgb,var(--blood) 16%,transparent); border-radius:2px; }}
  .ct-row span {{ position:relative; }}
  .ct-row .n {{ font-family:var(--f-mono); font-size:12px; color:var(--muted); white-space:nowrap; }}
</style>
<script>
(function () {{
  var C = {json.dumps(cfg, ensure_ascii=False)};
  var K = 'fg-tops-votado';
  var form = document.getElementById('ct-form'), msg = document.getElementById('ct-msg'), res = document.getElementById('ct-res');
  function esc(s) {{ return String(s).replace(/[&<>"]/g, function (c) {{ return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]; }}); }}
  var votado = false; try {{ votado = localStorage.getItem(K) === '1'; }} catch (e) {{}}

  form.innerHTML = C.cols.map(function (id) {{
    return '<label>' + esc(C.t.q[id]) + '<select name="' + id + '"><option value="">' + C.t.nada + '</option>' +
      C.o[id].map(function (o) {{ return '<option>' + esc(o) + '</option>'; }}).join('') + '</select></label>';
  }}).join('') + '<button type="submit">' + esc(C.t.votar) + '</button>';
  if (votado) {{ form.hidden = true; msg.textContent = C.t.ya; }}

  form.addEventListener('submit', function (ev) {{
    ev.preventDefault();
    var d = new URLSearchParams(), alguno = false;
    C.cols.forEach(function (id) {{
      var v = form.elements[id].value;
      if (v) {{ d.append('entry.' + C.e[id], v); alguno = true; }}
    }});
    if (!alguno) return;
    var b = form.querySelector('button'); b.disabled = true; b.textContent = C.t.enviando;
    // no-cors: Google no deja leer la respuesta, pero el voto llega.
    fetch(C.form, {{ method: 'POST', mode: 'no-cors', body: d }}).finally(function () {{
      try {{ localStorage.setItem(K, '1'); }} catch (e) {{}}
      form.hidden = true; msg.textContent = C.t.gracias;
      setTimeout(cargar, 2500);
    }});
  }});

  function pintar(filas) {{
    if (!filas.length) {{ res.innerHTML = '<p class="sub">' + esc(C.t.sin) + '</p>'; return; }}
    res.innerHTML = C.cols.map(function (id, i) {{
      var cuenta = {{}}, total = 0;
      filas.forEach(function (f) {{ var v = f[i]; if (v) {{ cuenta[v] = (cuenta[v] || 0) + 1; total++; }} }});
      var top = Object.keys(cuenta).sort(function (a, b) {{ return cuenta[b] - cuenta[a]; }}).slice(0, 5);
      if (!top.length) return '';
      var max = cuenta[top[0]];
      return '<div class="ct-card"><h3>' + esc(C.t.q[id]) + '</h3>' + top.map(function (n) {{
        return '<div class="ct-row"><i class="b" style="width:' + (cuenta[n] / max * 100) + '%"></i><span>' + esc(n) +
          '</span><span class="n">' + cuenta[n] + ' ' + (cuenta[n] === 1 ? C.t.voto : C.t.votos) + '</span></div>';
      }}).join('') + '</div>';
    }}).join('');
  }}

  // JSONP de la API de visualización: la hoja es de solo lectura por enlace.
  var n = 0;
  function cargar() {{
    var cb = 'fgTops' + (++n);
    window[cb] = function (r) {{
      try {{
        // Sin respuestas, Google toma la cabecera por un voto: fuera.
        var filas = (r.table.rows || []).filter(function (row) {{
          return !(row.c[1] && row.c[1].v === 'Easiest box');
        }}).map(function (row) {{
          return row.c.slice(1).map(function (c) {{ return c && c.v ? String(c.v) : ''; }});
        }});
        pintar(filas);
      }} catch (e) {{ res.innerHTML = '<p class="sub">' + esc(C.t.error) + '</p>'; }}
      delete window[cb];
    }};
    var s = document.createElement('script');
    s.src = 'https://docs.google.com/spreadsheets/d/' + C.hoja + '/gviz/tq?headers=1&tqx=responseHandler:' + cb + '&t=' + Date.now();
    s.onerror = function () {{ res.innerHTML = '<p class="sub">' + esc(C.t.error) + '</p>'; }};
    document.head.appendChild(s);
  }}
  cargar();
}})();
</script>
'''


def poner(cuerpo, lang):
    """Añade la pestaña y la sección a la página grande, junto a la matriz."""
    if 'id="v-tops"' in cuerpo:
        return cuerpo
    t = T[lang]
    i = cuerpo.find('<button role="tab" data-t="matriz"')
    j = cuerpo.find('</button>', i) + len('</button>')
    if i < 0:
        return cuerpo
    cuerpo = cuerpo[:j] + f'\n  <button role="tab" data-t="tops" aria-selected="false">{t["tab"]}</button>' + cuerpo[j:]
    k = cuerpo.find('<section id="v-matriz">')
    k = cuerpo.find('</section>', k) + len('</section>')
    cuerpo = cuerpo[:k] + seccion(lang) + cuerpo[k:]
    # La lista de pestañas que entiende el #hash del enlace.
    return cuerpo.replace("'matriz', 'cajas'", "'matriz', 'tops', 'cajas'", 1)
