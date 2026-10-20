"""Buscador de la web: un índice por idioma (buscar.json) y la lupa en el menú.

Va al final de montar.py, cuando ya están escritas todas las páginas:
- Las guías salen directas de guias_datos.py, trozo a trozo (cada regla,
  objeto, evento e inicio con su ancla), para que "T-Rex" o "Malice" lleven
  al sitio exacto de la ficha.
- El resto de páginas se leen del HTML ya montado: título, descripción y
  cada <h2>/<h3> con id.

Los nombres de las cartas están en inglés en todas las guías (así vienen
en las cajas que tenemos). Si un día tenemos los nombres de la edición en
castellano u otra, van en ALIAS y el buscador los encuentra igual.
"""
import html as _html
import json
import pathlib
import re

import guia
import paginas
from guias_datos import GUIAS

AQUI = pathlib.Path(__file__).parent
IDIOMAS = ["es", "en", "fr", "de", "it"]

# Nombre oficial en otro idioma -> nombre de la carta en la guía.
# Solo nombres comprobados en cartas reales, nunca traducciones nuestras.
ALIAS = {}

T = {
    "es": {"k": "Guía del killer", "m": "Guía del mapa", "obj": "Objeto", "ev": "Evento",
           "ini": "Inicio", "pag": "Página", "ph": "Busca cartas, reglas, killers, objetos…",
           "nada": "Nada con eso. Prueba con el nombre en inglés de la carta.", "btn": "Buscar"},
    "en": {"k": "Killer guide", "m": "Location guide", "obj": "Item", "ev": "Event",
           "ini": "Setup", "pag": "Page", "ph": "Search cards, rules, killers, items…",
           "nada": "Nothing found.", "btn": "Search"},
    "fr": {"k": "Guide du killer", "m": "Guide du lieu", "obj": "Objet", "ev": "Événement",
           "ini": "Mise en place", "pag": "Page", "ph": "Cherchez cartes, règles, killers, objets…",
           "nada": "Rien trouvé. Essayez le nom anglais de la carte.", "btn": "Rechercher"},
    "de": {"k": "Killer-Guide", "m": "Ort-Guide", "obj": "Gegenstand", "ev": "Ereignis",
           "ini": "Aufbau", "pag": "Seite", "ph": "Karten, Regeln, Killer, Gegenstände suchen…",
           "nada": "Nichts gefunden. Versuch den englischen Kartennamen.", "btn": "Suchen"},
    "it": {"k": "Guida del killer", "m": "Guida del luogo", "obj": "Oggetto", "ev": "Evento",
           "ini": "Setup", "pag": "Pagina", "ph": "Cerca carte, regole, killer, oggetti…",
           "nada": "Niente. Prova col nome inglese della carta.", "btn": "Cerca"},
}


def _txt(s):
    return re.sub(r"\s+", " ", _html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def _corta(s, n=170):
    s = _txt(s)
    return s if len(s) <= n else s[:n].rsplit(" ", 1)[0] + "…"


def _guias(lang):
    lg = lang if lang in ("es", "en") else "en"
    t = T[lang]
    out = []
    for g in GUIAS:
        d = g[lg]
        url = paginas.slug(g["caja"]) + ".html"
        for c, nombre in (("k", g["killer"]), ("m", g["mapa"])):
            sec = f'{t[c]} · {nombre}'
            if d[f"err_{c}"]:
                out.append({"t": f'{d[f"err_{c}_t"]} ({nombre})', "c": sec,
                            "s": _corta(" ".join(d[f"err_{c}"])), "u": f'{url}#{guia.ancla(c, "ojo")}'})
            for tit, xs in d[f"bloques_{c}"]:
                out.append({"t": f"{tit} ({nombre})", "c": sec, "s": _corta(" ".join(xs)),
                            "x": _txt(" ".join(xs)), "u": f"{url}#{guia.ancla(c, tit)}"})
        for s, n, x in d["obj"]:
            out.append({"t": n, "c": f'{t["obj"]} · {g["mapa"]}', "s": _corta(x),
                        "u": f'{url}#{guia.ancla("obj", n)}'})
        for n, x in d["ev"]:
            out.append({"t": _txt(n), "c": f'{t["ev"]} · {g["mapa"]}', "s": _corta(x),
                        "u": f'{url}#{guia.ancla("ev", n)}'})
        for s, n in g["inicios"]:
            out.append({"t": n, "c": f'{t["ini"]} · {g["mapa"]}', "s": "",
                        "u": f'{url}#{guia.ancla("ini", s)}'})
    for e in out:
        a = [k for k, v in ALIAS.items() if v.lower() in e["t"].lower()]
        if a:
            e["a"] = " ".join(a)
    return out


def _paginas(carpeta, lang):
    out = []
    for f in sorted(carpeta.glob("*.html")):
        if f.name in ("404.html",) or f.name.startswith("google") or f.name.startswith("guia-"):
            continue
        h = f.read_text(encoding="utf-8")
        if 'http-equiv="refresh"' in h:
            continue
        tit = re.search(r"<title>(.*?)</title>", h, re.S)
        des = re.search(r'<meta name="description" content="([^"]*)"', h)
        tit = _txt(tit.group(1)) if tit else f.stem
        out.append({"t": tit.split(":")[0].split(" | ")[0], "c": T[lang]["pag"],
                    "s": _corta(des.group(1) if des else ""), "u": f.name})
        for m in re.finditer(r'<h2[^>]*\bid="([^"]+)"[^>]*>(.*?)</h2>', h, re.S):
            out.append({"t": _txt(m.group(2)), "c": tit.split(":")[0], "s": "",
                        "u": f"{f.name}#{m.group(1)}"})
    return out


GT = {"es": ("Mapa", "Final Girl", "victorias en", "partidas"), "en": ("Location", "Final Girl", "win rate in", "games"),
      "fr": ("Lieu", "Final Girl", "de victoires en", "parties"), "de": ("Ort", "Final Girl", "Siegquote in", "Partien"),
      "it": ("Luogo", "Final Girl", "di vittorie in", "partite")}


def _datos(lang):
    """Mapas y Final Girls no tienen página propia: llevan a su caja o a la tabla."""
    g = GT[lang]
    out = []
    cajas = {}
    for f in paginas.D["films"]:
        cajas.setdefault(f["loc"], f["film"])
    for loc, film in sorted(cajas.items()):
        out.append({"t": loc, "c": g[0], "s": film, "u": paginas.slug(film) + ".html"})
    for n, wr, pl, caja in paginas.D["girls"]:
        out.append({"t": n, "c": g[1], "s": f"{wr*100:.0f}% {g[2]} {pl} {g[3]} · {caja}",
                    "u": "index.html#girls"})
    return out


def _carpeta(lang):
    return AQUI if lang == "es" else AQUI / lang


def indices():
    for lang in IDIOMAS:
        c = _carpeta(lang)
        datos = _guias(lang) + _paginas(c, lang) + _datos(lang)
        (c / "buscar.json").write_text(json.dumps(datos, ensure_ascii=False, separators=(",", ":")),
                                       encoding="utf-8")
        print(f"{'' if lang == 'es' else lang + '/'}buscar.json  {len(datos)} entradas")


BOTON = '<button type="button" class="lupa" aria-label="{btn}" data-ph="{ph}" data-nada="{nada}">⌕</button>'
CSS = ('<style id="buscar-css">.nav-sitio .lupa{border:1px solid var(--line);background:none;color:var(--muted);'
       'font:inherit;font-size:16px;line-height:1;cursor:pointer;border-radius:3px;padding:3px 8px 5px;margin-left:auto}'
       '.nav-sitio .lupa+.mas{margin-left:0}.nav-sitio .lupa:hover{color:var(--ink);border-color:var(--muted)}'
       '.bus{position:fixed;inset:0;z-index:90;background:rgba(0,0,0,.78);display:flex;justify-content:center;align-items:flex-start;padding:8vh 16px 16px}'
       '.bus[hidden]{display:none}.bus-c{width:100%;max-width:680px;background:var(--surface);border:1px solid var(--line);'
       'border-top:2px solid var(--blood);border-radius:3px;box-shadow:0 20px 50px #000;max-height:84vh;display:flex;flex-direction:column}'
       '.bus input{font:inherit;font-size:18px;padding:14px 16px;background:none;border:0;border-bottom:1px solid var(--line);color:var(--ink);outline:0}'
       '.bus ol{list-style:none;margin:0;padding:0;overflow:auto}.bus li{border-bottom:1px solid var(--line)}'
       '.bus li a{display:block;padding:10px 16px;color:var(--ink);text-decoration:none}.bus li a:hover,.bus li a.sel{background:var(--sunk)}'
       '.bus li b{display:block;font-size:15px}.bus li i{font-style:normal;font-family:var(--f-mono);font-size:11px;letter-spacing:.06em;'
       'text-transform:uppercase;color:var(--blood)}.bus li span{display:block;font-size:13px;color:var(--muted);margin-top:2px}'
       '.bus p{margin:0;padding:14px 16px;color:var(--muted)}'
       '@media(max-width:560px){.nav-sitio .lupa{margin-left:0}}</style>')


def _poner(f, lang, pre):
    h = f.read_text(encoding="utf-8")
    if 'class="lupa"' in h or 'class="nav-sitio"' not in h:
        return False
    t = T[lang]
    b = BOTON.format(**{k: _html.escape(v, quote=True) for k, v in t.items()})
    if '<button type="button" class="mas"' in h:
        h = h.replace('<button type="button" class="mas"', b + '\n  <button type="button" class="mas"', 1)
    else:
        h = re.sub(r"(<nav class=\"nav-sitio\"[^>]*>.*?)(</nav>)", lambda m: m.group(1) + b + m.group(2), h, 1, re.S)
    h = h.replace("</head>", CSS + "</head>", 1) if "</head>" in h else CSS + h
    h = h.replace("</body>", f'<script src="{pre}buscar.js" defer></script></body>', 1)
    f.write_text(h, encoding="utf-8")
    return True


def poner():
    n = 0
    for lang in IDIOMAS:
        c = _carpeta(lang)
        for f in c.glob("*.html"):
            n += _poner(f, lang, "" if lang == "es" else "../")
    print(f"lupa en {n} páginas")


def montar():
    indices()
    poner()


if __name__ == "__main__":
    montar()
