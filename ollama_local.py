#!/usr/bin/env python3
"""Conexion con los modelos locales (Ollama) del PC.

Por que existe: el pipeline necesita que un modelo *redacte*, nunca que
calcule. La regla del vault es explicita: "Numeros (win rates, partidas)
solo por script, nunca por LLM". Asi que aqui va, ademas del cliente, el
guardia que lo hace cumplir: `colar()` rechaza cualquier respuesta que
contenga una cifra que no estuviera en los datos que le dimos.

Un modelo que inventa un 71,2% no se nota leyendo: se nota cuando alguien
juega confiando en el. Mejor que el borrador se caiga aqui.
"""
import json
import re
import urllib.error
import urllib.request

HOST = "http://192.168.0.25:11434"

# Rol -> modelo. Los nombres salen de `ollama list` en el PC.
CEREBRO = "granite4.2:8b"      # cambios relevantes -> JSON
REDACTOR = "qwen3.5:9b"        # borradores en castellano
REDACTOR_LIGERO = "qwen3.5:4b"  # mismo papel si el 9b va justo de VRAM
TRADUCTOR = "aya:8b"           # F2 multidioma


class ModeloFalla(Exception):
    pass


def vivo(timeout=5):
    """Ollama responde? Si no, el pipeline para antes de tocar git."""
    try:
        with urllib.request.urlopen(f"{HOST}/api/tags", timeout=timeout) as r:
            return [m["name"] for m in json.load(r)["models"]]
    except (urllib.error.URLError, OSError, ValueError):
        return []


def chat(modelo, sistema, usuario, json_mode=False, temp=0.2, timeout=900,
         pensar=False, ctx=16384, max_tokens=2048):
    """Una llamada de chat.

    `pensar=False` importa mas de lo que parece: qwen3.5 y granite razonan
    en voz alta en un campo aparte, y con un prompt largo se gastan el
    presupuesto pensando y devuelven `content` vacio. Para pedir un JSON
    corto a partir de datos ya masticados, el razonamiento no aporta nada
    y si rompe la llamada.
    """
    cuerpo = {
        "model": modelo,
        "messages": [{"role": "system", "content": sistema},
                     {"role": "user", "content": usuario}],
        "stream": False,
        "think": pensar,
        "options": {"temperature": temp,
                    "num_ctx": ctx,
                    "num_predict": max_tokens},
    }
    if json_mode:
        cuerpo["format"] = "json"
    pet = urllib.request.Request(
        f"{HOST}/api/chat",
        data=json.dumps(cuerpo).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(pet, timeout=timeout) as r:
            return json.load(r)["message"]["content"].strip()
    except urllib.error.HTTPError as e:
        raise ModeloFalla(f"{modelo}: HTTP {e.code} {e.read()[:200]!r}")
    except (urllib.error.URLError, OSError) as e:
        raise ModeloFalla(f"{modelo}: sin respuesta ({e})")


def chat_json(modelo, sistema, usuario, **kw):
    bruto = chat(modelo, sistema, usuario, json_mode=True, **kw)
    try:
        return json.loads(bruto)
    except json.JSONDecodeError:
        # Algunos modelos envuelven el JSON en texto aunque se les pida
        # format=json. Se rescata el primer objeto completo y, si no hay,
        # se cae: un JSON a medias es peor que ninguno.
        m = re.search(r"\{.*\}", bruto, re.S)
        if not m:
            raise ModeloFalla(f"{modelo}: no devolvio JSON -> {bruto[:200]!r}")
        return json.loads(m.group(0))


# --- el guardia ------------------------------------------------------------

def numeros(texto):
    """Cifras de un texto, normalizadas: '13.920' y '65,53%' -> 13920.0, 65.53.

    La coma decimal y el punto de millar del castellano conviven en la
    misma frase, asi que no vale un float() a secas.
    """
    # Separador de millar por espacio ("13 920", y sus variantes finas e
    # inquebrantables). Sin esto el guardia ve un 13 y un 920, no encuentra
    # el 920 en los datos y tira un resumen que era correcto.
    texto = re.sub(r"(?<=\d)[\s   ](?=\d{3}(?!\d))", "", texto)
    out = set()
    for t in re.findall(r"\d[\d.,]*", texto):
        t = t.rstrip(".,")
        if "," in t:                       # 65,53 / 13.920,5
            t = t.replace(".", "").replace(",", ".")
        elif re.fullmatch(r"\d{1,3}(\.\d{3})+", t):   # 13.920
            t = t.replace(".", "")
        try:
            out.add(round(float(t), 2))
        except ValueError:
            pass
    return out


def permitidas(datos):
    """Todas las cifras que aparecen en los datos de entrada, en las formas
    en que un redactor puede escribirlas: cruda, en porcentaje y redondeada."""
    ok = set()
    for n in numeros(json.dumps(datos, ensure_ascii=False)):
        ok.add(n)
        ok.add(round(n, 1))
        ok.add(round(n))
        ok.add(round(n * 100, 2))
        ok.add(round(n * 100, 1))
        ok.add(round(n * 100))
    # Ordinales y cantidades pequenas de redaccion ("las 3 primeras").
    ok |= {float(i) for i in range(0, 101)}
    return ok


def colar(texto, datos):
    """Devuelve las cifras del texto que NO salen de los datos. Vacio = limpio."""
    return sorted(numeros(texto) - permitidas(datos))
