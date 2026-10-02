#!/usr/bin/env python3
"""Baja la hoja de la comunidad y recalcula los datos del sitio.

Por qué existe: los números del sitio se calcularon a mano una vez. La
hoja sigue creciendo, y una web de estadísticas con datos de hace un mes
es una web que miente despacio.

Qué NO toca: lo escrito a mano. Consejos, reviews, imágenes, nombres de
temporada y la correspondencia caja -> Final Girls se conservan tal cual
estaban. Esto solo recalcula lo que sale de contar partidas.

Uso:
    python3 refrescar.py            # recalcula y enseña el diff
    python3 refrescar.py --escribe  # además reescribe src/cuerpo.html
"""
import csv
import io
import json
import pathlib
import re
import sys
import urllib.request
from collections import defaultdict
from datetime import datetime

AQUI = pathlib.Path(__file__).parent
HOJA = "1xSl_BhqfVdHnYIYtuiWIIzr1BjD4ToLAYvDCWebNKGY"
GID = "465046674"          # pestaña Answers: una fila por partida
URL = f"https://docs.google.com/spreadsheets/d/{HOJA}/export?format=csv&gid={GID}"

MIN_CELDA = 20             # partidas mínimas para que una celda cuente
MIN_SECCION = 20           # idem para Dark Powers y Finales
MIN_SETUP = 7              # las hojas de preparacion se citan con menos muestra
MIN_GIRL = 20

MESES = ['ene', 'feb', 'mar', 'abr', 'may', 'jun',
         'jul', 'ago', 'sep', 'oct', 'nov', 'dic']


def mil(n):
    """13915 -> "13.915", como se escribe en castellano."""
    return f"{n:,}".replace(',', '.')


def pct(g, w):
    """Porcentaje de victoria con 4 decimales, como el resto del sitio."""
    return round(w / g, 4) if g else 0.0


def bajar():
    pet = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(pet, timeout=120) as r:
        bruto = r.read().decode('utf-8', 'replace')
    return list(csv.DictReader(io.StringIO(bruto)))


def fecha(t):
    """La hoja mezcla formatos de fecha según quién y cuándo rellenó."""
    for f in ('%m/%d/%Y %H:%M:%S', '%d/%m/%Y %H:%M:%S', '%Y-%m-%d %H:%M:%S'):
        try:
            return datetime.strptime(t.strip(), f)
        except ValueError:
            pass
    return None


def canonico(viejo):
    """La hoja la rellenan personas: el mismo killer aparece como
    'Terror from the Grave' y 'Terror from The Grave'. Sin normalizar,
    uno se parte en dos y las dos mitades se quedan fuera por muestra."""
    m = {}
    for k in viejo['killers']:
        m[k.lower()] = k
    for l in viejo['matrix']:
        m[l.lower()] = l
    return m


def limpiar(filas, canon=None):
    """Una partida vale si dice killer, mapa y quién ganó. El resto es ruido:
    filas a medio rellenar y las que la hoja deja en blanco al final."""
    out = []
    for f in filas:
        k = (f.get('Killer') or '').strip()
        l = (f.get('Location') or '').strip()
        g = (f.get('Who won the game?') or '').strip()
        if canon:
            k = canon.get(k.lower(), k)
            l = canon.get(l.lower(), l)
        if k and l and g in ('Final Girl', 'The Killer'):
            f['_gano'] = 1 if g == 'Final Girl' else 0
            f['_killer'], f['_loc'] = k, l
            out.append(f)
    return out


def cuenta(filas, clave):
    """Agrupa y devuelve {valor: [partidas, victorias]}."""
    d = defaultdict(lambda: [0, 0])
    for f in filas:
        v = clave(f)
        if v:
            d[v][0] += 1
            d[v][1] += f['_gano']
    return d


def tabla(d, minimo):
    """De {v: [g, w]} a [[v, wr, g], ...] ordenado por nombre."""
    return sorted(([k, pct(g, w), g] for k, (g, w) in d.items() if g >= minimo),
                  key=lambda x: x[0])


def recalcular(filas, viejo):
    D = json.loads(json.dumps(viejo))        # copia: lo editorial se conserva
    total = len(filas)

    # --- meta ---------------------------------------------------------
    victorias = sum(f['_gano'] for f in filas)
    fechas = [d for d in (fecha(f.get('Timestamp', '')) for f in filas) if d]
    ultima = max(fechas) if fechas else None
    dias = (ultima - min(fechas)).days if fechas else 1

    D['meta']['total'] = total
    D['meta']['wr'] = pct(total, victorias)
    D['meta']['perDay'] = round(total / max(dias, 1), 2)
    # Cuanta gente ha registrado partidas. Estaba escrito a mano y se
    # quedo en 669 hace meses.
    D['meta']['jugadores'] = len({(f.get('Nickname') or '').strip()
                                  for f in filas if (f.get('Nickname') or '').strip()})
    if ultima:
        D['meta']['last'] = f"{ultima.day} {MESES[ultima.month - 1]} {ultima.year}"

    # Temporadas: el orden y los nombres son los de siempre, solo cambian
    # las cifras. Lo que no cae en S1-S4 va a "Otras", como antes.
    temp = cuenta(filas, lambda f: (f.get('Season') or '').strip())
    seasons = []
    for i, nombre in enumerate(['Temporada 1', 'Temporada 2', 'Temporada 3', 'Temporada 4'], 1):
        g, w = temp.get(f'Season {i}', [0, 0])
        seasons.append([nombre, g, pct(g, w)])
    og = sum(v[0] for k, v in temp.items() if not re.fullmatch(r'Season [1-4]', k))
    ow = sum(v[1] for k, v in temp.items() if not re.fullmatch(r'Season [1-4]', k))
    seasons.append(['Otras', og, pct(og, ow)])
    D['meta']['seasons'] = seasons

    # --- killers ------------------------------------------------------
    porKiller = cuenta(filas, lambda f: f['_killer'])
    for k, v in D['killers'].items():
        g, w = porKiller.get(k, [0, 0])
        v['g'], v['wr'] = g, pct(g, w)
        propias = [f for f in filas if f['_killer'] == k]
        for etiqueta, col in (('Dark Power', 'Dark Power'), ('Finale', 'Finale')):
            c = cuenta(propias, lambda f: (f.get(col) or '').strip())
            filasx = tabla(c, MIN_SECCION)
            if filasx:
                v['secs'][etiqueta] = filasx

    # --- localizaciones y matriz --------------------------------------
    porLoc = cuenta(filas, lambda f: f['_loc'])
    D['locs'] = [[l, pct(porLoc[l][0], porLoc[l][1]), porLoc[l][0]]
                 for l in sorted(porLoc) if porLoc[l][0] >= MIN_CELDA]
    # El mismo mapa puede venir escrito de dos formas; ya viene normalizado.

    celdas = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    for f in filas:
        c = celdas[f['_loc']][f['_killer']]
        c[0] += 1
        c[1] += f['_gano']

    D['cells'] = {}
    D['matrix'] = {}
    for loc in celdas:
        cel, mat = {}, {}
        for k, (g, w) in celdas[loc].items():
            # Sin umbral: la pagina decide que celda pinta y cual deja en
            # blanco. Recortar aqui le quitaria informacion al cliente.
            cel[k] = [g, pct(g, w)]
            mat[k] = pct(g, w)
        if cel:
            D['cells'][loc] = cel
            D['matrix'][loc] = mat

    # --- hojas de preparación ----------------------------------------
    sets = defaultdict(lambda: defaultdict(lambda: [0, 0]))
    for f in filas:
        s = (f.get('Setup') or '').strip()
        if s:
            x = sets[f['_loc']][s]
            x[0] += 1
            x[1] += f['_gano']
    D['setups'] = {loc: t for loc, d in sets.items()
                   if (t := tabla(d, MIN_SETUP))}

    # --- Final Girls --------------------------------------------------
    porGirl = cuenta(filas, lambda f: (f.get('Final Girl') or '').strip())
    caja = {g: c for g, c in ((g, c) for c, gs in D['cajaGirls'].items() for g in gs)}
    antes = {g[0]: g[3] for g in D['girls']}
    D['girls'] = sorted(
        ([n, pct(g, w), g, antes.get(n) or caja.get(n, 'Otra')]
         for n, (g, w) in porGirl.items() if g >= MIN_GIRL),
        key=lambda x: -x[1])

    # --- cajas --------------------------------------------------------
    for f in D['films']:
        k, l = f['killer'], f['loc']
        g, w = celdas[l][k] if k in celdas[l] else (0, 0)
        f['plays'], f['wr'] = g, pct(g, w)
        lg, lw = porLoc.get(l, [0, 0])
        f['locPlays'], f['locWr'] = lg, pct(lg, lw)
        kg, kw = porKiller.get(k, [0, 0])
        f['killPlays'], f['killWr'] = kg, pct(kg, kw)
        f['secs'] = json.loads(json.dumps(D['killers'][k]['secs']))
        f['setups'] = D['setups'].get(l, [])

    # --- temporadas (bloque de cajas) ---------------------------------
    porCaja = {f['film']: (f['plays'], f['wr']) for f in D['films']}
    for t in D['temporadas']:
        g = sum(porCaja.get(c, (0, 0))[0] for c in t['cajas'])
        w = sum(round(porCaja.get(c, (0, 0))[0] * porCaja.get(c, (0, 0))[1])
                for c in t['cajas'])
        t['plays'], t['wr'] = g, pct(g, w)

    return D


def main():
    viejo_txt = (AQUI / 'src' / 'cuerpo.html').read_text(encoding="utf-8")
    m = re.search(r'var D = (\{.*?\});\n', viejo_txt, re.S)
    viejo = json.loads(m.group(1))

    print('Bajando la hoja...')
    filas = limpiar(bajar(), canonico(viejo))
    print(f'  {len(filas)} partidas válidas')

    nuevo = recalcular(filas, viejo)

    print('\n  partidas   ', viejo['meta']['total'], '->', nuevo['meta']['total'])
    print('  victorias  ', viejo['meta']['wr'], '->', nuevo['meta']['wr'])
    print('  última     ', viejo['meta']['last'], '->', nuevo['meta']['last'])
    print('  killers    ', len(viejo['killers']), '->', len(nuevo['killers']))
    print('  mapas      ', len(viejo['locs']), '->', len(nuevo['locs']))
    print('  final girls', len(viejo['girls']), '->', len(nuevo['girls']))

    if '--escribe' not in sys.argv:
        print('\nEn seco. Añade --escribe para guardar.')
        return

    nuevo_txt = viejo_txt[:m.start(1)] + json.dumps(nuevo, ensure_ascii=False) + viejo_txt[m.end(1):]
    (AQUI / 'src' / 'cuerpo.html').write_text(nuevo_txt, encoding="utf-8")

    # La cifra de partidas esta escrita a mano en titulos, descripciones y
    # textos de seccion, porque ahi tiene que estar en el HTML servido y no
    # pintada por JavaScript. Si solo cambiaran los datos, el sitio diria
    # una cosa en el titulo y otra en las tablas.
    antes, ahora = mil(viejo['meta']['total']), mil(nuevo['meta']['total'])
    tocados = []
    if antes != ahora:
        for f in ('src/cuerpo.html', 'src/salidas-cuerpo.html',
                  'montar.py', 'README.md', 'paginas.py'):
            ruta = AQUI / f
            if not ruta.exists():
                continue
            t = ruta.read_text(encoding="utf-8")
            if antes in t:
                ruta.write_text(t.replace(antes, ahora), encoding="utf-8")
                tocados.append(f)

    print(f'\nsrc/cuerpo.html actualizado.')
    if tocados:
        print(f'Cifra {antes} -> {ahora} en: ' + ', '.join(tocados))
    print('Ahora: python3 montar.py')


if __name__ == '__main__':
    main()
