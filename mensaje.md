# Mensaje a quien lleva la hoja

## Versión corta (la que enviaría)

Asunto: Built a site from the tracker data, want your OK before indexing

Hi,

I have been going through the tracker for a while and I wanted to say first that the way it is built is the reason any of this is possible. A separate Location column per killer sounds like a small decision, but it is what lets you cross every killer with every map. Most trackers collapse that and the data becomes useless for exactly the question people ask. Four and a half years, 669 people, 14,473 plays, and one logged today. Nothing else in this game comes close.

So I built a site with it: https://carchofo.github.io/final-girl-stats/

Anyone can find themselves by nickname and see their own matrix of killers and locations, plus which of the 22 box pairings they have played and which they are missing. One of your top contributors has played 21 of 22. The spreadsheet cannot show that, and it gives people a reason of their own to keep logging.

The site credits the sheet and links to your form, but it does not nag anyone to sign up. I would rather the reason to log plays came from seeing your own gaps.

It is set to noindex for now. I did not want it in Google before you told me it was fine.

Three things:

1. Are you happy with me using the data? Happy to credit it however you prefer.
2. Would you add a link to it from the sheet? People who want the numbers would find them, and people who want to log plays would land on your form.
3. I made a short logging form you can try: https://carchofo.github.io/final-girl-stats/registrar.html

   Five fields instead of 189. It opens your form prefilled and you confirm there, so the play goes into your sheet through your own form. It uses the prefilled link feature of Google Forms, so it never writes to your sheet and nothing is sent until someone presses Submit on your side.

   That page is not linked from anywhere and is set to noindex. It exists so you can try it. If you would rather I dropped it, I will delete it. And if you ever wanted a real write path, that should be a script you own and can switch off, not something I post to on my own.

One more thing so there are no surprises later: I would like to put store affiliate links on the box pages, the kind where I get a small cut if someone buys. Tell me if that bothers you and I will leave them out. There are no ads and I am not putting anything behind a paywall.

Whatever you decide, thanks for keeping it going this long. It is the only real data this game has, and it only exists because someone kept the spreadsheet tidy for four and a half years.

Rafel


## Si quieres algo aún más breve

Hi,

The tracker is the only real data this game has, and the per killer Location columns are what make it actually useful. I built this from it: https://carchofo.github.io/final-girl-stats/

People can look themselves up and see which boxes they are missing. It credits the sheet and links to your form. It is on noindex until you tell me it is fine to publish.

Would you be ok with it? And would you link to it from the sheet?

Thanks,
Rafel


## Notas

Sin guiones largos, por tu regla para mensajes externos.

El orden importa: primero lo que les das, luego lo que pides. Y el noindex
va antes de las preguntas, porque es la prueba de que no es un hecho
consumado.

No pide exclusividad ni nada raro. Solo permiso y un enlace.

Si contestan que sí:

    cd ~/Desktop/final-girl-web
    sed -i '' 's/^INDEXAR = False/INDEXAR = True/' montar.py
    python3 montar.py && git add -A && git commit -m "Indexable" && git push
