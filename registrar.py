"""registrar.html en otros idiomas: la misma plantilla que la española
(montar.plantilla, ya con los datos dentro), con los textos traducidos.

Solo cambia lo que ve la persona. Los valores que van al formulario
(Final Girl, The Killer, Neither...) son los del Google Form y no se tocan.
"""

TX = {
    "en": {
        "title": "Log a Final Girl game",
        "desc": "Shortcut to log a game in the community sheet: three steps with dropdowns instead of 190 fields.",
        "pares": [
            ("Hoja comunitaria · 30 segundos", "Community sheet · 30 seconds"),
            ('Registrar<span class="roja">una partida</span>', 'Log<span class="roja">a game</span>'),
            ("Tres pasos con desplegables en vez de recorrer ciento noventa campos. Al terminar se abre el formulario de la hoja comunitaria con todo puesto, y solo tienes que confirmar. La partida entra en su hoja, no en ninguna otra.",
             "Three steps with dropdowns instead of scrolling through 190 fields. At the end the community sheet's form opens with everything filled in, and you just confirm. The game goes into their sheet, nowhere else."),
            ("> La partida<", "> The game<"),
            (">Localización<", ">Location<"),
            (">Elige…<", ">Choose…<"),
            ("> El resultado<", "> The result<"),
            ("¿Quién ganó?", "Who won?"),
            ("> Gané yo<", "> I won<"),
            ("> Ganó el killer<", "> The killer won<"),
            ("¿Alguien usó su Final Health?", "Did anyone use their Final Health?"),
            ("> Nadie<", "> Nobody<"),
            ("> Yo<", "> Me<"),
            ("> El killer<", "> The killer<"),
            ("> Los dos<", "> Both<"),
            (">Dificultad<", ">Difficulty<"),
            ("> Detalles <em>opcional, pero es lo que más afina las estadísticas</em>",
             "> Details <em>optional, but it's what sharpens the stats the most</em>"),
            ("Tu nombre en la hoja", "Your name in the sheet"),
            ("El mismo que uses siempre", "The same one you always use"),
            ("Se guarda en este navegador, con tu último killer y Final Girl, para la próxima vez.",
             "Saved in this browser, with your last killer and Final Girl, for next time."),
            ("Abrir el formulario con esto puesto", "Open the form with this filled in"),
            ("<b>Qué pasa al pulsar</b> Se abre el formulario de la hoja comunitaria en otra pestaña, con estos campos ya rellenados. Pasa las páginas con Next y dale a Submit al final: nada se envía hasta entonces. Esta página no escribe en su hoja ni guarda nada fuera de tu navegador.",
             "<b>What happens when you click</b> The community sheet's form opens in a new tab with these fields filled in. Go through the pages with Next and hit Submit at the end: nothing is sent until then. This page doesn't write to their sheet or store anything outside your browser."),
            ("'Cómo ganaste'", "'How you won'"),
            ("'Misión'", "'Mission'"),
            ("'Forma en que lo derrotaste'", "'Form defeated'"),
            ("'Cuántos organismos'", "'How many Organisms'"),
            ("'Cómo moriste'", "'How you died'"),
            ("'Orden de muertes'", "'Death order'"),
            ("'De su caja'", "'From its box'"),
            ("'Todas'", "'All'"),
            ("'Elige…'", "'Choose…'"),
            ("'No lo sé / lo dejo'", "'Don\\'t know / skip'"),
            ("'La de su caja es '", "'Its box location is '"),
            ("'</b> contra <b>'", "'</b> vs <b>'"),
            ("' en ' + d.loc", "' at ' + d.loc"),
            ("'Victoria' : 'Derrota'", "'Win' : 'Loss'"),
            ("', en Extreme Horror'", "', on Extreme Horror'"),
            ("' Con ' + n + ' detalle' + (n > 1 ? 's' : '')", "' With ' + n + ' detail' + (n > 1 ? 's' : '')"),
        ],
    },
}


def pagina(lang, M):
    t = TX[lang]
    c = M.plantilla
    # El envoltorio (wrap, header, pie) lo pone idiomas.generar.
    c = c.replace('<div class="wrap">\n\n<header class="top">', "", 1)
    a, b = c.split("<footer>", 1)
    c = a + b.split("</div>", 1)[1]
    for es, otro in t["pares"]:
        c = c.replace(es, otro)
    return t["title"], t["desc"], c
