# Final Girl Stats

Sitio estático. Dos páginas: estadísticas de 13.951 partidas y la chuleta de salidas.

## Montar

```bash
python3 montar.py
```

Lee `cuerpo.html` y `salidas-cuerpo.html` (exportados del artifact de claude.ai)
y los envuelve en documentos completos con la cabecera que necesita un buscador,
más `sitemap.xml` y `robots.txt`.

**Antes de publicar, cambia `DOMINIO` en `montar.py`.** Ahora apunta a un
ejemplo, y las URL canónicas y el sitemap salen de ahí.

## Subir a GitHub Pages

```bash
git init && git add -A && git commit -m "Primera versión"
gh repo create final-girl-stats --public --source=. --push
gh api repos/:owner/final-girl-stats/pages -X POST \
  -f "source[branch]=main" -f "source[path]=/"
```

Queda en `https://<usuario>.github.io/final-girl-stats/`. Con dominio propio,
añade un fichero `CNAME` con el dominio y apunta el DNS.

## Que lo indexe Google

1. Alta en [Search Console](https://search.google.com/search-console)
2. Verificar el dominio
3. Enviar `sitemap.xml`
4. "Inspección de URL" → "Solicitar indexación" para la portada

Tarda de días a semanas.

## Qué falta para posicionar de verdad

Lo de arriba es higiene: sin ello no te encuentran, con ello solo tampoco.

Hoy todo vive en **dos URL**, y una URL solo posiciona para una cosa. Las
búsquedas reales son específicas: "ratchet lady win rate", "final girl best
killer", "hans the butcher strategy".

Hay datos para **70 páginas** (26 killers, 22 cajas, 22 localizaciones), cada
una respondiendo exactamente a una pregunta, con cifras que no están en
ningún otro sitio en forma legible. Generarlas desde `D` con una plantilla es
lo que mueve la aguja.

Y la decisión de fondo: **la comunidad busca en inglés**. Reddit, BGG y Discord
son angloparlantes. El contenido en castellano compite por un volumen mucho
menor.

## Ficheros

| | |
|---|---|
| `montar.py` | genera el sitio |
| `cuerpo.html`, `salidas-cuerpo.html` | fuente, exportada del artifact |
| `index.html`, `salidas.html` | generados, no editar a mano |
| `img/` | 22 portadas |
| `assets/` | GIF de la TV y su script |

Los datos salen de la hoja comunitaria de seguimiento. **Pedir permiso antes
de publicar** y enlazar su formulario.
