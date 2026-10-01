#!/usr/bin/env python3
"""Monta el sitio estatico a partir del cuerpo del artifact.

El artifact de claude.ai mete el contenido en el <body>, asi que ahi las
metas no cuentan. Este script envuelve el mismo cuerpo en un documento
completo con la cabecera que necesita un buscador.

Uso:  python3 montar.py
"""
import re
import json
import pathlib
import paginas

AQUI = pathlib.Path(__file__).parent
DOMINIO = "https://carchofo.github.io/final-girl-stats"

# Interruptor de indexacion.
#   False -> la pagina se puede ver y compartir, pero se pide a los buscadores
#            que NO la indexen. Para enseñarla a quien lleva la hoja de datos
#            antes de tener su confirmacion formal.
#   True  -> indexable. Cambiar SOLO cuando haya permiso explicito, y entonces
#            dar de alta el sitemap en Search Console.
INDEXAR = False

FORM = "https://docs.google.com/forms/d/e/1FAIpQLSf8Y8_bLqYdGlhHaf1VIod8FQfCH3r9qch6LXo0oyBeCJENiw/viewform"
HOJA = "https://docs.google.com/spreadsheets/d/1xSl_BhqfVdHnYIYtuiWIIzr1BjD4ToLAYvDCWebNKGY/edit"

# Llamada a registrar partidas. Va en las DOS paginas, arriba del todo: los
# datos salen de esa hoja, asi que cuanta mas gente registre, mejores son
# las cifras que mostramos. Es la parte del trato que nos toca.
CTA = """<aside class="cta-registro">
  <p><strong>Estos datos salen de partidas que registra la gente.</strong>
     Los lleva la comunidad en una hoja abierta, y cada partida que añades
     afina las cifras de esta página.</p>
  <p><a class="cta-btn" href="{form}" target="_blank" rel="noopener">Registrar una partida</a>
     <a class="cta-alt" href="{hoja}" target="_blank" rel="noopener">Ver la hoja original</a></p>
</aside>
<style>
  .cta-registro {{ border:1px solid var(--line-hi); border-left:3px solid var(--blood);
                   background:var(--surface); padding:14px 16px; margin:18px 0 6px;
                   border-radius:3px; }}
  .cta-registro p {{ margin:0 0 10px; font-size:14px; color:var(--muted); line-height:1.55; }}
  .cta-registro p:last-child {{ margin-bottom:0; }}
  .cta-registro strong {{ color:var(--ink); font-weight:600; }}
  .cta-btn {{ display:inline-block; background:var(--blood); color:#fff; text-decoration:none;
              padding:7px 14px; border-radius:3px; font-size:13px; font-weight:600;
              letter-spacing:.03em; }}
  .cta-btn:hover {{ filter:brightness(1.1); }}
  .cta-alt {{ display:inline-block; margin-left:12px; color:var(--muted); font-size:13px; }}
  .cta-alt:hover {{ color:var(--ink); }}
</style>
"""

ENLACES = {
    "https://claude.ai/artifact/9citaKuByjhsDA5S1qit6y": "salidas.html",
    "https://claude.ai/artifact/BEA6n9fvejJWTBwwzn75dp": "index.html",
}

NAV = """<nav class="nav-sitio" aria-label="Secciones">
  <a href="index.html"{act_index}>Estadísticas</a>
  <a href="salidas.html"{act_salidas}>Salidas</a>
  <a href="fichas.html"{act_fichas}>Fichas</a>
</nav>
<style>
  .nav-sitio {{ display:flex; gap:18px; padding:14px 0 2px; font-size:13px;
                letter-spacing:.06em; text-transform:uppercase; }}
  .nav-sitio a {{ color:var(--muted); text-decoration:none; padding-bottom:4px;
                  border-bottom:2px solid transparent; }}
  .nav-sitio a:hover {{ color:var(--ink); }}
  .nav-sitio a[aria-current] {{ color:var(--blood); border-color:var(--blood); }}
</style>
"""

# La estrategias de salida viene del artifact anterior al rediseño: tema claro,
# Big Shoulders y Newsreader. La de estadisticas es oscura con Jost. Dos
# paginas del mismo sitio no pueden verse de dos sitios distintos.
#
# Se arregla al montar, no editando el cuerpo, para que siga siendo un
# export limpio del artifact y se pueda volver a exportar sin perder esto.
#
# El selector repite las tres formas que usa el cuerpo original porque
# ":root:not([data-theme=light])" pesa mas que ":root" a secas: con un
# ":root" normal, las reglas del modo oscuro de abajo seguirian ganando.
UNIFICAR_ESTILO = """
<style>
  /* Identidad unica del sitio, aplicada sobre el tema antiguo. */
  :root,
  :root:not([data-theme="light"]),
  :root[data-theme="dark"] {
    color-scheme: dark;
    --paper:#0b0a0b; --surface:#151315; --sunk:#1d1a1d; --ink:#f2ecec;
    --muted:#9c8f93; --line:#262227; --line-hi:#3a333a;
    --blood:#e0454f; --blood-s:#2a1216; --mid:#3a3438;
    --verde:#4caf7d; --ambar:#d7a43a; --rojo:#e0454f;
    --glow:rgba(224,69,79,.30);
    --shadow:0 1px 2px rgba(0,0,0,.6), 0 10px 34px rgba(0,0,0,.45);
    --f-disp:"Jost","Futura","Century Gothic",sans-serif;
    --f-body:"Jost","Futura","Century Gothic",Helvetica,sans-serif;
    --f-mono:"IBM Plex Mono",ui-monospace,Menlo,monospace;
  }
  body { background:var(--paper); color:var(--ink); font-family:var(--f-body); }
  /* El cuerpo viejo da por hecho fondo claro en algunos sitios. */
  table, th, td { border-color:var(--line); }
  th { background:var(--sunk); color:var(--ink); }
</style>
"""

PAGINAS = [
    {
        "fuente": "src/cuerpo.html",
        "salida": "index.html",
        "title": "Estadísticas de Final Girl: 13.873 partidas reales",
        # Google corta la descripcion sobre los 155 caracteres: lo que
        # importa va delante.
        "desc": (
            "Victorias de cada killer en cada mapa de Final Girl, sobre 13.873 "
            "partidas de la comunidad. Qué caja es más dura y dónde pierde cada asesino."
        ),
        "img": "img/vhs-final-girl.jpg",
        "ogtitle": "La página que todo fan de Final Girl necesitaba",
        "ogdesc": "13.873 partidas reales de la comunidad: qué killer castiga en qué mapa, qué caja es más dura y cómo salir en el turno 1.",
        "prioridad": "1.0",
        "act_index": ' aria-current="page"',
        "act_salidas": "", "act_fichas": "",
        "reemplazos": {
            "<h1>Laboratorio<span class=\"roja\">Final Girl</span></h1>":
                "<h1>Estadísticas<span class=\"roja\">Final Girl</span></h1>",
        },
    },
    {
        "fuente": "src/salidas-cuerpo.html",
        "salida": "salidas.html",
        "title": "Salidas de Final Girl: las 4 aperturas y cuándo usar cada una",
        "desc": (
            "Las 4 aperturas de Final Girl turno a turno: cuál usar según tengas "
            "armas a la vista o víctimas cerca, dados y errores de reglas comunes."
        ),
        "img": "img/the-happy-trails-horror.jpg",
        "prioridad": "0.8",
        "act_index": "",
        "act_salidas": ' aria-current="page"', "act_fichas": "",
        "unificar_estilo": True,
    },
]

CABECERA = """<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0b0a0b">
<meta name="robots" content="{robots}">

<!-- Open Graph: lo que se ve al pegar el enlace en Reddit, Discord o BGG.
     Es de donde va a venir casi todo el trafico al principio, mucho antes
     que de Google. -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="La página que todo fan de Final Girl necesitaba">
<meta property="og:locale" content="es_ES">
<meta property="og:title" content="{ogtitle}">
<meta property="og:description" content="{ogdesc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{imgurl}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{ogtitle}">
<meta name="twitter:description" content="{ogdesc}">
<meta name="twitter:image" content="{imgurl}">

<script type="application/ld+json">{jsonld}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jost:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,300;1,500&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 16 16'><text y='13' font-size='13'>&#128373;</text></svg>">
</head>
<body>
"""

PIE = "\n</body>\n</html>\n"


def estilos():
    """El CSS vive dentro de cuerpo.html. Las páginas generadas lo reutilizan
    tal cual: duplicarlo a mano sería otra copia que mantener sincronizada,
    que es la enfermedad que este proyecto ya ha tenido una vez."""
    s = (AQUI / "src" / "cuerpo.html").read_text()
    bloques = re.findall(r"<style>.*?</style>", s, re.S)
    return "\n".join(bloques)


def datos():
    s = (AQUI / "src" / "cuerpo.html").read_text()
    m = re.search(r"var D = (\{.*?\});\n", s, re.S)
    return json.loads(m.group(1))


D = datos()
META = D["meta"]


def jsonld_de(pagina, url):
    """Datos estructurados: le dice al buscador que esto es un conjunto de
    datos con fuente y fecha, no un blog cualquiera."""
    base = {
        "@context": "https://schema.org",
        "@type": "Dataset",
        "name": pagina["title"],
        "description": pagina["desc"],
        "url": url,
        "inLanguage": "es",
        "keywords": ["Final Girl", "board game", "solo", "win rate", "estadísticas"],
        "temporalCoverage": f"../{META['last']}",
        "variableMeasured": "Porcentaje de victoria",
        "measurementTechnique": "Partidas registradas por jugadores",
        "distribution": {"@type": "DataDownload", "encodingFormat": "text/html", "contentUrl": url},
        "about": {
            "@type": "Game",
            "name": "Final Girl",
            "gamePlatform": "Juego de mesa",
            "numberOfPlayers": {"@type": "QuantitativeValue", "value": 1},
        },
        "size": f"{META['total']} partidas",
    }
    return json.dumps(base, ensure_ascii=False, separators=(",", ":"))


for p in PAGINAS:
    url = f"{DOMINIO}/{p['salida']}" if p["salida"] != "index.html" else f"{DOMINIO}/"
    cuerpo = (AQUI / p["fuente"]).read_text()
    # El cuerpo viene del artifact, que lleva su propio <title> porque alli
    # va dentro del <body>. Aqui ya hay uno en el <head>: dejar los dos
    # confunde al buscador sobre cual es el bueno.
    cuerpo = re.sub(r"^\s*<title>.*?</title>\s*", "", cuerpo, count=1, flags=re.S)

    # Los enlaces entre las dos paginas apuntaban al artifact de claude.ai:
    # en el sitio tienen que quedarse dentro. Ademas de ser lo correcto para
    # el visitante, los enlaces internos son como el buscador entiende que
    # las dos paginas son del mismo sitio y se refuerzan.
    for viejo, nuevo in ENLACES.items():
        cuerpo = cuerpo.replace(viejo, nuevo)

    # El pie citaba la fuente sin enlazarla. Si usas los datos de alguien,
    # el enlace es lo minimo, y ademas invita a registrar partidas desde
    # el unico sitio donde todo el mundo llega al final: abajo del todo.
    cuerpo = cuerpo.replace(
        "<p>Fuente: hoja pública de seguimiento de la comunidad de Final Girl,",
        f'<p>Fuente: <a href="{HOJA}" target="_blank" rel="noopener">hoja pública de '
        f'seguimiento</a> de la comunidad de Final Girl, mantenida por sus jugadores '
        f'(<a href="{FORM}" target="_blank" rel="noopener">registra las tuyas</a>),',
        1,
    )

    # El <h1> manda mas que el <title> para entender de que va la pagina.
    # "Laboratorio Final Girl" no lo busca nadie.
    for viejo, nuevo in p.get("reemplazos", {}).items():
        cuerpo = cuerpo.replace(viejo, nuevo)

    # Barra de navegacion: dos paginas sueltas sin enlaces entre si valen
    # menos que dos enlazadas, y al visitante le hace falta igual.
    # El cuerpo de salidas ya trae su propia barra (se añadió al artifact,
    # que no pasa por aquí). Meter otra dejaba dos seguidas.
    if "nav-sitio" not in cuerpo:
        for ancla in ('<header class="hero">', '<header class="top">'):
            if ancla in cuerpo:
                cuerpo = cuerpo.replace(ancla, NAV.format(**p) + ancla, 1)
                break
    # El aviso de registro ya NO va arriba de cada página: quien llega
    # buscando consejos se comía una petición antes de leer nada, y repetida
    # en 50 páginas se lee como insistencia. Queda solo en el pie, donde se
    # ha ganado el derecho a pedir.

    if p.get("unificar_estilo"):
        # DESPUES del cuerpo: a igual especificidad gana la ultima regla, y
        # el cuerpo trae las suyas.
        cuerpo = cuerpo + UNIFICAR_ESTILO
    html = CABECERA.format(
        title=p["title"],
        desc=p["desc"],
        url=url,
        imgurl=f"{DOMINIO}/{p['img']}",
        ogtitle=p.get("ogtitle", p["title"]),
        ogdesc=p.get("ogdesc", p["desc"]),
        jsonld=jsonld_de(p, url),
        robots="index,follow,max-image-preview:large" if INDEXAR
               else "noindex,nofollow",
    ) + cuerpo + PIE
    (AQUI / p["salida"]).write_text(html)
    print(f"{p['salida']}  {len(html)//1024} KB")

# --- páginas por killer y por caja -----------------------------------------
# Una URL solo posiciona para una cosa. Las búsquedas son concretas
# ("consejos Hans Final Girl"), así que cada killer y cada caja necesita su
# propia página, con el texto en el HTML y no pintado por JavaScript.
# El CSS a un fichero aparte: repetido en 47 páginas son 1,6 MB y el
# navegador lo baja una vez por página. En un .css lo baja una sola vez y
# lo cachea para todas.
CSS = estilos()
(AQUI / "estilos.css").write_text(
    re.sub(r"</?style>", "", CSS))
print("estilos.css")

generadas = paginas.generar()
for g in generadas:
    url = f"{DOMINIO}/{g['salida']}"
    cuerpo = (
        NAV.format(act_index="", act_salidas="", act_fichas="")
        + '<div class="wrap"><header class="top">'
        + g["cuerpo"].split("</h1>", 1)[0] + "</h1>"
        + (g["cuerpo"].split("</h1>", 1)[1] if "</h1>" in g["cuerpo"] else "")
        + '<footer><p>Datos de la <a href="' + HOJA + '" target="_blank" rel="noopener">hoja '
          'pública de seguimiento</a> de la comunidad de Final Girl '
          '(<a href="' + FORM + '" target="_blank" rel="noopener">registra tus partidas</a>). '
          'Vuelve a <a href="index.html">todas las estadísticas</a>.</p></footer>'
        + "</div>"
    )
    html = CABECERA.format(
        title=g["title"], desc=g["desc"], url=url,
        imgurl=f"{DOMINIO}/{g.get('img') or 'img/vhs-final-girl.jpg'}",
        ogtitle=g["title"],
        ogdesc=g["desc"],
        jsonld=jsonld_de(g, url),
        robots="index,follow,max-image-preview:large" if INDEXAR else "noindex,nofollow",
    ).replace("</head>", '<link rel="stylesheet" href="estilos.css"></head>') + cuerpo + PIE
    (AQUI / g["salida"]).write_text(html)
print(f"{len(generadas)} páginas de killer y caja")

# --- índice de fichas ------------------------------------------------------
# Sin esto las 47 páginas quedan huérfanas: nadie llega a ellas y un
# buscador tampoco, porque no hay ningún enlace que seguir. El sitemap las
# declara, pero los enlaces internos son lo que de verdad las sostiene.
def enlaces(tipo, titulo, nota):
    items = [g for g in generadas if g["tipo"] == tipo]
    items.sort(key=lambda g: g["title"])
    li = "".join(
        f'<li><a href="{g["salida"]}">{g["title"].split(":")[0].split(" en Final Girl")[0]}</a></li>'
        for g in items)
    return f'<h2>{titulo}</h2><p class="sub">{nota}</p><ul class="indice">{li}</ul>'

fichas = (
    NAV.format(act_index="", act_salidas="", act_fichas="")
    + '<div class="wrap"><header class="top">'
      '<p class="eyebrow">Índice · ' + str(len(generadas)) + ' fichas</p>'
      '<h1>Todas las<span class="roja">fichas</span></h1>'
      '<p class="dek">Una página por killer y por caja, con sus porcentajes de victoria, '
      'sus cartas más duras y los consejos de quien las ha jugado.</p></header>'
    + enlaces("killer", "Killers", "Dónde gana y dónde pierde cada uno, y qué Dark Powers y Finales castigan más.")
    + enlaces("caja", "Cajas", "Cada caja con su killer y su mapa, hojas de preparación y qué tiene de particular.")
    + '<footer><p>Vuelve a <a href="index.html">todas las estadísticas</a> '
      'o a la <a href="salidas.html">estrategias de salida</a>.</p></footer></div>'
    + '''<style>
  .indice { list-style:none; margin:0 0 26px; padding:0;
            display:grid; grid-template-columns:repeat(auto-fill,minmax(240px,1fr)); gap:1px;
            background:var(--line); border:1px solid var(--line); border-radius:3px; overflow:hidden; }
  .indice li { background:var(--surface); }
  .indice a { display:block; padding:11px 14px; color:var(--ink); text-decoration:none; font-size:14.5px; }
  .indice a:hover { background:var(--blood-s); color:var(--blood); }
</style>'''
)
url_fichas = f"{DOMINIO}/fichas.html"
(AQUI / "fichas.html").write_text(
    CABECERA.format(
        title="Fichas de Final Girl: todos los killers y todas las cajas",
        desc="Una página por cada killer y cada caja de Final Girl, con victorias por mapa, cartas más duras y consejos.",
        url=url_fichas, imgurl=f"{DOMINIO}/img/vhs-final-girl.jpg",
        ogtitle="Fichas de Final Girl: todos los killers y todas las cajas",
        ogdesc="Una página por cada killer y cada caja, con victorias por mapa y consejos.",
        jsonld=jsonld_de({"title": "Fichas de Final Girl", "desc": "Índice de killers y cajas."}, url_fichas),
        robots="index,follow,max-image-preview:large" if INDEXAR else "noindex,nofollow",
    ).replace("</head>", '<link rel="stylesheet" href="estilos.css"></head>') + fichas + PIE)
print("fichas.html (índice de las", len(generadas), "páginas)")

PAGINAS += [{"salida": "fichas.html", "prioridad": "0.9"}]
PAGINAS += [{"salida": g["salida"], "prioridad": g["prioridad"]} for g in generadas]

# --- borrador de registro de partidas --------------------------------------
# Pagina a proposito SUELTA: no entra en la navegacion, ni en fichas.html,
# ni en el sitemap, y lleva noindex pase lo que pase. Existe solo para
# enseñarsela a quien lleva la hoja por enlace directo. Si dicen que no,
# se borra el fichero y no lo vio nadie.
#
# No escribe en su hoja: construye un enlace prerrellenado de Google Forms,
# que es una funcion publica del propio formulario. Nada entra hasta que una
# persona pulsa Submit alli.
plantilla = (AQUI / "registrar_plantilla.html").read_text()
campos = json.loads((AQUI / "fg_form.json").read_text())
parejas = {f["killer"]: f["loc"] for f in D["films"]}
plantilla = plantilla.replace("__FORMJSON__", json.dumps(campos, ensure_ascii=False))
plantilla = plantilla.replace(
    "var FORM =",
    "var PAREJAS = " + json.dumps(parejas, ensure_ascii=False) + ";\n  var FORM =")

url_reg = f"{DOMINIO}/registrar.html"
(AQUI / "registrar.html").write_text(
    CABECERA.format(
        title="Registrar una partida de Final Girl",
        desc="Atajo para registrar una partida en la hoja comunitaria: cinco campos en vez de ciento ochenta y nueve.",
        url=url_reg, imgurl=f"{DOMINIO}/img/vhs-final-girl.jpg",
        ogtitle="Registrar una partida de Final Girl",
        ogdesc="Cinco campos en vez de ciento ochenta y nueve.",
        jsonld=jsonld_de({"title": "Registrar una partida", "desc": "Borrador."}, url_reg),
        robots="noindex,nofollow",   # siempre, aunque el resto se indexe
    ).replace("</head>", '<link rel="stylesheet" href="estilos.css"></head>')
    + NAV.format(act_index="", act_salidas="", act_fichas="")
    + plantilla + PIE)
print("registrar.html  (suelto: sin enlaces, sin sitemap, noindex fijo)")

# --- sitemap y robots -----------------------------------------------------
urls = "".join(
    f"<url><loc>{DOMINIO}/{'' if p['salida']=='index.html' else p['salida']}</loc>"
    f"<priority>{p['prioridad']}</priority></url>"
    for p in PAGINAS
)
if INDEXAR:
    (AQUI / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n'
    )
    (AQUI / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {DOMINIO}/sitemap.xml\n")
    print("sitemap.xml y robots.txt  -- INDEXABLE")
else:
    # Dos capas: robots.txt pide no rastrear, y cada pagina lleva noindex por
    # si llegan por un enlace directo sin pasar por robots.txt.
    (AQUI / "sitemap.xml").unlink(missing_ok=True)
    (AQUI / "robots.txt").write_text("User-agent: *\nDisallow: /\n")
    print("robots.txt  -- NO INDEXABLE (INDEXAR = False)")
    print("   La pagina se ve y se comparte, pero no entra en Google.")
    print("   Pon INDEXAR = True cuando tengas el permiso por escrito.")
