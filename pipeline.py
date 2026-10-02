#!/usr/bin/env python3
"""Pipeline automatico del PC (flujo/pipeline.md del vault).

    hoja -> refrescar.py -> cambios.py -> granite4.2 -> montar.py -> rama pc/datos

Reparto de responsabilidades, que es lo unico importante aqui:
  - Python cuenta. Todos los numeros salen de `refrescar.py` y `cambios.py`.
  - El modelo redacta. Recibe el JSON de cambios ya calculado y lo resume.
    Si cuela una cifra que no estaba en la entrada, `ollama_local.colar`
    lo caza y el resumen se descarta. Los datos se publican igual.
  - Claude en el Mac revisa la rama y mergea. Esto NUNCA toca `main`.

Uso:
    python pipeline.py            # ensena que haria, no escribe ni empuja
    python pipeline.py --escribe  # recalcula, monta y commitea en local
    python pipeline.py --escribe --push   # ademas empuja a origin/pc/datos
"""
import datetime
import json
import os
import pathlib
import shutil
import subprocess
import sys

import cambios
import ollama_local as ol

# La consola de Windows viene en cp1252 y los scripts hablan castellano.
# Sin esto el pipeline se cae por un acento mientras imprime, no por un fallo.
for _f in (sys.stdout, sys.stderr):
    try:
        _f.reconfigure(encoding='utf-8', errors='replace')
    except AttributeError:
        pass
ENTORNO = {**os.environ, 'PYTHONIOENCODING': 'utf-8', 'PYTHONUTF8': '1'}

AQUI = pathlib.Path(__file__).parent
RAMA = 'pc/datos'
CUERPO = AQUI / 'src' / 'cuerpo.html'
DATOS = AQUI / 'datos'

SISTEMA = """Eres el redactor de un sitio de estadisticas de Final Girl.

Recibes un JSON con los cambios de datos YA CALCULADOS. Tu trabajo es decir
cuales importan y por que, en castellano, para que un humano decida si vale
la pena tocar los textos de la web.

REGLAS INNEGOCIABLES:
- No calcules nada. No inventes ninguna cifra. Usa SOLO numeros que
  aparezcan literalmente en el JSON de entrada.
- Si un dato tiene "fiable": false o menos de 20 partidas, dilo asi:
  es una senal, no una conclusion.
- Si no hay nada relevante, dilo. No rellenes.

Responde SOLO con este JSON:
{"titular": "una frase",
 "relevantes": [{"que": "...", "porque": "...", "accion": "..."}],
 "ignorado": "que has descartado y por que",
 "tocar_textos": true|false}"""


def paso(txt):
    print(f'\n=== {txt}', flush=True)


def correr(args):
    r = subprocess.run([sys.executable, *args], cwd=AQUI, env=ENTORNO,
                       capture_output=True, text=True, encoding='utf-8',
                       errors='replace')
    print(r.stdout.strip())
    if r.returncode:
        print(r.stderr.strip(), file=sys.stderr)
        raise SystemExit(f'fallo: {" ".join(args)} (exit {r.returncode})')
    return r.stdout


def git(*args, check=True):
    r = subprocess.run(['git', *args], cwd=AQUI, capture_output=True,
                       text=True, encoding='utf-8', errors='replace')
    if check and r.returncode:
        raise SystemExit(f'git {" ".join(args)}: {r.stderr.strip()}')
    return r.stdout.strip()


def resumir(c):
    """granite4.2 convierte el diff en un resumen legible. Si falla o se
    inventa un numero, devuelve None: los datos se publican igual, solo
    nos quedamos sin la nota."""
    try:
        r = ol.chat_json(ol.CEREBRO, SISTEMA,
                         json.dumps(c, ensure_ascii=False), temp=0.1)
    except ol.ModeloFalla as e:
        print(f'  modelo no disponible: {e}')
        return None
    intrusas = ol.colar(json.dumps(r, ensure_ascii=False), c)
    if intrusas:
        print(f'  DESCARTADO: el modelo metio cifras que no estaban en los '
              f'datos: {intrusas}')
        return None
    print(f'  {r.get("titular", "")}')
    return r


def main():
    escribe = '--escribe' in sys.argv
    push = '--push' in sys.argv
    DATOS.mkdir(exist_ok=True)
    sello = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')

    paso(f'Rama de trabajo ({RAMA})')
    if escribe:
        if git('status', '--porcelain'):
            raise SystemExit('hay cambios sin commitear: paro antes de tocar nada')
        git('fetch', 'origin', check=False)
        actual = git('rev-parse', '--abbrev-ref', 'HEAD')
        if actual != RAMA:
            # La rama ya lleva las herramientas del PC, asi que se reutiliza.
            # Solo se crea desde main la primera vez: rehacerla cada dia
            # borraria pipeline.py y los borradores sin avisar.
            existe = (git('rev-parse', '--verify', RAMA, check=False)
                      or git('rev-parse', '--verify', f'origin/{RAMA}', check=False))
            if existe:
                git('checkout', RAMA)
                git('merge', '--ff-only', f'origin/{RAMA}', check=False)
            else:
                git('checkout', '-b', RAMA, 'origin/main')
    print(f'  {git("rev-parse", "--abbrev-ref", "HEAD")}')

    paso('Datos antiguos')
    viejo = cambios.D_actual()
    copia = AQUI / 'datos' / '_cuerpo_antes.html'
    shutil.copy2(CUERPO, copia)
    print(f'  {viejo["meta"]["total"]} partidas, ultima {viejo["meta"].get("last")}')

    paso('Bajando la hoja y recalculando (refrescar.py)')
    correr(['refrescar.py', '--escribe'] if escribe else ['refrescar.py'])
    if not escribe:
        print('\nEn seco: no se ha escrito nada. Anade --escribe.')
        copia.unlink(missing_ok=True)
        return

    paso('Que ha cambiado (aritmetica pura, sin modelo)')
    nuevo = cambios.D_actual()
    c = cambios.comparar(viejo, nuevo)
    (DATOS / 'cambios.json').write_text(
        json.dumps(c, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'  +{c["meta"]["partidas_nuevas"]} partidas | '
          f'{len(c["killers"])} killers movidos | '
          f'{len(c["cruces_nuevos"])} cruces nuevos | '
          f'{len(c["girls_nuevas"])} final girls nuevas')

    if not c['hay_algo']:
        print('\nSin novedades en la hoja. No se commitea nada.')
        copia.unlink(missing_ok=True)
        return

    paso(f'Resumen con {ol.CEREBRO}')
    r = resumir(c)
    (DATOS / 'resumen.json').write_text(
        json.dumps({'fecha': sello, 'resumen': r}, ensure_ascii=False, indent=2),
        encoding='utf-8')

    paso('Montando el sitio (montar.py)')
    correr(['montar.py'])

    paso('Commit')
    copia.unlink(missing_ok=True)
    git('add', '-A')
    if not git('status', '--porcelain'):
        print('  nada que commitear')
        return
    msg = (f'datos: {nuevo["meta"]["total"]} partidas '
           f'(+{c["meta"]["partidas_nuevas"]}) al {sello}')
    if r and r.get('titular'):
        msg += f'\n\n{r["titular"]}'
    if r and r.get('tocar_textos'):
        msg += '\n\nOJO: el resumen dice que hay textos que revisar.'
    msg += '\n\nGenerado por pipeline.py en el PC. Revisar antes de mergear a main.'
    git('commit', '-m', msg)
    print('  ' + git('log', '-1', '--oneline'))

    if push:
        paso('Push')
        git('push', '-u', 'origin', RAMA)
        print('  empujado. Le toca al Mac revisar y mergear.')
    else:
        print('\nCommit local hecho. Anade --push para subirlo.')


if __name__ == '__main__':
    main()
