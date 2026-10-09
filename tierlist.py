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
 "es": {"title": "Tier list de dificultad de Final Girl: cajas, killers y mapas ({n} partidas)",
        "desc": "Tier list de Final Girl con datos reales: cajas, killers y mapas de S a D por % de victorias en {n} partidas, y los tops que vota la comunidad.",
        "eb": "Por dificultad · {n} partidas reales", "h1": "Tier list de dificultad<span class=\"roja\">Final Girl</span>",
        "dek": "Cajas, killers y localizaciones ordenados de S a D por dificultad. No es una opinión: sale del % de victorias de {n} partidas registradas por la comunidad. Debajo, los tops que vota la gente.",
        "leyenda": "S: menos del 55% de victorias, lo más duro · A: 55–62% · B: 62–69% · C: 69–75% · D: 75% o más, lo más asequible. Media de todas las partidas: {media}.",
        "cajas": "Dificultad de las cajas", "killers": "Dificultad de los killers", "mapas": "Dificultad de las localizaciones",
        "nota_k": "Solo killers con 60 partidas o más.", "nota_m": "Solo localizaciones con 60 partidas o más.",
        "vic": "victorias", "part": "part.", "com": "Tops de la comunidad",
        "com_sub": "Aquí no mandan los datos sino los votos: mejor temporada, mejor película, mejor killer, la caja más fácil, la más difícil, la más inmersiva, la peor y la mejor localización. Vota el tuyo."},
 "en": {"title": "Final Girl difficulty tier list: boxes, killers and maps ({n} games)",
        "desc": "Final Girl tier list from real data: every box, killer and map ranked S to D by win rate across {n} games, plus community-voted tops.",
        "eb": "By difficulty · {n} real games", "h1": "Final Girl<span class=\"roja\">difficulty tier list</span>",
        "dek": "Boxes, killers and locations ranked S to D by difficulty. Not an opinion: it comes from the win rate of {n} games logged by the community. Below, the tops players vote for.",
        "leyenda": "S: under 55% wins, the hardest · A: 55–62% · B: 62–69% · C: 69–75% · D: 75% or more, the most forgiving. Average across all games: {media}.",
        "cajas": "Box difficulty", "killers": "Killer difficulty", "mapas": "Location difficulty",
        "nota_k": "Only killers with 60+ games.", "nota_m": "Only locations with 60+ games.",
        "vic": "wins", "part": "games", "com": "Community tops",
        "com_sub": "Here votes rule, not data: best series, best movie, best killer, easiest box, hardest, most immersive, worst and best location. Cast yours."},
 "fr": {"title": "Tier list Final Girl : classement des boîtes, killers et cartes ({n} parties)",
        "desc": "Tier list Final Girl : boîtes, killers et lieux de S à D selon le taux de victoire sur {n} parties, et les tops votés par la communauté.",
        "eb": "Par difficulté · {n} parties réelles", "h1": "Tier list de difficulté<span class=\"roja\">Final Girl</span>",
        "dek": "Boîtes, killers et lieux classés de S à D par difficulté. Ce n'est pas un avis : cela vient du taux de victoire de {n} parties enregistrées par la communauté. En dessous, les tops votés par les joueurs.",
        "leyenda": "S : moins de 55 % de victoires, le plus dur · A : 55–62 % · B : 62–69 % · C : 69–75 % · D : 75 % ou plus, le plus abordable. Moyenne de toutes les parties : {media}.",
        "cajas": "Difficulté des boîtes", "killers": "Difficulté des killers", "mapas": "Difficulté des lieux",
        "nota_k": "Seulement les killers avec 60 parties ou plus.", "nota_m": "Seulement les lieux avec 60 parties ou plus.",
        "vic": "victoires", "part": "parties", "com": "Tops de la communauté",
        "com_sub": "Ici ce sont les votes qui comptent : meilleure saison, meilleur film, meilleur killer, boîte la plus facile, la plus difficile, la plus immersive, la pire et le meilleur lieu. Votez."},
 "de": {"title": "Final Girl Tier List: Boxen, Killer und Karten im Ranking ({n} Partien)",
        "desc": "Final Girl Tier List aus echten Daten: Boxen, Killer und Schauplätze von S bis D nach Siegquote aus {n} Partien, dazu Community-Tops.",
        "eb": "Nach Schwierigkeit · {n} echte Partien", "h1": "Final Girl<span class=\"roja\">Schwierigkeits-Tier-List</span>",
        "dek": "Boxen, Killer und Schauplätze von S bis D nach Schwierigkeit. Keine Meinung: Grundlage ist die Siegquote aus {n} Partien der Community. Darunter die Tops, über die die Spieler abstimmen.",
        "leyenda": "S: unter 55 % Siege, am schwersten · A: 55–62 % · B: 62–69 % · C: 69–75 % · D: 75 % oder mehr, am gnädigsten. Durchschnitt aller Partien: {media}.",
        "cajas": "Schwierigkeit der Boxen", "killers": "Schwierigkeit der Killer", "mapas": "Schwierigkeit der Schauplätze",
        "nota_k": "Nur Killer mit mindestens 60 Partien.", "nota_m": "Nur Schauplätze mit mindestens 60 Partien.",
        "vic": "Siege", "part": "Partien", "com": "Community-Tops",
        "com_sub": "Hier zählen Stimmen, nicht Daten: beste Staffel, bester Film, bester Killer, leichteste Box, schwerste, atmosphärischste, schlechteste und bester Schauplatz. Stimm ab."},
 "it": {"title": "Tier list Final Girl: classifica di scatole, killer e mappe ({n} partite)",
        "desc": "Tier list di Final Girl: scatole, killer e mappe da S a D per percentuale di vittorie su {n} partite, più i top votati dalla community.",
        "eb": "Per difficoltà · {n} partite reali", "h1": "Tier list di difficoltà<span class=\"roja\">Final Girl</span>",
        "dek": "Scatole, killer e ambientazioni da S a D per difficoltà. Non è un'opinione: viene dalla percentuale di vittorie di {n} partite registrate dalla community. Sotto, i top votati dai giocatori.",
        "leyenda": "S: meno del 55% di vittorie, il più duro · A: 55–62% · B: 62–69% · C: 69–75% · D: 75% o più, il più abbordabile. Media di tutte le partite: {media}.",
        "cajas": "Difficoltà delle scatole", "killers": "Difficoltà dei killer", "mapas": "Difficoltà delle ambientazioni",
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
  #comunidad { margin-top:40px; }
  .tl-faq { margin-bottom:10px; }
  .tl-faq details { border-top:1px solid var(--line); padding:10px 2px; }
  .tl-faq details:last-child { border-bottom:1px solid var(--line); }
  .tl-faq summary { cursor:pointer; font-weight:600; }
  .tl-faq p { margin:8px 0 2px; color:var(--muted); }
  .tl-it .fg-tuya { display:block; width:max-content; margin:0 0 2px; font-size:9px; }
  .tl-it:has(.fg-tuya) { outline:2px solid var(--blood); outline-offset:-2px; }
  @media (max-width:560px){ .tl-l { width:40px; font-size:20px; } .tl-it { width:84px; height:84px; } }
</style>"""


# Preguntas que la gente busca tal cual. Las respuestas salen de los datos.
FAQ = {
 "es": {"h": "Preguntas frecuentes",
        "q": ["¿Cuál es la caja más difícil de Final Girl?", "¿Cuál es la caja más fácil de Final Girl?",
              "¿Cuál es el killer más difícil de Final Girl?", "¿Cuál es el killer más fácil?",
              "¿Qué localización es la más dura?", "¿Cómo se hace esta tier list?"],
        "a": ["{c0}, con un {c0w} de victorias en {c0g} partidas. Le siguen {c1} ({c1w}) y {c2} ({c2w}).",
              "{cz}, con un {czw} de victorias en {czg} partidas. Detrás van {cy} ({cyw}) y {cx} ({cxw}).",
              "{k0}: solo se le gana el {k0w} de las veces ({k0g} partidas). Después, {k1} ({k1w}) y {k2} ({k2w}).",
              "{kz}, con un {kzw} de victorias en {kzg} partidas.",
              "{m0}, con un {m0w} de victorias en {m0g} partidas.",
              "Con el % de victorias de {n} partidas reales que la comunidad apunta en una hoja pública. S es menos del 55% de victorias y D, el 75% o más. Se actualiza con los datos."]},
 "en": {"h": "FAQ",
        "q": ["What is the hardest Final Girl box?", "What is the easiest Final Girl box?",
              "Who is the hardest killer in Final Girl?", "Who is the easiest killer?",
              "Which location is the hardest?", "How is this tier list made?"],
        "a": ["{c0}, with a win rate of {c0w} over {c0g} games. Next come {c1} ({c1w}) and {c2} ({c2w}).",
              "{cz}, with a win rate of {czw} over {czg} games. Then {cy} ({cyw}) and {cx} ({cxw}).",
              "{k0}: players beat it only {k0w} of the time ({k0g} games). Then {k1} ({k1w}) and {k2} ({k2w}).",
              "{kz}, with a win rate of {kzw} over {kzg} games.",
              "{m0}, with a win rate of {m0w} over {m0g} games.",
              "From the win rate of {n} real games the community logs in a public sheet. S is under 55% wins, D is 75% or more. It updates with the data."]},
 "fr": {"h": "Questions fréquentes",
        "q": ["Quelle est la boîte la plus difficile de Final Girl ?", "Quelle est la boîte la plus facile ?",
              "Quel est le killer le plus difficile de Final Girl ?", "Quel est le killer le plus facile ?",
              "Quel lieu est le plus dur ?", "Comment cette tier list est-elle faite ?"],
        "a": ["{c0}, avec {c0w} de victoires sur {c0g} parties. Suivent {c1} ({c1w}) et {c2} ({c2w}).",
              "{cz}, avec {czw} de victoires sur {czg} parties. Puis {cy} ({cyw}) et {cx} ({cxw}).",
              "{k0} : on ne le bat que {k0w} du temps ({k0g} parties). Puis {k1} ({k1w}) et {k2} ({k2w}).",
              "{kz}, avec {kzw} de victoires sur {kzg} parties.",
              "{m0}, avec {m0w} de victoires sur {m0g} parties.",
              "À partir du taux de victoire de {n} parties réelles notées par la communauté dans une feuille publique. S : moins de 55 % de victoires, D : 75 % ou plus. Mise à jour avec les données."]},
 "de": {"h": "Häufige Fragen",
        "q": ["Welche Final-Girl-Box ist am schwersten?", "Welche Box ist am leichtesten?",
              "Welcher Killer ist in Final Girl am schwersten?", "Welcher Killer ist am leichtesten?",
              "Welcher Schauplatz ist am härtesten?", "Wie entsteht diese Tier List?"],
        "a": ["{c0}, mit {c0w} Siegen in {c0g} Partien. Danach {c1} ({c1w}) und {c2} ({c2w}).",
              "{cz}, mit {czw} Siegen in {czg} Partien. Dann {cy} ({cyw}) und {cx} ({cxw}).",
              "{k0}: Nur {k0w} der Partien werden gewonnen ({k0g} Partien). Danach {k1} ({k1w}) und {k2} ({k2w}).",
              "{kz}, mit {kzw} Siegen in {kzg} Partien.",
              "{m0}, mit {m0w} Siegen in {m0g} Partien.",
              "Aus der Siegquote von {n} echten Partien, die die Community in einer öffentlichen Tabelle einträgt. S: unter 55 % Siege, D: 75 % oder mehr. Wird mit den Daten aktualisiert."]},
 "it": {"h": "Domande frequenti",
        "q": ["Qual è la scatola più difficile di Final Girl?", "Qual è la scatola più facile?",
              "Qual è il killer più difficile di Final Girl?", "Qual è il killer più facile?",
              "Quale ambientazione è la più dura?", "Come è fatta questa tier list?"],
        "a": ["{c0}, con il {c0w} di vittorie su {c0g} partite. Seguono {c1} ({c1w}) e {c2} ({c2w}).",
              "{cz}, con il {czw} di vittorie su {czg} partite. Poi {cy} ({cyw}) e {cx} ({cxw}).",
              "{k0}: si vince solo il {k0w} delle volte ({k0g} partite). Poi {k1} ({k1w}) e {k2} ({k2w}).",
              "{kz}, con il {kzw} di vittorie su {kzg} partite.",
              "{m0}, con il {m0w} di vittorie su {m0g} partite.",
              "Dalla percentuale di vittorie di {n} partite reali che la community registra in un foglio pubblico. S: meno del 55% di vittorie, D: 75% o più. Si aggiorna con i dati."]},
}


def _faq(lang, cajas, killers, mapas, n):
    import json as _j
    f = FAQ[lang]
    v = {"n": n}
    for pre, items in (("c", cajas), ("k", killers), ("m", mapas)):
        o = sorted(items, key=lambda x: x[1])
        for i, it in enumerate(o[:3]):
            v[f"{pre}{i}"], v[f"{pre}{i}w"], v[f"{pre}{i}g"] = it[0], I.pc(it[1], lang, 0), I.num(it[2], lang)
        for letra, it in zip("zyx", o[::-1][:3]):
            v[f"{pre}{letra}"], v[f"{pre}{letra}w"], v[f"{pre}{letra}g"] = it[0], I.pc(it[1], lang, 0), I.num(it[2], lang)
    pares = [(q, a.format(**v)) for q, a in zip(f["q"], f["a"])]
    html = f'<h2 id="faq">{f["h"]}</h2><div class="tl-faq">' + "".join(
        f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in pares) + "</div>"
    ld = {"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": lang,
          "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in pares]}
    lista = {"@context": "https://schema.org", "@type": "ItemList", "name": T[lang]["cajas"],
             "itemListOrder": "https://schema.org/ItemListOrderAscending",
             "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": c[0]}
                                 for i, c in enumerate(sorted(cajas, key=lambda x: x[1]))]}
    return html + "".join('<script type="application/ld+json">' + _j.dumps(x, ensure_ascii=False) + "</script>" for x in (ld, lista))


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
         _faq(lang, cajas, killers, mapas, n),
         f'<h2 id="comunidad">{t["com"]}</h2><p class="sub">{t["com_sub"]}</p>',
         # La sección de la pestaña Tops, visible y sin su propio título.
         tops.seccion(lang).replace('<section id="v-tops" hidden>', '<section id="v-tops">', 1)
             .replace(f'<h2>{tops.T[lang]["h2"]}</h2>', "", 1)
             .replace(f'<p class="sub">{tops.T[lang]["sub0"]}</p>', "", 1),
         ESTILO]
    return (t["title"].format(n=n), t["desc"].format(n=n)[:158], "\n".join(h))
