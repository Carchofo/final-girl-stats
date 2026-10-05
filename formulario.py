"""Lee la estructura publica del Google Form de la hoja comunitaria y la
guarda en fg_form.json para el atajo de registrar.html.

Solo lee: el formulario publica sus campos en la propia pagina
(FB_PUBLIC_LOAD_DATA_). Ejecutar si cambian los campos: python3 formulario.py
"""
import json, re, urllib.request
from pathlib import Path

URL = ("https://docs.google.com/forms/d/e/"
       "1FAIpQLSf8Y8_bLqYdGlhHaf1VIod8FQfCH3r9qch6LXo0oyBeCJENiw/viewform")

html = urllib.request.urlopen(URL, timeout=30).read().decode("utf-8")
data = json.loads(re.search(r"FB_PUBLIC_LOAD_DATA_ = (.*?);</script>", html, re.S).group(1))

base, setup, killer = {}, {}, {}
seccion = None
for it in data[1][1]:
    titulo = it[1] or ""
    if len(it) < 5 or not it[4]:
        seccion = titulo.strip()
        continue
    if it[3] not in (0, 2, 3):          # solo texto, opcion unica y desplegable
        continue
    q = it[4][0]
    campo = {"entry": q[0], "ops": [o[0] for o in (q[1] or []) if o and o[0]],
             "req": bool(q[2])}
    if titulo == "Input Optional Data?":
        continue
    if titulo.endswith(" Setup"):
        setup[seccion] = campo
    elif titulo.startswith("Location (") or titulo.endswith(f"({seccion})") or (
            seccion in killer or titulo in ("How did you die?",)):
        k = seccion
        nombre = re.sub(r"\s*\(.*\)$", "", titulo).rstrip("?").strip()
        nombre = {"Location": "loc", "Finale Card": "finale",
                  "Dark Power Card": "dp"}.get(nombre, nombre)
        killer.setdefault(k, {})[nombre] = campo
    elif seccion is None or titulo in ("Final Girl", "Custom Final Girl", "Killer",
            "Who won the game?", "Final Health Revive?", "Difficulty Settings", "Nickname"):
        base[titulo] = campo
    else:
        # Extras de mapa, como Victory Type en USS Konrad o Missions en Falconwood.
        setup.setdefault("_extra", {}).setdefault(seccion, {})[titulo.rstrip("?")] = campo

out = {"base": base, "setup": setup, "killer": killer}
Path(__file__).with_name("fg_form.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(base), "base ·", len([k for k in setup if k != "_extra"]), "setups ·", len(killer), "killers")
