"""Copias ligeras de las imágenes que se ven pequeñas, y la cinta VHS en WebP.

Las portadas son de 500x700 y pesan 100-150 KB, pero en la tira de la
portada, las filas de los tops y la tier list se ven a 30-104 px: la home
bajaba 2,3 MB de imágenes y los tops más de 4. Aquí se sacan copias en
img/mini/ con la misma ruta que la original (img/shriek.jpg ->
img/mini/shriek.jpg). La original no se toca y sigue donde se ve grande.

Una copia solo se rehace si cambia su original: la huella de cada original
se guarda en img/mini/huellas.json. Así una portada recortada a mano
(pasó con Shriek) se refresca sola en el siguiente montaje.

Sin PIL (el PC) no se genera nada. Quien pinta una miniatura comprueba
antes que exista (mini_de) o, en el JavaScript, vuelve a la original con
onerror si no está.
"""
import hashlib
import json
from pathlib import Path

AQUI = Path(__file__).parent
IMG = AQUI / "img"
MINI = IMG / "mini"
HUELLAS = MINI / "huellas.json"

# (patrón dentro de img/, ancho en px). El ancho es el doble de lo más grande
# que se pinta la copia (104 px en la tier list), algo menos en las portadas:
# a 280 px seguían pesando 30-35 KB por el grano del dibujo.
GRUPOS = [
    ("*.jpg", 240),             # portadas de las cajas
    ("temporadas/*.jpg", 320),  # arte de cada temporada (150-220 KB)
    ("art/*.jpg", 280),         # arte de cada killer: 400 px, en los tops se ve a 28
    ("loc/*.png", 280),         # logos de los mapas: 480x93 y hasta 130 KB
]
ANCHO_GUIA = 240                # objetos de las guías: se ven a 108x148

# La cinta VHS: cabecera de la home (1200 px, y 800 en el móvil) y textura de
# fondo de todas las páginas. El fondo va al 13 % de opacidad: no necesita
# detalle, y el filtro que le ponía el CSS (grayscale .35, contrast .85) va
# ya aplicado en la imagen, así el navegador no lo recalcula.
VHS = IMG / "vhs-final-girl.jpg"
VHS_SALIDAS = [("vhs-final-girl.webp", 1200, 70, False),
               ("vhs-final-girl-m.webp", 800, 66, False),
               ("fondo-vhs.webp", 720, 42, True)]


def _huellas():
    try:
        return json.loads(HUELLAS.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _huella(p, extra):
    return hashlib.md5(p.read_bytes() + str(extra).encode()).hexdigest()[:16]


def _copia(src, dst, ancho, Image):
    im = Image.open(src)
    if im.width > ancho:
        im = im.resize((ancho, round(im.height * ancho / im.width)), Image.LANCZOS)
    dst.parent.mkdir(parents=True, exist_ok=True)
    if src.suffix.lower() == ".png":
        im = im.convert("RGBA").quantize(256, method=Image.Quantize.FASTOCTREE)
        im.save(dst, optimize=True)
    else:
        im.convert("RGB").save(dst, "JPEG", quality=78, optimize=True, progressive=True)


def _vhs(Image):
    from PIL import ImageOps
    base = Image.open(VHS).convert("RGB")
    for nombre, ancho, q, fondo in VHS_SALIDAS:
        im = base.resize((ancho, round(base.height * ancho / base.width)), Image.LANCZOS)
        if fondo:
            im = Image.blend(im, ImageOps.grayscale(im).convert("RGB"), .35)
            im = im.point(lambda v: round((v - 128) * .85 + 128))
        im.save(IMG / nombre, "WEBP", quality=q, method=6)


def generar():
    """Crea o rehace las copias que falten o cuyo original haya cambiado."""
    try:
        from PIL import Image
    except ImportError:
        return 0
    h, hechas = _huellas(), 0
    for patron, ancho in GRUPOS:
        for src in sorted(IMG.glob(patron)):
            if src.name.startswith("vhs-final-girl"):
                continue
            rel = src.relative_to(IMG).as_posix()
            dst = MINI / rel
            hu = _huella(src, ancho)
            if dst.exists() and h.get(rel) == hu:
                continue
            _copia(src, dst, ancho, Image)
            h[rel] = hu
            hechas += 1
    if VHS.exists():
        hu = _huella(VHS, VHS_SALIDAS)
        if h.get("vhs") != hu or not all((IMG / n).exists() for n, *_ in VHS_SALIDAS):
            _vhs(Image)
            h["vhs"] = hu
            hechas += 1
    if hechas:
        MINI.mkdir(parents=True, exist_ok=True)
        HUELLAS.write_text(json.dumps(h, indent=0, sort_keys=True), encoding="utf-8")
    return hechas


def mini_de(rel, ancho=None):
    """Ruta (dentro de img/) de la copia pequeña de img/<rel>, o None.

    Con ancho, la crea si falta (las de las guías se piden así, una a una).
    """
    rel = rel.replace("\\", "/")
    src, dst = IMG / rel, MINI / rel
    if not src.exists():
        return None
    if ancho:
        h = _huellas()
        hu = _huella(src, ancho)
        if not dst.exists() or h.get(rel) != hu:
            try:
                from PIL import Image
            except ImportError:
                return "mini/" + rel if dst.exists() else None
            _copia(src, dst, ancho, Image)
            h[rel] = hu
            HUELLAS.write_text(json.dumps(h, indent=0, sort_keys=True), encoding="utf-8")
    return "mini/" + rel if dst.exists() else None


if __name__ == "__main__":
    print(generar(), "imágenes nuevas o rehechas")
