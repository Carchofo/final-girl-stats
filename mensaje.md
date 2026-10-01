# Mensaje a quien lleva la hoja

## Versión corta (la que enviaría)

Asunto: Built a site from the tracker data, want your OK before indexing

Hi,

I built a site with the tracker data: https://carchofo.github.io/final-girl-stats/

It links to your form from the top of every page and from the footer, so people who look at the numbers can add their own plays. There is also a tab where anyone can find themselves by nickname and see their own matrix of killers and locations, which is something the spreadsheet cannot show.

It is set to noindex for now. I did not want it in Google before you told me it was fine.

Two things:

1. Are you happy with me using the data? Happy to credit it however you prefer.
2. Would you add a link to it from the sheet? People who want the numbers would find them, and people who want to log plays would land on your form.

Thanks for keeping the tracker going. It is the only real data this game has.

Rafel


## Si quieres algo aún más breve

Hi,

I built this from the tracker data: https://carchofo.github.io/final-girl-stats/

It links back to your form from every page. It is on noindex until you tell me it is fine to publish.

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
