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

FORM = "https://docs.google.com/forms/d/e/1FAIpQLSeAWTzHjQvttvkZkpPQxGMZZoflJdXF5aZqsm44p42JItNDFQ/formResponse"
HOJA = "1pFBklqcyVw17038m-NPmq7Q_CVnMBMELxNN6lyFTMZU"
# Tres casillas por categoría: el 1º suma 3 puntos, el 2º 2 y el 3º 1.
ENTRADAS = {"easiest_box_1": "1941202498", "easiest_box_2": "1055419443", "easiest_box_3": "1425232451", "hardest_box_1": "359424908", "hardest_box_2": "1001047716", "hardest_box_3": "337431242", "most_immersive_box_1": "1588180815", "most_immersive_box_2": "232916496", "most_immersive_box_3": "1020920136", "worst_box_1": "376232544", "worst_box_2": "1036205401", "worst_box_3": "781557868", "best_killer_1": "1383692492", "best_killer_2": "1023437847", "best_killer_3": "916331605", "best_location_1": "1137060530", "best_location_2": "1908626071", "best_location_3": "2048900617", "best_series_1": "770362820", "best_series_2": "1839676813", "best_series_3": "890327225", "best_box_1": "360846821", "best_box_2": "1158631747", "best_box_3": "40424145", "most_complex_killer_1": "1031299552", "most_complex_killer_2": "1872729929", "most_complex_killer_3": "1263855913"}
COLUMNAS = ["easiest_box", "hardest_box", "most_immersive_box", "worst_box", "best_killer",
            "best_location", "best_series", "best_box", "most_complex_killer"]
# Orden en pantalla (COLUMNAS es el orden de las columnas de la hoja, no tocar).
ORDEN = ["best_series", "best_box", "best_killer", "easiest_box", "hardest_box", "most_immersive_box",
         "worst_box", "best_location", "most_complex_killer"]
PUNTOS = [3, 2, 1]

T = {
 "es": {"sub0": "Lo que dice la gente, no los datos.", "ir": "Vota tus tops ↓", "h2v": "Vota", "tab": "Tops", "pts": "pts", "rk": "1º|2º|3º", "sub2": "Elige hasta 3 por categoría: el 1º vale 3 puntos, el 2º 2 y el 3º 1.", "h2": "Tops de la comunidad",
        "sub": "Lo que dice la gente, no los datos. Vota lo tuyo: todas las preguntas son opcionales y puedes dejar las que no sepas.",
        "votar": "Votar", "gracias": "¡Gracias! Tu voto ya cuenta.", "ya": "Ya has votado desde este navegador. Así va la cosa:",
        "nada": "—", "votos": "votos", "voto": "voto", "sin": "Aún no hay votos. Sé el primero.",
        "error": "No se han podido cargar los resultados ahora mismo.", "enviando": "Enviando…",
        "q": {"easiest_box": "Caja más fácil", "hardest_box": "Caja más difícil", "most_immersive_box": "Caja más inmersiva",
              "worst_box": "Peor caja", "best_killer": "Mejor killer", "best_location": "Mejor localización",
              "best_setup": "Mejor Setup", "best_series": "Mejor temporada", "best_final_girl": "Mejor Final Girl",
              "best_box": "Mejor película (caja)", "most_complex_killer": "Killer más complejo de reglas"}},
 "en": {"sub0": "What players think, not what the data says.", "ir": "Vote your tops ↓", "h2v": "Vote", "tab": "Tops", "pts": "pts", "rk": "1st|2nd|3rd", "sub2": "Pick up to 3 per category: 1st is worth 3 points, 2nd 2 and 3rd 1.", "h2": "Community tops",
        "sub": "What players think, not what the data says. Cast your vote: every question is optional, skip the ones you don't know.",
        "votar": "Vote", "gracias": "Thanks! Your vote counts.", "ya": "You've already voted from this browser. Here's how it stands:",
        "nada": "—", "votos": "votes", "voto": "vote", "sin": "No votes yet. Be the first.",
        "error": "Results couldn't be loaded right now.", "enviando": "Sending…",
        "q": {"easiest_box": "Easiest box", "hardest_box": "Hardest box", "most_immersive_box": "Most immersive box",
              "worst_box": "Worst box", "best_killer": "Best killer", "best_location": "Best location",
              "best_setup": "Best Setup", "best_series": "Best series", "best_final_girl": "Best Final Girl",
              "best_box": "Best movie (box)", "most_complex_killer": "Most complex killer (rules)"}},
 "fr": {"sub0": "L'avis des joueurs, pas celui des chiffres.", "ir": "Votez vos tops ↓", "h2v": "Votez", "tab": "Tops", "pts": "pts", "rk": "1er|2e|3e", "sub2": "Choisissez jusqu'à 3 par catégorie : le 1er vaut 3 points, le 2e 2 et le 3e 1.", "h2": "Tops de la communauté",
        "sub": "L'avis des joueurs, pas celui des chiffres. Votez : toutes les questions sont facultatives.",
        "votar": "Voter", "gracias": "Merci ! Votre vote compte.", "ya": "Vous avez déjà voté depuis ce navigateur. Voici les résultats :",
        "nada": "—", "votos": "votes", "voto": "vote", "sin": "Pas encore de votes. Soyez le premier.",
        "error": "Impossible de charger les résultats pour le moment.", "enviando": "Envoi…",
        "q": {"easiest_box": "Boîte la plus facile", "hardest_box": "Boîte la plus difficile", "most_immersive_box": "Boîte la plus immersive",
              "worst_box": "Pire boîte", "best_killer": "Meilleur killer", "best_location": "Meilleur lieu",
              "best_setup": "Meilleur Setup", "best_series": "Meilleure saison", "best_final_girl": "Meilleure Final Girl",
              "best_box": "Meilleur film (boîte)", "most_complex_killer": "Killer aux règles les plus complexes"}},
 "de": {"sub0": "Was die Spieler denken, nicht was die Daten sagen.", "ir": "Stimm ab ↓", "h2v": "Abstimmen", "tab": "Tops", "pts": "Pkt.", "rk": "1.|2.|3.", "sub2": "Wähle bis zu 3 pro Kategorie: Platz 1 bringt 3 Punkte, Platz 2 zwei und Platz 3 einen.", "h2": "Community-Tops",
        "sub": "Was die Spieler denken, nicht was die Daten sagen. Stimm ab: Jede Frage ist optional.",
        "votar": "Abstimmen", "gracias": "Danke! Deine Stimme zählt.", "ya": "Du hast in diesem Browser schon abgestimmt. So sieht es aus:",
        "nada": "—", "votos": "Stimmen", "voto": "Stimme", "sin": "Noch keine Stimmen. Sei die erste Stimme.",
        "error": "Die Ergebnisse konnten gerade nicht geladen werden.", "enviando": "Wird gesendet…",
        "q": {"easiest_box": "Leichteste Box", "hardest_box": "Schwerste Box", "most_immersive_box": "Atmosphärischste Box",
              "worst_box": "Schlechteste Box", "best_killer": "Bester Killer", "best_location": "Bester Schauplatz",
              "best_setup": "Bestes Setup", "best_series": "Beste Staffel", "best_final_girl": "Bestes Final Girl",
              "best_box": "Bester Film (Box)", "most_complex_killer": "Killer mit den komplexesten Regeln"}},
 "it": {"sub0": "Cosa pensano i giocatori, non cosa dicono i dati.", "ir": "Vota i tuoi top ↓", "h2v": "Vota", "tab": "Top", "pts": "pt", "rk": "1º|2º|3º", "sub2": "Scegli fino a 3 per categoria: il 1º vale 3 punti, il 2º 2 e il 3º 1.", "h2": "Top della community",
        "sub": "Cosa pensano i giocatori, non cosa dicono i dati. Vota: ogni domanda è facoltativa.",
        "votar": "Vota", "gracias": "Grazie! Il tuo voto conta.", "ya": "Hai già votato da questo browser. Ecco come va:",
        "nada": "—", "votos": "voti", "voto": "voto", "sin": "Ancora nessun voto. Sii il primo.",
        "error": "Non è stato possibile caricare i risultati ora.", "enviando": "Invio…",
        "q": {"easiest_box": "Scatola più facile", "hardest_box": "Scatola più difficile", "most_immersive_box": "Scatola più immersiva",
              "worst_box": "Scatola peggiore", "best_killer": "Miglior killer", "best_location": "Miglior ambientazione",
              "best_setup": "Miglior Setup", "best_series": "Miglior stagione", "best_final_girl": "Miglior Final Girl",
              "best_box": "Miglior film (scatola)", "most_complex_killer": "Killer con le regole più complesse"}},
}


def _opciones():
    return json.loads((AQUI / "tops_opciones.json").read_text(encoding="utf-8"))


def _imagenes():
    """Foto para cada opción: portada de la caja, arte del killer si lo hay.

    Localización y temporada no tienen foto propia: llevan la portada de su
    caja (la localización) o de la primera caja de la temporada.
    """
    import paginas
    D = paginas.datos()
    img = {}
    for f in D["films"]:
        portada = f"img/{paginas.slug(f['film'])}.jpg"
        if not (AQUI / portada).exists():
            continue
        img.setdefault(f["film"], portada)
        img.setdefault(f["loc"], portada)
        arte = f"img/art/{paginas.slug(f['killer'])}.jpg"
        img.setdefault(f["killer"], arte if (AQUI / arte).exists() else portada)
    for t in D["temporadas"]:
        if t["id"].startswith("S") and t["cajas"]:
            p = f"img/{paginas.slug(t['cajas'][0])}.jpg"
            if (AQUI / p).exists():
                img.setdefault("Series " + t["id"][1:], p)
    return img


def seccion(lang):
    t = T[lang]
    pre = "" if lang == "es" else "../"
    img = {k: pre + v for k, v in _imagenes().items()}
    cfg = {"form": FORM, "hoja": HOJA, "e": ENTRADAS, "cols": COLUMNAS, "orden": ORDEN, "p": PUNTOS,
           "o": _opciones(), "img": img, "t": t}
    return f'''
<section id="v-tops" hidden>
  <h2>{t["h2"]}</h2>
  <p class="sub">{t["sub0"]}</p>
  <a class="ct-ir" href="#ct-votar">{t["ir"]}</a>
  <div id="ct-res" class="ct-res"></div>
  <h2 id="ct-votar" class="ct-h2v">{t["h2v"]}</h2>
  <p class="sub">{t["sub2"]}</p>
  <div id="ct-form" class="ct-form"></div>
</section>
<style>
  .ct-ir {{ display:inline-block; margin:6px 0 4px; background:var(--blood); color:#fff !important; text-decoration:none;
            border-radius:3px; padding:9px 18px; font-weight:600; font-size:14px; }}
  .ct-h2v {{ margin-top:34px; scroll-margin-top:16px; }}
  .ct-res {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:14px; margin-top:16px; }}
  .ct-card {{ background:var(--surface); border:1px solid var(--line); border-top:2px solid var(--blood); border-radius:3px; padding:12px 14px; min-width:0; }}
  .ct-card h3 {{ margin:0 0 10px; font-size:15px; }}
  .ct-uno {{ position:relative; display:block; height:120px; margin:0 0 8px; border-radius:3px; overflow:hidden; background:var(--sunk); }}
  .ct-uno img {{ width:100%; height:100%; object-fit:cover; object-position:center 30%; display:block; }}
  .ct-uno span {{ position:absolute; left:0; right:0; bottom:0; padding:22px 10px 7px; font-weight:700; font-size:15px; color:#fff;
                  background:linear-gradient(transparent,rgba(0,0,0,.85)); display:flex; justify-content:space-between; gap:8px; }}
  .ct-uno span i {{ font-style:normal; font-family:var(--f-mono); font-size:12px; font-weight:400; opacity:.85; white-space:nowrap; }}
  .ct-row {{ position:relative; display:flex; align-items:center; gap:8px; padding:4px 6px; font-size:13.5px; }}
  .ct-row .b {{ position:absolute; inset:0 auto 0 0; background:color-mix(in srgb,var(--blood) 16%,transparent); border-radius:2px; }}
  .ct-row > * {{ position:relative; }}
  .ct-row img {{ width:28px; height:28px; object-fit:cover; border-radius:2px; flex:none; }}
  .ct-row .nm {{ flex:1; min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }}
  .ct-row .n {{ font-family:var(--f-mono); font-size:12px; color:var(--muted); white-space:nowrap; }}
  .ct-vacio {{ margin:0; }}
  .ct-form {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(250px,1fr)); gap:12px 14px; margin:14px 0 6px; }}
  .ct-cat {{ min-width:0; border:1px solid var(--line); border-radius:3px; padding:10px 12px 12px; display:flex; flex-direction:column; gap:6px; }}
  .ct-cat h3 {{ margin:0 0 2px; font-size:14px; }}
  .ct-cat label {{ display:flex; align-items:center; gap:8px; font-family:var(--f-mono); font-size:11px; color:var(--muted); }}
  .ct-cat label span {{ width:30px; flex:none; }}
  .ct-cat select {{ flex:1; min-width:0; width:100%; font:inherit; font-size:13.5px; padding:6px; background:var(--sunk);
                    color:var(--ink); border:1px solid var(--line); border-radius:3px; }}
  .ct-enviar {{ margin-top:6px; align-self:flex-start; background:var(--blood); color:#fff; border:0; border-radius:3px;
                padding:7px 16px; font:inherit; font-size:13px; font-weight:600; cursor:pointer; }}
  .ct-enviar[disabled] {{ opacity:.6; cursor:default; }}
  .ct-ok {{ margin:4px 0 0; font-size:12.5px; color:var(--muted); }}
</style>
<script>
(function () {{
  var C = {json.dumps(cfg, ensure_ascii=False)};
  var res = document.getElementById('ct-res'), form = document.getElementById('ct-form');
  function esc(s) {{ return String(s).replace(/[&<>"]/g, function (c) {{ return {{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]; }}); }}
  // Un voto por categoría y navegador.
  function votada(id) {{ try {{ return localStorage.getItem('fg-top-' + id) === '1'; }} catch (e) {{ return false; }} }}
  var RK = C.t.rk.split('|'), FILAS = [];
  // Baja al formulario sin tocar el #hash, que es el que elige la pestaña.
  document.querySelector('.ct-ir').onclick = function (e) {{
    e.preventDefault(); document.getElementById('ct-votar').scrollIntoView({{ behavior: 'smooth' }});
  }};

  function ranking(id) {{
    var i = C.cols.indexOf(id), pts = {{}}, votos = {{}};
    FILAS.forEach(function (f) {{
      [0, 1, 2].forEach(function (r) {{
        var v = f[i * 3 + r];
        if (v) {{ pts[v] = (pts[v] || 0) + C.p[r]; votos[v] = (votos[v] || 0) + 1; }}
      }});
    }});
    var top = Object.keys(pts).sort(function (a, b) {{ return pts[b] - pts[a] || votos[b] - votos[a]; }}).slice(0, 5);
    if (!top.length) return '<p class="sub ct-vacio">' + esc(C.t.sin) + '</p>';
    var max = pts[top[0]];
    function cifra(n) {{ return pts[n] + ' ' + C.t.pts + ' · ' + votos[n] + ' ' + (votos[n] === 1 ? C.t.voto : C.t.votos); }}
    // El primero, en grande y con su foto; el resto, en filas con miniatura.
    var h = '<div class="ct-uno">' + (C.img[top[0]] ? '<img src="' + C.img[top[0]] + '" alt="" loading="lazy">' : '') +
      '<span>' + esc(top[0]) + '<i>' + cifra(top[0]) + '</i></span></div>';
    return h + top.slice(1).map(function (n, k) {{
      return '<div class="ct-row"><i class="b" style="width:' + (pts[n] / max * 100) + '%"></i>' +
        (C.img[n] ? '<img src="' + C.img[n] + '" alt="" loading="lazy">' : '') +
        '<span class="nm">' + (k + 2) + '. ' + esc(n) + '</span><span class="n">' + cifra(n) + '</span></div>';
    }}).join('');
  }}

  function pintar() {{
    res.innerHTML = C.orden.map(function (id) {{
      return '<div class="ct-card"><h3>' + esc(C.t.q[id]) + '</h3>' + ranking(id) + '</div>';
    }}).join('');
  }}

  // El formulario se pinta una vez y no se toca al recargar resultados:
  // lo que el visitante tenga a medias no se pierde.
  form.innerHTML = C.orden.map(function (id) {{
    return '<div class="ct-cat" data-id="' + id + '"><h3>' + esc(C.t.q[id]) + '</h3>' +
      (votada(id) ? '<p class="ct-ok">' + esc(C.t.gracias) + '</p>'
        : [1, 2, 3].map(function (r) {{
            return '<label><span>' + RK[r - 1] + '</span><select data-r="' + r + '"><option value="">' + C.t.nada + '</option>' +
              C.o[id].map(function (o) {{ return '<option>' + esc(o) + '</option>'; }}).join('') + '</select></label>';
          }}).join('') + '<button type="button" class="ct-enviar">' + esc(C.t.votar) + '</button>') + '</div>';
  }}).join('');
  form.querySelectorAll('.ct-enviar').forEach(function (b) {{
    b.onclick = function () {{
      var card = b.closest('.ct-cat'), id = card.getAttribute('data-id');
      var d = new URLSearchParams(), usados = {{}}, alguno = false;
      card.querySelectorAll('select').forEach(function (sel) {{
        var v = sel.value, r = sel.getAttribute('data-r');
        if (v && !usados[v]) {{ usados[v] = 1; d.append('entry.' + C.e[id + '_' + r], v); alguno = true; }}
      }});
      if (!alguno) return;
      b.disabled = true; b.textContent = C.t.enviando;
      // no-cors: Google no deja leer la respuesta, pero el voto llega.
      fetch(C.form, {{ method: 'POST', mode: 'no-cors', body: d }}).finally(function () {{
        try {{ localStorage.setItem('fg-top-' + id, '1'); }} catch (e) {{}}
        card.innerHTML = '<h3>' + esc(C.t.q[id]) + '</h3><p class="ct-ok">' + esc(C.t.gracias) + '</p>';
        setTimeout(cargar, 2500);
      }});
    }};
  }});

  // JSONP de la API de visualización: la hoja es de solo lectura por enlace.
  var n = 0;
  function cargar() {{
    var cb = 'fgTops' + (++n);
    window[cb] = function (r) {{
      try {{
        // Sin respuestas, Google toma la cabecera por un voto: fuera.
        FILAS = (r.table.rows || []).filter(function (row) {{
          return !(row.c[1] && row.c[1].v === 'easiest_box #1');
        }}).map(function (row) {{
          return row.c.slice(1).map(function (c) {{ return c && c.v ? String(c.v) : ''; }});
        }});
        pintar();
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
