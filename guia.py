"""Guías de juego dentro de la ficha de cada caja: una del killer y otra del
mapa, por separado porque en Final Girl se pueden mezclar.

El contenido está en guias_datos.py. Aquí solo se pinta. Las fotos de las
cartas llevan filtro de peli vieja (img/guias/<caja>/).
"""
import pathlib

from guias_datos import GUIAS

AQUI = pathlib.Path(__file__).parent

# Direcciones sueltas de la primera guía (estuvieron publicadas unas horas):
# montar.py las redirige a su sección de la ficha.
CAJA = "A Rotten Harvest"
SAL_K = "guia-grimlash.html"
SAL_M = "guia-shady-acres.html"

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
}

CSS = """<style>
.gu-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:14px;margin:12px 0 6px}
.gu-grid figure{margin:0}.gu-grid img,.gu-it img{display:block;background:#ece5d5;padding:5px;border-radius:7px;box-sizing:border-box;cursor:zoom-in;box-shadow:0 10px 22px rgba(0,0,0,.6),0 0 0 1px rgba(0,0,0,.4);transform:rotate(-1.6deg);transition:transform .2s}.gu-grid img{width:100%;aspect-ratio:2/3}.gu-it img{aspect-ratio:5/7}.gu-grid figure:nth-child(even) img,.gu-it:nth-child(even) img{transform:rotate(1.8deg)}.gu-grid img:hover,.gu-it img:hover{transform:rotate(0) scale(1.04)}.gu-zoom{position:fixed;inset:0;z-index:99;background:rgba(0,0,0,.85);display:flex;align-items:center;justify-content:center;cursor:zoom-out}.gu-zoom img{max-width:92vw;max-height:88vh;background:#ece5d5;padding:8px;border-radius:10px;box-shadow:0 20px 50px #000}
.gu-grid figcaption{font-family:var(--f-mono);font-size:11px;letter-spacing:.06em;text-transform:uppercase;margin-top:6px;color:var(--muted)}
.gu-obj{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px;margin:12px 0}
.gu-it{display:flex;gap:12px;align-items:flex-start;background:var(--surface);border:1px solid var(--line);border-radius:3px;padding:10px}
.gu-it img{width:104px;flex:none;margin:2px 4px 4px 2px}.gu-it b.n{display:block;font-size:15px;margin-bottom:4px}
.gu-it p{margin:0;font-size:14px}.gu-ev{margin:10px 0}.gu-ev dt{font-weight:700;margin-top:10px}.gu-ev dd{margin:2px 0 0}
.gu-err{border-left:3px solid var(--blood);padding:4px 0 4px 14px;margin:10px 0}
.gu-ley{font-family:var(--f-mono);font-size:12px;color:var(--muted)}
.gu-sec ul{display:block;padding-left:20px}.gu-sec li{display:list-item!important;grid-template-columns:none!important;margin:4px 0;padding:2px 0!important;border-top:0!important}.gu-sec li b,.gu-sec li i{display:inline!important}.gu-sec li::before{content:none!important}
</style>"""

ZOOM = ('<script>document.addEventListener("click",function(e){var z=document.querySelector(".gu-zoom");if(z){z.remove();return}'
        'var i=e.target.closest(".gu-grid img,.gu-it img");if(!i)return;var d=document.createElement("div");d.className="gu-zoom";'
        'd.innerHTML=\'<img src="\'+i.src+\'" alt="">\';document.body.appendChild(d)})</script>')


def por_caja(film):
    return next((g for g in GUIAS if g["caja"] == film), None)


def por_killer(nombre):
    return next((g for g in GUIAS if g["killer"] == nombre), None)


def _lista(xs):
    return "<ul>" + "".join(f"<li>{x}</li>" for x in xs) + "</ul>"


def _lg(lang):
    return lang if lang in TXT else "en"


def enlaces(lang, g):
    """Los dos enlaces de arriba de la ficha de la caja, que bajan a cada guía."""
    tt = TXT[_lg(lang)]
    return (f'<p class="gu-link" style="font-weight:700">📖 <a href="#{ANCLA["k"]}" style="color:var(--blood)">{tt["k"].format(n=g["killer"])}</a> · '
            f'<a href="#{ANCLA["m"]}" style="color:var(--blood)">{tt["m"].format(n=g["mapa"])}</a></p>')


def secciones(lang, g):
    """Las dos guías como secciones de la ficha de la caja (FR/DE/IT van en inglés)."""
    lg = _lg(lang)
    tt, d = TXT[lg], g[lg]
    pre = "" if lang == "es" else "../"
    ruta = f"{pre}img/guias/{g['dir']}/"

    def bloques(bs):
        return "".join(f"<h3>{t}</h3>{_lista(xs)}" for t, xs in bs)

    def err(t, xs):
        return f'<h3>{t}</h3><div class="gu-err">{_lista(xs)}</div>' if xs else ""

    k = err(d["err_k_t"], d["err_k"]) + bloques(d["bloques_k"])
    m = err(d["err_m_t"], d["err_m"]) + bloques(d["bloques_m"])
    if g["inicios"]:
        m += (f'<h3>{tt["inicios"]}</h3><p class="sub">{tt["inicios_sub"]}</p><div class="gu-grid">' +
              "".join(f'<figure><img src="{ruta}{s}.jpg" alt="{n}" loading="lazy"><figcaption>{n}</figcaption></figure>'
                      for s, n in g["inicios"]) + '</div>')
    if d["obj"]:
        m += (f'<h3>{tt["obj"]}</h3><div class="gu-obj">' +
              "".join(f'<div class="gu-it">' + (f'<img src="{ruta}{s}.jpg" alt="{n}" loading="lazy">' if s else '') +
                      f'<div><b class="n">{n}</b><p>{x}</p></div></div>' for s, n, x in d["obj"]) + '</div>')
    if d.get("falta"):
        m += f'<p class="sub">{d["falta"]}</p>'
    if d["ev"]:
        m += (f'<h3>{tt["ev"].format(n=g["mapa"])}</h3><dl class="gu-ev">' +
              "".join(f'<dt>{n}</dt><dd>{x}</dd>' for n, x in d["ev"]) + '</dl>')
    if d.get("falta_ev"):
        m += f'<p class="sub">{d["falta_ev"]}</p>'
    m += f'<p class="sub">{tt["nota"]}</p>'

    out = [CSS]
    for cual, cuerpo, nombre in (("k", k, g["killer"]), ("m", m, g["mapa"])):
        out.append(f'<section id="{ANCLA[cual]}" class="gu-sec" style="scroll-margin-top:20px;margin-top:40px;'
                   f'border-top:2px solid var(--blood);padding-top:6px"><h2>📖 {tt[cual].format(n=nombre)}</h2>'
                   f'<p class="sub">{tt["mix_" + cual]} <a href="#">{tt["arriba"]}</a></p>'
                   + (f'<p class="gu-ley">{d["ley"]}</p>' if cual == "k" else '') + f'{cuerpo}</section>')
    out.append(ZOOM)
    return "\n".join(out)
