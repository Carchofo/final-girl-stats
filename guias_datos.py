"""Contenido de las guías de juego, caja a caja (killer y mapa por separado).

Texto nuestro, a partir del reglamento, las cartas que ha fotografiado Rafel
y la wiki de Final Girl. Lo que no sale de ahí no se escribe: cuando falta
una página del reglamento, se dice. Iconos: ver "ley" de cada guía.

Cada bloque es (título, [puntos]). Objetos: (archivo o None, nombre, texto).
"""

GUIAS = [
    # ------------------------------------------------------------------ S4 F2
    {
        "caja": "A Rotten Harvest", "killer": "Grimlash", "mapa": "Shady Acres", "dir": "a-rotten-harvest",
        "arte_k": "img/art/grimlash.jpg", "arte_m": "img/loc/shady-acres.png",
        "inicios": [("reap-what-you-sow", "Reap What You Sow"), ("final-crop", "Final Crop"), ("dusk-sacrifice", "Dusk Sacrifice"),
                    ("harvest-season", "Harvest Season"), ("demands-of-the-earth", "Demands of the Earth")],
        "es": {
            "ley": "🩸 = Bloodlust · 🌾 = Field Space · 🎭 = sube el Horror",
            "err_k_t": "Errores frecuentes",
            "err_k": [
                "<b>Grimlash se mueve 1</b> en su Killer Action. Cuando una carta de Terror trae el icono de la <b>bota</b> (mover), se mueve lo que marque su movimiento en el nivel actual de 🩸, no 1.",
                "Una curación ❤️ <b>no</b> cura y baja Harvest Madness a la vez: por cada corazón, una cosa u otra.",
                "Al <b>bajar</b> de nivel de Harvest Madness <b>pierdes</b> la carta de ese nivel.",
            ],
            "bloques_k": [
                ("Harvest Madness 🎃 · preparación", [
                    "Separa las cartas de Harvest Madness por nivel y baraja cada grupo: <b>3 mazos</b>.",
                    "Pon el marcador en la casilla de salida del track de Harvest Madness (la del borde naranja), arriba del tablero del Killer."]),
                ("Harvest Madness 🎃 · cómo funciona", [
                    "Cada vez que sale el icono 🎃, el marcador avanza <b>1 casilla a la derecha</b>.",
                    "Al llegar a un <b>nivel nuevo</b>, roba <b>2 cartas</b> del mazo de ese nivel, <b>quédate 1</b> y descarta la otra. Su efecto dura mientras sigas en ese nivel o más arriba.",
                    "<b>Si pasas del nivel 3</b> (la casilla de la calavera), <b>pierdes la partida</b> al instante.",
                    "Al resolver una curación ❤️, por cada corazón eliges: <b>recuperar vida</b> como siempre <b>o bajar 1</b> la Harvest Madness. Las dos cosas a la vez, no.",
                    "Si bajas a un nivel inferior, <b>descarta la carta del nivel que dejas</b>. Si luego vuelves a ese nivel, robas otra vez 2 y te quedas 1. Si al robar no quedan bastantes, baraja los descartes de ese nivel.",
                    "Los efectos de <b>una vez por turno</b> se usan girando la carta boca abajo; en el <b>Upkeep</b> vuelve boca arriba."]),
            ],
            "err_m_t": "Errores frecuentes",
            "err_m": [
                "Los <b>Children no son Minions</b>, pero sí Enemies: no resuelven las acciones de Killer o Minion de las cartas de Terror, salvo que la carta diga que las hacen ellos.",
                "<b>Si mezclas Shady Acres con otro killer</b>, los Children siguen sin ser Minions: las cartas de ese killer que hablan de Minions no les afectan.",
                "Si atacas a los Children y hay varios en el espacio, <b>los atacas a todos</b> y repartes el daño; el que sobra se pierde.",
                "Una abducción en un espacio <b>sin víctimas</b> no se pierde: cuenta como un ataque.",
            ],
            "bloques_m": [
                ("Preparación especial", [
                    "Baraja las <b>Ancient Curses</b> y déjalas boca abajo.",
                    "Pon la carta de <b>Children</b> junto al tablero, un Child en el <b>Altar of the Old Gods</b> y el resto sobre la carta.",
                    "Coloca el token de acción de los Children <b>encima</b> de las acciones de Minion o Killer de la carta de Finale: actúan antes que el resto de enemigos."]),
                ("Los Children", [
                    "Su carta marca su vida, ataque y movimiento. Son Enemies, no Minions.",
                    "Actúan al <b>principio de la fase del Killer</b>, antes que Minions y Killer, uno a uno: del más cercano al Altar al más lejano.",
                    "En cada <b>Upkeep</b> aparece un Child en el Altar, salvo que ya estén los tres en el tablero o no queden víctimas.",
                    "Se pueden atacar y matar: el muerto vuelve a la carta y puede volver a salir.",
                    "Las víctimas te siguen a un espacio con Children, salvo que también esté el Killer.",
                    "En la fase de Panic, las víctimas en un espacio con un Child entran en pánico si ese turno ha muerto al menos una víctima."]),
                ("Abducciones", [
                    "Cuando un Child resuelve el icono de abducción en un espacio con víctima, tira un dado.",
                    "<b>1-2:</b> la víctima se sacrifica en el Altar (muere). El Child vuelve al Altar, sube el 🩸 como siempre y la víctima va al dorso de la carta de arriba de las Ancient Curses.",
                    "<b>3-6:</b> no pasa nada."]),
                ("Ancient Curses", ["Con <b>3 víctimas sacrificadas</b> encima, se quitan y se revela la maldición, que entra en juego. Puede haber varias a la vez."]),
                ("Field Spaces 🌾", ["Los espacios con la espiga son Field Spaces. Muchas cartas de la caja los usan, para bien y para mal."]),
            ],
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
            "falta": "Faltan por fotografiar: Bag of Feed, Combine Keys, Corn Cob Pipe y Cornhusk Effigy.",
            "falta_ev": "Faltan 2 de sus 10 eventos: It Lurks Between the Rows y The Ravens Are Circling.",
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
            "ley": "🩸 = Bloodlust · 🌾 = Field Space · 🎭 = raise Horror",
            "err_k_t": "Common mistakes",
            "err_k": [
                "<b>Grimlash moves 1</b> in his Killer Action. When a Terror card shows the <b>boot</b> (move) icon, he moves whatever his movement is at the current 🩸 level, not 1.",
                "A ❤️ heal does <b>not</b> heal and lower Harvest Madness at once: each heart does one or the other.",
                "When Harvest Madness <b>drops</b> a level, you <b>lose</b> that level's card.",
            ],
            "bloques_k": [
                ("Harvest Madness 🎃 · setup", [
                    "Split the Harvest Madness cards by level and shuffle each: <b>3 decks</b>.",
                    "Put the marker on the starting space of the Harvest Madness track (outlined in orange), near the top of the Killer board."]),
                ("Harvest Madness 🎃 · how it works", [
                    "Each time you see the 🎃 icon, move the marker <b>1 space right</b>.",
                    "When it reaches a <b>new level</b>, draw <b>2 cards</b> from that level's deck, <b>keep 1</b> and discard the other. Its effect lasts while you stay at that level or above.",
                    "<b>If you go beyond level 3</b> (the skull space), <b>you lose the game</b> immediately.",
                    "When resolving a ❤️ heal, for each heart you choose: <b>recover health</b> as normal <b>or lower</b> Harvest Madness by 1. Never both.",
                    "If you drop to a lower level, <b>discard the card for the level you left</b>. If you later return to it, draw 2 again and keep 1. If the deck runs short, reshuffle that level's discards.",
                    "<b>Once-per-turn</b> effects are used by flipping the card facedown; it flips back faceup in the <b>Upkeep</b>."]),
            ],
            "err_m_t": "Common mistakes",
            "err_m": [
                "The <b>Children are not Minions</b>, but they are Enemies: they don't resolve Killer or Minion actions on Terror cards unless the card says the Children do it.",
                "<b>If you mix Shady Acres with another killer</b>, the Children still aren't Minions: that killer's cards that mention Minions don't affect them.",
                "If you attack the Children and there are several in the space, <b>you attack all of them</b> and split the damage; leftover damage is lost.",
                "An abduction in a space <b>with no Victims</b> isn't wasted: it counts as an attack.",
            ],
            "bloques_m": [
                ("Special setup", [
                    "Shuffle the <b>Ancient Curse</b> cards into a facedown deck.",
                    "Put the <b>Children</b> card near the board, one Child on the <b>Altar of the Old Gods</b> and the rest on the card.",
                    "Place the Children Action token <b>above</b> the Minion or Killer actions on the Finale card: they act before any other Enemies."]),
                ("The Children", [
                    "Their card shows their health, attack and movement. They are Enemies, not Minions.",
                    "They act at the <b>start of the Killer phase</b>, before Minions and Killer, one at a time: closest to the Altar first.",
                    "Each <b>Upkeep</b> a Child spawns on the Altar, unless all three are already out or there are no Victims left.",
                    "They can be attacked and killed: a dead Child goes back to the card and can spawn again.",
                    "Victims follow you into a space with Children, unless the Killer is there too.",
                    "In the Panic phase, Victims in a space with a Child panic if at least one Victim was killed that turn."]),
                ("Abductions", [
                    "When a Child resolves the abduction icon in a space with a Victim, roll a die.",
                    "<b>1-2:</b> the Victim is sacrificed on the Altar (killed). The Child goes back to the Altar, 🩸 goes up as usual and the Victim goes on the back of the top Ancient Curse card.",
                    "<b>3-6:</b> nothing happens."]),
                ("Ancient Curses", ["With <b>3 sacrificed Victims</b> on it, remove them and reveal the curse, which comes into play. Several can be active at once."]),
                ("Field Spaces 🌾", ["Spaces with the wheat icon are Field Spaces. Lots of cards in this box use them, for better and worse."]),
            ],
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
            "falta": "Still to photograph: Bag of Feed, Combine Keys, Corn Cob Pipe and Cornhusk Effigy.",
            "falta_ev": "Missing 2 of its 10 events: It Lurks Between the Rows and The Ravens Are Circling.",
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
    },
    # ------------------------------------------------------------------ S4 F5
    {
        "caja": "The Raptor Games", "killer": "Raptors", "mapa": "Isla Lagarto", "dir": "the-raptor-games",
        "arte_k": "img/art/raptors.jpg", "arte_m": "img/loc/isla-lagarto.png",
        "inicios": [("facility-construction", "Facility Construction"), ("beach-landing", "Beach Landing"),
                    ("look-at-the-volcano", "Look at the Volcano!")],
        "es": {
            "ley": "⌛ = Tiempo · ✴ = daño · 🩸 = Bloodlust · 💔 = perder vida",
            "err_k_t": "Ojo con esto",
            "err_k": [
                "La <b>Pack</b> cuenta como el Killer a todos los efectos; los <b>Raptors sueltos</b> son Minions. Si una carta dice «Raptor(s)», no incluye a la Pack; si dice «Pack», no incluye a los sueltos.",
                "Ganas al eliminar <b>la Pack</b>, aunque queden Raptors sueltos en el tablero.",
                "Un Raptor que aparece durante la fase del Killer <b>no actúa</b> hasta la siguiente fase del Killer.",
                "Los Raptors sueltos <b>se paran</b> al entrar en un espacio contigo o con una víctima (o si empiezan a moverse ahí). Las cartas de Terror del mapa no llevan ese icono, pero la regla también vale.",
            ],
            "bloques_k": [
                ("Preparación especial", [
                    "Baraja las cartas de <b>Spawn</b> boca abajo junto a la carta de <b>Raptors</b>, y pon los meeples de Raptor encima de esa carta.",
                    "La <b>Pack</b> empieza en la casilla del Killer (K) de la carta de inicio, en lugar del meeple de Killer de la caja básica."]),
                ("La Pack", [
                    "Es un grupo grande de Raptors y cuenta como Killer a todos los efectos.",
                    "Su vida es el número de Raptors que la forman: empieza en <b>5</b> (1 Final Health y 4 de vida) y <b>no tiene tope</b>.",
                    "El ataque del tablero del Killer es lo que hace la Pack en cada ataque, sea del tamaño que sea."]),
                ("Raptors sueltos", [
                    "Son los meeples de Raptor. Cuentan como <b>Minions</b> a todos los efectos.",
                    "Tienen <b>1 de vida</b> y usan el movimiento del tablero del Killer.",
                    "Atacan poco, pero cuando lo hacen, <b>cada uno</b> hace 1 ✴."]),
                ("Unirse a la Pack", [
                    "Con el icono de la Pack, los Raptors van hacia ella por el <b>camino más corto</b>. Si hay varios, eligen el que les deje más cerca de la Pack antes de pararse.",
                    "Si un Raptor acaba en el espacio de la Pack, <b>se une</b> al momento: quita el meeple y suma 1 de vida a la Pack por cada uno.",
                    "Los meeples que salen del tablero vuelven a la carta de Raptors para futuras apariciones."]),
                ("Aparición de Raptors", [
                    "Con el icono de spawn, roba una carta de <b>Spawn</b> y saca ese número de Raptors. El espacio se decide tirando un dado en la tabla de la carta de Raptors; si hay varios válidos, eliges tú.",
                    "Nunca aparecen en espacios que ya no son accesibles.",
                    "Si no quedan meeples suficientes, el Raptor más cercano a la Pack se une a ella y usas su meeple; repite hasta completar la carta.",
                    "Si no quedan cartas de Spawn, baraja el descarte y roba.",
                    "El último efecto del track de 🩸 también saca un Raptor, como una carta de Spawn de 1."]),
            ],
            "err_m_t": "Ojo con esto",
            "err_m": [
                "Los espacios con <b>lava</b> dejan de ser accesibles para todos, también para los Raptors y el T-Rex.",
                "Si <b>Game Makers</b> sale al preparar la partida, descártala y roba otra.",
            ],
            "bloques_m": [
                ("El volcán", [
                    "La <b>primera vez</b> que resuelves el icono del volcán, entra en erupción: todos los que estén en el <b>Volcano</b> reciben 💔, los que queden en el espacio entran en pánico, y pones ahí la ficha de lava del volcán: deja de ser accesible.",
                    "Las <b>siguientes veces</b>, la lava se extiende a un espacio adyacente: roba una carta de <b>Lava</b> para saber cuál y sigue sus instrucciones.",
                    "Con las <b>4 fichas de lava</b> en el tablero, ignora el icono del volcán."]),
                ("Espacios especiales", [
                    "Los <b>3 espacios de las esquinas</b> con el icono de playa son <b>Beach</b>.",
                    "Los <b>2 espacios de los bordes</b> con el icono de acantilado son <b>Cliff</b>.",
                    "Varias cartas del mapa se refieren a ellos."]),
                ("T-Rex y valla eléctrica", [
                    "El mapa trae un <b>T-Rex</b> (con su carta y su token de acción) y una <b>valla eléctrica</b> con su dado y 3 marcadores. Nos falta fotografiar la página del reglamento que los explica: la añadiremos cuando la tengamos."]),
            ],
            "obj": [
                ("shotgun", "Shotgun", "Arma · alcance 0-1 · 3 ✴ · 2 manos · 2 usos. Reparte el daño: la mitad (redondeando arriba) a un Enemy de tu espacio y la otra mitad (abajo) a uno adyacente. Si en un espacio no hay Enemy, ese daño se pierde."),
                ("throwing-axe", "Throwing Axe", "Arma · alcance 0-1 · 1 ✴ · 1 mano. Si la usas a alcance 1, se descarta."),
                ("safari-knife", "Safari Knife", "Arma · alcance 0 · 1 ✴ · 1 mano."),
                ("flaming-torch", "Flaming Torch", "Arma · alcance 0 · 1 ✴ · 1 mano · 3 usos. Úsala para atacar o para ignorar 1 ✴ de un ataque de un Enemy."),
                ("tranquilizer-gun", "Tranquilizer Gun", "1 mano · 2 usos. Cuando quieras, haz 1 ✴ a un Enemy en un espacio adyacente; si se estaba moviendo, se para."),
                ("wildlife-net", "Wildlife Net", "2 manos. Descártala cuando te ataque un Enemy para ignorar ese ataque y todos los de ese mismo Enemy durante el resto del turno."),
                ("whistle", "Whistle", "Una vez por fase de Acción, gasta 1 ⌛: todas las víctimas adyacentes vienen a tu espacio, y luego todos los Enemies van a por ti y se mueven. Mientras la tengas, te sigue 1 víctima más."),
                ("bait", "Bait", "Descártala para poner la <b>cabra</b> en tu espacio o en uno adyacente. Los Enemies y el T-Rex van siempre a por la cabra hasta que muere. Tiene 1 ❤️ y no se mueve."),
                ("safari-rover-keys", "Safari Rover Keys", "4 usos. Pon el token del <b>Rover</b> en tu espacio; se mueve contigo. Con el Rover te pueden seguir hasta 3 víctimas y puedes gastar un uso para moverte 1 espacio. Sin usos, se acaba la gasolina: descarta la carta y el Rover."),
                ("bush-plane", "Bush Plane", "Cuando salvas al menos una víctima en el <b>Airstrip</b>, puedes descartarla para salvar al momento a otra víctima de cualquier espacio."),
                ("enhanced-goggles", "Enhanced Goggles", "Puedes ignorar todos los iconos 💔 de las cartas de acción <b>Walk</b> y <b>Sprint</b>."),
                ("generator-codes", "Generator Codes", "Descártala para poner o quitar cualquiera de los marcadores de la <b>valla eléctrica</b>."),
                ("private-stash", "Private Stash", "Al cogerla, descártala y elige: lo que marcan sus iconos, o coger la carta de arriba de cualquier mazo de objetos."),
            ],
            "falta": "Faltan por fotografiar: Safari Rifle, Cattle Prod y First Aid Kit.",
            "ev": [
                ("Supply Drop", "Pon los 3 tokens de suministro en los espacios Beach y Cliff más lejanos a ti (uno por espacio). En un espacio con token puedes gastar 2 ⌛ para quitarlo y coger un objeto al azar de los apartados al preparar. Se descarta cuando no quedan tokens."),
                ("Fierce Competitors", "Por cada víctima que salves: ⌛."),
                ("Terrified Child", "La víctima más lejana a ti es el Terrified Child. Mientras queden otras víctimas, no te sigue y no se puede salvar, elegir como objetivo ni matar. Si la salvas: desbloqueas tu Ultimate Ability o bajas el Horror a 0. Si muere: el 🩸 sube al máximo."),
                ("Game Makers", "Si sale al preparar, descártala y roba otra. Si no, resuelve sus tres iconos (volcán, un evento nuevo y la garra naranja) y descártala."),
                ("The Alpha", "La víctima más cercana a ti es el Alpha. Si muere: 🩸. Cuando alguien que esté con el Alpha o a su lado vaya a ser atacado (no los Enemies), el Alpha se pone en su espacio y tiras un dado: <b>1-2</b> muere el Alpha · <b>3-4</b> el ataque sigue normal · <b>5-6</b> se cancela."),
                ("The Power Is Down", "Quita todos los marcadores de la valla eléctrica y resuelve una vez la garra naranja. No tires el dado de la valla en el próximo Upkeep. Se descarta al final de ese Upkeep."),
                ("Power Surge", "Pon todos los marcadores de la valla eléctrica. No tires su dado en el próximo Upkeep. Se descarta al final de ese Upkeep."),
                ("Tropical Storm", "En la próxima fase de Acción, tira un dado menos (mínimo 1) en todas las tiradas de Horror. Si no haces ninguna tirada de Horror: 3 ⌛. Se descarta al final de esa fase."),
                ("Herbal Remedies", "Coge una víctima muerta que elijas y ponla en tu espacio. Se descarta."),
                ("The Hunter", "Pon al Hunter en el espacio más lejano a ti. En cada Upkeep, el Hunter entra en pánico y hace ✴ a todos los de su espacio."),
            ],
        },
        "en": {
            "ley": "⌛ = Time · ✴ = damage · 🩸 = Bloodlust · 💔 = lose health",
            "err_k_t": "Watch out",
            "err_k": [
                "The <b>Pack</b> counts as the Killer for all purposes; <b>individual Raptors</b> are Minions. A card that says \"Raptor(s)\" doesn't include the Pack; one that says \"Pack\" doesn't include individual Raptors.",
                "You win when <b>the Pack</b> is eliminated, even if individual Raptors are still on the board.",
                "A Raptor that spawns during the Killer phase <b>doesn't activate</b> until the next Killer phase.",
                "Individual Raptors <b>stop</b> when they enter (or start moving in) a space with you or a Victim. Location Terror cards don't show that icon, but the rule still applies.",
            ],
            "bloques_k": [
                ("Special setup", [
                    "Shuffle the <b>Spawn</b> cards facedown next to the <b>Raptors</b> card, and put the Raptor meeples on that card.",
                    "The <b>Pack</b> starts on the Killer space (K) of the Setup card, instead of the core box Killer meeple."]),
                ("The Pack", [
                    "A large group of Raptors that counts as the Killer for all purposes.",
                    "Its health is the number of Raptors in it: it starts at <b>5</b> (1 Final Health and 4 Health) with <b>no upper limit</b>.",
                    "The Attack Value on the Killer board is what the Pack deals per attack, whatever its size."]),
                ("Individual Raptors", [
                    "The Raptor meeples. They are <b>Minions</b> for all purposes.",
                    "They have <b>1 health</b> and use the Movement Value on the Killer board.",
                    "They don't attack often, but when they do, <b>each one</b> deals 1 ✴."]),
                ("Joining the Pack", [
                    "On the Pack icon, Raptors head for the Pack by the <b>shortest path</b>. If several are equal, they take the one that gets them closest to the Pack before stopping.",
                    "A Raptor in the Pack's space <b>joins it</b> immediately: remove the meeple and add 1 health to the Pack for each one.",
                    "Meeples removed from the board go back to the Raptors card for future spawns."]),
                ("Spawning Raptors", [
                    "On the spawn icon, draw a <b>Spawn</b> card and spawn that many Raptors. The space comes from a die roll on the Raptors card's table; if several are legal, you choose.",
                    "They never spawn in spaces that are no longer accessible.",
                    "If there aren't enough meeples, the Raptor closest to the Pack joins it and you use its meeple; repeat until the card is resolved.",
                    "If the Spawn deck runs out, shuffle the discards and draw.",
                    "The final effect on the 🩸 track also spawns a Raptor, like a Spawn card of 1."]),
            ],
            "err_m_t": "Watch out",
            "err_m": [
                "<b>Lava</b> spaces are no longer accessible to anyone, Raptors and T-Rex included.",
                "If <b>Game Makers</b> is drawn during setup, discard it and draw another.",
            ],
            "bloques_m": [
                ("The volcano", [
                    "The <b>first time</b> you resolve the volcano icon, it erupts: everyone at the <b>Volcano</b> takes 💔, anyone left in the space panics, and you place the Volcano Lava token there: it's no longer accessible.",
                    "<b>After that</b>, the lava spreads to an adjacent space: draw a <b>Lava</b> card to see which one and follow it.",
                    "Once all <b>4 Lava tokens</b> are on the board, ignore the volcano icon."]),
                ("Special spaces", [
                    "The <b>3 corner spaces</b> with the beach icon are <b>Beach</b> spaces.",
                    "The <b>2 edge spaces</b> with the cliff icon are <b>Cliff</b> spaces.",
                    "Several location cards refer to them."]),
                ("T-Rex and electric fence", [
                    "The location comes with a <b>T-Rex</b> (card and action token) and an <b>electric fence</b> with its die and 3 markers. We still need to photograph the rulebook page that covers them: we'll add it when we have it."]),
            ],
            "obj": [
                ("shotgun", "Shotgun", "Weapon · range 0-1 · 3 ✴ · 2 hands · 2 uses. Split the damage: half (rounded up) to an Enemy in your space and half (rounded down) to one in an adjacent space. Damage to a space with no Enemy is lost."),
                ("throwing-axe", "Throwing Axe", "Weapon · range 0-1 · 1 ✴ · 1 hand. If used at range 1, discard it."),
                ("safari-knife", "Safari Knife", "Weapon · range 0 · 1 ✴ · 1 hand."),
                ("flaming-torch", "Flaming Torch", "Weapon · range 0 · 1 ✴ · 1 hand · 3 uses. Use it to attack or to ignore 1 ✴ from an Enemy attack."),
                ("tranquilizer-gun", "Tranquilizer Gun", "1 hand · 2 uses. Any time, deal 1 ✴ to an Enemy in an adjacent space; if it was moving, its movement ends."),
                ("wildlife-net", "Wildlife Net", "2 hands. Discard it when attacked by an Enemy to ignore that attack and every attack from that Enemy for the rest of the turn."),
                ("whistle", "Whistle", "Once per Action phase, spend 1 ⌛: all adjacent Victims move to your space, then all Enemies target you and move. While you have it, one extra Victim follows you."),
                ("bait", "Bait", "Discard to place the <b>Goat</b> in your space or an adjacent one. Enemies and the T-Rex always target the Goat until it's killed. It has 1 ❤️ and doesn't move."),
                ("safari-rover-keys", "Safari Rover Keys", "4 uses. Place the <b>Rover</b> token in your space; it moves with you. With the Rover, up to 3 Victims can follow you and you can spend a use to move 1 space. When the uses run out, it's out of gas: discard the card and the Rover."),
                ("bush-plane", "Bush Plane", "When you save at least one Victim at the <b>Airstrip</b>, you may discard it to immediately save one more Victim from any space."),
                ("enhanced-goggles", "Enhanced Goggles", "You may ignore all 💔 icons on <b>Walk</b> and <b>Sprint</b> Action cards."),
                ("generator-codes", "Generator Codes", "Discard to add or remove any of the <b>electric fence</b> markers."),
                ("private-stash", "Private Stash", "When you take it, discard it and choose: what its icons show, or the top card of any Item deck."),
            ],
            "falta": "Still to photograph: Safari Rifle, Cattle Prod and First Aid Kit.",
            "ev": [
                ("Supply Drop", "Put the 3 Supply tokens on the Beach and Cliff spaces furthest from you (one each). On a space with a token you can spend 2 ⌛ to remove it and take a random Item set aside during setup. Discard when no tokens are left."),
                ("Fierce Competitors", "For each Victim you save: ⌛."),
                ("Terrified Child", "The Victim furthest from you is the Terrified Child. While other Victims remain, it won't follow you and can't be saved, targeted or killed. Saved: unlock your Ultimate Ability or reduce Horror to 0. Killed: 🩸 goes to the maximum."),
                ("Game Makers", "If drawn during setup, discard and draw another. Otherwise resolve its three icons (volcano, a new Event and the orange claw) and discard it."),
                ("The Alpha", "The Victim closest to you is the Alpha. If killed: 🩸. When anyone with or next to the Alpha would be attacked (not Enemies), the Alpha moves to their space and you roll: <b>1-2</b> the Alpha dies · <b>3-4</b> the attack goes on · <b>5-6</b> it's cancelled."),
                ("The Power Is Down", "Remove all electric fence markers and resolve the orange claw once. Don't roll the fence die in the next Upkeep. Discard at the end of that Upkeep."),
                ("Power Surge", "Place all electric fence markers. Don't roll its die in the next Upkeep. Discard at the end of that Upkeep."),
                ("Tropical Storm", "In the next Action phase, roll one die fewer (minimum 1) on every Horror Roll. If you make no Horror Roll: 3 ⌛. Discard at the end of that phase."),
                ("Herbal Remedies", "Take a killed Victim of your choice and place it in your space. Discard."),
                ("The Hunter", "Place the Hunter in the space furthest from you. Each Upkeep, the Hunter panics and deals ✴ to everyone in his space."),
            ],
        },
    },
    # ------------------------------------------------------------------ S4 F1
    {
        "caja": "Bad Times at Buddyland", "killer": "Billy", "mapa": "Buddyland", "dir": "bad-times-at-buddyland",
        "arte_k": "img/art/billy.jpg", "arte_m": "img/loc/buddyland.png",
        "inicios": [("playin-hooky", "Playin' Hooky"), ("hide-and-seek", "Hide and Seek")],
        "es": {
            "ley": "⌛ = Tiempo · ✴ = daño · 🩸 = Bloodlust · 🎭 = sube el Horror · ⊘🎭 = la máscara tachada de la carta",
            "err_k_t": "Ojo con esto",
            "err_k": [
                "Billy tiene <b>minions</b> (los Buddies) que van apareciendo y <b>actúan antes que él</b>.",
                "Hasta que sale el Finale, Billy empieza su fase recuperando <b>1 de vida si hay alguna fuente de energía encendida</b>. Apagarlas es lo que le impide curarse.",
            ],
            "bloques_k": [
                ("Cómo juega (según la wiki)", [
                    "Buddies: Target Victim/Final Girl → Strike once.",
                    "Billy, antes del Finale y después de los Buddies: +1 de vida si hay una fuente de energía activa → Target Victim/Final Girl → Strike once.",
                    "Su track de Horror mezcla efectos A y B: aparecer un Buddy (o uno en tu espacio), descartar la siguiente carta de Terror o subir el Horror.",
                    "Nos falta fotografiar la página de Billy del reglamento para completarlo."]),
            ],
            "err_m_t": "Ojo con esto",
            "err_m": [
                "Las <b>fuentes de energía</b> se colocan por el tablero <b>antes</b> de sacar la carta de inicio.",
            ],
            "bloques_m": [
                ("El mapa (según la wiki)", [
                    "Los espacios de <b>Arcade</b> del centro del tablero salen en varias cartas.",
                    "Las <b>fuentes de energía</b> (Power Source) se reparten por el tablero antes de sacar la carta de inicio. Te conviene ir apagándolas: con alguna encendida, Billy se cura.",
                    "Nos falta fotografiar la página del reglamento de Buddyland para completarlo."]),
            ],
            "obj": [
                ("janitors-mop", "Janitor's Mop", "Arma · alcance 0 · 1 ✴ · 2 manos. Una vez por fase de Acción, si estás solo en un espacio, puedes gastar 2 ⌛ por ⊘🎭."),
                ("security-bot", "Security Bot", "Pon el token del <b>Bot</b> en tu espacio. Cuando ganes movimiento, puedes usarlo para mover el Bot. Al Bot le siguen hasta 2 víctimas, y las víctimas en una salida con el Bot se pueden salvar."),
                ("security-badge", "Security Badge", "Al cogerla, coge también la carta de acción <b>Planning</b>. Las víctimas de tu espacio nunca entran en pánico."),
                ("arcade-token", "Arcade Token", "Descártala en un espacio de <b>Arcade</b> para gastar 3 ⌛ por 3 ⊘🎭."),
            ],
            "falta": "Faltan por fotografiar 12 de sus 16 objetos y 3 de sus 5 inicios (Buddy Day, Birthday Bash y Pizza Party).",
            "ev": [
                ("Birthday Girl", "La Birthday Girl empieza en la <b>Party Room</b>. Si está sola en la fase de Panic, entra en pánico. Si la salvas: 4 ⌛. Si muere: 🩸."),
                ("Nick the Janitor", "Nick empieza en el <b>Janitor's Closet</b> y te puede seguir incluso al espacio del Killer. Cuando entra en un espacio con un Enemy, le hace 2 ✴; luego sale del tablero y vuelve al Closet en el siguiente Upkeep. Si muere: 2 🩸."),
                ("Sing-A-Long", "En cada Upkeep: 🎭. Se descarta cuando el nivel de Horror llega a la zona roja."),
                ("Pizza Delivery", "La víctima más cercana a la <b>Entrance</b> es el Pizza Guy. Mientras esté en tu espacio, puedes tirar 2 dados más al resolver una carta de acción <b>Search</b>. Si muere, todas las víctimas de su espacio y de los adyacentes entran en pánico."),
            ],
            "falta_ev": "Faltan 6 de sus 10 eventos: Broken Machine, Buddy Up, Hidden Prizes, Party Time, Playtime Shenanigans y Tragic Collapse.",
        },
        "en": {
            "ley": "⌛ = Time · ✴ = damage · 🩸 = Bloodlust · 🎭 = raise Horror · ⊘🎭 = the card's crossed-out mask",
            "err_k_t": "Watch out",
            "err_k": [
                "Billy has <b>minions</b> (the Buddies) that spawn during the game and <b>act before him</b>.",
                "Until the Finale, Billy starts his phase recovering <b>1 health if any power source is active</b>. Turning them off is what stops him healing.",
            ],
            "bloques_k": [
                ("How he plays (from the wiki)", [
                    "Buddies: Target Victim/Final Girl → Strike once.",
                    "Billy, before the Finale and after the Buddies: +1 health if a power source is active → Target Victim/Final Girl → Strike once.",
                    "His Horror track mixes A and B effects: spawn a Buddy (or one in your space), discard the next Terror card or raise Horror.",
                    "We still need to photograph Billy's rulebook page to complete this."]),
            ],
            "err_m_t": "Watch out",
            "err_m": [
                "The <b>power sources</b> go around the board <b>before</b> you draw the Setup card.",
            ],
            "bloques_m": [
                ("The location (from the wiki)", [
                    "The <b>Arcade</b> spaces in the middle of the board feature on several cards.",
                    "<b>Power Source</b> tokens are placed around the board before the Setup card. Turn them off as you go: while any is on, Billy heals.",
                    "We still need to photograph the Buddyland rulebook page to complete this."]),
            ],
            "obj": [
                ("janitors-mop", "Janitor's Mop", "Weapon · range 0 · 1 ✴ · 2 hands. Once per Action phase, while alone in a space, you may spend 2 ⌛ for ⊘🎭."),
                ("security-bot", "Security Bot", "Place the <b>Bot</b> token in your space. When you gain movement, you may use it to move the Bot instead. Up to 2 Victims may follow the Bot, and Victims at an exit with the Bot can be saved."),
                ("security-badge", "Security Badge", "When you take it, also take the <b>Planning</b> Action card. Victims in your space never panic."),
                ("arcade-token", "Arcade Token", "Discard while in an <b>Arcade</b> space to spend 3 ⌛ for 3 ⊘🎭."),
            ],
            "falta": "Still to photograph: 12 of its 16 Items and 3 of its 5 setups (Buddy Day, Birthday Bash and Pizza Party).",
            "ev": [
                ("Birthday Girl", "The Birthday Girl starts in the <b>Party Room</b>. If she's alone during the Panic phase, she panics. Saved: 4 ⌛. Killed: 🩸."),
                ("Nick the Janitor", "Nick starts in the <b>Janitor's Closet</b> and can follow you even into the Killer's space. When he enters a space with an Enemy, he deals 2 ✴ to it; then he leaves the board and returns to the Closet next Upkeep. Killed: 2 🩸."),
                ("Sing-A-Long", "Each Upkeep: 🎭. Discard when the Horror level reaches the red area."),
                ("Pizza Delivery", "The Victim closest to the <b>Entrance</b> is the Pizza Guy. While he's in your space, you may roll 2 extra dice when resolving a <b>Search</b> Action card. If he's killed, all Victims in his space and adjacent spaces panic."),
            ],
            "falta_ev": "Missing 6 of its 10 events: Broken Machine, Buddy Up, Hidden Prizes, Party Time, Playtime Shenanigans and Tragic Collapse.",
        },
    },
]
