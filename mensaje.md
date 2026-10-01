# Mensaje a quien lleva la hoja

## Versión corta (la que enviaría)

Asunto: Built a site from the tracker data, want your OK before indexing

Hi,

I built a site with the tracker data: https://carchofo.github.io/final-girl-stats/

Anyone can find themselves by nickname and see their own matrix of killers and locations, plus which of the 22 box pairings they have played and which they are missing. One of your top contributors has played 21 of 22. The spreadsheet cannot show that, and it gives people a reason of their own to keep logging.

The site credits the sheet and links to your form, but it does not nag anyone to sign up. I would rather the reason to log plays came from seeing your own gaps.

It is set to noindex for now. I did not want it in Google before you told me it was fine.

Two things:

1. Are you happy with me using the data? Happy to credit it however you prefer.
2. Would you add a link to it from the sheet? People who want the numbers would find them, and people who want to log plays would land on your form.

Thanks for keeping the tracker going. It is the only real data this game has.

Rafel


## Si quieres algo aún más breve

Hi,

I built this from the tracker data: https://carchofo.github.io/final-girl-stats/

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
