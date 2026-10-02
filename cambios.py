#!/usr/bin/env python3
"""Compara el D de antes con el de ahora y dice que ha cambiado de verdad.

Todo lo que hay aqui es aritmetica. Ningun modelo toca estos numeros: el
LLM solo recibe la salida de este fichero y la redacta. Esa separacion es
la unica forma de que la web no empiece a mentir despacio.

Umbrales del vault: 5 partidas para mostrar una celda, 20 para afirmar.
"""
import json
import re
import pathlib

AQUI = pathlib.Path(__file__).parent

MIN_MOSTRAR = 5
MIN_AFIRMAR = 20
SALTO_WR = 0.01        # 1 punto porcentual: por debajo es ruido de muestreo


def leer_D(texto):
    m = re.search(r'var D = (\{.*?\});\n', texto, re.S)
    if not m:
        raise SystemExit('src/cuerpo.html: no encuentro "var D = {...}"')
    return json.loads(m.group(1))


def D_actual():
    return leer_D((AQUI / 'src' / 'cuerpo.html').read_text(encoding='utf-8'))


def _pt(a, b):
    """Diferencia en puntos porcentuales, 2 decimales."""
    return round((b - a) * 100, 2)


def comparar(viejo, nuevo):
    c = {
        'meta': {},
        'killers': [],
        'cruces_nuevos': [],
        'girls_nuevas': [],
        'setups_nuevos': [],
        'cajas': [],
    }

    vm, nm = viejo['meta'], nuevo['meta']
    c['meta'] = {
        'partidas_antes': vm['total'],
        'partidas_ahora': nm['total'],
        'partidas_nuevas': nm['total'] - vm['total'],
        'wr_antes': round(vm['wr'] * 100, 2),
        'wr_ahora': round(nm['wr'] * 100, 2),
        'wr_salto_pt': _pt(vm['wr'], nm['wr']),
        'ultima_antes': vm.get('last'),
        'ultima_ahora': nm.get('last'),
        'jugadores_antes': vm.get('jugadores'),
        'jugadores_ahora': nm.get('jugadores'),
    }

    # --- killers: solo los que se mueven de forma apreciable ----------
    for k, nv in nuevo['killers'].items():
        vv = viejo['killers'].get(k)
        if not vv:
            c['killers'].append({'killer': k, 'novedad': True,
                                 'partidas': nv['g'],
                                 'wr': round(nv['wr'] * 100, 2)})
            continue
        if nv['g'] == vv['g']:
            continue
        salto = _pt(vv['wr'], nv['wr'])
        if abs(salto) * 0.01 < SALTO_WR:
            continue
        c['killers'].append({
            'killer': k,
            'partidas_antes': vv['g'], 'partidas_ahora': nv['g'],
            'wr_antes': round(vv['wr'] * 100, 2),
            'wr_ahora': round(nv['wr'] * 100, 2),
            'salto_pt': salto,
            'fiable': nv['g'] >= MIN_AFIRMAR,
        })
    c['killers'].sort(key=lambda x: -abs(x.get('salto_pt', 0)))

    # --- cruces killer x mapa que cruzan un umbral --------------------
    for loc, ks in nuevo['cells'].items():
        vks = viejo['cells'].get(loc, {})
        for k, (g, wr) in ks.items():
            antes = vks.get(k, [0, 0.0])[0]
            for umbral, etiqueta in ((MIN_MOSTRAR, 'se puede mostrar'),
                                     (MIN_AFIRMAR, 'se puede afirmar')):
                if antes < umbral <= g:
                    c['cruces_nuevos'].append({
                        'mapa': loc, 'killer': k,
                        'partidas': g, 'wr': round(wr * 100, 2),
                        'cruza': etiqueta, 'umbral': umbral,
                    })

    # --- final girls que entran en tabla ------------------------------
    antes_g = {g[0] for g in viejo['girls']}
    for n, wr, g, caja in nuevo['girls']:
        if n not in antes_g:
            c['girls_nuevas'].append({'girl': n, 'partidas': g,
                                      'wr': round(wr * 100, 2), 'caja': caja})

    # --- hojas de preparacion nuevas ----------------------------------
    for loc, lista in nuevo.get('setups', {}).items():
        antes_s = {s[0] for s in viejo.get('setups', {}).get(loc, [])}
        for nombre, wr, g in lista:
            if nombre not in antes_s:
                c['setups_nuevos'].append({'mapa': loc, 'setup': nombre,
                                           'partidas': g,
                                           'wr': round(wr * 100, 2)})

    # --- cajas (killer + mapa de su pelicula) -------------------------
    vf = {f['film']: f for f in viejo['films']}
    for f in nuevo['films']:
        a = vf.get(f['film'])
        if not a or a['plays'] == f['plays']:
            continue
        salto = _pt(a['wr'], f['wr'])
        if abs(salto) * 0.01 < SALTO_WR:
            continue
        c['cajas'].append({'caja': f['film'], 'killer': f['killer'],
                           'mapa': f['loc'],
                           'partidas_antes': a['plays'],
                           'partidas_ahora': f['plays'],
                           'wr_antes': round(a['wr'] * 100, 2),
                           'wr_ahora': round(f['wr'] * 100, 2),
                           'salto_pt': salto,
                           'fiable': f['plays'] >= MIN_AFIRMAR})
    c['cajas'].sort(key=lambda x: -abs(x['salto_pt']))

    c['hay_algo'] = bool(c['meta']['partidas_nuevas'] or c['killers']
                         or c['cruces_nuevos'] or c['girls_nuevas']
                         or c['setups_nuevos'] or c['cajas'])
    return c


if __name__ == '__main__':
    import sys
    a, b = sys.argv[1], sys.argv[2]
    va = leer_D(pathlib.Path(a).read_text(encoding='utf-8'))
    vb = leer_D(pathlib.Path(b).read_text(encoding='utf-8'))
    print(json.dumps(comparar(va, vb), ensure_ascii=False, indent=2))
