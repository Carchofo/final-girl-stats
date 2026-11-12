#!/usr/bin/env python3
"""Genera una página por killer y por caja a partir de los datos.

Por qué existe: la web vivía en dos URL, y una URL solo puede posicionar
para una cosa. Las búsquedas reales son concretas ("consejos Hans Final
Girl", "cómo ganar Carnival of Blood"), así que hace falta una página por
cada una, con texto de verdad en el HTML y no pintado por JavaScript.

Los datos ya están estructurados: esto solo los convierte en prosa.

Uso:  python3 paginas.py     (lo llama montar.py)
"""
import json
import pathlib

import mecanicas
import re
import unicodedata

AQUI = pathlib.Path(__file__).parent
# --- Afiliados -------------------------------------------------------------
# Vacío = no se pinta nada. Pon tu identificador y aparecen los enlaces.
#
# Son enlaces de BÚSQUEDA por nombre, no a fichas de producto concretas:
# una ficha cambia de URL o desaparece y te quedas con enlaces rotos en 22
# páginas sin enterarte. Una búsqueda por el nombre de la caja aguanta.
AFILIADOS = {
    # Amazon tiene un programa y un identificador POR PAIS: el tag de
    # amazon.es no cobra nada en amazon.com. Hay que darse de alta en cada
    # uno que interese. Rellena solo los que tengas; los vacios no se pintan.
    "amazon": {
        "nombre": "Amazon",
        "url": "https://www.{dom}/s?k={q}&tag={tag}",
        "tags": {
            "ES": {"dom": "amazon.es",    "tag": "finalgirlst06-21"},
            "US": {"dom": "amazon.com",   "tag": "finalgirlstat-20"},
            "GB": {"dom": "amazon.co.uk", "tag": "finalgirlstat-21"},
            "DE": {"dom": "amazon.de",    "tag": "finalgirlst03-21"},
            "FR": {"dom": "amazon.fr",    "tag": "finalgirlst02-21"},
            "IT": {"dom": "amazon.it",    "tag": "finalgirlst0e-21"},
            "CA": {"dom": "amazon.ca",    "tag": "finalgirlst08-20"},
            "MX": {"dom": "amazon.com.mx","tag": ""},
            "AU": {"dom": "amazon.com.au","tag": ""},
        },
    },
    # Tiendas de un solo pais. Solo se pintan a quien vive donde envian:
    # ensenar una tienda espanola a alguien de Ohio es ruido.
    # "zacatrus": {"nombre": "Zacatrus", "paises": ["ES"],
    #              "url": "https://zacatrus.es/catalogsearch/result/?q={q}&acc={tag}",
    #              "tag": ""},
}

# A quien se le ensena el enlace de Amazon cuando no sabemos de donde es.
PAIS_POR_DEFECTO = "US"

MIN_CELDA = 20          # partidas mínimas para citar una combinación
MIN_SECCION = 20        # ídem para Dark Powers y Finales


def slug(t):
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode()
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', t.lower())).strip('-')


def pc(x, dec=1):
    return f"{x*100:.{dec}f}".replace('.', ',') + '%'


def datos():
    s = (AQUI / 'src' / 'cuerpo.html').read_text(encoding="utf-8")
    return json.loads(re.search(r'var D = (\{.*?\});\n', s, re.S).group(1))


def descripciones():
    """Quien es cada killer y como juega. Los datos de juego salen de la
    Final Girl Wiki (CC BY-SA): el texto es nuestro, los hechos son suyos,
    y por eso cada ficha la enlaza."""
    f = AQUI / 'killers_desc.json'
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}


DESC = descripciones()
D = datos()
FILMS = {f['film']: f for f in D['films']}
KILLERS = D['killers']
CELLS = D['cells']
LOCS = dict((l[0], (l[1], l[2])) for l in D['locs'])
CONSEJOS = D['consejos']
MEDIA = D['meta']['wr']


def mapas_de(killer):
    """Mapas donde ese killer tiene muestra suficiente, de mejor a peor."""
    r = [(loc, c[1], c[0]) for loc, d in CELLS.items()
         for k, c in d.items() if k == killer and c[0] >= MIN_CELDA]
    return sorted(r, key=lambda x: -x[1])


TIENDA_T = {
    "es": ("Dónde conseguirla", "Enlaces de afiliado: si compras, a mí me llega una comisión y a ti te cuesta lo mismo. No cambian lo que dicen los datos de arriba."),
    "en": ("Where to get it", "Affiliate links: if you buy, I get a small commission at no extra cost to you. It doesn't change what the data above says."),
    "fr": ("Où la trouver", "Liens affiliés : si vous achetez, je touche une petite commission, sans surcoût pour vous. Cela ne change rien aux données ci-dessus."),
    "de": ("Wo man sie bekommt", "Affiliate-Links: Wenn du kaufst, bekomme ich eine kleine Provision, für dich ohne Mehrkosten. An den Daten oben ändert das nichts."),
    "it": ("Dove trovarla", "Link di affiliazione: se compri, ricevo una piccola commissione senza costi in più per te. Non cambia quello che dicono i dati sopra."),
}


def bloque_tienda(nombre, lang="es"):
    """Enlaces de compra, solo si hay algún afiliado configurado.

    Geolocalizado en el navegador: cada país tiene su Amazon y su tag, y
    el tag de amazon.es no cobra nada en amazon.com. Se decide por la zona
    horaria del visitante, que ya está en su equipo. No se llama a ningún
    servicio de geolocalización: eso sería una petición a un tercero, con
    su rastreo y su aviso de cookies, para acertar un país.

    Sin JavaScript queda el enlace por defecto, que funciona igual.

    El aviso de que son enlaces de afiliado va SIEMPRE y antes de los
    enlaces, no escondido en el pie: el sitio se sostiene sobre datos
    que presta la comunidad, y ahí no se juega con la confianza.
    """
    import json
    import urllib.parse
    q = urllib.parse.quote_plus("Final Girl " + nombre)

    enlaces = []
    for a in AFILIADOS.values():
        if a.get("tags"):                      # multipaís (Amazon)
            porpais = {p: a["url"].format(dom=v["dom"], q=q, tag=v["tag"])
                       for p, v in a["tags"].items() if v.get("tag")}
            if not porpais:
                continue
            defecto = porpais.get(PAIS_POR_DEFECTO) or list(porpais.values())[0]
            enlaces.append(
                f'<a class="tienda" href="{defecto}" data-geo=\'{json.dumps(porpais)}\' '
                f'target="_blank" rel="noopener sponsored nofollow">{a["nombre"]}</a>')
        elif a.get("tag"):                     # un solo país
            url = a["url"].format(q=q, tag=a["tag"])
            paises = json.dumps(a.get("paises") or [])
            enlaces.append(
                f'<a class="tienda" href="{url}" data-solo=\'{paises}\' hidden '
                f'target="_blank" rel="noopener sponsored nofollow">{a["nombre"]}</a>')

    if not enlaces:
        return ""

    h2, aviso = TIENDA_T.get(lang, TIENDA_T["es"])
    return (f'<h2>{h2}</h2>'
            f'<div class="aviso"><p class="sub" style="margin-bottom:10px">{aviso}</p>'
            f'<p>{" ".join(enlaces)}</p></div>' + JS_GEO)


# Tabla zona horaria -> pais. Corta a proposito: cubre los paises donde
# hay programa de afiliados, y el resto cae en el por defecto.
JS_GEO = """<script>
(function () {
  var ZONAS = {
    'Europe/Madrid':'ES','Atlantic/Canary':'ES','Africa/Ceuta':'ES',
    'Europe/London':'GB','Europe/Dublin':'GB',
    'Europe/Berlin':'DE','Europe/Vienna':'DE','Europe/Zurich':'DE',
    'Europe/Paris':'FR','Europe/Brussels':'FR',
    'Europe/Rome':'IT','Europe/Malta':'IT',
    'America/Mexico_City':'MX','America/Monterrey':'MX','America/Tijuana':'MX',
    'America/Toronto':'CA','America/Vancouver':'CA','America/Edmonton':'CA',
    'America/Winnipeg':'CA','America/Halifax':'CA','America/Montreal':'CA'
  };
  var pais = null;
  try {
    var tz = Intl.DateTimeFormat().resolvedOptions().timeZone || '';
    pais = ZONAS[tz] || (tz.indexOf('Australia/') === 0 ? 'AU'
                      : (tz.indexOf('America/') === 0 ? 'US' : null));
  } catch (e) {}

  document.querySelectorAll('a.tienda[data-geo]').forEach(function (a) {
    try {
      var m = JSON.parse(a.getAttribute('data-geo'));
      if (pais && m[pais]) a.href = m[pais];
    } catch (e) {}
  });
  // Tiendas de un solo pais: ocultas salvo que el visitante viva alli.
  document.querySelectorAll('a.tienda[data-solo]').forEach(function (a) {
    try {
      var p = JSON.parse(a.getAttribute('data-solo'));
      if (pais && p.indexOf(pais) !== -1) a.hidden = false;
    } catch (e) {}
  });
})();
</script>"""


def tabla(cab, filas):
    if not filas:
        return ''
    th = ''.join(f'<th{" class=n" if i else ""}>{c}</th>' for i, c in enumerate(cab))
    tr = ''.join(
        '<tr>' + ''.join(f'<td{" class=n" if i else ""}>{c}</td>' for i, c in enumerate(f)) + '</tr>'
        for f in filas)
    return f'<div class="tabla-wrap"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


def arte_ficha(ruta, pre="", alt=""):
    """Ilustración arriba a la derecha de la ficha (killer: su arte; caja: la portada),
    montada como una diapositiva de 35 mm."""
    if not (AQUI / ruta).exists():
        return ""
    # Portadas: el logo arriba, la cara abajo. Arte de killer: centrado arriba.
    pos = "center 25%" if "/art/" in ruta else "center 70%"
    if "/loc/" in ruta:  # logos de mapa: enteros, sobre fondo oscuro
        pos = "center;object-fit:contain;background:#0d0a0b;padding:10px;box-sizing:border-box"
    return ('<style>header.top{display:flow-root}'
            '.diapo{float:right;position:relative;width:min(34%,230px);margin:0 0 8px 18px;padding:16px 16px 24px;box-sizing:border-box;'
            'background:linear-gradient(145deg,#efe9dc,#d6cfbf);border-radius:6px;transform:rotate(2deg);'
            'box-shadow:0 14px 30px rgba(0,0,0,.65),0 2px 0 rgba(255,255,255,.35) inset,0 -2px 0 rgba(0,0,0,.15) inset}'
            '.diapo img{display:block;width:100%;aspect-ratio:1;object-fit:cover;border-radius:7px}'
            '.diapo::after{content:"";position:absolute;inset:16px 16px 24px;border-radius:7px;pointer-events:none;'
            'box-shadow:0 0 0 1px rgba(0,0,0,.35),inset 0 0 28px rgba(0,0,0,.75)}'
            '.diapo::before{content:"FINALGIRLSTATS";position:absolute;left:0;right:0;bottom:8px;text-align:center;'
            'font:700 8px/1 var(--f-mono),monospace;letter-spacing:.25em;color:#8a8170}</style>'
            '<span class="diapo"><img class="ficha-arte" src="' + pre + ruta + '" alt="' + alt.replace('"', '&quot;') + '" style="object-position:' + pos + '"></span>')


# --------------------------------------------------------------------------
# Páginas de killer
# --------------------------------------------------------------------------
def pagina_killer(nombre, k):
    mapas = mapas_de(nombre)
    caja = k.get('box')
    f = FILMS.get(caja)
    propio = f['loc'] if f else None
    aqui = next((m for m in mapas if m[0] == propio), None)

    h = [arte_ficha(f"img/art/{slug(nombre)}.jpg", alt=nombre),
         f'<p class="eyebrow">Killer · {len(mapas)} mapas con datos</p>',
         f'<h1 data-caja="{caja or ""}">{nombre}<span class="roja">{pc(k["wr"])} de victorias</span></h1>']
    import guia
    g = guia.por_killer(nombre)
    if g:
        h.append(f'<p class="gu-link" style="font-weight:700">📖 <a href="{slug(g["caja"])}.html#{guia.ANCLA["k"]}" style="color:var(--blood)">Guía de {nombre}: cómo juega y errores frecuentes →</a></p>')

    intro = (f'Sobre <b>{k["g"]} partidas</b> registradas, la Final Girl gana el '
             f'{pc(k["wr"])} de las veces contra {nombre}. '
             f'La media de todo el juego es {pc(MEDIA)}, así que ')
    dif = (k['wr'] - MEDIA) * 100
    intro += ('está por encima: es de los killers que menos problemas da.'
              if dif > 4 else
              'está por debajo: es de los duros.' if dif < -4 else
              'queda justo en la media.')
    h.append(f'<p class="dek">{intro}</p>')

    d = DESC.get(nombre)
    if d and d.get('q'):
        h.append('<h2>Quién es</h2>')
        h.append(f'<p>{d["q"]}</p>')
        if d.get('j'):
            h.append('<h3>Cómo juega</h3>')
            h.append(f'<p>{d["j"]}</p>')
        if d.get('wiki'):
            u = 'https://finalgirl.fandom.com/wiki/' + d['wiki'].replace(' ', '_')
            h.append(f'<p class="sub">Datos de juego tomados de la '
                     f'<a href="{u}" target="_blank" rel="noopener">Final Girl Wiki</a>, '
                     f'bajo licencia CC BY-SA.</p>')

    h.append(mecanicas.killer(nombre, 'es'))
    h.append(guia.fase_html('es', g, h='h2'))

    if caja:
        h.append(f'<p>Viene en la caja <a href="{slug(caja)}.html"><b>{caja}</b></a>'
                 + (f', emparejado con <b>{propio}</b>.' if propio else '.') + '</p>')

    # El dato que de verdad dice algo: su mapa contra su media.
    if aqui and len(mapas) >= 2:
        d = (aqui[1] - k['wr']) * 100
        if abs(d) >= 4:
            peor = mapas[-1]
            mejor = mapas[0]
            h.append('<div class="aviso"><h3>El mapa cambia la pelea</h3>'
                     f'<p>En {propio}, su localización de caja, gana el <b>{pc(aqui[1])}</b>, '
                     f'frente al {pc(k["wr"])} que saca repartido por todos los mapas: '
                     f'<b>{"+" if d>0 else ""}{d:.1f}'.replace('.', ',') + ' puntos</b>. '
                     + ('El mapa juega a tu favor, no al suyo.' if d > 0
                        else 'Esa localización le sienta bien: no te confíes por su media.')
                     + f' Donde más gana es {mejor[0]} ({pc(mejor[1])}) y donde menos, '
                       f'{peor[0]} ({pc(peor[1])}).</p></div>')

    if len(mapas) >= 2:
        h.append('<h2>Dónde gana y dónde pierde</h2>')
        h.append('<p class="sub">Porcentaje de victoria de la Final Girl en cada localización, '
                 f'con al menos {MIN_CELDA} partidas registradas.</p>')
        h.append(tabla(['Localización', 'Victorias', 'Partidas'],
                       [[m[0], pc(m[1]), m[2]] for m in mapas]))

    for titulo, clave in (('Dark Powers', 'Dark Power'), ('Cartas de Finale', 'Finale')):
        filas = [x for x in k.get('secs', {}).get(clave, []) if x[2] >= MIN_SECCION]
        if len(filas) >= 2:
            filas.sort(key=lambda x: x[1])
            h.append(f'<h2>{titulo}</h2>')
            h.append(f'<p class="sub">De la que más castiga a la que menos. '
                     f'Mínimo {MIN_SECCION} partidas.</p>')
            h.append(tabla([titulo[:-1] if titulo.endswith('s') else titulo, 'Victorias', 'Partidas'],
                           [[x[0], pc(x[1]), x[2]] for x in filas]))
            peor = filas[0]
            h.append(f'<p>La peor papeleta es <b>{peor[0]}</b>: con ella encima la partida se gana '
                     f'solo el {pc(peor[1])} de las veces, sobre {peor[2]} partidas.</p>')

    # La ficha del killer tambien vende: quien llega buscando "como ganar a
    # Hans" muchas veces no tiene la caja. Se enlaza la suya, no el killer.
    if caja:
        h.append(bloque_tienda(caja))

    c = CONSEJOS.get(caja or '', {})
    if c.get('foro'):
        h.append('<h2>Qué dice quien lo ha jugado</h2>')
        h.append(f'<div class="aviso"><p>{c["foro"]}</p></div>')

    h.append('<h2>Cómo salir contra él</h2>')
    h.append('<p>Las cuatro aperturas y cuándo usar cada una están en la '
             '<a href="salidas.html">estrategias de salida</a>. '
             'Para cruzar a este killer con cualquier otro mapa, la matriz completa está en '
             '<a href="index.html">las estadísticas</a>.</p>')

    titulo = f'{nombre} en Final Girl (juego de mesa): victorias por mapa y cómo ganarle'
    desc = (f'La Final Girl gana el {pc(k["wr"])} contra {nombre} sobre {k["g"]} partidas. '
            f'Dónde le va mejor y peor, sus Dark Powers y Finales más duros, y consejos.')
    return titulo, desc[:155], '\n'.join(h)


# --------------------------------------------------------------------------
# Páginas de caja
# --------------------------------------------------------------------------
MESA_T = {'es': 'En nuestra mesa', 'en': 'At our table', 'fr': 'À notre table', 'de': 'An unserem Tisch', 'it': 'Al nostro tavolo'}


def mesa(caja, lang):
    """Impresiones propias de partida (mesa.json), si las hay."""
    f = AQUI / 'mesa.json'
    d = json.loads(f.read_text(encoding='utf-8')).get(caja, {}) if f.exists() else {}
    t = d.get(lang) or d.get('en')
    return f'<h2>{MESA_T[lang]}</h2>{t}' if t else ''


def pagina_caja(f):
    c = CONSEJOS.get(f['film'], {})
    k = KILLERS.get(f['killer'], {})
    h = [arte_ficha(f"img/{slug(f['film'])}.jpg", alt=f['film']),
         f'<p class="eyebrow">Caja · {f.get("fnum","")} · {f["plays"]} partidas</p>',
         f'<h1 data-caja="{f["film"]}">{f["film"]}<span class="roja">{pc(f["wr"])} de victorias</span></h1>']
    import guia
    if guia.por_caja(f["film"]):
        h.append(guia.enlaces("es", guia.por_caja(f["film"])))

    dif = (f['wr'] - MEDIA) * 100
    h.append(f'<p class="dek">{f["killer"]} en {f["loc"]}. '
             f'Sobre {f["plays"]} partidas registradas se gana el {pc(f["wr"])} de las veces, '
             + (f'{abs(dif):.1f}'.replace('.', ',') + f' puntos por {"encima" if dif>0 else "debajo"} de la media del juego '
                f'({pc(MEDIA)}).' if abs(dif) >= 1 else f'justo en la media del juego ({pc(MEDIA)}).')
             + '</p>')

    if f['plays'] < 90:
        h.append('<div class="aviso"><h3>Cuidado con la muestra</h3>'
                 f'<p>Solo {f["plays"]} partidas registradas. Repartidas entre Dark Powers, '
                 'Finales y hojas de preparación, cada desglose queda en muy pocas: '
                 'tómalos como indicio, no como hecho.</p></div>')

    if c:
        h.append('<h2>Qué tiene de particular</h2>')
        trozos = [c.get('mec'), c.get('com')]
        h.append('<p>' + ' '.join(t for t in trozos if t) + '</p>')
        if c.get('nivel') or c.get('mapa'):
            h.append(tabla(['', ''], [x for x in (
                ['Nivel', c.get('nivel', '—')],
                ['El mapa', c.get('mapa', '—')]) if x[1]]))

    h.append(mesa(f['film'], 'es'))
    h.append(mecanicas.killer(f['killer'], 'es'))
    h.append(mecanicas.mapa(f['loc'], 'es'))

    if k:
        h.append('<h2>El killer</h2>')
        h.append(f'<p><a href="{slug(f["killer"])}.html"><b>{f["killer"]}</b></a> gana el '
                 f'{pc(k["wr"])} repartido por todos los mapas, sobre {k["g"]} partidas. '
                 f'Aquí, en {f["loc"]}, la cifra es {pc(f["wr"])}.</p>')

    setups = [s for s in f.get('setups', []) if s[2] >= MIN_SECCION]
    if len(setups) >= 2:
        setups.sort(key=lambda x: x[1])
        h.append('<h2>Hojas de preparación</h2>')
        h.append('<p class="sub">De la más dura a la más fácil. '
                 f'Mínimo {MIN_SECCION} partidas.</p>')
        h.append(tabla(['Preparación', 'Victorias', 'Partidas'],
                       [[s[0], pc(s[1]), s[2]] for s in setups]))
        d = (setups[-1][1] - setups[0][1]) * 100
        if d >= 10:
            h.append(f'<p>Entre <b>{setups[0][0]}</b> y <b>{setups[-1][0]}</b> hay '
                     f'<b>{d:.0f} puntos</b> de diferencia. El montaje inicial pesa más de lo que parece.</p>')

    for titulo, clave in (('Dark Powers', 'Dark Power'), ('Cartas de Finale', 'Finale')):
        filas = [x for x in f.get('secs', {}).get(clave, []) if x[2] >= MIN_SECCION]
        if len(filas) >= 2:
            filas.sort(key=lambda x: x[1])
            h.append(f'<h2>{titulo}</h2>')
            h.append(tabla([titulo, 'Victorias', 'Partidas'],
                           [[x[0], pc(x[1]), x[2]] for x in filas]))

    if c.get('foro'):
        h.append('<h2>Consejos de quien la ha jugado</h2>')
        h.append(f'<div class="aviso"><p>{c["foro"]}</p></div>')

    r = D['reviews'].get(f['film'])
    if r:
        h.append('<h2>Qué dicen las reviews</h2>')
        h.append(f'<div class="aviso"><p><b>{r.get("veredicto","")}</b></p></div>')

    h.append(bloque_tienda(f["film"]))

    h.append('<h2>Cómo empezar la partida</h2>')
    h.append('<p>Las cuatro aperturas, con cuál usar según lo que veas en el montaje, '
             'están en la <a href="salidas.html">estrategias de salida</a>.</p>')

    if guia.por_caja(f["film"]):
        h.append(guia.secciones("es", guia.por_caja(f["film"])))

    titulo = f'{f["film"]} (Final Girl): estadísticas y consejos, {pc(f["wr"],0)} de victorias'
    desc = (f'{f["killer"]} en {f["loc"]}. Se gana el {pc(f["wr"])} sobre {f["plays"]} partidas. '
            f'Hojas de preparación, Dark Powers, Finales y consejos.')
    if guia.por_caja(f["film"]):
        # Con guía: que el título lo diga y nombre al killer (es lo que se busca).
        titulo = f'{f["film"]} (Final Girl): guía de {f["killer"]}, reglas y consejos · {pc(f["wr"],0)} de victorias'
        desc = (f'Cómo jugar contra {f["killer"]} en {f["loc"]}: preparación, reglas especiales y cada Dark Power '
                f'y Finale explicados. Se gana el {pc(f["wr"],0)} de {f["plays"]} partidas.')
    return titulo, desc[:155], '\n'.join(h)


def generar():
    out = []
    for nombre, k in KILLERS.items():
        if k.get('g', 0) < 60:        # sin volumen no hay página que sostener
            continue
        t, d, cuerpo = pagina_killer(nombre, k)
        out.append({'caja': k.get('box') or '', 'salida': slug(nombre) + '.html', 'title': t, 'desc': d,
                    'cuerpo': cuerpo, 'prioridad': '0.7', 'tipo': 'killer'})
    for f in D['films']:
        t, d, cuerpo = pagina_caja(f)
        out.append({'caja': f['film'], 'salida': slug(f['film']) + '.html', 'title': t, 'desc': d,
                    'cuerpo': cuerpo, 'prioridad': '0.7', 'tipo': 'caja',
                    'img': f.get('img')})
    return out


if __name__ == '__main__':
    p = generar()
    print(f'{len(p)} páginas: '
          f'{sum(1 for x in p if x["tipo"]=="killer")} killers, '
          f'{sum(1 for x in p if x["tipo"]=="caja")} cajas')
    for x in p[:3]:
        print(f'  {x["salida"]:<34} {len(x["cuerpo"])//1024} KB  {x["title"][:60]}')


# --- datos estructurados comunes ---------------------------------------------
# Fecha de los datos en ISO (D['meta']['last'] viene como "8 nov 2026") y la
# entidad del juego, con editorial y BGG: así un buscador o una IA sabe de qué
# "Final Girl" hablamos (no de la película ni del tropo).
_MESES = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']


def fecha_iso(t=None):
    d, m, y = (t or D['meta']['last']).split()
    return f"{y}-{_MESES.index(m[:3].lower()) + 1:02d}-{int(d):02d}"


JUEGO = {
    "@type": "Game", "name": "Final Girl",
    "description": "Solo horror board game", "numberOfPlayers": {"@type": "QuantitativeValue", "value": 1},
    "publisher": {"@type": "Organization", "name": "Van Ryder Games", "url": "https://www.vanrydergames.com/"},
    "sameAs": ["https://boardgamegeek.com/boardgame/277659/final-girl"],
}


def tipo_ld(salida):
    """Qué es cada página: datos, artículo o herramienta."""
    s = salida.rsplit("/", 1)[-1]
    if s == "salidas.html":
        return "Article"
    if s in ("crear-tier-list.html", "registrar.html"):
        return "WebApplication"
    return "Dataset"


def ld(name, desc, url, lang, salida, dominio, extra=None):
    hoy = fecha_iso()
    base = {"@context": "https://schema.org", "@type": tipo_ld(salida),
            "name": name, "description": desc, "url": url, "inLanguage": lang,
            "isAccessibleForFree": True, "dateModified": hoy, "about": JUEGO,
            "creator": {"@type": "Organization", "name": "Final Girl Stats", "url": dominio + "/"}}
    t = base["@type"]
    if t == "Dataset":
        base.update({"keywords": ["Final Girl", "board game", "solo", "win rate", "statistics"],
                     "temporalCoverage": f"2022-01/{hoy}",
                     "variableMeasured": "Win rate",
                     "measurementTechnique": "Games logged by players in the community tracking sheet",
                     "size": f"{D['meta']['total']} games"})
    elif t == "Article":
        base.update({"headline": name[:110], "author": base["creator"], "publisher": base["creator"]})
    else:
        base.update({"applicationCategory": "GameApplication", "operatingSystem": "Any",
                     "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}})
    if extra:
        base.update(extra)
    return json.dumps(base, ensure_ascii=False, separators=(",", ":"))


# --- sello: fecha de los datos y qué es Final Girl, en texto plano -----------
# Va en todas las páginas, fuera del JavaScript: es lo que lee un bot que no
# ejecuta JS (la mayoría de los de IA) y le dice de qué juego hablamos y de
# cuándo son los datos.
SELLO_TXT = {
    "es": ("Datos hasta el {f} · {n} partidas.", "Final Girl Stats es una web de fans, no oficial, sobre <b>Final Girl</b>, el juego de mesa de terror en solitario de Van Ryder Games."),
    "en": ("Data up to {f} · {n} games.", "Final Girl Stats is an unofficial fan site about <b>Final Girl</b>, the solo horror board game by Van Ryder Games."),
    "fr": ("Données jusqu'au {f} · {n} parties.", "Final Girl Stats est un site de fans non officiel sur <b>Final Girl</b>, le jeu de société d'horreur en solo de Van Ryder Games."),
    "de": ("Daten bis {f} · {n} Partien.", "Final Girl Stats ist eine inoffizielle Fanseite über <b>Final Girl</b>, das Solo-Horror-Brettspiel von Van Ryder Games."),
    "it": ("Dati fino al {f} · {n} partite.", "Final Girl Stats è un sito di fan non ufficiale su <b>Final Girl</b>, il gioco da tavolo horror in solitario di Van Ryder Games."),
}
_SELLO_RE = re.compile(r"\n?<!--sello-->.*?<!--/sello-->", re.S)


def sellar(raiz):
    iso = fecha_iso()
    total = D['meta']['total']
    hechas = 0
    for f in list(raiz.glob("*.html")) + [p for l in SELLO_TXT if l != "es" for p in (raiz / l).glob("*.html")]:
        lang = f.parent.name if f.parent != raiz else "es"
        s = f.read_text(encoding="utf-8")
        if "</body>" not in s or 'content="noindex' in s:
            continue
        a, b = SELLO_TXT[lang]
        n = f"{total:,}".replace(",", "." if lang in ("es", "de", "it") else (" " if lang == "fr" else ","))
        fecha = f'<time datetime="{iso}">{iso}</time>'
        sello = ('<!--sello--><p class="sello" style="max-width:1040px;margin:28px auto 18px;padding:0 20px;'
                 'font-size:12.5px;line-height:1.6;color:var(--muted,#9c8f93)">'
                 + a.format(f=fecha, n=n) + " " + b + "</p><!--/sello-->")
        s = _SELLO_RE.sub("", s).replace("</body>", sello + "\n</body>", 1)
        s = re.sub(r'(<h1[^>]*>[^<]*?\S)(<span class="roja">)', r'\1 \2', s, count=1)
        f.write_text(s, encoding="utf-8")
        hechas += 1
    return hechas


# --- resumen en texto plano para la portada ---------------------------------
# La portada pinta todo con JavaScript: sin él no hay ni un porcentaje. Este
# bloque, plegado al final, deja escrito lo que más se pregunta (qué killer y
# qué caja son más duros o más fáciles) con enlaces a las fichas.
RESUMEN_TXT = {
    "es": ("Resumen en texto", "De media, la Final Girl gana el {m} de {n} partidas.", "Killers más duros", "Killers más fáciles", "Cajas más duras", "Cajas más fáciles", "Todos en el <a href=\"fichas.html\">índice de fichas</a>.", "partidas"),
    "en": ("Summary in text", "On average, the Final Girl wins {m} of {n} games.", "Hardest killers", "Easiest killers", "Hardest boxes", "Easiest boxes", "All of them in the <a href=\"fichas.html\">killer and box index</a>.", "games"),
    "fr": ("Résumé en texte", "En moyenne, la Final Girl gagne {m} des {n} parties.", "Killers les plus durs", "Killers les plus faciles", "Boîtes les plus dures", "Boîtes les plus faciles", "Tous dans l'<a href=\"fichas.html\">index des fiches</a>.", "parties"),
    "de": ("Zusammenfassung als Text", "Im Schnitt gewinnt das Final Girl {m} von {n} Partien.", "Härteste Killer", "Leichteste Killer", "Härteste Boxen", "Leichteste Boxen", "Alle im <a href=\"fichas.html\">Index der Killer und Boxen</a>.", "Partien"),
    "it": ("Riassunto in testo", "In media la Final Girl vince il {m} di {n} partite.", "Killer più duri", "Killer più facili", "Scatole più dure", "Scatole più facili", "Tutti nell'<a href=\"fichas.html\">indice delle schede</a>.", "partite"),
}
_RES_RE = re.compile(r"\n?<!--resumen-->.*?<!--/resumen-->", re.S)


def _num(n, lang):
    return f"{n:,}".replace(",", {"es": ".", "de": ".", "it": ".", "fr": " "}.get(lang, ","))


def _pc(x, lang):
    s = f"{x * 100:.1f}"
    return (s if lang == "en" else s.replace(".", ",")) + (" %" if lang == "fr" else "%")


def resumir_portadas(raiz):
    ks = sorted(((nm, k) for nm, k in KILLERS.items() if k.get("g", 0) >= 60), key=lambda x: x[1]["wr"])
    cs = sorted(D["films"], key=lambda f: f["wr"])
    for lang, txt in RESUMEN_TXT.items():
        f = raiz / "index.html" if lang == "es" else raiz / lang / "index.html"
        if not f.exists():
            continue
        tit, med, kd, kf, cd, cf, todos, part = txt
        li = lambda filas: "".join(f'<li><a href="{slug(n)}.html">{n}</a>: {_pc(w, lang)} ({_num(g, lang)} {part})</li>' for n, w, g in filas)
        kk = [(nm, k["wr"], k["g"]) for nm, k in ks]
        cc = [(c["film"], c["wr"], c["plays"]) for c in cs]
        bloque = ('<!--resumen--><details class="resumen-txt" style="max-width:1040px;margin:30px auto 0;padding:0 20px;color:var(--muted,#9c8f93);font-size:14px">'
                  f'<summary style="cursor:pointer">{tit}</summary>'
                  f'<p>{med.format(m="<b>" + _pc(D["meta"]["wr"], lang) + "</b>", n=_num(D["meta"]["total"], lang))}</p>'
                  f'<h2 style="font-size:15px">{kd}</h2><ul>{li(kk[:5])}</ul>'
                  f'<h2 style="font-size:15px">{kf}</h2><ul>{li(kk[::-1][:5])}</ul>'
                  f'<h2 style="font-size:15px">{cd}</h2><ul>{li(cc[:5])}</ul>'
                  f'<h2 style="font-size:15px">{cf}</h2><ul>{li(cc[::-1][:5])}</ul>'
                  f'<p>{todos}</p></details><!--/resumen-->')
        s = _RES_RE.sub("", f.read_text(encoding="utf-8"))
        s = s.replace("<!--sello-->", bloque + "\n<!--sello-->", 1) if "<!--sello-->" in s else s.replace("</body>", bloque + "\n</body>", 1)
        f.write_text(s, encoding="utf-8")
