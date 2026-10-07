#!/usr/bin/env python3
"""Bloque "Cómo funciona" de las fichas: mecánicas del killer y del mapa.

Los textos salen de la Final Girl Wiki (CC BY-SA), resumidos sin añadir
nada: mecanicas_killers.json y mecanicas_mapas.json. wiki.py descarga las
páginas a wiki_cache.json; de ahí se resumen. Cada bloque enlaza su página
de origen, que es lo que pide la licencia y lo que permite comprobarlo.

Si una ficha no tiene página en la wiki, no se pinta nada: mejor un hueco
que una mecánica inventada.
"""
import json
import pathlib

AQUI = pathlib.Path(__file__).parent
WIKI = "https://finalgirl.fandom.com/wiki/"


def _carga(f):
    p = AQUI / f
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


KILLERS = _carga("mecanicas_killers.json")
MAPAS = _carga("mecanicas_mapas.json")
CACHE = _carga("wiki_cache.json")

T = {
    "es": {"k": "Cómo funciona {n}", "m": "El mapa: {n}", "src": "Resumen de la página de la <a href=\"{u}\" target=\"_blank\" rel=\"noopener\">Final Girl Wiki</a> (CC BY-SA).", "extras": "Cartas propias"},
    "en": {"k": "How {n} works", "m": "The map: {n}", "src": "Summarised from the <a href=\"{u}\" target=\"_blank\" rel=\"noopener\">Final Girl Wiki</a> page (CC BY-SA).", "extras": "Unique cards"},
    "fr": {"k": "Comment fonctionne {n}", "m": "La carte : {n}", "src": "Résumé de la page du <a href=\"{u}\" target=\"_blank\" rel=\"noopener\">Final Girl Wiki</a> (CC BY-SA).", "extras": "Cartes propres"},
    "de": {"k": "So funktioniert {n}", "m": "Die Karte: {n}", "src": "Zusammengefasst aus der Seite im <a href=\"{u}\" target=\"_blank\" rel=\"noopener\">Final Girl Wiki</a> (CC BY-SA).", "extras": "Eigene Karten"},
    "it": {"k": "Come funziona {n}", "m": "La mappa: {n}", "src": "Riassunto dalla pagina della <a href=\"{u}\" target=\"_blank\" rel=\"noopener\">Final Girl Wiki</a> (CC BY-SA).", "extras": "Carte proprie"},
}


def _url(clave):
    t = (CACHE.get(clave) or {}).get("titulo") or clave
    return WIKI + t.replace(" ", "_")


def _lista(items):
    # .top li trae numeración de las listas de tops; aquí van viñetas normales.
    return ('<ul class="mec">' + "".join(f"<li>{x}</li>" for x in items) + "</ul>"
            '<style>.top ul.mec{list-style:disc;padding-left:22px;margin:0 0 12px}'
            '.top ul.mec li{display:list-item;border:0;padding:3px 0}'
            '.top ul.mec li::before{content:none}</style>') if items else ""


def killer(nombre, lang):
    d = (KILLERS.get(nombre) or {}).get(lang) or {}
    if not d.get("mecanicas"):
        return ""
    t = T[lang]
    return (f'<h2>{t["k"].format(n=nombre)}</h2>' + _lista(d["mecanicas"])
            + f'<p class="sub">{t["src"].format(u=_url(nombre))}</p>')


def mapa(loc, lang):
    e = MAPAS.get(loc) or {}
    d = e.get(lang) or {}
    if not (d.get("disposicion") or d.get("mecanicas")):
        return ""
    t = T[lang]
    h = f'<h2>{t["m"].format(n=loc)}</h2>'
    if d.get("disposicion"):
        h += f'<p>{d["disposicion"]}</p>'
    h += _lista(d.get("mecanicas") or [])
    if e.get("extras"):
        h += f'<p class="sub">{t["extras"]}: {", ".join(e["extras"])}</p>'
    return h + f'<p class="sub">{t["src"].format(u=_url(loc))}</p>'
