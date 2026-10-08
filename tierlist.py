#!/usr/bin/env python3
"""Página "Tier list": cajas, killers y mapas por tramos de % de victorias,
más los tops que vota la comunidad.

Existe para quien busca "Final Girl tier list", "ranking" o "tops": el
ranking de la pestaña Tops se carga con JavaScript y un buscador apenas lo
ve; aquí la tier list va escrita en el HTML.

Los tramos son fijos y se explican en la propia página. No es opinión: sale
del % de victorias de las partidas registradas. S es lo más duro.
"""
import pathlib

import idiomas as I
import paginas as P
import tops

AQUI = pathlib.Path(__file__).parent

# (letra, tope superior de % de victorias). Lo que no entra en ninguno, D.
TRAMOS = [("S", 0.55), ("A", 0.62), ("B", 0.69), ("C", 0.75)]
MIN_MAPA = 60

T = {
 "es": {"title": "Tier list de Final Girl: ranking de cajas, killers y mapas ({n} partidas)",
        "desc": "Tier list de Final Girl con datos reales: cajas, killers y mapas de S a D por % de victorias en {n} partidas, y los tops que vota la comunidad.",
        "eb": "Ranking · {n} partidas reales", "h1": "Tier list<span class=\"roja\">Final Girl</span>",
        "dek": "Cajas, killers y localizaciones ordenados de S a D por dificultad. No es una opinión: sale del % de victorias de {n} partidas registradas por la comunidad. Debajo, los tops que vota la gente.",
        "leyenda": "S: menos del 55% de victorias, lo más duro · A: 55–62% · B: 62–69% · C: 69–75% · D: 75% o más, lo más asequible. Media de todas las partidas: {media}.",
        "cajas": "Tier list de cajas", "killers": "Tier list de killers", "mapas": "Tier list de localizaciones",
        "nota_k": "Solo killers con 60 partidas o más.", "nota_m": "Solo localizaciones con 60 partidas o más.",
        "vic": "victorias", "part": "part.", "com": "Tops de la comunidad",
        "com_sub": "Aquí no mandan los datos sino los votos: mejor temporada, mejor película, mejor killer, la caja más fácil, la más difícil, la más inmersiva, la peor y la mejor localización. Vota el tuyo."},
 "en": {"title": "Final Girl tier list: boxes, killers and maps ranked ({n} games)",
        "desc": "Final Girl tier list from real data: every box, killer and map ranked S to D by win rate across {n} games, plus community-voted tops.",
        "eb": "Rankings · {n} real games", "h1": "Final Girl<span class=\"roja\">tier list</span>",
        "dek": "Boxes, killers and locations ranked S to D by difficulty. Not an opinion: it comes from the win rate of {n} games logged by the community. Below, the tops players vote for.",
        "leyenda": "S: under 55% wins, the hardest · A: 55–62% · B: 62–69% · C: 69–75% · D: 75% or more, the most forgiving. Average across all games: {media}.",
        "cajas": "Box tier list", "killers": "Killer tier list", "mapas": "Location tier list",
        "nota_k": "Only killers with 60+ games.", "nota_m": "Only locations with 60+ games.",
        "vic": "wins", "part": "games", "com": "Community tops",
        "com_sub": "Here votes rule, not data: best series, best movie, best killer, easiest box, hardest, most immersive, worst and best location. Cast yours."},
 "fr": {"title": "Tier list Final Girl : classement des boîtes, killers et cartes ({n} parties)",
        "desc": "Tier list Final Girl : boîtes, killers et lieux de S à D selon le taux de victoire sur {n} parties, et les tops votés par la communauté.",
        "eb": "Classement · {n} parties réelles", "h1": "Tier list<span class=\"roja\">Final Girl</span>",
        "dek": "Boîtes, killers et lieux classés de S à D par difficulté. Ce n'est pas un avis : cela vient du taux de victoire de {n} parties enregistrées par la communauté. En dessous, les tops votés par les joueurs.",
        "leyenda": "S : moins de 55 % de victoires, le plus dur · A : 55–62 % · B : 62–69 % · C : 69–75 % · D : 75 % ou plus, le plus abordable. Moyenne de toutes les parties : {media}.",
        "cajas": "Tier list des boîtes", "killers": "Tier list des killers", "mapas": "Tier list des lieux",
        "nota_k": "Seulement les killers avec 60 parties ou plus.", "nota_m": "Seulement les lieux avec 60 parties ou plus.",
        "vic": "victoires", "part": "parties", "com": "Tops de la communauté",
        "com_sub": "Ici ce sont les votes qui comptent : meilleure saison, meilleur film, meilleur killer, boîte la plus facile, la plus difficile, la plus immersive, la pire et le meilleur lieu. Votez."},
 "de": {"title": "Final Girl Tier List: Boxen, Killer und Karten im Ranking ({n} Partien)",
        "desc": "Final Girl Tier List aus echten Daten: Boxen, Killer und Schauplätze von S bis D nach Siegquote aus {n} Partien, dazu Community-Tops.",
        "eb": "Ranking · {n} echte Partien", "h1": "Final Girl<span class=\"roja\">Tier List</span>",
        "dek": "Boxen, Killer und Schauplätze von S bis D nach Schwierigkeit. Keine Meinung: Grundlage ist die Siegquote aus {n} Partien der Community. Darunter die Tops, über die die Spieler abstimmen.",
        "leyenda": "S: unter 55 % Siege, am schwersten · A: 55–62 % · B: 62–69 % · C: 69–75 % · D: 75 % oder mehr, am gnädigsten. Durchschnitt aller Partien: {media}.",
        "cajas": "Tier List der Boxen", "killers": "Tier List der Killer", "mapas": "Tier List der Schauplätze",
        "nota_k": "Nur Killer mit mindestens 60 Partien.", "nota_m": "Nur Schauplätze mit mindestens 60 Partien.",
        "vic": "Siege", "part": "Partien", "com": "Community-Tops",
        "com_sub": "Hier zählen Stimmen, nicht Daten: beste Staffel, bester Film, bester Killer, leichteste Box, schwerste, atmosphärischste, schlechteste und bester Schauplatz. Stimm ab."},
 "it": {"title": "Tier list Final Girl: classifica di scatole, killer e mappe ({n} partite)",
        "desc": "Tier list di Final Girl: scatole, killer e mappe da S a D per percentuale di vittorie su {n} partite, più i top votati dalla community.",
        "eb": "Classifica · {n} partite reali", "h1": "Tier list<span class=\"roja\">Final Girl</span>",
        "dek": "Scatole, killer e ambientazioni da S a D per difficoltà. Non è un'opinione: viene dalla percentuale di vittorie di {n} partite registrate dalla community. Sotto, i top votati dai giocatori.",
        "leyenda": "S: meno del 55% di vittorie, il più duro · A: 55–62% · B: 62–69% · C: 69–75% · D: 75% o più, il più abbordabile. Media di tutte le partite: {media}.",
        "cajas": "Tier list delle scatole", "killers": "Tier list dei killer", "mapas": "Tier list delle ambientazioni",
        "nota_k": "Solo killer con almeno 60 partite.", "nota_m": "Solo ambientazioni con almeno 60 partite.",
        "vic": "vittorie", "part": "partite", "com": "Top della community",
        "com_sub": "Qui contano i voti, non i dati: miglior stagione, miglior film, miglior killer, scatola più facile, più difficile, più immersiva, peggiore e miglior ambientazione. Vota."},
}

ESTILO = """<style>
  .tl { margin:10px 0 26px; border:1px solid var(--line); border-radius:3px; overflow:hidden; }
  .tl-fila { display:flex; border-top:1px solid var(--line); background:var(--surface); }
  .tl-fila:first-child { border-top:0; }
  .tl-l { flex:none; width:56px; display:flex; align-items:center; justify-content:center;
          font-weight:800; font-size:26px; color:#fff; }
  .tl-S .tl-l { background:#b3122a; } .tl-A .tl-l { background:#c8452c; } .tl-B .tl-l { background:#b8862b; }
  .tl-C .tl-l { background:#5f8a3a; } .tl-D .tl-l { background:#2f7a6b; }
  .tl-items { display:flex; flex-wrap:wrap; gap:8px; padding:8px; min-height:60px; }
  .tl-it { position:relative; width:104px; height:104px; border-radius:3px; overflow:hidden; background:var(--sunk);
           color:#fff; text-decoration:none; display:block; }
  .tl-it img { width:100%; height:100%; object-fit:cover; object-position:center 62%; display:block; }
  .tl-it img[src*="art/"] { object-position:center 25%; }
  .tl-it span { position:absolute; left:0; right:0; bottom:0; padding:16px 5px 4px; font-size:11.5px; line-height:1.2;
                font-weight:600; background:linear-gradient(transparent,rgba(0,0,0,.9)); }
  .tl-it b { display:block; font-family:var(--f-mono); font-size:10.5px; font-weight:400; opacity:.85; }
  .tl-ley { font-size:13px; }
  .tl-it .fg-tuya { display:block; width:max-content; margin:0 0 2px; font-size:9px; }
  .tl-it:has(.fg-tuya) { outline:2px solid var(--blood); outline-offset:-2px; }
  @media (max-width:560px){ .tl-l { width:40px; font-size:20px; } .tl-it { width:84px; height:84px; } }
</style>"""


def _tramo(wr):
    for letra, tope in TRAMOS:
        if wr < tope:
            return letra
    return "D"


def _tier(items, lang, pre, cajas=False):
    """items: (nombre, wr, partidas, enlace o None, imagen o None)."""
    t = T[lang]
    grupos = {l: [] for l in "SABCD"}
    for it in sorted(items, key=lambda x: x[1]):
        grupos[_tramo(it[1])].append(it)
    filas = []
    for letra in "SABCD":
        celdas = []
        for nombre, wr, g, href, img in grupos[letra]:
            tag = f'a href="{href}"' if href else "div"
            foto = f'<img src="{pre}{img}" alt="{nombre}" loading="lazy">' if img else ""
            dc = f' data-caja="{nombre}"' if cajas else ""
            celdas.append(f'<{tag} class="tl-it">{foto}<span{dc}>{nombre}'
                          f'<b>{I.pc(wr, lang, 0)} {t["vic"]} · {I.num(g, lang)} {t["part"]}</b></span></{tag.split()[0]}>')
        filas.append(f'<div class="tl-fila tl-{letra}"><div class="tl-l">{letra}</div>'
                     f'<div class="tl-items">{"".join(celdas)}</div></div>')
    return '<div class="tl">' + "".join(filas) + "</div>"


def pagina(lang):
    """(title, desc, cuerpo) con el mismo formato que las fichas."""
    t = T[lang]
    D = P.D
    m = D["meta"]
    n = I.num(m["total"], lang)
    pre = "" if lang == "es" else "../"
    img = tops._imagenes()
    cajas = [(f["film"], f["wr"], f["plays"], P.slug(f["film"]) + ".html", img.get(f["film"])) for f in D["films"]]
    killers = [(nm, k["wr"], k["g"], P.slug(nm) + ".html", img.get(nm))
               for nm, k in P.KILLERS.items() if k.get("g", 0) >= 60]
    mapas = [(l[0], l[1], l[2], None, img.get(l[0])) for l in D["locs"] if l[2] >= MIN_MAPA]
    h = [f'<p class="eyebrow">{t["eb"].format(n=n)}</p>',
         f'<h1>{t["h1"]}</h1>',
         f'<p class="dek">{t["dek"].format(n=n)}</p></header>',
         f'<p class="sub tl-ley">{t["leyenda"].format(media=I.pc(m["wr"], lang))}</p>',
         f'<h2>{t["cajas"]}</h2>', _tier(cajas, lang, pre, True),
         f'<h2>{t["killers"]}</h2><p class="sub">{t["nota_k"]}</p>', _tier(killers, lang, pre),
         f'<h2>{t["mapas"]}</h2><p class="sub">{t["nota_m"]}</p>', _tier(mapas, lang, pre),
         f'<h2 id="comunidad">{t["com"]}</h2><p class="sub">{t["com_sub"]}</p>',
         # La sección de la pestaña Tops, visible y sin su propio título.
         tops.seccion(lang).replace('<section id="v-tops" hidden>', '<section id="v-tops">', 1)
             .replace(f'<h2>{tops.T[lang]["h2"]}</h2>', "", 1),
         ESTILO]
    return (t["title"].format(n=n), t["desc"].format(n=n)[:158], "\n".join(h))
