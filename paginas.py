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
    # "amazon":   {"tag": "", "nombre": "Amazon",
    #              "url": "https://www.amazon.es/s?k={q}&tag={tag}"},
    # "zacatrus": {"tag": "", "nombre": "Zacatrus",
    #              "url": "https://zacatrus.es/catalogsearch/result/?q={q}&acc={tag}"},
}

MIN_CELDA = 20          # partidas mínimas para citar una combinación
MIN_SECCION = 20        # ídem para Dark Powers y Finales


def slug(t):
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode()
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', t.lower())).strip('-')


def pc(x, dec=1):
    return f"{x*100:.{dec}f}".replace('.', ',') + '%'


def datos():
    s = (AQUI / 'src' / 'cuerpo.html').read_text()
    return json.loads(re.search(r'var D = (\{.*?\});\n', s, re.S).group(1))


def descripciones():
    """Quien es cada killer y como juega. Los datos de juego salen de la
    Final Girl Wiki (CC BY-SA): el texto es nuestro, los hechos son suyos,
    y por eso cada ficha la enlaza."""
    f = AQUI / 'killers_desc.json'
    return json.loads(f.read_text()) if f.exists() else {}


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


def bloque_tienda(nombre):
    """Enlaces de compra, solo si hay algún afiliado configurado.

    El aviso de que son enlaces de afiliado va SIEMPRE y antes de los
    enlaces, no escondido en el pie: el sitio se sostiene sobre datos
    que presta la comunidad, y ahí no se juega con la confianza.
    """
    activos = [a for a in AFILIADOS.values() if a.get("tag")]
    if not activos:
        return ""
    import urllib.parse
    q = urllib.parse.quote_plus("Final Girl " + nombre)
    enlaces = " ".join(
        f'<a class="tienda" href="{a["url"].format(q=q, tag=a["tag"])}" '
        f'target="_blank" rel="noopener sponsored nofollow">{a["nombre"]}</a>'
        for a in activos)
    return ('<h2>Dónde conseguirla</h2>'
            '<div class="aviso"><p class="sub" style="margin-bottom:10px">'
            'Enlaces de afiliado: si compras, a mí me llega una comisión y a ti '
            'te cuesta lo mismo. No cambian lo que dicen los datos de arriba.</p>'
            f'<p>{enlaces}</p></div>')


def tabla(cab, filas):
    if not filas:
        return ''
    th = ''.join(f'<th{" class=n" if i else ""}>{c}</th>' for i, c in enumerate(cab))
    tr = ''.join(
        '<tr>' + ''.join(f'<td{" class=n" if i else ""}>{c}</td>' for i, c in enumerate(f)) + '</tr>'
        for f in filas)
    return f'<div class="tabla-wrap"><table><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


# --------------------------------------------------------------------------
# Páginas de killer
# --------------------------------------------------------------------------
def pagina_killer(nombre, k):
    mapas = mapas_de(nombre)
    caja = k.get('box')
    f = FILMS.get(caja)
    propio = f['loc'] if f else None
    aqui = next((m for m in mapas if m[0] == propio), None)

    h = [f'<p class="eyebrow">Killer · {len(mapas)} mapas con datos</p>',
         f'<h1>{nombre}<span class="roja">en {pc(k["wr"])} de victorias</span></h1>']

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
                     f'<b>{"+" if d>0 else ""}{d:.1f} puntos</b>. '
                     + ('El mapa juega a tu favor, no al suyo.' if d < 0
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

    titulo = f'{nombre} en Final Girl: victorias por mapa y cómo ganarle'
    desc = (f'La Final Girl gana el {pc(k["wr"])} contra {nombre} sobre {k["g"]} partidas. '
            f'Dónde le va mejor y peor, sus Dark Powers y Finales más duros, y consejos.')
    return titulo, desc[:155], '\n'.join(h)


# --------------------------------------------------------------------------
# Páginas de caja
# --------------------------------------------------------------------------
def pagina_caja(f):
    c = CONSEJOS.get(f['film'], {})
    k = KILLERS.get(f['killer'], {})
    h = [f'<p class="eyebrow">Caja · {f.get("fnum","")} · {f["plays"]} partidas</p>',
         f'<h1>{f["film"]}<span class="roja">{pc(f["wr"])} de victorias</span></h1>']

    dif = (f['wr'] - MEDIA) * 100
    h.append(f'<p class="dek">{f["killer"]} en {f["loc"]}. '
             f'Sobre {f["plays"]} partidas registradas se gana el {pc(f["wr"])} de las veces, '
             + (f'{abs(dif):.1f} puntos por {"encima" if dif>0 else "debajo"} de la media del juego '
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

    titulo = f'{f["film"]}: estadísticas y consejos ({pc(f["wr"],0)} de victorias)'
    desc = (f'{f["killer"]} en {f["loc"]}. Se gana el {pc(f["wr"])} sobre {f["plays"]} partidas. '
            f'Hojas de preparación, Dark Powers, Finales y consejos.')
    return titulo, desc[:155], '\n'.join(h)


def generar():
    out = []
    for nombre, k in KILLERS.items():
        if k.get('g', 0) < 60:        # sin volumen no hay página que sostener
            continue
        t, d, cuerpo = pagina_killer(nombre, k)
        out.append({'salida': slug(nombre) + '.html', 'title': t, 'desc': d,
                    'cuerpo': cuerpo, 'prioridad': '0.7', 'tipo': 'killer'})
    for f in D['films']:
        t, d, cuerpo = pagina_caja(f)
        out.append({'salida': slug(f['film']) + '.html', 'title': t, 'desc': d,
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
