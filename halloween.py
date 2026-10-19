"""Página de temporada: qué caja de Final Girl jugar la noche de Halloween.

Todo sale de datos reales: el % de victorias de la hoja comunitaria (cajas
con 50 partidas o más) y los votos de "caja más inmersiva" de los tops, que
se leen de su hoja al montar (si no hay red, esa sección no sale).
"""
import csv
import io
import urllib.request

import paginas as P

SALIDA = "halloween.html"
MIN = 50
HOJA_TOPS = "https://docs.google.com/spreadsheets/d/1pFBklqcyVw17038m-NPmq7Q_CVnMBMELxNN6lyFTMZU/gviz/tq?tqx=out:csv"

T = {
    "es": {
        "title": "Final Girl para Halloween: qué caja jugar la noche del 31 (con datos reales)",
        "desc": "Qué caja de Final Girl jugar en Halloween: las más inmersivas según la comunidad, las más difíciles para pasar miedo y las más fáciles para estrenarse. Con el % de victorias de miles de partidas.",
        "eb": "Especial Halloween · 31 de octubre",
        "h1": 'Final Girl<span class="roja">para Halloween</span>',
        "dek": "¿Una partida de terror para la noche del 31? Elige caja según lo que busques, con el % de victorias de {n} partidas reales y los votos de la comunidad.",
        "inm": "Las más inmersivas", "inm_s": "Las que más meten en la peli, según los votos de la comunidad en los tops.",
        "dif": "Para pasar miedo de verdad", "dif_s": "Las cajas donde menos se gana. Para quien quiere sufrir.",
        "fac": "Para estrenarse esta noche", "fac_s": "Las cajas donde más se gana. Buenas para quien juega por primera vez.",
        "vic": "de victorias", "par": "partidas", "pts": "pts",
        "fin": "¿Ya la has jugado? <a href=\"registrar.html\">Registra tu partida</a>, <a href=\"tops.html#comunidad\">vota tus tops</a> o <a href=\"crear-tier-list.html\">crea tu tier list</a>.",
        "nota": "Cajas con al menos {m} partidas registradas.",
    },
    "en": {
        "title": "Final Girl for Halloween: which box to play on the 31st (by the numbers)",
        "desc": "Which Final Girl box to play on Halloween: the most immersive according to the community, the hardest to really get scared and the easiest to start with. With win rates from thousands of games.",
        "eb": "Halloween special · October 31",
        "h1": 'Final Girl<span class="roja">for Halloween</span>',
        "dek": "A horror game for the night of the 31st? Pick a box by what you're after, with win rates from {n} real games and the community's votes.",
        "inm": "The most immersive", "inm_s": "The ones that pull you into the movie the most, by community votes in the tops.",
        "dif": "To really get scared", "dif_s": "The boxes with the lowest win rate. For those who want to suffer.",
        "fac": "To start tonight", "fac_s": "The boxes with the highest win rate. Good for a first game.",
        "vic": "win rate", "par": "games", "pts": "pts",
        "fin": "Already played it? <a href=\"registrar.html\">Log your game</a>, <a href=\"tops.html#comunidad\">vote your tops</a> or <a href=\"crear-tier-list.html\">make your tier list</a>.",
        "nota": "Boxes with at least {m} logged games.",
    },
}


def _inmersivas():
    """Puntos de 'caja más inmersiva' (3/2/1), solo el último voto de cada navegador."""
    try:
        txt = urllib.request.urlopen(HOJA_TOPS, timeout=15).read().decode("utf-8")
    except Exception:
        return []
    filas = list(csv.reader(io.StringIO(txt)))
    if not filas:
        return []
    cab = filas[0]
    cols = [cab.index(f"most_immersive_box #{i}") for i in (1, 2, 3)]
    uid = cab.index("id") if "id" in cab else None
    pts, vistos = {}, set()
    for f in reversed(filas[1:]):
        v = [f[c] if c < len(f) else "" for c in cols]
        if not any(v):
            continue
        u = f[uid] if uid is not None and uid < len(f) else ""
        if u:
            if u in vistos:
                continue
            vistos.add(u)
        for i, x in enumerate(v):
            if x:
                pts[x] = pts.get(x, 0) + 3 - i
    return sorted(pts.items(), key=lambda kv: -kv[1])[:5]


def _tarjetas(cajas, pre, t, extra=None):
    out = []
    for f in cajas:
        img = f'<img src="{pre}{f["img"]}" alt="" loading="lazy">' if f.get("img") else ""
        dato = extra(f) if extra else f'{P.pc(f["wr"])} {t["vic"]} · {f["plays"]} {t["par"]}'
        out.append(f'<a class="hw-c" href="{P.slug(f["film"])}.html">{img}<span><b>{f["film"]}</b>'
                   f'<i>{f["killer"]} · {f["loc"]}</i><em>{dato}</em></span></a>')
    return '<div class="hw-g">' + "".join(out) + "</div>"


def pagina(lang):
    t = T[lang]
    pre = "" if lang == "es" else "../"
    films = {f["film"]: f for f in P.D["films"]}
    con = [f for f in P.D["films"] if f["plays"] >= MIN]
    tot = P.D["meta"]["total"]; n = f"{tot:,}".replace(",", "." if lang == "es" else ",")
    css = """<style>
.hw-g{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:14px;margin:12px 0 8px}
.hw-c{position:relative;display:block;aspect-ratio:3/4;overflow:hidden;border:1px solid var(--line);border-radius:3px;color:#fff;text-decoration:none;background:var(--sunk)}
.hw-c img{width:100%;height:100%;object-fit:cover;object-position:center 62%;display:block;transition:transform .3s}
.hw-c:hover img{transform:scale(1.05)}
.hw-c span{position:absolute;inset:auto 0 0 0;padding:40px 12px 10px;background:linear-gradient(transparent,rgba(0,0,0,.9));display:flex;flex-direction:column;gap:2px}
.hw-c b{font-size:16px}.hw-c i{font-style:normal;font-size:12px;opacity:.8}
.hw-c em{font-style:normal;font-family:var(--f-mono);font-size:12px;color:#ffb3b8}
</style>"""
    h = [f'<p class="eyebrow">🎃 {t["eb"]}</p>', f'<h1>{t["h1"]}</h1>',
         f'<p class="dek">{t["dek"].format(n=n)}</p></header>', css]
    inm = [(films[k], p) for k, p in _inmersivas() if k in films]
    if inm:
        ptos = dict((f["film"], p) for f, p in inm)
        h += [f'<h2>{t["inm"]}</h2><p class="sub">{t["inm_s"]}</p>',
              _tarjetas([f for f, _ in inm], pre, t, lambda f: f'{ptos[f["film"]]} {t["pts"]} · {P.pc(f["wr"])} {t["vic"]}')]
    h += [f'<h2>{t["dif"]}</h2><p class="sub">{t["dif_s"]}</p>', _tarjetas(sorted(con, key=lambda f: f["wr"])[:5], pre, t),
          f'<h2>{t["fac"]}</h2><p class="sub">{t["fac_s"]}</p>', _tarjetas(sorted(con, key=lambda f: -f["wr"])[:5], pre, t),
          f'<p class="sub">{t["nota"].format(m=MIN)}</p>', f'<p>{t["fin"]}</p>']
    return t["title"], t["desc"][:158], "\n".join(h)
