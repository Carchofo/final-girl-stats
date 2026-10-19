"""Guías de juego por caja (de momento, A Rotten Harvest).

El texto es nuestro: las reglas y las cartas explicadas con nuestras palabras
a partir del reglamento y de las cartas de Rafel. Las fotos de las cartas
llevan filtro de peli vieja (img/guias/<caja>/).

Iconos que aún no tenemos claros se escriben tal cual (🎭 = la máscara de la
carta) para no inventar qué hacen.
"""
import pathlib

AQUI = pathlib.Path(__file__).parent

CAJA = "A Rotten Harvest"
KILLER = "Grimlash"
MAPA = "Shady Acres"
SAL_K = "guia-grimlash.html"
SAL_M = "guia-shady-acres.html"
SALIDAS = (SAL_K, SAL_M)
DIR = "img/guias/a-rotten-harvest/"

INICIOS = ["reap-what-you-sow", "final-crop", "dusk-sacrifice", "harvest-season", "demands-of-the-earth"]
INICIO_N = {"reap-what-you-sow": "Reap What You Sow", "final-crop": "Final Crop", "dusk-sacrifice": "Dusk Sacrifice",
            "harvest-season": "Harvest Season", "demands-of-the-earth": "Demands of the Earth"}

T = {
    "es": {
        "title": "Guía de A Rotten Harvest (Final Girl): reglas, objetos y eventos de Shady Acres",
        "desc": "Cómo se juega A Rotten Harvest: Grimlash, los Children, las Ancient Curses, los Field Spaces, los 5 inicios, todos los objetos y eventos, y errores frecuentes.",
        "eb": "Guía · Temporada 4 · Grimlash en Shady Acres",
        "h1": 'A Rotten Harvest<span class="roja">guía de juego</span>',
        "dek": "Las reglas especiales de la caja explicadas en corto, los objetos y eventos de Shady Acres, y los errores que más se cometen. Para consultar en mitad de la partida.",
        "ficha": "Estadísticas de la caja",
        "nota": "Texto nuestro a partir del reglamento y las cartas. Si ves un error, dínoslo.",
        "leyenda": "🩸 = Bloodlust · 🌾 = Field Space · 🎭 = el icono de la máscara de la carta",
        "s_err": "Errores frecuentes",
        "err": [
            "<b>Grimlash se mueve 1</b> en su Killer Action. Cuando una carta de Terror trae el icono de la <b>bota</b> (mover), se mueve lo que marque su movimiento en el nivel actual de 🩸, no 1.",
            "Los <b>Children no son Minions</b>, pero sí Enemies: no resuelven las acciones de Killer o Minion de las cartas de Terror, salvo que la carta diga que las hacen ellos.",
            "<b>Si mezclas Shady Acres con otro killer</b>, los Children siguen sin ser Minions: las cartas de ese killer que hablan de Minions no les afectan.",
            "Si atacas a los Children y hay varios en el espacio, <b>los atacas a todos</b> y repartes el daño; el que sobra se pierde.",
            "Una abducción en un espacio <b>sin víctimas</b> no se pierde: cuenta como un ataque.",
        ],
        "s_killer": "Grimlash",
        "killer": [
            "Empieza con <b>4 de Horror y 10 de vida</b>.",
            "Fase inicial: Target Final Girl or Victim → Move 1 → Attack → si ha muerto una víctima, <b>1 Harvest Madness</b>.",
            "<b>Harvest Madness</b> te da habilidades extra, pero acaba matándote.",
        ],
        "s_prep": "Preparación especial",
        "prep": [
            "Baraja las <b>Ancient Curses</b> y déjalas boca abajo.",
            "Pon la carta de <b>Children</b> junto al tablero, un Child en el <b>Altar of the Old Gods</b> y el resto sobre la carta.",
            "Coloca el token de acción de los Children <b>encima</b> de las acciones de Minion o Killer de la carta de Finale: actúan antes que el resto de enemigos.",
        ],
        "s_reglas": "Reglas especiales",
        "h_children": "Los Children",
        "children": [
            "Su carta marca su vida, ataque y movimiento. Son Enemies, no Minions.",
            "Actúan al <b>principio de la fase del Killer</b>, antes que Minions y Killer, uno a uno: del más cercano al Altar al más lejano.",
            "En cada <b>Upkeep</b> aparece un Child en el Altar, salvo que ya estén los tres en el tablero o no queden víctimas.",
            "Se pueden atacar y matar: el muerto vuelve a la carta y puede volver a salir.",
            "Las víctimas te siguen a un espacio con Children, salvo que también esté el Killer.",
            "En la fase de Panic, las víctimas en un espacio con un Child entran en pánico si ese turno ha muerto al menos una víctima.",
        ],
        "h_abd": "Abducciones",
        "abd": [
            "Cuando un Child resuelve el icono de abducción en un espacio con víctima, tira un dado.",
            "<b>1-2:</b> la víctima se sacrifica en el Altar (muere). El Child vuelve al Altar, sube el 🩸 como siempre y la víctima va al dorso de la carta de arriba de las Ancient Curses.",
            "<b>3-6:</b> no pasa nada.",
        ],
        "h_curse": "Ancient Curses",
        "curse": ["Con <b>3 víctimas sacrificadas</b> encima, se quitan y se revela la maldición, que entra en juego. Puede haber varias a la vez."],
        "h_field": "Field Spaces 🌾",
        "field": ["Los espacios con la espiga son Field Spaces. Muchas cartas de la caja los usan, para bien y para mal."],
        "s_inicios": "Los 5 inicios",
        "inicios_sub": "K = dónde empieza el killer · figura amarilla = la Final Girl · números = víctimas en cada espacio.",
        "s_obj": "Objetos",
        "obj": [
            ("moonshine-jug", "Moonshine Jug", "Descártalo para recuperar <b>4 de vida</b>."),
            ("cowboy-boots", "Cowboy Boots", "2 usos. Muévete hasta <b>2 espacios</b>."),
            ("pilgrims-hat", "Pilgrim's Hat", "Si empiezas el movimiento en un 🌾, puedes moverte <b>1 espacio más</b>."),
            ("farmers-almanac", "Farmer's Almanac", "2 usos. Tras robar una carta de <b>Terror</b> y antes de resolverla, puedes ponerla al fondo y robar la siguiente."),
            ("mechanics-toolbox", "Mechanic's Toolbox", "Descártala para recuperar <b>1 objeto descartado</b>, con todos sus usos."),
            ("childrens-toys", "Children's Toys", "2 usos. Cambia un <b>Child</b> de tu espacio por una víctima normal."),
            ("locus-of-insanity", "Locus of Insanity", "3 usos. Una vez por turno, con 🎭, puedes ponerte en <b>cualquier 🌾</b>."),
            ("scythe", "Scythe", "Arma · alcance 0-1 · 1 daño · 2 manos. Al atacar Enemies en un 🌾, puedes <b>repartir el daño</b> entre ellos. Luego ese espacio queda <b>Harvested</b> y deja de ser 🌾."),
            ("pilgrims-musket", "Pilgrim's Musket", "Arma · alcance 1 · 2 daños · 2 manos · 2 usos. <b>No sirve</b> contra Enemies en un 🌾."),
            ("rusty-pitchfork", "Rusty Pitchfork", "Arma · alcance 0 · 2 daños · 2 manos. Si tu tirada final de Horror no saca <b>ningún éxito</b>, se descarta."),
            ("decrepit-plow", "Decrepit Plow", "Arma · alcance 0 · 2 daños · 1 mano · 2 usos."),
            ("sickle", "Sickle", "Arma · alcance 0 · 1 daño · 1 mano. Sin límite de usos."),
        ],
        "obj_falta": "Faltan por fotografiar: Bag of Feed, Combine Keys, Corn Cob Pipe y Cornhusk Effigy.",
        "s_ev": "Eventos de Shady Acres",
        "ev": [
            ("Umbral Evocation", "Pon el token <b>Harvest Shadow</b> en el espacio del Killer. Cada vez que tú o una víctima entráis ahí: 🩸."),
            ("Acres of Hatred", "Por cada 🌾 con al menos una víctima: 🩸 (máx. 2). Se descarta."),
            ("“The Fields Are Moving…”", "Pon un token de Field en <b>Hayfield</b> y <b>Cow Pasture</b>: pasan a ser 🌾."),
            ("Festering Rot", "Cada vez que muere una víctima en un 🌾: 🎭."),
            ("It Hungers For Us", "Todas las víctimas entran en pánico. Por cada víctima en el espacio del Killer o adyacente: 🎭 (máx. 3). Se descarta."),
            ("Harvest Cultist", "La víctima más cercana a ti pasa a ser el Cultist. En cada Upkeep se acerca 1 espacio a ti; si está contigo, os movéis los dos 1 espacio hacia el Killer. Salvarla tiene premio."),
            ("Ralph the Mechanic", "Ralph empieza en <b>Ralph's Garage</b>. Mientras esté contigo, los objetos con usos limitados que cojas ganan un uso extra."),
            ("Sally McCoy", "Sally empieza en la <b>McCoy Farmhouse</b>. Al salvarla, busca las <b>Combine Keys</b> en el mazo de objetos."),
        ],
    },
    "en": {
        "title": "A Rotten Harvest guide (Final Girl): Shady Acres rules, items and events",
        "desc": "How to play A Rotten Harvest: Grimlash, the Children, Ancient Curses, Field Spaces, the 5 setups, every item and event, and common mistakes.",
        "eb": "Guide · Season 4 · Grimlash at Shady Acres",
        "h1": 'A Rotten Harvest<span class="roja">play guide</span>',
        "dek": "The box's special rules in short, the Shady Acres items and events, and the most common mistakes. Made to check mid-game.",
        "ficha": "Box stats",
        "nota": "Our own wording, based on the rulebook and the cards. Spot a mistake? Let us know.",
        "leyenda": "🩸 = Bloodlust · 🌾 = Field Space · 🎭 = the card's mask icon",
        "s_err": "Common mistakes",
        "err": [
            "<b>Grimlash moves 1</b> in his Killer Action. When a Terror card shows the <b>boot</b> (move) icon, he moves whatever his movement is at the current 🩸 level, not 1.",
            "The <b>Children are not Minions</b>, but they are Enemies: they don't resolve Killer or Minion actions on Terror cards unless the card says the Children do it.",
            "<b>If you mix Shady Acres with another killer</b>, the Children still aren't Minions: that killer's cards that mention Minions don't affect them.",
            "If you attack the Children and there are several in the space, <b>you attack all of them</b> and split the damage; leftover damage is lost.",
            "An abduction in a space <b>with no Victims</b> isn't wasted: it counts as an attack.",
        ],
        "s_killer": "Grimlash",
        "killer": [
            "Starts at <b>4 Horror and 10 Health</b>.",
            "Initial Killer phase: Target Final Girl or Victim → Move 1 → Attack → if a Victim was killed, <b>1 Harvest Madness</b>.",
            "<b>Harvest Madness</b> gives you extra abilities, but eventually kills you.",
        ],
        "s_prep": "Special setup",
        "prep": [
            "Shuffle the <b>Ancient Curse</b> cards into a facedown deck.",
            "Put the <b>Children</b> card near the board, one Child on the <b>Altar of the Old Gods</b> and the rest on the card.",
            "Place the Children Action token <b>above</b> the Minion or Killer actions on the Finale card: they act before any other Enemies.",
        ],
        "s_reglas": "Special rules",
        "h_children": "The Children",
        "children": [
            "Their card shows their health, attack and movement. They are Enemies, not Minions.",
            "They act at the <b>start of the Killer phase</b>, before Minions and Killer, one at a time: closest to the Altar first.",
            "Each <b>Upkeep</b> a Child spawns on the Altar, unless all three are already out or there are no Victims left.",
            "They can be attacked and killed: a dead Child goes back to the card and can spawn again.",
            "Victims follow you into a space with Children, unless the Killer is there too.",
            "In the Panic phase, Victims in a space with a Child panic if at least one Victim was killed that turn.",
        ],
        "h_abd": "Abductions",
        "abd": [
            "When a Child resolves the abduction icon in a space with a Victim, roll a die.",
            "<b>1-2:</b> the Victim is sacrificed on the Altar (killed). The Child goes back to the Altar, 🩸 goes up as usual and the Victim goes on the back of the top Ancient Curse card.",
            "<b>3-6:</b> nothing happens.",
        ],
        "h_curse": "Ancient Curses",
        "curse": ["With <b>3 sacrificed Victims</b> on it, remove them and reveal the curse, which comes into play. Several can be active at once."],
        "h_field": "Field Spaces 🌾",
        "field": ["Spaces with the wheat icon are Field Spaces. Lots of cards in this box use them, for better and worse."],
        "s_inicios": "The 5 setups",
        "inicios_sub": "K = Killer start · yellow figure = Final Girl · numbers = Victims in each space.",
        "s_obj": "Items",
        "obj": [
            ("moonshine-jug", "Moonshine Jug", "Discard to recover <b>4 Health</b>."),
            ("cowboy-boots", "Cowboy Boots", "2 uses. Move up to <b>2 spaces</b>."),
            ("pilgrims-hat", "Pilgrim's Hat", "If you start your movement in a 🌾, you may move <b>1 extra space</b>."),
            ("farmers-almanac", "Farmer's Almanac", "2 uses. After drawing a <b>Terror</b> card but before resolving it, you may put it on the bottom and draw the next one."),
            ("mechanics-toolbox", "Mechanic's Toolbox", "Discard to take back <b>1 discarded Item</b>, with all its uses."),
            ("childrens-toys", "Children's Toys", "2 uses. Swap a <b>Child</b> in your space for a normal Victim."),
            ("locus-of-insanity", "Locus of Insanity", "3 uses. Once per turn, with 🎭, you may place yourself in <b>any 🌾</b>."),
            ("scythe", "Scythe", "Weapon · range 0-1 · 1 damage · 2 hands. When attacking Enemies in a 🌾, you may <b>split the damage</b> between them. Then that space becomes <b>Harvested</b> and is no longer a 🌾."),
            ("pilgrims-musket", "Pilgrim's Musket", "Weapon · range 1 · 2 damage · 2 hands · 2 uses. <b>Can't</b> be used against Enemies in a 🌾."),
            ("rusty-pitchfork", "Rusty Pitchfork", "Weapon · range 0 · 2 damage · 2 hands. If your final Horror Roll has <b>no successes</b>, discard it."),
            ("decrepit-plow", "Decrepit Plow", "Weapon · range 0 · 2 damage · 1 hand · 2 uses."),
            ("sickle", "Sickle", "Weapon · range 0 · 1 damage · 1 hand. No use limit."),
        ],
        "obj_falta": "Still to photograph: Bag of Feed, Combine Keys, Corn Cob Pipe and Cornhusk Effigy.",
        "s_ev": "Shady Acres events",
        "ev": [
            ("Umbral Evocation", "Put the <b>Harvest Shadow</b> token in the Killer's space. Each time you or a Victim enters it: 🩸."),
            ("Acres of Hatred", "For each 🌾 with at least one Victim: 🩸 (max 2). Discard."),
            ("“The Fields Are Moving…”", "Put a Field token on <b>Hayfield</b> and <b>Cow Pasture</b>: they become 🌾."),
            ("Festering Rot", "Whenever a Victim is killed in a 🌾: 🎭."),
            ("It Hungers For Us", "All Victims panic. For each Victim in the Killer's space or adjacent: 🎭 (max 3). Discard."),
            ("Harvest Cultist", "The closest Victim to you becomes the Cultist. Each Upkeep it moves 1 space toward you; if it's with you, you both move 1 space toward the Killer. Saving it has a reward."),
            ("Ralph the Mechanic", "Ralph starts in <b>Ralph's Garage</b>. While he's with you, limited-use Items you take get an extra use."),
            ("Sally McCoy", "Sally starts in the <b>McCoy Farmhouse</b>. When saved, search the Item deck for the <b>Combine Keys</b>."),
        ],
    },
}


# Cabeceras de cada guía (killer y mapa van por separado: se pueden mezclar).
CAB = {
    "es": {
        "k": {"title": "Guía de Grimlash (Final Girl): cómo juega y errores frecuentes",
              "desc": "Cómo juega Grimlash en Final Girl: su fase de Killer, Harvest Madness y los errores más comunes. Vale con cualquier mapa.",
              "eb": "Guía de killer · Temporada 4", "h1": 'Grimlash<span class="roja">guía del killer</span>',
              "dek": "Lo que hace Grimlash y los errores que más se cometen con él. Sirve con cualquier mapa: si lo juegas en Shady Acres, abre también la guía del mapa."},
        "m": {"title": "Guía de Shady Acres (Final Girl): Children, Ancient Curses, objetos y eventos",
              "desc": "Cómo se juega Shady Acres: Children, abducciones, Ancient Curses, Field Spaces, los 5 inicios, todos los objetos y eventos, y errores frecuentes. Vale con cualquier killer.",
              "eb": "Guía de mapa · Temporada 4", "h1": 'Shady Acres<span class="roja">guía del mapa</span>',
              "dek": "Las reglas especiales del mapa en corto, sus objetos y eventos, y los errores que más se cometen. Sirve con cualquier killer: si juegas contra Grimlash, abre también la suya."},
        "otra_k": "Guía de su mapa: Shady Acres", "otra_m": "Guía de su killer: Grimlash",
    },
    "en": {
        "k": {"title": "Grimlash guide (Final Girl): how he plays and common mistakes",
              "desc": "How Grimlash plays in Final Girl: his Killer phase, Harvest Madness and the most common mistakes. Works with any location.",
              "eb": "Killer guide · Season 4", "h1": 'Grimlash<span class="roja">killer guide</span>',
              "dek": "What Grimlash does and the mistakes people make most with him. Works with any location: if you play him at Shady Acres, open the location guide too."},
        "m": {"title": "Shady Acres guide (Final Girl): Children, Ancient Curses, items and events",
              "desc": "How to play Shady Acres: Children, abductions, Ancient Curses, Field Spaces, the 5 setups, every item and event, and common mistakes. Works with any killer.",
              "eb": "Location guide · Season 4", "h1": 'Shady Acres<span class="roja">location guide</span>',
              "dek": "The location's special rules in short, its items and events, and the most common mistakes. Works with any killer: if you face Grimlash, open his guide too."},
        "otra_k": "Its location guide: Shady Acres", "otra_m": "Its killer guide: Grimlash",
    },
}


def _lista(xs):
    return "<ul>" + "".join(f"<li>{x}</li>" for x in xs) + "</ul>"


def pagina(lang, cual):
    """(title, desc, cuerpo) de la guía del killer (cual="k") o del mapa ("m").
    El cuerpo va justo después de <header class="top">."""
    t, c = T[lang], CAB[lang][cual]
    pre = "" if lang == "es" else "../"
    import paginas
    css = """<style>
.gu-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:14px;margin:12px 0 6px}
.gu-grid figure{margin:0}.gu-grid img,.gu-it img{display:block;background:#ece5d5;padding:5px;border-radius:7px;box-sizing:border-box;cursor:zoom-in;box-shadow:0 10px 22px rgba(0,0,0,.6),0 0 0 1px rgba(0,0,0,.4);transform:rotate(-1.6deg);transition:transform .2s}.gu-grid img{width:100%}.gu-grid figure:nth-child(even) img,.gu-it:nth-child(even) img{transform:rotate(1.8deg)}.gu-grid img:hover,.gu-it img:hover{transform:rotate(0) scale(1.04)}.gu-zoom{position:fixed;inset:0;z-index:99;background:rgba(0,0,0,.85);display:flex;align-items:center;justify-content:center;cursor:zoom-out}.gu-zoom img{max-width:92vw;max-height:88vh;background:#ece5d5;padding:8px;border-radius:10px;box-shadow:0 20px 50px #000}
.gu-grid figcaption{font-family:var(--f-mono);font-size:11px;letter-spacing:.06em;text-transform:uppercase;margin-top:6px;color:var(--muted)}
.gu-obj{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px;margin:12px 0}
.gu-it{display:flex;gap:12px;align-items:flex-start;background:var(--surface);border:1px solid var(--line);border-radius:3px;padding:10px}
.gu-it img{width:104px;flex:none;margin:2px 4px 4px 2px}.gu-it b.n{display:block;font-size:15px;margin-bottom:4px}
.gu-it p{margin:0;font-size:14px}.gu-ev{margin:10px 0}.gu-ev dt{font-weight:700;margin-top:10px}.gu-ev dd{margin:2px 0 0}
.gu-err{border-left:3px solid var(--blood);padding:4px 0 4px 14px;margin:10px 0}
.gu-ley{font-family:var(--f-mono);font-size:12px;color:var(--muted)}
</style>"""
    arte = "img/art/grimlash.jpg" if cual == "k" else "img/loc/shady-acres.png"
    otra = (SAL_M, CAB[lang]["otra_k"]) if cual == "k" else (SAL_K, CAB[lang]["otra_m"])
    h = [paginas.arte_ficha(arte, pre),
         f'<p class="eyebrow">{c["eb"]}</p>', f'<h1>{c["h1"]}</h1>',
         f'<p class="dek">{c["dek"]}</p>',
         f'<p><a href="{otra[0]}" style="font-weight:700;color:var(--blood)">📖 {otra[1]} →</a> · '
         f'<a href="{paginas.slug(KILLER if cual == "k" else CAJA)}.html">{t["ficha"]} →</a></p>',
         f'<p class="gu-ley">{t["leyenda"]}</p></header>', css]
    if cual == "k":
        h += [f'<h2>{t["s_err"]}</h2><div class="gu-err">{_lista(t["err"][:1])}</div>',
              f'<h2>{t["s_killer"]}</h2>{_lista(t["killer"])}']
    else:
        h += [f'<h2>{t["s_err"]}</h2><div class="gu-err">{_lista(t["err"][1:])}</div>',
         f'<h2>{t["s_prep"]}</h2>{_lista(t["prep"])}',
         f'<h2>{t["s_reglas"]}</h2>',
         f'<h3>{t["h_children"]}</h3>{_lista(t["children"])}',
         f'<h3>{t["h_abd"]}</h3>{_lista(t["abd"])}',
         f'<h3>{t["h_curse"]}</h3>{_lista(t["curse"])}',
         f'<h3>{t["h_field"]}</h3>{_lista(t["field"])}',
         f'<h2>{t["s_inicios"]}</h2><p class="sub">{t["inicios_sub"]}</p><div class="gu-grid">' +
         "".join(f'<figure><img src="{pre}{DIR}{s}.jpg" alt="{INICIO_N[s]}" loading="lazy"><figcaption>{INICIO_N[s]}</figcaption></figure>'
                 for s in INICIOS) + '</div>',
         f'<h2>{t["s_obj"]}</h2><div class="gu-obj">' +
         "".join(f'<div class="gu-it"><img src="{pre}{DIR}{s}.jpg" alt="{n}" loading="lazy"><div><b class="n">{n}</b><p>{d}</p></div></div>'
                 for s, n, d in t["obj"]) + f'</div><p class="sub">{t["obj_falta"]}</p>',
         f'<h2>{t["s_ev"]}</h2><dl class="gu-ev">' + "".join(f'<dt>{n}</dt><dd>{d}</dd>' for n, d in t["ev"]) + '</dl>']
    h += [f'<p class="sub">{t["nota"]}</p>',
         # Tocar una carta la abre en grande.
         '<script>document.addEventListener("click",function(e){var z=document.querySelector(".gu-zoom");if(z){z.remove();return}'
         'var i=e.target.closest(".gu-grid img,.gu-it img");if(!i)return;var d=document.createElement("div");d.className="gu-zoom";'
         'd.innerHTML=\'<img src="\'+i.src+\'" alt="">\';document.body.appendChild(d)})</script>']
    return c["title"], c["desc"], "\n".join(h)
