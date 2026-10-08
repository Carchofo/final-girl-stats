#!/usr/bin/env python3
"""Versiones en inglés, francés, alemán e italiano de las fichas.

Por qué existe: casi todo el que busca Final Girl lo busca en inglés, y
detrás van Alemania, Francia e Italia. Con la web solo en español, Google
no tiene nada que enseñarles.

Se traducen las páginas que se generan desde datos (killers, cajas e
índice), que es donde están las búsquedas concretas. La página grande y
la de salidas están escritas a mano en español; cada idioma tiene su
propia portada que enlaza a ellas avisando de que están en español.

Cada página declara sus equivalentes con hreflang: así Google enseña a
cada visitante la de su idioma en vez de tratarlas como copias.

Los textos de juego (quién es cada killer, consejos del foro) están en
textos_<idioma>.json. Las cifras salen de los mismos datos que la versión
española, así que nunca pueden decir cosas distintas.

Uso: lo llama montar.py.
"""
import json
import pathlib
import re

import mecanicas
import paginas as P

AQUI = pathlib.Path(__file__).parent
IDIOMAS = ["en", "fr", "de", "it"]
LOCALE = {"es": "es_ES", "en": "en_US", "fr": "fr_FR", "de": "de_DE", "it": "it_IT"}

T = {
"en": {
    "nav": ["Stats", "Openings", "All pages"],
    "es_nota": "",
    "killer_eb": "Killer · {n} maps with data",
    "killer_h1": "{wr} win rate",
    "intro": "Across <b>{g} recorded games</b>, the Final Girl beats {k} {wr} of the time. The average for the whole game is {media}, so ",
    "intro_up": "that is above average: one of the easier killers.",
    "intro_down": "that is below average: one of the tough ones.",
    "intro_eq": "that is right on the average.",
    "quien": "Who is {k}", "juega": "How {k} plays",
    "wiki": "Game details from the <a href=\"{u}\" target=\"_blank\" rel=\"noopener\">Final Girl Wiki</a>, under a CC BY-SA licence.",
    "caja": "Comes in the <a href=\"{u}\"><b>{c}</b></a> box", "pareja": ", paired with <b>{l}</b>.",
    "mapa_h3": "The map changes the fight",
    "mapa_p": "On {l}, its box location, the Final Girl wins <b>{a}</b>, against {wr} across all maps: <b>{d} points</b>. ",
    "mapa_neg": "The map works for you, not for the killer.",
    "mapa_pos": "That location suits the killer: don't trust the average.",
    "mapa_fin": " The best map is {m} ({mw}) and the worst is {p} ({pw}).",
    "donde": "Best and worst maps for {k}",
    "donde_sub": "Final Girl win rate on each location, with at least {n} recorded games.",
    "th": ["Location", "Win rate", "Games"],
    "dp": "Dark Powers", "dp1": "Dark Power", "fin": "Finale cards", "fin1": "Finale card",
    "sec_sub": "From the most punishing to the easiest. At least {n} games.",
    "peor": "The worst draw is <b>{c}</b>: with it in play the game is won only {wr} of the time, across {g} games.",
    "foro_k": "What players say",
    "salir": "How to start the game",
    "salir_p": "The four openings and when to use each one are in the <a href=\"salidas.html\">opening strategies</a>. To compare this killer on every map, see the <a href=\"index.html\">full interactive stats</a>.",
    "k_title": "{k} in Final Girl: win rate by map and how to beat {k}",
    "k_desc": "The Final Girl wins {wr} against {k} across {g} games. Best and worst maps, hardest Dark Powers and Finales, and tips.",
    "box_eb": "Box · {f} · {g} games",
    "box_h1": "{wr} win rate",
    "box_dek": "{k} on {l}. Across {g} recorded games it is won {wr} of the time, ",
    "box_dif": "{d} points {dir} the game average ({media}).", "encima": "above", "debajo": "below",
    "box_eq": "right on the game average ({media}).",
    "muestra_h3": "Small sample",
    "muestra_p": "Only {g} recorded games. Split across Dark Powers, Finales and Setups, each breakdown ends up with very few: take them as a hint, not a fact.",
    "particular": "What makes it different",
    "nivel": "Level", "elmapa": "The map",
    "elkiller": "The killer",
    "elkiller_p": "<a href=\"{u}\"><b>{k}</b></a> has a {wr} win rate across all maps, over {g} games. Here, on {l}, the figure is {wr2}.",
    "setups": "Setups", "setup1": "Setup",
    "setups_sub": "From the hardest to the easiest. At least {n} games.",
    "setups_gap": "Between <b>{a}</b> and <b>{b}</b> there are <b>{d} points</b> of difference. The starting setup matters more than it looks.",
    "foro_c": "Tips from players", "reviews": "What reviews say",
    "salir_c": "The four openings, with which one to use depending on the setup, are in the <a href=\"salidas.html\">opening strategies</a>.",
    "c_title": "{c} (Final Girl): stats and tips, {wr} win rate",
    "c_desc": "{k} on {l}. Won {wr} of {g} games. Setups, Dark Powers, Finales and tips.",
    "pie": "Data from the <a href=\"{h}\" target=\"_blank\" rel=\"noopener\">public tracking sheet</a> kept by the Final Girl community (<a href=\"{f}\" target=\"_blank\" rel=\"noopener\">log your games</a>). Back to <a href=\"fichas.html\">all killers and boxes</a>.",
    "hub_title": "Final Girl stats: win rate of every killer and box ({n} games)",
    "hub_desc": "Win rate of every killer and every box in Final Girl, from {n} community games. Hardest killers, best maps, Dark Powers and Finales.",
    "hub_eb": "{n} real games · {j} players",
    "hub_h1": "Final Girl<span class=\"roja\">stats</span>",
    "hub_dek": "How often the Final Girl survives each killer and each box, from {n} games logged by the community. Average win rate: <b>{media}</b>.",
    "hub_lab": "Want to cross any killer with any map? Use the <a href=\"index.html\">full interactive stats</a>.",
    "hub_k": "Killers, hardest first", "hub_c": "Boxes, hardest first",
    "hub_th_k": ["Killer", "Win rate", "Games"], "hub_th_c": ["Box", "Win rate", "Games"],
    "hub_reg": "Played a game? <a href=\"{f}\" target=\"_blank\" rel=\"noopener\">Log it on the community form</a>: every game sharpens these numbers.",
},
"fr": {
    "nav": ["Stats", "Ouvertures", "Fiches"],
    "es_nota": "",
    "killer_eb": "Killer · {n} cartes avec données",
    "killer_h1": "{wr} de victoires",
    "intro": "Sur <b>{g} parties enregistrées</b>, la Final Girl bat {k} dans {wr} des cas. La moyenne du jeu est de {media}, donc ",
    "intro_up": "c'est au-dessus : un des killers les plus abordables.",
    "intro_down": "c'est en dessous : un des plus coriaces.",
    "intro_eq": "c'est pile dans la moyenne.",
    "quien": "Qui est {k}", "juega": "Comment joue {k}",
    "wiki": "Données de jeu tirées du <a href=\"{u}\" target=\"_blank\" rel=\"noopener\">Final Girl Wiki</a>, sous licence CC BY-SA.",
    "caja": "Fourni dans la boîte <a href=\"{u}\"><b>{c}</b></a>", "pareja": ", associé à <b>{l}</b>.",
    "mapa_h3": "La carte change le combat",
    "mapa_p": "Sur {l}, son lieu d'origine, la Final Girl gagne <b>{a}</b>, contre {wr} toutes cartes confondues : <b>{d} points</b>. ",
    "mapa_neg": "La carte joue pour vous, pas pour le killer.",
    "mapa_pos": "Ce lieu lui réussit : ne vous fiez pas à sa moyenne.",
    "mapa_fin": " Sa meilleure carte est {m} ({mw}) et la pire {p} ({pw}).",
    "donde": "Meilleures et pires cartes contre {k}",
    "donde_sub": "Taux de victoire de la Final Girl sur chaque lieu, avec au moins {n} parties enregistrées.",
    "th": ["Lieu", "Victoires", "Parties"],
    "dp": "Dark Powers", "dp1": "Dark Power", "fin": "Cartes Finale", "fin1": "Carte Finale",
    "sec_sub": "De la plus punitive à la plus facile. Au moins {n} parties.",
    "peor": "Le pire tirage est <b>{c}</b> : avec elle en jeu, la partie n'est gagnée que dans {wr} des cas, sur {g} parties.",
    "foro_k": "Ce qu'en disent les joueurs",
    "salir": "Comment démarrer la partie",
    "salir_p": "Les quatre ouvertures et quand utiliser chacune sont dans les <a href=\"salidas.html\">stratégies d'ouverture</a>. Pour comparer ce killer sur toutes les cartes, voir les <a href=\"index.html\">statistiques interactives</a>.",
    "k_title": "{k} dans Final Girl : victoires par carte et comment le battre",
    "k_desc": "La Final Girl gagne {wr} contre {k} sur {g} parties. Meilleures et pires cartes, Dark Powers et Finales les plus durs, et conseils.",
    "box_eb": "Boîte · {f} · {g} parties",
    "box_h1": "{wr} de victoires",
    "box_dek": "{k} sur {l}. Sur {g} parties enregistrées, on gagne dans {wr} des cas, ",
    "box_dif": "{d} points {dir} de la moyenne du jeu ({media}).", "encima": "au-dessus", "debajo": "en dessous",
    "box_eq": "pile dans la moyenne du jeu ({media}).",
    "muestra_h3": "Échantillon réduit",
    "muestra_p": "Seulement {g} parties enregistrées. Réparties entre Dark Powers, Finales et Setups, chaque détail en compte très peu : à prendre comme un indice, pas comme un fait.",
    "particular": "Ce qui la rend unique",
    "nivel": "Niveau", "elmapa": "La carte",
    "elkiller": "Le killer",
    "elkiller_p": "<a href=\"{u}\"><b>{k}</b></a> affiche {wr} de victoires toutes cartes confondues, sur {g} parties. Ici, sur {l}, le chiffre est de {wr2}.",
    "setups": "Setups", "setup1": "Setup",
    "setups_sub": "Du plus dur au plus facile. Au moins {n} parties.",
    "setups_gap": "Entre <b>{a}</b> et <b>{b}</b>, il y a <b>{d} points</b> d'écart. La mise en place compte plus qu'il n'y paraît.",
    "foro_c": "Conseils de joueurs", "reviews": "Ce qu'en disent les critiques",
    "salir_c": "Les quatre ouvertures, avec laquelle choisir selon la mise en place, sont dans les <a href=\"salidas.html\">stratégies d'ouverture</a>.",
    "c_title": "{c} (Final Girl) : stats et conseils, {wr} de victoires",
    "c_desc": "{k} sur {l}. Gagnée dans {wr} des {g} parties. Setups, Dark Powers, Finales et conseils.",
    "pie": "Données issues de la <a href=\"{h}\" target=\"_blank\" rel=\"noopener\">feuille de suivi publique</a> de la communauté Final Girl (<a href=\"{f}\" target=\"_blank\" rel=\"noopener\">enregistrez vos parties</a>). Retour à <a href=\"fichas.html\">tous les killers et boîtes</a>.",
    "hub_title": "Statistiques Final Girl : victoires par killer et par boîte ({n} parties)",
    "hub_desc": "Taux de victoire de chaque killer et de chaque boîte de Final Girl, sur {n} parties de la communauté. Killers les plus durs, meilleures cartes, Dark Powers et Finales.",
    "hub_eb": "{n} parties réelles · {j} joueurs",
    "hub_h1": "Final Girl<span class=\"roja\">statistiques</span>",
    "hub_dek": "À quelle fréquence la Final Girl survit à chaque killer et à chaque boîte, sur {n} parties enregistrées par la communauté. Moyenne : <b>{media}</b>.",
    "hub_lab": "Envie de croiser n'importe quel killer avec n'importe quelle carte ? Voir les <a href=\"index.html\">statistiques interactives complètes</a>.",
    "hub_k": "Killers, du plus dur au plus facile", "hub_c": "Boîtes, de la plus dure à la plus facile",
    "hub_th_k": ["Killer", "Victoires", "Parties"], "hub_th_c": ["Boîte", "Victoires", "Parties"],
    "hub_reg": "Vous avez joué ? <a href=\"{f}\" target=\"_blank\" rel=\"noopener\">Enregistrez la partie sur le formulaire communautaire</a> : chaque partie affine ces chiffres.",
},
"de": {
    "nav": ["Statistik", "Eröffnungen", "Übersicht"],
    "es_nota": "",
    "killer_eb": "Killer · {n} Karten mit Daten",
    "killer_h1": "{wr} Siegquote",
    "intro": "In <b>{g} erfassten Partien</b> besiegt das Final Girl {k} in {wr} der Fälle. Der Schnitt des ganzen Spiels liegt bei {media}, also ",
    "intro_up": "darüber: einer der leichteren Killer.",
    "intro_down": "darunter: einer der harten.",
    "intro_eq": "genau im Schnitt.",
    "quien": "Wer ist {k}", "juega": "Wie {k} spielt",
    "wiki": "Spieldaten aus dem <a href=\"{u}\" target=\"_blank\" rel=\"noopener\">Final Girl Wiki</a>, unter CC-BY-SA-Lizenz.",
    "caja": "Enthalten in der Box <a href=\"{u}\"><b>{c}</b></a>", "pareja": ", zusammen mit <b>{l}</b>.",
    "mapa_h3": "Die Karte verändert den Kampf",
    "mapa_p": "Auf {l}, dem Schauplatz seiner Box, gewinnt das Final Girl <b>{a}</b>, gegenüber {wr} über alle Karten: <b>{d} Punkte</b>. ",
    "mapa_neg": "Die Karte spielt für dich, nicht für den Killer.",
    "mapa_pos": "Dieser Schauplatz liegt dem Killer: Verlass dich nicht auf den Schnitt.",
    "mapa_fin": " Die beste Karte ist {m} ({mw}), die schlechteste {p} ({pw}).",
    "donde": "Beste und schlechteste Karten gegen {k}",
    "donde_sub": "Siegquote des Final Girl auf jedem Schauplatz, mit mindestens {n} erfassten Partien.",
    "th": ["Schauplatz", "Siegquote", "Partien"],
    "dp": "Dark Powers", "dp1": "Dark Power", "fin": "Finale-Karten", "fin1": "Finale-Karte",
    "sec_sub": "Von der härtesten zur leichtesten. Mindestens {n} Partien.",
    "peor": "Die schlimmste Karte ist <b>{c}</b>: Mit ihr im Spiel wird nur in {wr} der Fälle gewonnen, bei {g} Partien.",
    "foro_k": "Was Spieler sagen",
    "salir": "Wie man die Partie beginnt",
    "salir_p": "Die vier Eröffnungen und wann man welche nutzt, stehen in den <a href=\"salidas.html\">Eröffnungsstrategien</a>. Um diesen Killer auf allen Karten zu vergleichen, siehe die <a href=\"index.html\">interaktive Statistik</a>.",
    "k_title": "{k} in Final Girl: Siegquote nach Karte und wie man ihn schlägt",
    "k_desc": "Das Final Girl gewinnt {wr} gegen {k} in {g} Partien. Beste und schlechteste Karten, härteste Dark Powers und Finales, Tipps.",
    "box_eb": "Box · {f} · {g} Partien",
    "box_h1": "{wr} Siegquote",
    "box_dek": "{k} auf {l}. In {g} erfassten Partien wird in {wr} der Fälle gewonnen, ",
    "box_dif": "{d} Punkte {dir} dem Spielschnitt ({media}).", "encima": "über", "debajo": "unter",
    "box_eq": "genau im Spielschnitt ({media}).",
    "muestra_h3": "Kleine Stichprobe",
    "muestra_p": "Nur {g} erfasste Partien. Aufgeteilt auf Dark Powers, Finales und Setups bleiben je Auswertung sehr wenige: eher ein Hinweis als ein Fakt.",
    "particular": "Was sie besonders macht",
    "nivel": "Schwierigkeit", "elmapa": "Die Karte",
    "elkiller": "Der Killer",
    "elkiller_p": "<a href=\"{u}\"><b>{k}</b></a> hat über alle Karten eine Siegquote von {wr}, bei {g} Partien. Hier, auf {l}, sind es {wr2}.",
    "setups": "Setups", "setup1": "Setup",
    "setups_sub": "Vom härtesten zum leichtesten. Mindestens {n} Partien.",
    "setups_gap": "Zwischen <b>{a}</b> und <b>{b}</b> liegen <b>{d} Punkte</b>. Der Aufbau wiegt schwerer, als man denkt.",
    "foro_c": "Tipps von Spielern", "reviews": "Was Rezensionen sagen",
    "salir_c": "Die vier Eröffnungen, und welche je nach Aufbau passt, stehen in den <a href=\"salidas.html\">Eröffnungsstrategien</a>.",
    "c_title": "{c} (Final Girl): Statistik und Tipps, {wr} Siegquote",
    "c_desc": "{k} auf {l}. {wr} von {g} Partien gewonnen. Setups, Dark Powers, Finales und Tipps.",
    "pie": "Daten aus der <a href=\"{h}\" target=\"_blank\" rel=\"noopener\">öffentlichen Tabelle</a> der Final-Girl-Community (<a href=\"{f}\" target=\"_blank\" rel=\"noopener\">trag deine Partien ein</a>). Zurück zu <a href=\"fichas.html\">allen Killern und Boxen</a>.",
    "hub_title": "Final Girl Statistik: Siegquote jedes Killers und jeder Box ({n} Partien)",
    "hub_desc": "Siegquote jedes Killers und jeder Box von Final Girl, aus {n} Community-Partien. Härteste Killer, beste Karten, Dark Powers und Finales.",
    "hub_eb": "{n} echte Partien · {j} Spieler",
    "hub_h1": "Final Girl<span class=\"roja\">Statistik</span>",
    "hub_dek": "Wie oft das Final Girl jeden Killer und jede Box überlebt, aus {n} von der Community erfassten Partien. Schnitt: <b>{media}</b>.",
    "hub_lab": "Jeden Killer mit jeder Karte kreuzen? Dafür gibt es die <a href=\"index.html\">komplette interaktive Statistik</a>.",
    "hub_k": "Killer, härteste zuerst", "hub_c": "Boxen, härteste zuerst",
    "hub_th_k": ["Killer", "Siegquote", "Partien"], "hub_th_c": ["Box", "Siegquote", "Partien"],
    "hub_reg": "Eine Partie gespielt? <a href=\"{f}\" target=\"_blank\" rel=\"noopener\">Trag sie im Community-Formular ein</a>: Jede Partie schärft diese Zahlen.",
},
"it": {
    "nav": ["Statistiche", "Aperture", "Schede"],
    "es_nota": "",
    "killer_eb": "Killer · {n} mappe con dati",
    "killer_h1": "{wr} di vittorie",
    "intro": "Su <b>{g} partite registrate</b>, la Final Girl batte {k} nel {wr} dei casi. La media di tutto il gioco è {media}, quindi ",
    "intro_up": "è sopra la media: uno dei killer più abbordabili.",
    "intro_down": "è sotto la media: uno dei più duri.",
    "intro_eq": "è proprio nella media.",
    "quien": "Chi è {k}", "juega": "Come gioca {k}",
    "wiki": "Dati di gioco tratti dalla <a href=\"{u}\" target=\"_blank\" rel=\"noopener\">Final Girl Wiki</a>, con licenza CC BY-SA.",
    "caja": "Incluso nella scatola <a href=\"{u}\"><b>{c}</b></a>", "pareja": ", abbinato a <b>{l}</b>.",
    "mapa_h3": "La mappa cambia lo scontro",
    "mapa_p": "Su {l}, la sua ambientazione, la Final Girl vince il <b>{a}</b>, contro il {wr} su tutte le mappe: <b>{d} punti</b>. ",
    "mapa_neg": "La mappa gioca a tuo favore, non del killer.",
    "mapa_pos": "Quell'ambientazione gli si addice: non fidarti della media.",
    "mapa_fin": " La mappa migliore è {m} ({mw}) e la peggiore {p} ({pw}).",
    "donde": "Mappe migliori e peggiori contro {k}",
    "donde_sub": "Percentuale di vittoria della Final Girl su ogni ambientazione, con almeno {n} partite registrate.",
    "th": ["Ambientazione", "Vittorie", "Partite"],
    "dp": "Dark Powers", "dp1": "Dark Power", "fin": "Carte Finale", "fin1": "Carta Finale",
    "sec_sub": "Dalla più punitiva alla più facile. Almeno {n} partite.",
    "peor": "La pescata peggiore è <b>{c}</b>: con lei in gioco la partita si vince solo nel {wr} dei casi, su {g} partite.",
    "foro_k": "Cosa dicono i giocatori",
    "salir": "Come iniziare la partita",
    "salir_p": "Le quattro aperture e quando usarle sono nelle <a href=\"salidas.html\">strategie di apertura</a>. Per confrontare questo killer su ogni mappa, vedi le <a href=\"index.html\">statistiche interattive</a>.",
    "k_title": "{k} in Final Girl: vittorie per mappa e come batterlo",
    "k_desc": "La Final Girl vince il {wr} contro {k} su {g} partite. Mappe migliori e peggiori, Dark Powers e Finali più duri, e consigli.",
    "box_eb": "Scatola · {f} · {g} partite",
    "box_h1": "{wr} di vittorie",
    "box_dek": "{k} su {l}. Su {g} partite registrate si vince nel {wr} dei casi, ",
    "box_dif": "{d} punti {dir} la media del gioco ({media}).", "encima": "sopra", "debajo": "sotto",
    "box_eq": "proprio nella media del gioco ({media}).",
    "muestra_h3": "Campione ridotto",
    "muestra_p": "Solo {g} partite registrate. Divise tra Dark Powers, Finali e Setup, ogni dettaglio ne conta pochissime: prendilo come un indizio, non come un fatto.",
    "particular": "Cosa la rende particolare",
    "nivel": "Livello", "elmapa": "La mappa",
    "elkiller": "Il killer",
    "elkiller_p": "<a href=\"{u}\"><b>{k}</b></a> ha il {wr} di vittorie su tutte le mappe, su {g} partite. Qui, su {l}, la cifra è {wr2}.",
    "setups": "Setup", "setup1": "Setup",
    "setups_sub": "Dal più duro al più facile. Almeno {n} partite.",
    "setups_gap": "Tra <b>{a}</b> e <b>{b}</b> ci sono <b>{d} punti</b> di differenza. La preparazione iniziale pesa più di quanto sembri.",
    "foro_c": "Consigli di chi l'ha giocata", "reviews": "Cosa dicono le recensioni",
    "salir_c": "Le quattro aperture, con quale usare in base alla preparazione, sono nelle <a href=\"salidas.html\">strategie di apertura</a>.",
    "c_title": "{c} (Final Girl): statistiche e consigli, {wr} di vittorie",
    "c_desc": "{k} su {l}. Vinta nel {wr} di {g} partite. Setup, Dark Powers, Finali e consigli.",
    "pie": "Dati dal <a href=\"{h}\" target=\"_blank\" rel=\"noopener\">foglio pubblico</a> della community di Final Girl (<a href=\"{f}\" target=\"_blank\" rel=\"noopener\">registra le tue partite</a>). Torna a <a href=\"fichas.html\">tutti i killer e le scatole</a>.",
    "hub_title": "Statistiche Final Girl: vittorie per killer e scatola ({n} partite)",
    "hub_desc": "Percentuale di vittoria di ogni killer e ogni scatola di Final Girl, su {n} partite della community. Killer più duri, mappe migliori, Dark Powers e Finali.",
    "hub_eb": "{n} partite reali · {j} giocatori",
    "hub_h1": "Final Girl<span class=\"roja\">statistiche</span>",
    "hub_dek": "Quanto spesso la Final Girl sopravvive a ogni killer e a ogni scatola, su {n} partite registrate dalla community. Media: <b>{media}</b>.",
    "hub_lab": "Vuoi incrociare qualsiasi killer con qualsiasi mappa? Usa le <a href=\"index.html\">statistiche interattive complete</a>.",
    "hub_k": "Killer, dal più duro", "hub_c": "Scatole, dalla più dura",
    "hub_th_k": ["Killer", "Vittorie", "Partite"], "hub_th_c": ["Scatola", "Vittorie", "Partite"],
    "hub_reg": "Hai giocato una partita? <a href=\"{f}\" target=\"_blank\" rel=\"noopener\">Registrala nel modulo della community</a>: ogni partita affina questi numeri.",
},
}


def pc(x, lang, dec=1):
    s = f"{x*100:.{dec}f}"
    if lang == "en":
        return s + "%"
    s = s.replace(".", ",")
    return s + (" %" if lang in ("fr", "de") else "%")


def num(n, lang):
    s = f"{n:,}"
    return s if lang == "en" else s.replace(",", " " if lang == "fr" else ".")


def textos(lang):
    f = AQUI / f"textos_{lang}.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else None


def pagina_killer(nombre, k, lang, tx):
    t = T[lang]
    mapas = P.mapas_de(nombre)
    caja = k.get("box")
    f = P.FILMS.get(caja)
    propio = f["loc"] if f else None
    aqui = next((m for m in mapas if m[0] == propio), None)
    wr = pc(k["wr"], lang)
    h = [f'<p class="eyebrow">{t["killer_eb"].format(n=len(mapas))}</p>',
         f'<h1 data-caja="{caja or ""}">{nombre}<span class="roja">{t["killer_h1"].format(wr=wr)}</span></h1>']
    dif = (k["wr"] - P.MEDIA) * 100
    intro = t["intro"].format(g=num(k["g"], lang), k=nombre, wr=wr, media=pc(P.MEDIA, lang))
    intro += t["intro_up"] if dif > 4 else t["intro_down"] if dif < -4 else t["intro_eq"]
    h.append(f'<p class="dek">{intro}</p>')

    d = tx["desc"].get(nombre)
    wiki = P.DESC.get(nombre, {}).get("wiki")
    if d and d.get("q"):
        h.append(f'<h2>{t["quien"].format(k=nombre)}</h2><p>{d["q"]}</p>')
        if d.get("j"):
            h.append(f'<h3>{t["juega"].format(k=nombre)}</h3><p>{d["j"]}</p>')
        if wiki:
            u = "https://finalgirl.fandom.com/wiki/" + wiki.replace(" ", "_")
            h.append(f'<p class="sub">{t["wiki"].format(u=u)}</p>')

    h.append(mecanicas.killer(nombre, lang))
    if caja:
        h.append("<p>" + t["caja"].format(u=P.slug(caja) + ".html", c=caja)
                 + (t["pareja"].format(l=propio) if propio else ".") + "</p>")

    if aqui and len(mapas) >= 2:
        dd = (aqui[1] - k["wr"]) * 100
        if abs(dd) >= 4:
            mejor, peor = mapas[0], mapas[-1]
            ds = f'{"+" if dd > 0 else ""}{dd:.1f}'
            if lang != "en":
                ds = ds.replace(".", ",")
            h.append(f'<div class="aviso"><h3>{t["mapa_h3"]}</h3><p>'
                     + t["mapa_p"].format(l=propio, a=pc(aqui[1], lang), wr=wr, d=ds)
                     + (t["mapa_neg"] if dd > 0 else t["mapa_pos"])
                     + t["mapa_fin"].format(m=mejor[0], mw=pc(mejor[1], lang),
                                            p=peor[0], pw=pc(peor[1], lang))
                     + "</p></div>")

    if len(mapas) >= 2:
        h.append(f'<h2>{t["donde"].format(k=nombre)}</h2>')
        h.append(f'<p class="sub">{t["donde_sub"].format(n=P.MIN_CELDA)}</p>')
        h.append(P.tabla(t["th"], [[m[0], pc(m[1], lang), m[2]] for m in mapas]))

    for tit, uno, clave in ((t["dp"], t["dp1"], "Dark Power"), (t["fin"], t["fin1"], "Finale")):
        filas = [x for x in k.get("secs", {}).get(clave, []) if x[2] >= P.MIN_SECCION]
        if len(filas) >= 2:
            filas.sort(key=lambda x: x[1])
            h.append(f'<h2>{tit}</h2><p class="sub">{t["sec_sub"].format(n=P.MIN_SECCION)}</p>')
            h.append(P.tabla([uno] + t["th"][1:], [[x[0], pc(x[1], lang), x[2]] for x in filas]))
            p0 = filas[0]
            h.append("<p>" + t["peor"].format(c=p0[0], wr=pc(p0[1], lang), g=p0[2]) + "</p>")

    c = tx["cons"].get(caja or "", {})
    if c.get("foro"):
        h.append(f'<h2>{t["foro_k"]}</h2><div class="aviso"><p>{c["foro"]}</p></div>')
    h.append(f'<h2>{t["salir"]}</h2><p>{t["salir_p"]}</p>')

    title = t["k_title"].format(k=nombre)
    desc = t["k_desc"].format(wr=wr, k=nombre, g=num(k["g"], lang))
    return title, desc[:158], "\n".join(h)


def pagina_caja(f, lang, tx):
    t = T[lang]
    c = tx["cons"].get(f["film"], {})
    k = P.KILLERS.get(f["killer"], {})
    wr = pc(f["wr"], lang)
    h = [f'<p class="eyebrow">{t["box_eb"].format(f=f.get("fnum", ""), g=f["plays"])}</p>',
         f'<h1 data-caja="{f["film"]}">{f["film"]}<span class="roja">{t["box_h1"].format(wr=wr)}</span></h1>']
    dif = (f["wr"] - P.MEDIA) * 100
    media = pc(P.MEDIA, lang)
    ds = f"{abs(dif):.1f}" if lang == "en" else f"{abs(dif):.1f}".replace(".", ",")
    h.append('<p class="dek">' + t["box_dek"].format(k=f["killer"], l=f["loc"], g=f["plays"], wr=wr)
             + (t["box_dif"].format(d=ds, dir=t["encima"] if dif > 0 else t["debajo"], media=media)
                if abs(dif) >= 1 else t["box_eq"].format(media=media)) + "</p>")
    if f["plays"] < 90:
        h.append(f'<div class="aviso"><h3>{t["muestra_h3"]}</h3><p>{t["muestra_p"].format(g=f["plays"])}</p></div>')
    if c:
        h.append(f'<h2>{t["particular"]}</h2>')
        h.append("<p>" + " ".join(x for x in (c.get("mec"), c.get("com")) if x) + "</p>")
        filas = [x for x in ([t["nivel"], c.get("nivel")], [t["elmapa"], c.get("mapa")]) if x[1]]
        if filas:
            h.append(P.tabla(["", ""], filas))
    h.append(mecanicas.killer(f["killer"], lang))
    h.append(mecanicas.mapa(f["loc"], lang))
    if k:
        h.append(f'<h2>{t["elkiller"]}</h2><p>'
                 + t["elkiller_p"].format(u=P.slug(f["killer"]) + ".html", k=f["killer"],
                                          wr=pc(k["wr"], lang), g=num(k["g"], lang),
                                          l=f["loc"], wr2=wr) + "</p>")
    setups = [s for s in f.get("setups", []) if s[2] >= P.MIN_SECCION]
    if len(setups) >= 2:
        setups.sort(key=lambda x: x[1])
        h.append(f'<h2>{t["setups"]}</h2><p class="sub">{t["setups_sub"].format(n=P.MIN_SECCION)}</p>')
        h.append(P.tabla([t["setup1"]] + t["th"][1:], [[s[0], pc(s[1], lang), s[2]] for s in setups]))
        d = (setups[-1][1] - setups[0][1]) * 100
        if d >= 10:
            h.append("<p>" + t["setups_gap"].format(a=setups[0][0], b=setups[-1][0], d=f"{d:.0f}") + "</p>")
    for tit, uno, clave in ((t["dp"], t["dp1"], "Dark Power"), (t["fin"], t["fin1"], "Finale")):
        filas = [x for x in f.get("secs", {}).get(clave, []) if x[2] >= P.MIN_SECCION]
        if len(filas) >= 2:
            filas.sort(key=lambda x: x[1])
            h.append(f"<h2>{tit}</h2>")
            h.append(P.tabla([uno] + t["th"][1:], [[x[0], pc(x[1], lang), x[2]] for x in filas]))
    if c.get("foro"):
        h.append(f'<h2>{t["foro_c"]}</h2><div class="aviso"><p>{c["foro"]}</p></div>')
    r = tx.get("rev", {}).get(f["film"])
    if r:
        h.append(f'<h2>{t["reviews"]}</h2><div class="aviso"><p><b>{r}</b></p></div>')
    h.append(f'<h2>{t["salir"]}</h2><p>{t["salir_c"]}</p>')
    title = t["c_title"].format(c=f["film"], wr=pc(f["wr"], lang, 0))
    desc = t["c_desc"].format(k=f["killer"], l=f["loc"], wr=wr, g=f["plays"])
    return title, desc[:158], "\n".join(h)


def hub(lang, generadas):
    t = T[lang]
    m = P.D["meta"]
    n = num(m["total"], lang)
    ks = sorted(((nm, k) for nm, k in P.KILLERS.items() if k.get("g", 0) >= 60),
                key=lambda x: x[1]["wr"])
    cs = sorted(P.D["films"], key=lambda f: f["wr"])
    h = [f'<p class="eyebrow">{t["hub_eb"].format(n=n, j=m.get("jugadores", ""))}</p>',
         f'<h1>{t["hub_h1"]}</h1>',
         f'<p class="dek">{t["hub_dek"].format(n=n, media=pc(m["wr"], lang))}</p></header>',
         f'<p>{t["hub_lab"]}</p>',
         f'<h2>{t["hub_k"]}</h2>',
         P.tabla(t["hub_th_k"], [[f'<a href="{P.slug(nm)}.html" data-caja="{k.get("box") or ""}">{nm}</a>', pc(k["wr"], lang), num(k["g"], lang)]
                                 for nm, k in ks]),
         f'<h2>{t["hub_c"]}</h2>',
         P.tabla(t["hub_th_c"], [[f'<a href="{P.slug(f["film"])}.html" data-caja="{f["film"]}">{f["film"]}</a>', pc(f["wr"], lang), f["plays"]]
                                 for f in cs]),
         f'<div class="aviso"><p>{t["hub_reg"].format(f="{FORM}")}</p></div>']
    return (t["hub_title"].format(n=n), t["hub_desc"].format(n=n)[:158], "\n".join(h))


def alternativos(salida_es, dominio, existe):
    """<link hreflang> de una página a todas sus versiones, ella incluida."""
    base = "" if salida_es == "index.html" else salida_es
    out = [f'<link rel="alternate" hreflang="es" href="{dominio}/{base}">']
    for l in IDIOMAS:
        if existe(l):
            out.append(f'<link rel="alternate" hreflang="{l}" href="{dominio}/{l}/{base}">')
    en = "en/" if existe("en") else ""
    out.append(f'<link rel="alternate" hreflang="x-default" href="{dominio}/{en}{base}">')
    return "\n".join(out)


def selector(lang, salida, existe):
    """Enlaces a las otras versiones de la misma página."""
    base = "" if salida == "index.html" else salida
    pre = "../" if lang != "es" else ""
    items = [("es", f"{pre}{base or 'index.html'}")] + [
        (l, f"{pre}{l}/{base or 'index.html'}" if lang == "es" else f"../{l}/{base or 'index.html'}")
        for l in IDIOMAS if existe(l)]
    return ('<p class="idiomas">' + " · ".join(
        f'<a href="{u}" hreflang="{l}"' + (' aria-current="true"' if l == lang else "") + f'>{l.upper()}</a>'
        for l, u in items) + "</p>")


ESTILO_IDIOMAS = ('<style>.idiomas{font-family:var(--f-mono);font-size:12px;letter-spacing:.08em;'
                  'margin:10px 0 0;color:var(--muted)}.idiomas a{color:var(--muted);text-decoration:none}'
                  '.idiomas a[aria-current]{color:var(--blood)}.idiomas a:hover{color:var(--ink)}</style>')


def generar(M):
    """M es el módulo montar (CABECERA, PIE, DOMINIO, HOJA, FORM...).
    Devuelve (paginas_para_sitemap, mapa_de_alternativos)."""
    dominio = M.DOMINIO
    hechos = {}
    sitemap = []
    for lang in IDIOMAS:
        tx = textos(lang)
        if not tx:
            continue
        t = T[lang]
        dir_ = AQUI / lang
        dir_.mkdir(exist_ok=True)
        pags = []
        for nombre, k in P.KILLERS.items():
            if k.get("g", 0) < 60:
                continue
            pags.append((P.slug(nombre) + ".html", *pagina_killer(nombre, k, lang, tx), None))
        for f in P.D["films"]:
            pags.append((P.slug(f["film"]) + ".html", *pagina_caja(f, lang, tx), f.get("img")))
        pags.append(("fichas.html", *hub(lang, pags), None))
        import tierlist
        pags.append(("tops.html", *tierlist.pagina(lang), None))
        hechos[lang] = {p[0] for p in pags}
        for p in pags:
            sitemap.append((lang, p[0]))
        hechos[lang + "_pags"] = pags
        for salida in ("index.html", "salidas.html"):
            if (AQUI / "src" / "i18n" / f"{salida.split('.')[0].replace('index', 'cuerpo')}.{lang}.html").exists():
                hechos[lang].add(salida)
                sitemap.append((lang, salida))

    def existe_en(salida):
        return lambda l: salida in hechos.get(l, set())

    for lang in IDIOMAS:
        if lang not in hechos:
            continue
        t = T[lang]
        nav = nav_de(lang, M).format(act_index="", act_salidas="", act_fichas="")
        for salida, title, desc, cuerpo, img in hechos[lang + "_pags"]:
            url = f"{dominio}/{lang}/{'' if salida == 'index.html' else salida}"
            cuerpo = cuerpo.replace("{FORM}", M.FORM)
            if salida == "fichas.html":
                head, rest = cuerpo.split("</header>", 1)
                cuerpo_html = ('<div class="wrap"><header class="top">' + head
                               + selector(lang, salida, existe_en(salida)) + "</header>" + rest)
            else:
                a, b = cuerpo.split("</h1>", 1)
                cuerpo_html = ('<div class="wrap"><header class="top">' + a + "</h1>"
                               + selector(lang, salida, existe_en(salida)) + b)
            html = (M.CABECERA.format(
                        title=title, desc=desc, url=url,
                        imgurl=f"{dominio}/{img or 'img/vhs-final-girl.jpg'}",
                        ogtitle=title, ogdesc=desc,
                        jsonld=jsonld(title, desc, url, lang, M),
                        robots="index,follow,max-image-preview:large" if M.INDEXAR else "noindex,nofollow")
                    .replace('<html lang="es">', f'<html lang="{lang}">')
                    .replace('content="es_ES"', f'content="{LOCALE[lang]}"')
                    .replace('content="La página que todo fan de Final Girl necesitaba"', 'content="Final Girl Stats"')
                    .replace("</head>", alternativos(salida, dominio, existe_en(salida))
                             + '\n<link rel="stylesheet" href="../estilos.css">' + ESTILO_IDIOMAS + "</head>")
                    + nav + cuerpo_html
                    + '<footer><p>' + t["pie"].format(h=M.HOJA, f=M.FORM) + "</p></footer></div>"
                    + M.PIE)
            (AQUI / lang / salida).write_text(html, encoding="utf-8")
        for salida in ("index.html", "salidas.html"):
            if salida in hechos[lang]:
                grande(lang, salida, M, existe_en(salida))
        print(f"{lang}/  {len(hechos[lang])} páginas")

    return sitemap, existe_en


def jsonld(title, desc, url, lang, M):
    m = P.D["meta"]
    return json.dumps({
        "@context": "https://schema.org", "@type": "Dataset",
        "name": title, "description": desc, "url": url, "inLanguage": lang,
        "keywords": ["Final Girl", "board game", "solo", "win rate", "statistics"],
        "temporalCoverage": f"../{m['last']}",
        "isAccessibleForFree": True,
        "creator": {"@type": "Organization", "name": "Final Girl Stats", "url": M.DOMINIO + "/"},
        "about": {"@type": "Game", "name": "Final Girl",
                  "numberOfPlayers": {"@type": "QuantitativeValue", "value": 1}},
    }, ensure_ascii=False, separators=(",", ":"))


def parchear_es(ruta, salida, dominio, existe):
    """Añade hreflang y el selector de idioma a una página española ya escrita."""
    s = ruta.read_text(encoding="utf-8")
    if 'class="idiomas"' in s or not any(existe(l) for l in IDIOMAS):
        return
    s = s.replace("</head>", alternativos(salida, dominio, existe) + "\n" + ESTILO_IDIOMAS + "</head>", 1)
    sel = selector("es", salida, existe)
    s = re.sub(r"(</h1>)", r"\1" + sel.replace("\\", "\\\\"), s, count=1)
    ruta.write_text(s, encoding="utf-8")


# --------------------------------------------------------------------------
# Las dos páginas grandes (estadísticas y salidas)
# --------------------------------------------------------------------------
# Están escritas a mano, así que su traducción vive en src/i18n/<pagina>.<idioma>.html.
# Esos ficheros NO llevan los datos: tienen marcas /*@@D@@*/ que se rellenan
# aquí con los datos del día, sacados de la versión española. Así refrescar
# los datos no obliga a volver a traducir nada.
#
# Si alguien cambia el texto español, la traducción no se entera: hay que
# volver a pasarla. traduccion_vieja() avisa al montar.

NAV_TXT = {
    "en": ["Stats", "Openings", "All pages", "More sections", "Stats", "Tops", "Movies", "Series", "Killers", "Maps", "Final Girls", "Players", "Sections", "Extremes"],
    "fr": ["Stats", "Ouvertures", "Fiches", "Plus de sections", "Stats", "Tops", "Films", "Saisons", "Killers", "Cartes", "Final Girls", "Joueurs", "Sections", "Extrêmes"],
    "de": ["Statistik", "Eröffnungen", "Übersicht", "Weitere Bereiche", "Stats", "Tops", "Filme", "Staffeln", "Killer", "Karten", "Final Girls", "Spieler", "Bereiche", "Extreme"],
    "it": ["Statistiche", "Aperture", "Schede", "Altre sezioni", "Stats", "Top", "Film", "Stagioni", "Killer", "Mappe", "Final Girls", "Giocatori", "Sezioni", "Estremi"],
}

TITULOS = {
    "en": {"index.html": ("Final Girl stats: win rates from {n} real games",
                          "Win rate of every killer on every map in Final Girl, from {n} community games. Which box is hardest and where each killer loses."),
           "salidas.html": ("Final Girl openings: the 4 openings and when to use each",
                            "The 4 Final Girl openings turn by turn: which to use depending on weapons in sight or victims nearby, dice, and common rules mistakes.")},
    "fr": {"index.html": ("Statistiques Final Girl : victoires sur {n} parties réelles",
                          "Victoires de chaque killer sur chaque carte de Final Girl, sur {n} parties de la communauté. Quelle boîte est la plus dure et où chaque killer perd."),
           "salidas.html": ("Ouvertures Final Girl : les 4 ouvertures et quand les utiliser",
                            "Les 4 ouvertures de Final Girl tour par tour : laquelle choisir selon les armes en vue ou les victimes proches, dés et erreurs de règles courantes.")},
    "de": {"index.html": ("Final Girl Statistik: Siegquoten aus {n} echten Partien",
                          "Siegquote jedes Killers auf jeder Karte von Final Girl, aus {n} Community-Partien. Welche Box am härtesten ist und wo jeder Killer verliert."),
           "salidas.html": ("Final Girl Eröffnungen: die 4 Eröffnungen und wann man sie nutzt",
                            "Die 4 Eröffnungen von Final Girl Zug für Zug: welche je nach sichtbaren Waffen oder nahen Opfern, Würfel und häufige Regelfehler.")},
    "it": {"index.html": ("Statistiche Final Girl: vittorie su {n} partite reali",
                          "Vittorie di ogni killer su ogni mappa di Final Girl, su {n} partite della community. Quale scatola è più dura e dove perde ogni killer."),
           "salidas.html": ("Aperture di Final Girl: le 4 aperture e quando usarle",
                            "Le 4 aperture di Final Girl turno per turno: quale usare in base alle armi in vista o alle vittime vicine, dadi ed errori di regole comuni.")},
}


def nav_de(lang, M):
    t = NAV_TXT[lang]
    es = ["Estadísticas", "Salidas", "Fichas", "Más secciones", "Stats", "Tops", "Películas", "Temporadas", "Killers", "Mapas", "Final Girls", "Jugadores", "Secciones", "Extremos"]
    nav = M.NAV
    for a, b in zip(es, t):
        nav = nav.replace(f">{a}<", f">{b}<").replace(f'aria-label="{a}"', f'aria-label="{b}"')
    return nav


def _lineas_datos(fuente):
    """Las líneas 'var X = {...};' de la página española, por nombre."""
    out = {}
    for l in (AQUI / "src" / fuente).read_text(encoding="utf-8").split("\n"):
        m = re.match(r"\s*var (\w+) = ([\[{].*);\s*$", l)
        if m and len(l) > 3000:
            out[m.group(1)] = m.group(2)
    return out


def _traducir_datos(obj, lang, tx, mapa):
    def walk(o, ruta):
        if isinstance(o, dict):
            return {k: walk(v, ruta + [k]) for k, v in o.items()}
        if isinstance(o, list):
            return [walk(v, ruta) for v in o]
        if isinstance(o, str):
            if len(ruta) >= 3 and ruta[0] == "consejos":
                return tx["cons"].get(ruta[1], {}).get(ruta[2], o)
            if o in mapa:
                return mapa[o].get(lang, o)
        return o
    return walk(obj, [])


def cifras(lang):
    m = P.D["meta"]
    c = {"partidas": num(m["total"], lang), "jugadores": str(m.get("jugadores", "")),
         "media": pc(m["wr"], lang)}
    for k in ("combis", "combisOk", "top25", "top1", "unicas"):
        if m.get(k) is not None:
            c[k] = str(m[k])
    for k in ("wrTop10", "wrResto"):
        if m.get(k) is not None:
            c[k] = pc(m[k], lang)
    return c


def grande(lang, salida, M, existe):
    base = "cuerpo" if salida == "index.html" else "salidas"
    fuente_es = "cuerpo.html" if salida == "index.html" else "salidas-cuerpo.html"
    cuerpo = (AQUI / "src" / "i18n" / f"{base}.{lang}.html").read_text(encoding="utf-8")
    tx = textos(lang)
    mapa = json.loads((AQUI / "src" / "i18n" / "datos.json").read_text(encoding="utf-8"))
    for nombre, valor in _lineas_datos(fuente_es).items():
        marca = f"/*@@{nombre}@@*/"
        if marca not in cuerpo:
            continue
        if nombre == "D":
            valor = json.dumps(_traducir_datos(json.loads(valor), lang, tx, mapa),
                               ensure_ascii=False)
        cuerpo = cuerpo.replace(marca, valor, 1)
    if "/*@@" in cuerpo:
        raise SystemExit(f"{base}.{lang}: marca de datos sin rellenar")

    cuerpo = re.sub(r"^\s*<title>.*?</title>\s*", "", cuerpo, count=1, flags=re.S)
    if salida == "index.html":
        cuerpo = filtrar_jugadores(cuerpo, lang)
    for clave, valor in cifras(lang).items():
        cuerpo = re.sub(r'(<span data-dato="%s">)[^<]*(</span>)' % clave,
                        r"\g<1>" + valor + r"\g<2>", cuerpo)
    if "var DESC = {};" in cuerpo:
        desc = {k: dict(P.DESC.get(k, {}), **{x: v[x] for x in ("q", "j") if v.get(x)})
                for k, v in tx["desc"].items()}
        cuerpo = cuerpo.replace("var DESC = {};", "var DESC = " + json.dumps(desc, ensure_ascii=False) + ";", 1)
    for viejo, nuevo in M.ENLACES.items():
        cuerpo = cuerpo.replace(viejo, nuevo)
    # Imágenes: la página vive un nivel más abajo.
    cuerpo = re.sub(r"""(["'(])(img|assets)/""", r"\1../\2/", cuerpo)

    act = {"act_index": "", "act_salidas": "", "act_fichas": ""}
    act["act_index" if salida == "index.html" else "act_salidas"] = ' aria-current="page"'
    nav = nav_de(lang, M).format(**act)
    if "nav-sitio" not in cuerpo:
        for ancla in ('<header class="hero">', '<header class="top">'):
            if ancla in cuerpo:
                cuerpo = cuerpo.replace(ancla, nav + ancla, 1)
                break
    else:
        # la de salidas trae su propia barra en español
        cuerpo = re.sub(r'<nav class="nav-sitio".*?</nav>', nav.split("<style")[0].strip(), cuerpo, count=1, flags=re.S)
    if salida == "salidas.html":
        cuerpo += M.UNIFICAR_ESTILO
    cuerpo = poner_aviso_movil(cuerpo, lang)
    if salida == "index.html":
        import tops
        cuerpo = tops.poner(cuerpo, lang)
        cuerpo = sin_snippet(ocultar_pestanas(cuerpo))
    if salida == "index.html":
        # Igual que en la española: "Laboratorio" no lo busca nadie.
        cuerpo = re.sub(r"<h1>.*?</h1>", f'<h1>{NAV_TXT[lang][0]}<span class="roja">Final Girl</span></h1>',
                        cuerpo, count=1, flags=re.S)
    cuerpo = re.sub(r"(</h1>)", lambda m: m.group(1) + selector(lang, salida, existe), cuerpo, count=1)

    n = num(P.D["meta"]["total"], lang)
    title, desc = (x.format(n=n) for x in TITULOS[lang][salida])
    url = f"{M.DOMINIO}/{lang}/{'' if salida == 'index.html' else salida}"
    img = "img/vhs-final-girl.jpg" if salida == "index.html" else "img/the-happy-trails-horror.jpg"
    html = (M.CABECERA.format(
                title=title, desc=desc[:158], url=url, imgurl=f"{M.DOMINIO}/{img}",
                ogtitle=title, ogdesc=desc[:158], jsonld=jsonld(title, desc, url, lang, M),
                robots="index,follow,max-image-preview:large" if M.INDEXAR else "noindex,nofollow")
            .replace('<html lang="es">', f'<html lang="{lang}">')
            .replace('content="es_ES"', f'content="{LOCALE[lang]}"')
            .replace('content="La página que todo fan de Final Girl necesitaba"', 'content="Final Girl Stats"')
            .replace("</head>", alternativos(salida, M.DOMINIO, existe) + "\n" + ESTILO_IDIOMAS + "</head>")
            + cuerpo + M.PIE)
    (AQUI / lang / salida).write_text(html, encoding="utf-8")


# --------------------------------------------------------------------------
# Jugadores que han pedido no salir
# --------------------------------------------------------------------------
# excluir_nicks.json es una lista de nicks (mayúsculas no importan). Se
# quitan de la pestaña Jugadores en todos los idiomas. Sus partidas siguen
# contando en todas las cifras: lo que desaparece es su ficha personal.
CONTACTO = "contacto@finalgirlstats.com"

AVISO_NICK = {
    "es": "¿Eres tú y prefieres no salir? Escribe a {c} con tu nick y te quitamos de esta lista. Tus partidas seguirán contando en las cifras, pero sin tu nombre.",
    "en": "Is that you and you'd rather not be listed? Email {c} with your nickname and we'll remove you. Your games will still count in the numbers, just without your name.",
    "fr": "C'est vous et vous préférez ne pas apparaître ? Écrivez à {c} avec votre pseudo et nous vous retirerons. Vos parties compteront toujours dans les chiffres, sans votre nom.",
    "de": "Bist du das und möchtest nicht gelistet sein? Schreib an {c} mit deinem Nick und wir entfernen dich. Deine Partien zählen weiter in den Zahlen, nur ohne deinen Namen.",
    "it": "Sei tu e preferisci non comparire? Scrivi a {c} con il tuo nick e ti togliamo. Le tue partite continueranno a contare nei numeri, ma senza il tuo nome.",
}


# Pestañas de la portada apagadas por ahora. Para volver a encender una,
# quítala de aquí: el código y los datos siguen en su sitio.
PESTANAS_OCULTAS = {"girls"}


def ocultar_pestanas(html):
    """Quita el botón de la pestaña y su enlace del menú "+". La sección
    sigue en la página pero oculta, y sin botón no hay forma de abrirla."""
    for t in PESTANAS_OCULTAS:
        html = re.sub(r'\s*<button role="tab" data-t="' + t + r'"[^>]*>[^<]*</button>', "", html)
        html = re.sub(r'\s*<a href="(?:\.\./)?index\.html#' + t + r'">[^<]*</a>', "", html)
    return html


def sin_snippet(html):
    """Google armaba la descripción del resultado con las cifras sueltas
    (KPIs, tablas). data-nosnippet le impide usarlas: tira de la frase de
    presentación o de la meta description."""
    html = html.replace('<div class="kpis">', '<div class="kpis" data-nosnippet>')
    return re.sub(r'<section id="(v-[a-z]+)"', r'<section id="\1" data-nosnippet', html)


def excluidos():
    f = AQUI / "excluir_nicks.json"
    return {n.strip().lower() for n in json.loads(f.read_text(encoding="utf-8"))} if f.exists() else set()


def filtrar_jugadores(cuerpo, lang):
    """Quita los nicks excluidos de UJ y añade el aviso de borrado."""
    fuera = excluidos()
    def limpia(m):
        uj = json.loads(m.group(2))
        uj = {k: v for k, v in uj.items() if k.strip().lower() not in fuera}
        return m.group(1) + json.dumps(uj, ensure_ascii=False, separators=(",", ":")) + ";"
    def limpia_um(m):
        um = json.loads(m.group(2))
        if isinstance(um.get("u"), dict):
            um["u"] = {k: v for k, v in um["u"].items() if k.strip().lower() not in fuera}
        return m.group(1) + json.dumps(um, ensure_ascii=False, separators=(",", ":")) + ";"
    if fuera:
        cuerpo = re.sub(r"(var UJ = )(\{.*?\});(?=\n)", limpia, cuerpo, count=1, flags=re.S)
        cuerpo = re.sub(r"(var UM = )(\{.*?\});(?=\n)", limpia_um, cuerpo, count=1, flags=re.S)
    c = f'<a href="mailto:{CONTACTO}">{CONTACTO}</a>'
    aviso = f'<p class="sub" id="ju-borrar" style="font-size:12.5px">{AVISO_NICK[lang].format(c=c)}</p>'
    if 'id="ju-borrar"' not in cuerpo:
        cuerpo = cuerpo.replace('<div class="barlist" id="ju-lista">', aviso + '<div class="barlist" id="ju-lista">', 1)
    return cuerpo


# --------------------------------------------------------------------------
# Aviso en el móvil
# --------------------------------------------------------------------------
# La matriz y las tablas grandes se leen mal en una pantalla estrecha. Mejor
# decirlo que dejar que alguien piense que la web está rota. Solo se ve por
# debajo de 700 px y se puede cerrar; se recuerda en el navegador.
AVISO_MOVIL = {
    "es": "Estás en el móvil: la página funciona, pero la matriz y las tablas grandes se ven mejor en un ordenador o con el móvil en horizontal.",
    "en": "You're on a phone: everything works, but the matrix and big tables read better on a computer or with your phone in landscape.",
    "fr": "Vous êtes sur mobile : tout fonctionne, mais la matrice et les grands tableaux se lisent mieux sur ordinateur ou en mode paysage.",
    "de": "Du bist am Handy: Alles funktioniert, aber die Matrix und großen Tabellen lesen sich am Computer oder im Querformat besser.",
    "it": "Sei sul telefono: tutto funziona, ma la matrice e le tabelle grandi si leggono meglio su computer o con il telefono in orizzontale.",
}


def aviso_movil(lang):
    return ('<div class="aviso-movil" id="aviso-movil" hidden><p>' + AVISO_MOVIL[lang]
            + '</p><button type="button" aria-label="OK">✕</button></div>'
            '<style>.aviso-movil{display:none}'
            '@media (max-width:700px){.aviso-movil:not([hidden]){display:flex;gap:10px;align-items:flex-start;'
            'margin:10px 0 4px;padding:10px 12px;background:var(--surface);border:1px solid var(--line);'
            'border-left:3px solid var(--blood);border-radius:3px;font-size:13px;line-height:1.45;color:var(--muted)}'
            '.aviso-movil p{margin:0;flex:1}.aviso-movil button{background:none;border:0;color:var(--muted);'
            'font-size:16px;line-height:1;cursor:pointer;padding:2px 4px}}</style>'
            '<script>(function(){var a=document.getElementById("aviso-movil");if(!a)return;'
            'var visto=false;try{visto=localStorage.getItem("fg-aviso-movil")==="1"}catch(e){}'
            'if(!visto)a.hidden=false;a.querySelector("button").onclick=function(){a.hidden=true;'
            'try{localStorage.setItem("fg-aviso-movil","1")}catch(e){}}})();</script>')


def poner_aviso_movil(cuerpo, lang):
    if 'id="aviso-movil"' in cuerpo:
        return cuerpo
    i = cuerpo.find("</nav>")
    return cuerpo if i < 0 else cuerpo[:i + 6] + aviso_movil(lang) + cuerpo[i + 6:]
