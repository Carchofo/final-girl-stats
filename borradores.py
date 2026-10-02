#!/usr/bin/env python3
"""Borradores de review por caja, a partir de los datos y nada mas.

Un aviso que conviene no perder de vista: una review de verdad lleva
pros, contras y fuentes que salen de lo que dice la gente en BGG y en
blogs. Un modelo local no tiene acceso a eso, y si se le pide igualmente
se lo inventa con buena letra. La regla del vault lo prohibe.

Asi que esto genera la mitad que SI sale de los datos:
  - `datos`:     hechos calculados en Python (victorias, cartas que mas
                 cuestan, mejores y peores mapas del killer, significancia).
  - `veredicto` y `claves`: redactados por qwen3.5 a partir de esos hechos,
                 con el guardia de cifras puesto.
  - `pros`, `contras`, `fuentes`: VACIOS a proposito. Los rellena un humano
                 (o Claude con buscador) leyendo reviews reales.

Uso:
    python borradores.py                       # lista las cajas y su estado
    python borradores.py "Madness in the Dark" # una caja
    python borradores.py --todas               # las que no tengan review
"""
import json
import pathlib
import re
import sys
import unicodedata

import cambios
import ollama_local as ol

for _f in (sys.stdout, sys.stderr):
    try:
        _f.reconfigure(encoding='utf-8', errors='replace')
    except AttributeError:
        pass

AQUI = pathlib.Path(__file__).parent
SALIDA = AQUI / 'reviews'

MIN_SECCION = 20
MIN_SETUP = 7


def slug(t):
    t = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode()
    return re.sub(r'-+', '-', re.sub(r'[^a-z0-9]+', '-', t.lower())).strip('-')


def pc(x):
    return round(x * 100, 1)


def z(a, b):
    """Test de dos proporciones. a y b son (wr, partidas).

    Sin esto, "su peor Dark Power" puede ser ruido de 20 partidas. Con
    z >= 1,96 la diferencia tiene una pinta razonable de ser real.
    """
    (wa, ga), (wb, gb) = a, b
    if not ga or not gb:
        return 0.0
    q = (wa * ga + wb * gb) / (ga + gb)
    d = q * (1 - q) * (1 / ga + 1 / gb)
    return round(abs(wa - wb) / d ** .5, 2) if d > 0 else 0.0


def extremos(lista, minimo):
    """De [[nombre, wr, partidas], ...] saca la mejor, la peor y si la
    distancia entre ellas aguanta un test de significancia."""
    a = [x for x in lista if x[0] != 'Unrevealed' and x[2] >= minimo]
    if len(a) < 2:
        return None
    mejor = max(a, key=lambda x: x[1])
    peor = min(a, key=lambda x: x[1])
    zz = z((mejor[1], mejor[2]), (peor[1], peor[2]))
    return {
        'mejor': {'carta': mejor[0], 'wr': pc(mejor[1]), 'partidas': mejor[2]},
        'peor': {'carta': peor[0], 'wr': pc(peor[1]), 'partidas': peor[2]},
        'z': zz,
        'significativo': zz >= 1.96,
    }


def hechos(D, nombre):
    f = next((x for x in D['films'] if x['film'] == nombre), None)
    if not f:
        raise SystemExit(f'no existe la caja "{nombre}"')
    k, loc = f['killer'], f['loc']

    # El killer en cada mapa: donde se le gana y donde no.
    suyos = sorted(((l, pc(v[k][1]), v[k][0]) for l, v in D['cells'].items()
                    if k in v and v[k][0] >= MIN_SECCION),
                   key=lambda x: -x[1])

    # Ese mapa con OTROS killers: separa la caja de sus dos mitades.
    celda = D['cells'].get(loc, {})
    otros = [(v[1], v[0]) for kk, v in celda.items()
             if kk != k and v[0] >= MIN_SECCION]
    mapa_sin_el = (pc(sum(w * g for w, g in otros) / sum(g for _, g in otros))
                   if otros else None)

    ranking = sorted(D['films'], key=lambda x: x['wr'])
    puesto = [x['film'] for x in ranking].index(nombre) + 1

    return {
        'caja': nombre, 'killer': k, 'mapa': loc, 'serie': f.get('serie'),
        'partidas': f['plays'], 'wr': pc(f['wr']),
        'puesto_dificultad': f'{puesto} de {len(ranking)} (1 = la mas dura)',
        'media_del_juego': pc(D['meta']['wr']),
        'killer_en_general': {'wr': pc(f['killWr']), 'partidas': f['killPlays']},
        'mapa_en_general': {'wr': pc(f['locWr']), 'partidas': f['locPlays']},
        'mapa_con_otros_killers': mapa_sin_el,
        'mejores_mapas_del_killer': suyos[:3],
        'peores_mapas_del_killer': suyos[-3:][::-1],
        'dark_power': extremos(f['secs'].get('Dark Power', []), MIN_SECCION),
        'finale': extremos(f['secs'].get('Finale', []), MIN_SECCION),
        'setup': extremos(f.get('setups', []), MIN_SETUP),
    }


SISTEMA = """Escribes el borrador de una ficha de Final Girl en castellano de
Espana, para gente que ya juega.

Recibes SOLO datos ya calculados de miles de partidas registradas.

REGLAS INNEGOCIABLES:
- No inventes NINGUNA cifra. Usa solo numeros que esten en el JSON de entrada.
- No inventes reglas, cartas, objetos ni nombres que no aparezcan en la entrada.
- No digas lo que opina la gente: no tienes esa informacion.
- Si un contraste tiene "significativo": false, no lo presentes como un
  hecho: di que apunta en esa direccion pero la muestra no da para afirmarlo.
- Tono seco y util. Nada de marketing.

Responde SOLO con este JSON:
{"veredicto": "2-3 frases: cuanto cuesta esta caja y por que, segun los numeros",
 "claves": ["3 o 4 frases sueltas, cada una apoyada en un dato de la entrada"]}"""


def borrador(D, nombre, modelo=ol.REDACTOR):
    h = hechos(D, nombre)
    print(f'  {nombre}: {h["partidas"]} partidas, {h["wr"]}% ... ', end='', flush=True)
    try:
        r = ol.chat_json(modelo, SISTEMA, json.dumps(h, ensure_ascii=False), temp=0.3)
    except ol.ModeloFalla as e:
        print(f'FALLA ({e})')
        r = None
    if r:
        intrusas = ol.colar(json.dumps(r, ensure_ascii=False), h)
        if intrusas:
            print(f'DESCARTADO, cifras inventadas: {intrusas}')
            r = None
        else:
            print('ok')

    return {
        'caja': nombre,
        'estado': 'borrador-pc' if r else 'solo-datos',
        'modelo': modelo if r else None,
        'veredicto': (r or {}).get('veredicto', ''),
        'claves': (r or {}).get('claves', []),
        'pros': [],       # requieren reviews reales; no las inventa el PC
        'contras': [],
        'confirma': [],   # pares [lo que dice alguien, lo que dicen los datos]
        'fuentes': [],
        'datos': h,
        'nota': ('pros, contras, confirma y fuentes van vacios a proposito: '
                 'salen de reviews reales y el modelo local no las tiene. '
                 'Los rellena un humano antes de publicar.'),
    }


def main():
    D = cambios.D_actual()
    hechas = set(D.get('reviews', {}))
    cajas = [f['film'] for f in D['films']]
    SALIDA.mkdir(exist_ok=True)

    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if '--todas' in sys.argv:
        objetivo = [c for c in cajas if c not in hechas]
    elif args:
        objetivo = args
    else:
        print(f'{len(cajas)} cajas, {len(hechas)} con review publicada.\n')
        for c in cajas:
            f = SALIDA / f'{slug(c)}.json'
            est = 'PUBLICADA' if c in hechas else ('borrador' if f.exists() else '-')
            print(f'  [{est:>9}] {c}')
        print('\npython borradores.py --todas   para las que faltan')
        return

    vivos = ol.vivo()
    usa_ligero = ol.REDACTOR not in vivos
    if usa_ligero:
        print(f'OJO: {ol.REDACTOR} no esta en Ollama. Uso {ol.REDACTOR_LIGERO}.')
    modelo = ol.REDACTOR_LIGERO if usa_ligero else ol.REDACTOR

    print(f'Redactando con {modelo}:')
    for c in objetivo:
        b = borrador(D, c, modelo)
        (SALIDA / f'{slug(c)}.json').write_text(
            json.dumps(b, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'\n{len(objetivo)} en reviews/. Los revisa el Mac antes de entrar en D.')


if __name__ == '__main__':
    main()
