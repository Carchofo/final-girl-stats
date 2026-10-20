"""Guías de juego dentro de la ficha de cada caja: una del killer y otra del
mapa, por separado porque en Final Girl se pueden mezclar.

El contenido está en guias_datos.py. Aquí solo se pinta. Las fotos de las
cartas llevan filtro de peli vieja (img/guias/<caja>/).
"""
import pathlib
import re
import unicodedata

from guias_datos import GUIAS

AQUI = pathlib.Path(__file__).parent

# Direcciones sueltas de la primera guía (estuvieron publicadas unas horas):
# montar.py las redirige a su sección de la ficha.
CAJA = "A Rotten Harvest"
SAL_K = "guia-grimlash.html"
SAL_M = "guia-shady-acres.html"

FICHA_K = {"es": "Ficha de {n} →", "en": "{n} page →", "fr": "Fiche de {n} →", "de": "Seite von {n} →", "it": "Scheda di {n} →"}


def _slug(t):
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", t.lower())).strip("-")


ANCLA = {"k": "guia-killer", "m": "guia-mapa"}

TXT = {
    "es": {"k": "Guía de {n} (killer)", "m": "Guía de {n} (mapa)", "arriba": "↑ arriba",
           "mix_k": "Vale con cualquier mapa.", "mix_m": "Vale con cualquier killer.",
           "inicios": "Inicios", "inicios_sub": "K = dónde empieza el killer · figura amarilla = la Final Girl · números = víctimas en cada espacio.",
           "obj": "Objetos", "ev": "Eventos de {n}",
           "nota": "Texto nuestro a partir del reglamento, las cartas y la wiki. Si ves un error, dínoslo."},
    "en": {"k": "{n} guide (killer)", "m": "{n} guide (location)", "arriba": "↑ top",
           "mix_k": "Works with any location.", "mix_m": "Works with any killer.",
           "inicios": "Setups", "inicios_sub": "K = Killer start · yellow figure = Final Girl · numbers = Victims in each space.",
           "obj": "Items", "ev": "{n} events",
           "nota": "Our own wording, based on the rulebook, the cards and the wiki. Spot a mistake? Let us know."},
    "fr": {"k": "Guide de {n} (killer)", "m": "Guide de {n} (lieu)", "arriba": "↑ haut",
           "mix_k": "Se joue avec n'importe quel lieu.", "mix_m": "Se joue avec n'importe quel killer.",
           "inicios": "Mises en place", "inicios_sub": "K = départ du Killer · figurine jaune = la Final Girl · chiffres = Victimes par case.",
           "obj": "Objets", "ev": "Événements de {n}",
           "nota": "Texte à nous, d'après le livret de règles, les cartes et le wiki. Noms des cartes en anglais. Une erreur ? Dites-le-nous."},
    "de": {"k": "Guide zu {n} (Killer)", "m": "Guide zu {n} (Ort)", "arriba": "↑ nach oben",
           "mix_k": "Passt zu jedem Ort.", "mix_m": "Passt zu jedem Killer.",
           "inicios": "Aufbauten", "inicios_sub": "K = Start des Killers · gelbe Figur = die Final Girl · Zahlen = Opfer pro Feld.",
           "obj": "Gegenstände", "ev": "Ereignisse von {n}",
           "nota": "Eigener Text nach Regelheft, Karten und Wiki. Kartennamen auf Englisch. Fehler gefunden? Sag uns Bescheid."},
    "it": {"k": "Guida di {n} (killer)", "m": "Guida di {n} (luogo)", "arriba": "↑ su",
           "mix_k": "Va bene con qualsiasi luogo.", "mix_m": "Va bene con qualsiasi killer.",
           "inicios": "Preparazioni", "inicios_sub": "K = partenza del Killer · figura gialla = la Final Girl · numeri = Vittime per spazio.",
           "obj": "Oggetti", "ev": "Eventi di {n}",
           "nota": "Testo nostro, dal regolamento, dalle carte e dalla wiki. Nomi delle carte in inglese. Un errore? Faccelo sapere."},
}

CSS = """<style>
.gu-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:14px;margin:12px 0 6px}
.gu-grid figure{margin:0}.gu-grid img,.gu-it img{display:block;background:#ece5d5;padding:5px;border-radius:7px;box-sizing:border-box;cursor:zoom-in;box-shadow:0 10px 22px rgba(0,0,0,.6),0 0 0 1px rgba(0,0,0,.4);transform:rotate(-1.6deg);transition:transform .2s}.gu-grid img{width:100%;aspect-ratio:2/3}.gu-it img{aspect-ratio:5/7}.gu-grid figure:nth-child(even) img,.gu-it:nth-child(even) img{transform:rotate(1.8deg)}.gu-grid img:hover,.gu-it img:hover{transform:rotate(0) scale(1.04)}.gu-sec img.ico-k{border-radius:0!important;width:22px;height:22px}.gu-sec img.ico{display:inline-block;width:20px;height:20px;vertical-align:-4px;margin:0 1px;border-radius:50%}.gu-ej{margin:6px 0 14px 20px;padding:10px 14px;background:var(--sunk);border-left:3px solid var(--blood);border-radius:3px;font-size:14.5px}.gu-figs{display:flex;flex-wrap:wrap;gap:18px;margin:8px 0 14px 20px;align-items:flex-start}.gu-figs figure{margin:0;max-width:min(100%,460px)}.gu-figs img{display:block;max-width:100%;max-height:240px;background:#ece5d5;padding:6px;border-radius:7px;box-sizing:border-box;cursor:zoom-in;box-shadow:0 12px 26px rgba(0,0,0,.7),0 0 0 1px rgba(0,0,0,.45);transform:rotate(-1.4deg);transition:transform .2s}.gu-figs figure:nth-child(even) img{transform:rotate(1.6deg)}.gu-figs img:hover{transform:rotate(0) scale(1.03)}.gu-sec h3 img.gu-tico{box-shadow:0 2px 6px rgba(0,0,0,.7),0 0 0 2px #ece5d5}.gu-figs figcaption{font-size:13.5px;line-height:1.45;color:var(--ink);opacity:.85;margin-top:10px;max-width:460px;border-left:2px solid var(--blood);padding-left:8px}.gu-sec h3 img.gu-tico{width:28px;height:28px;border-radius:50%;object-fit:cover;vertical-align:-7px;margin-left:6px}.gu-evc{cursor:help;text-decoration:underline dotted var(--blood);text-underline-offset:4px}.gu-evc::after{content:" 🂠";font-size:13px;opacity:.6}.gu-evpop{position:fixed;z-index:95;width:330px;pointer-events:none;background:#ece5d5;padding:6px;border-radius:8px;box-shadow:0 16px 36px rgba(0,0,0,.8);transform:rotate(-1.5deg)}.gu-evpop img{display:block;width:100%;border-radius:5px}.gu-fase{padding-left:22px;margin:6px 0 12px}.gu-fase li{margin:6px 0;padding-left:4px}.gu-fase li::marker{color:var(--blood);font-weight:700}.gu-foto{margin:14px 0 6px}.gu-foto img{display:block;width:100%;border-radius:6px;cursor:zoom-in;box-shadow:0 10px 22px rgba(0,0,0,.6)}.gu-zoom{position:fixed;inset:0;z-index:99;background:rgba(0,0,0,.85);display:flex;align-items:center;justify-content:center;cursor:zoom-out}.gu-zoom img{max-width:92vw;max-height:88vh;background:#ece5d5;padding:8px;border-radius:10px;box-shadow:0 20px 50px #000}
.gu-grid figcaption{font-family:var(--f-mono);font-size:11px;letter-spacing:.06em;text-transform:uppercase;margin-top:6px;color:var(--muted)}
.gu-obj{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px;margin:12px 0}
.gu-it{display:flex;gap:12px;align-items:flex-start;background:var(--surface);border:1px solid var(--line);border-radius:3px;padding:10px}
.gu-it img{width:104px;flex:none;margin:2px 4px 4px 2px}.gu-it b.n{display:block;font-size:15px;margin-bottom:4px}
.gu-it p{margin:0;font-size:14px}.gu-ev{margin:10px 0}.gu-ev dt{font-weight:700;margin-top:10px}.gu-sec [id]{scroll-margin-top:20px}.gu-hit{outline:2px solid var(--blood);outline-offset:4px}.gu-ev dd{margin:2px 0 0}
.gu-err{border-left:3px solid var(--blood);padding:4px 0 4px 14px;margin:10px 0}
.gu-ley{font-family:var(--f-mono);font-size:12px;color:var(--muted)}
.gu-sec ul{display:block;padding-left:20px}.gu-sec li{display:list-item!important;grid-template-columns:none!important;margin:4px 0;padding:2px 0!important;border-top:0!important}.gu-sec li b,.gu-sec li i{display:inline!important}.gu-sec li::before{content:none!important}
</style>"""

EVPOP = ('<script>(function(){var p;function q(){if(p){p.remove();p=null}}'
         'function ver(t,x,y){q();p=document.createElement("div");p.className="gu-evpop";p.innerHTML=\'<img src="\'+t.dataset.img+\'" alt="">\';document.body.appendChild(p);'
         'var w=330,h=230,X=Math.min(x+18,innerWidth-w-10),Y=Math.min(Math.max(10,y-h/2),innerHeight-h-10);p.style.left=X+"px";p.style.top=Y+"px"}'
         'document.addEventListener("mouseover",function(e){var t=e.target.closest(".gu-evc");if(t)ver(t,e.clientX,e.clientY)});'
         'document.addEventListener("mousemove",function(e){if(p&&e.target.closest(".gu-evc")){var w=330,h=230;p.style.left=Math.min(e.clientX+18,innerWidth-w-10)+"px";p.style.top=Math.min(Math.max(10,e.clientY-h/2),innerHeight-h-10)+"px"}});'
         'document.addEventListener("mouseout",function(e){if(e.target.closest(".gu-evc"))q()});'
         'document.addEventListener("click",function(e){var t=e.target.closest(".gu-evc");if(t&&matchMedia("(hover:none)").matches){var r=t.getBoundingClientRect();p?q():ver(t,Math.min(r.left,innerWidth-250),r.bottom+170)}else if(!t)q()})})()</script>')
ZOOM = ('<script>document.addEventListener("click",function(e){var z=document.querySelector(".gu-zoom");if(z){z.remove();return}'
        'var i=e.target.closest(".gu-grid img,.gu-it img,.gu-foto img,.gu-figs img");if(!i)return;var d=document.createElement("div");d.className="gu-zoom";'
        'd.innerHTML=\'<img src="\'+i.src+\'" alt="">\';document.body.appendChild(d)})</script>')


def ancla(*partes):
    """Id estable para enlazar desde el buscador a un trozo de la guía."""
    t = unicodedata.normalize("NFKD", "-".join(partes)).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", re.sub(r"<[^>]+>", "", t).lower()).strip("-")


def por_caja(film):
    return next((g for g in GUIAS if g["caja"] == film), None)


def por_killer(nombre):
    return next((g for g in GUIAS if g["killer"] == nombre), None)


def _lista(xs):
    return "<ul>" + "".join(f"<li>{x}</li>" for x in xs) + "</ul>"


def _lg(lang, g=None):
    """Idioma de la guía; si aún no hay traducción, en inglés."""
    if lang in TXT and (g is None or lang in g):
        return lang
    return "en" if g is None or "en" in g else "es"


def enlaces(lang, g):
    """Los dos enlaces de arriba de la ficha de la caja, que bajan a cada guía."""
    tt = TXT[_lg(lang, g)]
    return (f'<p class="gu-link" style="font-weight:700">📖 <a href="#{ANCLA["k"]}" style="color:var(--blood)">{tt["k"].format(n=g["killer"])}</a> · '
            f'<a href="#{ANCLA["m"]}" style="color:var(--blood)">{tt["m"].format(n=g["mapa"])}</a></p>')


# Iconos de verdad (recortados de las cartas, img/ico/) junto a la palabra que
# los nombra. Por caja, porque "ojo" solo es un icono en Volk'ar.
ICO_PAL = {
    "The Green Terror": {
        "es": [(r"(?:dos |un |el )?ojos? tachados?", "ojo-tachado"), (r"4 ojos morados|\bReveal\b", "reveal"), (r"\bojo\b", "ojo")],
        "en": [(r"(?:two |a |the )?crossed-out eyes?", "ojo-tachado"), (r"4 purple eyes|\bReveal\b", "reveal"), (r"\beye\b", "ojo")],
        "fr": [(r"(?:deux |un )?(?:œil barré|yeux barrés)", "ojo-tachado"), (r"4 yeux violets|\bReveal\b", "reveal"), (r"\bœil\b", "ojo")],
        "de": [(r"durchgestrichene[ns]? Augen?", "ojo-tachado"), (r"4 violetten Augen|\bReveal\b", "reveal"), (r"\bAuge\b", "ojo")],
        "it": [(r"(?:due |un )?(?:occhio barrato|occhi barrati)", "ojo-tachado"), (r"4 occhi viola|\bReveal\b", "reveal"), (r"\bocchio\b", "ojo")],
    },
}
ICO_LEY = {
    "The Green Terror": {
        "es": "{ojo} = carta boca arriba al Path · {ojo-tachado} = carta boca abajo · {reveal} = Reveal, se revela",
        "en": "{ojo} = faceup card to the Path · {ojo-tachado} = facedown card · {reveal} = Reveal",
        "fr": "{ojo} = carte face visible au Path · {ojo-tachado} = carte face cachée · {reveal} = Reveal, elle se révèle",
        "de": "{ojo} = Karte offen in den Path · {ojo-tachado} = Karte verdeckt · {reveal} = Reveal, sie wird enthüllt",
        "it": "{ojo} = carta scoperta nel Path · {ojo-tachado} = carta coperta · {reveal} = Reveal, si rivela",
    },
}


# Emojis puestos a falta de foto, cambiados por el icono real recortado.
ICO_EMOJI = {"A Knock at the Door": {"🔺": "asesino-arriba", "🔻": "asesino-abajo"}}


def ico(n):
    return f'<img class="ico" src="/img/ico/{n}.png" alt="" width="20" height="20">'


def con_iconos(html, caja, lang):
    """Pone el icono detrás de cada palabra que lo nombra, sin tocar etiquetas."""
    pal = ICO_PAL.get(caja, {}).get(lang)
    if not pal:
        pal = []
    patron = re.compile("|".join(f"(?P<i{i}>{p})" for i, (p, _) in enumerate(pal)) or r"(?!x)x")

    def cambia(m):
        n = pal[int(m.lastgroup[1:])][1]
        return m.group(0) + " " + ico(n)
    trozos = re.split(r"(<[^>]+>)", html)
    out = [t if t.startswith("<") else patron.sub(cambia, t) for t in trozos]
    html = "".join(out).replace("👁", ico("ojo"))
    for e, n in ICO_EMOJI.get(caja, {}).items():
        html = html.replace(e, f'<img class="ico ico-k" src="/img/ico/{n}.png" alt="" width="22" height="22">')
    return html


def secciones(lang, g):
    """Las dos guías como secciones de la ficha de la caja."""
    lg = _lg(lang, g)
    tt, d = TXT[lg], g[lg]
    pre = "" if lang == "es" else "../"
    ruta = f"{pre}img/guias/{g['dir']}/"

    def bloques(c, bs):
        figs, icos = g.get("figs_" + c, {}), g.get("icos_" + c, {})

        def tit(i, t):
            return t + (f' <img class="gu-tico" src="{ruta}{icos[i]}.jpg" alt="">' if i in icos else "")

        def fig(i):
            if i not in figs:
                return ""
            hay = [(f, c) for f, c in figs[i] if (AQUI / "img" / "guias" / g["dir"] / f"{f}.jpg").exists()]
            sin = [c for f, c in figs[i] if (f, c) not in hay]
            ej = "".join(f'<p class="gu-ej">{(c.get(lg, c.get("en", "")) if isinstance(c, dict) else c)}</p>' for c in sin if isinstance(c, dict))
            if not hay:
                return ej
            return ej + ('<div class="gu-figs">' + "".join(
                f'<figure><img src="{ruta}{f}.jpg" alt="{cap}" loading="lazy">' + (f'<figcaption>{cap}</figcaption>' if cap else '') + '</figure>'
                for f, cap in ((f, c.get(lg, c.get("en", "")) if isinstance(c, dict) else c) for f, c in hay)) + '</div>')
        return "".join(f'<h3 id="{ancla(c, t)}">{tit(i, t)}</h3>{_lista(xs)}{fig(i)}' for i, (t, xs) in enumerate(bs))

    def err(c, t, xs):
        return f'<h3 id="{ancla(c, "ojo")}">{t}</h3><div class="gu-err">{_lista(xs)}</div>' if xs else ""

    fase = ""
    if d.get("fase"):
        fase = (f'<h3 id="{ancla("k", "fase")}">{d["fase_t"]}</h3><ol class="gu-fase">' +
                "".join(f"<li>{x}</li>" for x in d["fase"]) + "</ol>")
        if g.get("fase_fig"):
            fase += (f'<div class="gu-figs"><figure><img src="{ruta}{g["fase_fig"]}.jpg" alt="" loading="lazy"></figure></div>')
    k = fase + err("k", d["err_k_t"], d["err_k"]) + bloques("k", d["bloques_k"])
    m = err("m", d["err_m_t"], d["err_m"]) + bloques("m", d["bloques_m"])
    if g["inicios"]:
        m += (f'<h3>{tt["inicios"]}</h3><p class="sub">{tt["inicios_sub"]}</p><div class="gu-grid">' +
              "".join(f'<figure id="{ancla("ini", s)}"><img src="{ruta}{s}.jpg" alt="{n}" loading="lazy"><figcaption>{n}</figcaption></figure>'
                      for s, n in g["inicios"]) + '</div>')
    if d["obj"]:
        m += (f'<h3>{tt["obj"]}</h3><div class="gu-obj">' +
              "".join(f'<div class="gu-it" id="{ancla("obj", n)}">' + (f'<img src="{ruta}{s}.jpg" alt="{n}" loading="lazy">' if s else '') +
                      f'<div><b class="n">{n}</b><p>{x}</p></div></div>' for s, n, x in d["obj"]) + '</div>')
    if d.get("falta"):
        m += f'<p class="sub">{d["falta"]}</p>'
    if d["ev"]:
        m += (f'<h3>{tt["ev"].format(n=g["mapa"])}</h3><dl class="gu-ev">' +
              "".join(f'<dt id="{ancla("ev", n)}"' + (f' class="gu-evc" tabindex="0" data-img="{ruta}{ancla("ev", n)}.jpg"' if (AQUI / "img" / "guias" / g["dir"] / f'{ancla("ev", n)}.jpg').exists() else '') + f'>{n}</dt><dd>{x}</dd>' for n, x in d["ev"]) + '</dl>')
    if d.get("falta_ev"):
        m += f'<p class="sub">{d["falta_ev"]}</p>'
    m += f'<p class="sub">{tt["nota"]}</p>'

    def foto(c, nombre):
        f = "foto-finales" if c == "k" else "foto-tablero"
        if not (AQUI / "img" / "guias" / g["dir"] / f"{f}.jpg").exists():
            return ""
        return f'<figure class="gu-foto"><img src="{ruta}{f}.jpg" alt="{nombre}" loading="lazy"></figure>'

    ley = d["ley"]
    if g["caja"] in ICO_LEY:
        extra = ICO_LEY[g["caja"]][lg]
        for n in ("ojo-tachado", "ojo", "reveal"):
            extra = extra.replace("{" + n + "}", ico(n))
        ley = extra + " · " + ley
    k = con_iconos(k, g["caja"], lg)
    m = con_iconos(m, g["caja"], lg)
    ley = con_iconos(ley, g["caja"], lg)

    out = [CSS]
    for cual, cuerpo, nombre in (("k", k, g["killer"]), ("m", m, g["mapa"])):
        out.append(f'<section id="{ANCLA[cual]}" class="gu-sec" style="scroll-margin-top:20px;margin-top:40px;'
                   f'border-top:2px solid var(--blood);padding-top:6px"><h2>📖 {tt[cual].format(n=nombre)}</h2>'
                   f'<p class="sub">{tt["mix_" + cual]} <a href="#">{tt["arriba"]}</a>'
                   + (f' · <a href="{_slug(g["killer"])}.html">{FICHA_K[lg].format(n=g["killer"])}</a>' if cual == "k" else '')
                   + (f' · <a href="#{ANCLA["k" if cual == "m" else "m"]}">{tt["k" if cual == "m" else "m"].format(n=g["killer"] if cual == "m" else g["mapa"])}</a>')
                   + '</p>'
                   + (f'<p class="gu-ley">{ley}</p>' if cual == "k" else '') + foto(cual, nombre) + f'{cuerpo}</section>')
    out.append(ZOOM)
    out.append(EVPOP)
    return "\n".join(out)
