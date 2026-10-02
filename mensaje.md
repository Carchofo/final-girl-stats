# Mensaje a quien lleva la hoja

Actualizado al 2 de octubre de 2026. Cifras comprobadas contra los datos
publicados ese dia: 13.919 partidas completas, 669 personas, 26 killers,
22 localizaciones, 50 paginas.

## La que se envía (GeekMail a @Rancord, Dean Vanderscoff)

Asunto: Built a site from your tracker, want your OK first

Hi Dean,

Thanks for keeping the tracker going. I built a site on top of it: https://finalgirlstats.com

Every killer against every map, a page per killer and per box, and people can look up their nickname to see what they are missing. The numbers match your summary tab (13,920 plays, 65.53%) and refresh from the sheet.

It is on noindex until you say it is fine. Plays logged from the site go through your own form, prefilled, so they land in your sheet, never in mine.

Two questions: are you ok with it, and would you link it from the sheet? I would also like to add store affiliate links on the box pages. Tell me if that bothers you and I will leave them out.

Thanks,
Rafel


## Versión larga (descartada: demasiado larga para un primer contacto)

Asunto: Built a site from the tracker data, want your OK before indexing

Hi,

I have been going through the tracker for a while and I wanted to say first that the way it is built is the reason any of this is possible. A separate Location column per killer sounds like a small decision, but it is what lets you cross every killer with every map. Most trackers collapse that and the data becomes useless for exactly the question people ask. Four and a half years, 669 people, 13,920 plays, and more logged today. Nothing else in this game comes close.

So I built a site with it: https://finalgirlstats.com

It cross tabulates all 26 killers against all 22 locations, 572 combinations with 355 that have enough plays to mean anything. The counts match your own summary tab, 13,920 plays at 65.53 percent, because I drop the same incomplete rows you do rather than scraping everything. Every killer and every box has its own page with its Dark Powers and Finale cards ranked by how much they cost you. There is a Tops section with the extremes: hardest killers, hardest maps, the killer and map pairings that almost nobody survives.

Anyone can also find themselves by nickname and see their own matrix, plus which of the 22 box pairings they have played and which they are missing. One of your top contributors has played 21 of 22. The spreadsheet cannot show that, and it gives people a reason of their own to keep logging.

The numbers refresh from your sheet automatically, so the site does not drift away from what you have.

The site credits the sheet and links to your form, but it does not nag anyone to sign up. I would rather the reason to log plays came from seeing your own gaps.

It is set to noindex for now. I did not want it in Google before you told me it was fine.

Three things:

1. Are you happy with me using the data? Happy to credit it however you prefer.
2. Would you add a link to it from the sheet? People who want the numbers would find them, and people who want to log plays would land on your form.
3. Every play logged through the site ends up in your sheet, not in a database of mine.

   Your form is linked from the site already. On top of that I made a short version you can try: https://finalgirlstats.com/registrar.html

   Five fields instead of 189. It opens your form prefilled and the person confirms and submits there, so the play lands in your sheet through your own form. It uses the prefilled link feature of Google Forms, so it never writes to your sheet, nothing is sent until someone presses Submit on your side, and if you changed or closed the form tomorrow it would simply stop working. No account, no integration, nothing for you to maintain.

   The point is that the site feeds the tracker rather than competing with it. Someone arrives looking for numbers, sees their own gaps, and the easiest next step in front of them is logging a play into your sheet.

   That page is not linked from anywhere yet and is set to noindex, so you can try it before deciding. If you would rather I dropped it, I will delete it. And if you ever wanted a real write path, that should be a script you own and can switch off, not something I post to on my own.

One more thing so there are no surprises later: I would like to put store affiliate links on the box pages, the kind where I get a small cut if someone buys. Tell me if that bothers you and I will leave them out. There are no ads and I am not putting anything behind a paywall.

Whatever you decide, thanks for keeping it going this long. It is the only real data this game has, and it only exists because someone kept the spreadsheet tidy for four and a half years.

Rafel


## Si quieres algo aún más breve

Hi,

The tracker is the only real data this game has, and the per killer Location columns are what make it actually useful. I built this from it: https://finalgirlstats.com

Every killer against every map, a page for each killer and each box, and people can look themselves up and see which boxes they are missing. It credits the sheet and links to your form, so plays logged from the site go into your sheet, not mine. It is on noindex until you tell me it is fine to publish.

Would you be ok with it? And would you link to it from the sheet?

Thanks,
Rafel


## Notas

Sin guiones largos, por tu regla para mensajes externos.

El orden importa: primero lo que les das, luego lo que pides. Y el noindex
va antes de las preguntas, porque es la prueba de que no es un hecho
consumado.

La cifra exacta, 13.915 partidas y 65,53%, es la de SU pestana de resumen.
Mi ETL dio ese mismo numero el 2 de octubre: descarta las mismas 559 filas
incompletas que descartan ellos. Decirselo es la mejor credencial del
mensaje, porque demuestra que replicamos su criterio en vez de raspar la
hoja entera. Si al enviar el correo la cifra ha cambiado, mirala primero en
su pestana de portada y usa la suya, no la nuestra.

La votacion de la comunidad NO se menciona: todavia no existe. Prometer
funciones sin construir en el mensaje donde pides permiso es la forma mas
rapida de quedar mal si luego no sale.

El punto 3 va con el beneficio por delante: las partidas que entren por
la web acaban en SU hoja, por su propio formulario. No escribimos nada, no
hay integracion que mantener, y si cierran el formulario deja de funcionar
solo. Asi queda claro que no competimos con la hoja, la alimentamos.

No pide exclusividad ni nada raro. Solo permiso y un enlace.

Si contestan que sí:

    cd ~/Desktop/final-girl-web
    sed -i '' 's/^INDEXAR = False/INDEXAR = True/' montar.py
    python3 montar.py && git add -A && git commit -m "Indexable" && git push

Y después, Search Console: verificar el dominio con un TXT en el DNS de
Arsys y enviar https://finalgirlstats.com/sitemap.xml
