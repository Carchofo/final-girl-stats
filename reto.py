"""Franja del reto semanal de r/finalgirl (lo organiza u/Mykl) en la portada.

Solo enlazamos su post y ponemos nuestras cifras de esa combinación: ni su
imagen ni su texto. Cada semana se cambia RETO a mano; con RETO = None no
sale nada.
"""
import json
import pathlib
import re

AQUI = pathlib.Path(__file__).parent

# Ejemplo: {"n": 149, "killer": "Hans", "loc": "Camp Happy Trail",
#           "url": "https://www.reddit.com/r/finalgirl/comments/..."}
# "loc" con el nombre de la matriz (Camp Happy Trail, no Trails).
RETO = None

T = {
    "es": ("Reto de la semana", "en", "de victorias", "partidas", "Únete en r/finalgirl"),
    "en": ("This week's challenge", "at", "win rate", "games", "Join on r/finalgirl"),
    "fr": ("Défi de la semaine", "à", "de victoires", "parties", "Participez sur r/finalgirl"),
    "de": ("Challenge der Woche", "auf", "Siegquote", "Partien", "Mitmachen auf r/finalgirl"),
    "it": ("Sfida della settimana", "a", "di vittorie", "partite", "Partecipa su r/finalgirl"),
}


def _celda(killer, loc):
    s = (AQUI / "src" / "cuerpo.html").read_text(encoding="utf-8")
    D = json.loads(re.search(r"var D = (\{.*?\});\n", s, re.S).group(1))
    return (D["cells"].get(loc) or {}).get(killer)


def poner(cuerpo, lang):
    """Mete la franja justo encima de las pestañas de la portada."""
    if not RETO or 'class="reto"' in cuerpo:
        return cuerpo
    i = cuerpo.find('<nav class="tabs"')
    if i < 0:
        return cuerpo
    t = T[lang]
    c = _celda(RETO["killer"], RETO["loc"])
    pc = (f'{c[1] * 100:.0f}%'.replace(".", ",") + f' {t[2]} · {c[0]} {t[3]} · ') if c else ""
    franja = (
        '<style>.reto{display:block;margin:0 0 14px;padding:9px 14px;border:1px dashed var(--blood);'
        'color:inherit;text-decoration:none;font-size:14px}.reto b{color:var(--blood)}'
        '.reto:hover{background:rgba(224,59,72,.08)}</style>'
        f'<a class="reto" href="{RETO["url"]}" target="_blank" rel="noopener">🔪 {t[0]} #{RETO["n"]}: '
        f'<b>{RETO["killer"]} {t[1]} {RETO["loc"]}</b> · {pc}{t[4]} →</a>\n'
    )
    return cuerpo[:i] + franja + cuerpo[i:]
