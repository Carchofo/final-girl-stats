import json, os, re, sys, unicodedata
sys.path.insert(0, os.path.dirname(__file__))
from planes import P
D = json.load(open('/private/tmp/claude-501/D.json'))
K = json.load(open('/Users/mac/Desktop/final-girl-web/killers_desc.json'))
WEB = '/Users/mac/Desktop/final-girl-web'
MIOS = ['Hans', 'Evomorph', 'The Intruders', 'Big Bad Wolf', 'Ratchet Lady']

def slug(s):
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')

def peor(arr):
    a = [x for x in arr if x[0] != 'Unrevealed' and x[2] >= 20]
    return min(a, key=lambda x: x[1]) if a else None

SET = {}
for f in D['films']:
    a = [x for x in f['setups'] if x[2] >= 20]
    if len(a) < 2: continue
    b, w = max(a, key=lambda x: x[1]), min(a, key=lambda x: x[1])
    # Solo si la diferencia probablemente no es azar (test de dos proporciones).
    q = (b[1]*b[2] + w[1]*w[2]) / (b[2] + w[2])
    z = (b[1] - w[1]) / (q*(1-q)*(1/b[2] + 1/w[2])) ** .5
    if z >= 1.96: SET[f['killer']] = (b, w, round(z, 2))
def evitar(v):
    # Dark Power o Finale muy descompensado frente al resto de los de su killer:
    # z >= 3 (casi imposible que sea azar) y al menos 15 puntos de diferencia.
    out = []
    for sec in ('Dark Power', 'Finale'):
        a = [x for x in v['secs'].get(sec, []) if x[0] != 'Unrevealed' and x[2] >= 20]
        for x in a:
            r = [y for y in a if y is not x]
            if not r: continue
            n2 = sum(y[2] for y in r); w2 = sum(y[1]*y[2] for y in r) / n2
            q = (x[1]*x[2] + w2*n2) / (x[2] + n2)
            z = (w2 - x[1]) / (q*(1-q)*(1/x[2] + 1/n2)) ** .5
            if z >= 3 and w2 - x[1] >= .15: out.append([sec, x[0], x[1], x[2], round(w2, 4)])
    return out
KX = []
for k, v in D['killers'].items():
    p = P[k]
    sl = slug(k)
    KX.append(dict(
        k=k, box=v.get('box'), wr=v['wr'], n=v['g'], mio=k in MIOS,
        base=K.get(k, {}).get('j') or '',
        s=p['s'], por=p['por'], ojo=p['ojo'], src=p['src'],
        set=SET.get(k), ev=evitar(v), dp=peor(v['secs'].get('Dark Power', [])), fin=peor(v['secs'].get('Finale', [])),
        ficha=('https://finalgirlstats.com/' + sl + '.html') if os.path.exists(f'{WEB}/{sl}.html') else None))
KX.sort(key=lambda x: (not x['mio'], x['wr']))
assert len(KX) == 26

SEC = '''
<section id="killers">
  <h2><span class="num">09</span> Contra cada killer</h2>
  <p class="sub">Los 26, primero los tuyos y luego del más duro al más fácil. Qué salida usar, qué te va a matar y qué Dark Power y Finale temer. La salida es criterio propio a partir de las reglas de cada caja y del foro; la fuente de cada aviso va indicada.</p>
  <div class="barlist" id="kx-list"></div>
  <div class="detalle" id="kx-det"></div>
  <p class="riesgo" style="margin-top:14px"><b>Umbrales</b> Win rate visible desde 5 partidas; Dark Power y Finale más duros solo con 20 o más. Sin datos suficientes, se queda en blanco.</p>
</section>
'''

JS = '''
<script>
  var KX = %s;
  var SRC = { foro: 'Foro BGG', reglas: 'Reglas de la caja', datos: 'Datos', poca: 'Poca información' };
  (function () {
    var pc = function (x) { return (x * 100).toFixed(1).replace('.', ',') + '%%'; };
    var fuente = function (s) { return s.split('+').map(function (t) { return SRC[t]; }).join(' · '); };
    var esc = function (s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;'); };
    function det(x) {
      var h = '<h3>' + esc(x.k) + '</h3><p class="loc">' + (x.box ? esc(x.box) : 'Película corta') + '</p>';
      h += '<div class="split">' +
        (x.n >= 5 ? '<div><b>' + pc(x.wr) + '</b><span>Victorias contra él<br>' + x.n + ' partidas' + (x.n < 20 ? ' · pocas' : '') + '</span></div>' : '') +
        (x.s ? '<div><b>Salida ' + x.s + '</b><span>' + esc(x.por) + '</span></div>' : '') +
        '</div>';
      if (x.base) h += '<p class="sec-t">Cómo es</p><p>' + esc(x.base) + '</p>';
      h += '<p class="sec-t">Lo que te mata · ' + fuente(x.src) + '</p><p>' + esc(x.ojo) + '</p>';
      if (x.set) {
        h += '<p class="sec-t">Carta de Setup · aquí sí importa</p><p><b>Para aprender, empieza con ' + esc(x.set[0][0]) + '</b>: es el Setup con más victorias (' + pc(x.set[0][1]) + ', ' + x.set[0][2] + ' partidas). Cuando la domines, prueba ' + esc(x.set[1][0]) + ', el más duro (' + pc(x.set[1][1]) + ', ' + x.set[1][2] + ' partidas).' +
          (x.set[2] < 2.3 ? ' <em>Diferencia en el límite de lo fiable: pocas partidas.</em>' : '') + '</p>';
      }
      if (x.ev.length) {
        h += '<div class="aviso" style="margin:16px 0 0"><h3>Descompensado</h3>' + x.ev.map(function (e) {
          return '<p><b>' + e[0] + ' ' + esc(e[1]) + '</b>: ' + pc(e[2]) + ' de victorias en ' + e[3] + ' partidas, frente al ' + pc(e[4]) + ' del resto.</p>';
        }).join('') + '<p class="riesgo"><b>Si quieres evitarlo</b> Sale al azar, así que no se puede esquivar en partida. Si buscas una partida equilibrada, sácalo del mazo antes de barajar. Es una regla de la casa, no oficial.</p></div>';
      }
      if (x.dp || x.fin) {
        h += '<p class="sec-t">Lo que más hunde, según los datos</p><div class="tabla-wrap"><table class="mini">' +
          (x.dp ? '<tr class="peor"><td>Dark Power: ' + esc(x.dp[0]) + '</td><td>' + pc(x.dp[1]) + '</td><td>' + x.dp[2] + '</td></tr>' : '') +
          (x.fin ? '<tr class="peor"><td>Finale: ' + esc(x.fin[0]) + '</td><td>' + pc(x.fin[1]) + '</td><td>' + x.fin[2] + '</td></tr>' : '') +
          '</table></div>';
      }
      if (x.ficha) h += '<p style="margin-top:12px"><a href="' + x.ficha + '" style="color:var(--blood)">Ficha completa de ' + esc(x.k) + ' →</a></p>';
      document.getElementById('kx-det').innerHTML = h;
    }
    var lista = document.getElementById('kx-list');
    lista.innerHTML = KX.map(function (x, i) {
      return '<button type="button" class="bar" data-i="' + i + '" aria-pressed="false">' +
        '<span class="fill" style="width:' + (x.wr * 100).toFixed(1) + '%%"></span>' +
        '<span class="nm">' + esc(x.k) + (x.mio ? '<span class="mine">Tuyo</span>' : '') +
        '<i>' + (x.s ? 'Salida ' + x.s : 'Sin salida recomendada') + '</i></span>' +
        '<span class="pc">' + (x.n >= 5 ? pc(x.wr) : '—') + '</span>' +
        '<span class="pl">' + x.n + '</span></button>';
    }).join('');
    lista.querySelectorAll('.bar').forEach(function (b) {
      b.addEventListener('click', function () {
        lista.querySelectorAll('.bar').forEach(function (o) { o.setAttribute('aria-pressed', 'false'); });
        b.setAttribute('aria-pressed', 'true');
        det(KX[parseInt(b.dataset.i, 10)]);
      });
    });
    lista.querySelector('.bar').setAttribute('aria-pressed', 'true');
    det(KX[0]);
  })();
</script>
''' % json.dumps(KX, ensure_ascii=False)

def aplicar(path, out):
    s = open(path).read()
    assert 'id="killers"' not in s, 'ya tiene la seccion 09'
    assert s.count('<footer>') == 1
    s = s.replace('<footer>', SEC + '\n<footer>', 1)
    i = s.rfind('<style>')  # el bloque de identidad final; los scripts van antes
    s = s[:i] + JS + '\n' + s[i:]
    open(out, 'w').write(s)

aplicar(sys.argv[1], sys.argv[2])
print('ok', sys.argv[2])
