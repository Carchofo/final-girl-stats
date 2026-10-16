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
    "es": ("Reto de la semana", "en", "de victorias", "partidas", "Comenta tu partida en r/finalgirl"),
    "en": ("Weekly challenge", "at", "win rate", "games", "Share your game on r/finalgirl"),
    "fr": ("Défi de la semaine", "à", "de victoires", "parties", "Racontez votre partie sur r/finalgirl"),
    "de": ("Challenge der Woche", "auf", "Siegquote", "Partien", "Erzähl deine Partie auf r/finalgirl"),
    "it": ("Sfida della settimana", "a", "di vittorie", "partite", "Racconta la tua partita su r/finalgirl"),
}


def _celda(killer, loc):
    s = (AQUI / "src" / "cuerpo.html").read_text(encoding="utf-8")
    D = json.loads(re.search(r"var D = (\{.*?\});\n", s, re.S).group(1))
    return (D["cells"].get(loc) or {}).get(killer)


def poner(cuerpo, lang):
    """Tarjeta tipo noticia justo encima de las pestañas de la portada."""
    if not RETO or 'class="reto"' in cuerpo:
        return cuerpo
    i = cuerpo.find('<nav class="tabs"')
    if i < 0:
        return cuerpo
    import paginas
    t = T[lang]
    pre = "" if lang == "es" else "../"
    arte = f"img/art/{paginas.slug(RETO['killer'])}.jpg"
    img = f'<img src="{pre}{arte}" alt="" loading="lazy">' if (AQUI / arte).exists() else ""
    c = _celda(RETO["killer"], RETO["loc"])
    pc = f'{c[1] * 100:.0f}% {t[2]} · {c[0]} {t[3]}' if c else ""
    franja = (
        '<style>.reto{display:flex;gap:14px;align-items:stretch;margin:0 0 16px;border:1px solid #3a2a2c;'
        'background:#151012;color:inherit;text-decoration:none;overflow:hidden}'
        '.reto img{width:110px;object-fit:cover;object-position:50% 25%;flex:none}'
        '.reto div{padding:10px 14px 12px 0;display:flex;flex-direction:column;gap:4px}'
        '.reto small{font-family:var(--f-mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--blood)}'
        '.reto strong{font-family:"Anton",var(--f-disp);font-weight:400;font-size:26px;line-height:1;letter-spacing:.03em;text-transform:uppercase}'
        '.reto span{font-size:13px;opacity:.75}.reto em{font-style:normal;font-weight:600;color:var(--blood);font-size:14px}'
        '.reto:hover{border-color:var(--blood)}@media(max-width:560px){.reto img{width:84px}.reto strong{font-size:20px}}</style>'
        f'<a class="reto" href="{RETO["url"]}" target="_blank" rel="noopener">{img}<div>'
        f'<small>🔪 {t[0]} #{RETO["n"]}</small>'
        f'<strong>{RETO["killer"]} {t[1]} {RETO["loc"]}</strong>'
        + (f'<span>{pc}</span>' if pc else '') +
        f'<em>{t[4]} →</em></div></a>\n'
    )
    return cuerpo[:i] + franja + cuerpo[i:]
