#!/usr/bin/env python3
"""Descarga de la Final Girl Wiki (CC BY-SA) las páginas de cada mapa,
cada killer y cada mecánica que enlazan, a wiki_cache.json.

Solo hechos: lo que se publica sale de aquí y se cita con enlace.
Uso: python3 wiki.py
"""
import json, pathlib, re, time, urllib.parse, urllib.request
import paginas as P

AQUI = pathlib.Path(__file__).parent
API = "https://finalgirl.fandom.com/api.php"

def wikitext(titulo):
    q = urllib.parse.urlencode({"action": "parse", "page": titulo, "prop": "wikitext",
                                "format": "json", "redirects": 1})
    req = urllib.request.Request(f"{API}?{q}", headers={"User-Agent": "finalgirlstats.com wiki reader"})
    d = json.load(urllib.request.urlopen(req, timeout=30))
    if "error" in d:
        return None, None
    return d["parse"]["title"], d["parse"]["wikitext"]["*"]

def main():
    cache = {}
    paginas = {}
    for loc in P.LOCS:
        paginas[loc] = ("loc", loc.replace("Camp Happy Trail", "Camp Happy Trails"))
    for k, d in P.DESC.items():
        if k in P.KILLERS:
            paginas[k] = ("killer", d.get("wiki") or k)
    for clave, (tipo, titulo) in paginas.items():
        t, w = wikitext(titulo)
        cache[clave] = {"tipo": tipo, "titulo": t, "texto": w}
        time.sleep(0.3)
    # Mecánicas enlazadas en la sección Gameplay de cada página
    mec = set()
    for v in cache.values():
        w = v["texto"] or ""
        m = re.search(r"==\s*(Gameplay|Mechanics|Special Rules)\s*==(.*?)(\n==[^=]|\Z)", w, re.S)
        if m:
            mec |= {x.split("|")[0] for x in re.findall(r"\[\[([^\]]+)\]\]", m.group(2)) if not x.startswith("File:")}
    for titulo in sorted(mec):
        t, w = wikitext(titulo)
        cache["mec:" + titulo] = {"tipo": "mecanica", "titulo": t, "texto": w}
        time.sleep(0.3)
    (AQUI / "wiki_cache.json").write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")
    faltan = [k for k, v in cache.items() if not v["texto"]]
    print(len(cache), "páginas;", "sin página:", faltan)

if __name__ == "__main__":
    main()
