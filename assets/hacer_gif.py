from PIL import Image, ImageSequence, ImageDraw, ImageFilter, ImageChops

TV = "static-tv.gif"
SALIDA = "tv_resultado.gif"
SCREEN_BOX = (18, 30, 152, 140)   # pantalla medida sobre el frame real (TV 220x175)

# Guion de la animacion, de arriba a abajo.
#   ("tv", ms)            -> estatica normal durante ese tiempo
#   ("flash", ruta, ms)   -> la imagen aparece en pantalla ese tiempo
# Un "flash" corto se reparte en varios fotogramas de la estatica de debajo,
# para que no sea una foto congelada sino un destello con ruido detras.
GUION = [
    ("tv", 2000),
    ("flash", "FG_FF1_Hans_FinaleCards_v2_11-03-20-1_1500x.webp", 200),
    ("tv", 2000),
    ("flash", "Sledgemassart (2).webp", 200),
    ("tv", 1000),
    ("flash", "hqdefault.jpg", 200),
    ("tv", 1200),
]

sx0, sy0, sx1, sy1 = SCREEN_BOX
sw, sh = sx1 - sx0, sy1 - sy0


def quitar_bandas(im, umbral=18):
    """Recorta el letterbox negro (hqdefault.jpg es 16:9 dentro de 4:3)."""
    gris = im.convert("L")
    caja = ImageChops.add(gris, gris, 1.0, -umbral).getbbox()
    return im.crop(caja) if caja else im


def encajar(ruta):
    """Escala para cubrir la pantalla y recorta el sobrante, sin deformar."""
    im = quitar_bandas(Image.open(ruta).convert("RGB"))
    escala = max(sw / im.width, sh / im.height)
    im = im.resize((round(im.width * escala), round(im.height * escala)), Image.LANCZOS)
    izq, arr = (im.width - sw) // 2, (im.height - sh) // 2
    return im.crop((izq, arr, izq + sw, arr + sh))


# Esquinas redondeadas: un recorte cuadrado sobre un CRT canta.
mascara = Image.new("L", (sw, sh), 0)
ImageDraw.Draw(mascara).rounded_rectangle((0, 0, sw - 1, sh - 1), radius=14, fill=255)
mascara = mascara.filter(ImageFilter.GaussianBlur(1.2))

scan = Image.new("L", (sw, sh), 255)
d = ImageDraw.Draw(scan)
for y in range(0, sh, 3):
    d.line((0, y, sw, y), fill=215)
scan_rgb = Image.merge("RGB", (scan, scan, scan))

tv_gif = Image.open(TV)
gif_frames = [f.copy().convert("RGB") for f in ImageSequence.Iterator(tv_gif)]
DUR = tv_gif.info.get("duration", 100)

# --- Reflejo de la pantalla ------------------------------------------------
# El brillo del cristal esta en TODOS los fotogramas; el ruido de la estatica
# cambia en cada uno. Promediando los 26 el ruido se cancela y queda el
# reflejo limpio. Sin esto, al pegar la imagen el brillo desaparece y se nota
# que hay algo pegado encima en vez de algo mostrandose EN la tele.
medio = gif_frames[0].crop(SCREEN_BOX).convert("L")
for n, f in enumerate(gif_frames[1:], start=2):
    medio = Image.blend(medio, f.crop(SCREEN_BOX).convert("L"), 1.0 / n)

# Solo lo que destaca sobre el nivel medio de la pantalla es reflejo: la
# mediana da ese nivel sin que la arrastren el brillo ni las zonas oscuras.
hist = medio.histogram()
total, suma, base = sum(hist), 0, 0
for valor, cuenta in enumerate(hist):
    suma += cuenta
    if suma >= total / 2:
        base = valor
        break
brillo = medio.point(lambda v: max(0, v - base) * 2).filter(ImageFilter.GaussianBlur(2))


def con_reflejo(img):
    """Superpone el brillo del cristal, en modo pantalla (screen)."""
    inv_img = ImageChops.invert(img)
    inv_luz = ImageChops.invert(Image.merge("RGB", (brillo, brillo, brillo)))
    return ImageChops.invert(ImageChops.multiply(inv_img, inv_luz))

frames, durations = [], []
i = 0  # avanza siempre, para que la estatica no se repita igual tras cada corte

for paso in GUION:
    if paso[0] == "tv":
        _, ms = paso
        for _ in range(max(1, round(ms / DUR))):
            frames.append(gif_frames[i % len(gif_frames)])
            durations.append(DUR)
            i += 1
    else:
        _, ruta, ms = paso
        imagen = con_reflejo(Image.blend(encajar(ruta), scan_rgb, 0.10))
        n = max(1, round(ms / DUR))
        for _ in range(n):
            fondo = gif_frames[i % len(gif_frames)].copy()
            fondo.paste(imagen, (sx0, sy0), mascara)
            frames.append(fondo)
            durations.append(DUR)
            i += 1

frames[0].save(
    SALIDA, save_all=True, append_images=frames[1:],
    duration=durations, loop=0, optimize=False, disposal=2,
)
print(f"{SALIDA}: {len(frames)} frames, {sum(durations)} ms")
for paso in GUION:
    print(f"  {paso[-1]:>5} ms  " + ("estatica" if paso[0] == "tv" else paso[1]))
