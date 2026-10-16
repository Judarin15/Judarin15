"""Genera los paneles SVG animados del README de perfil (estética RINCÓN/OS).

Uso:  python scripts/generar_svgs.py
Edita los datos de la sección CONTENIDO y vuelve a ejecutarlo.
Las fuentes van incrustadas (scripts/fonts) para que GitHub las muestre igual.
"""
from pathlib import Path
from html import escape
import base64

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'assets'
FONTS = Path(__file__).resolve().parent / 'fonts'

# ───────── CONTENIDO ─────────
PERFIL = {
    'nombre': 'JULIÁN RINCÓN',
    'rol': 'Desarrollador web junior en Cúcuta, Colombia.',
    'linea': 'Tecnólogo SENA en Análisis y Desarrollo de Software. Estudiante de Ing. de Sistemas.',
    'usuario': 'Judarin15',
}
ARRANQUE = [
    ('$ ./arranque --usuario judarin15', ''),
    ('prueba de memoria ............ ', '64K OK'),
    ('nodo ......................... ', 'CÚCUTA 7.89N 72.51O'),
    ('montando ~/proyectos ......... ', '4 DESTACADOS'),
    ('estado ....................... ', 'DISPONIBLE PARA TRABAJAR'),
]
COMANDOS = ['ver --proyectos', 'abrir portafolio', 'contratar --junior --remoto']

HABILIDADES = [
    ('Frontend', [('HTML y CSS', 3, 30), ('JavaScript', 2, 24), ('React', 2, 18), ('TypeScript', 2, 12), ('Tailwind CSS', 2, 12), ('Next.js', 1, 8)]),
    ('Backend y datos', [('Firebase', 2, 9), ('Google Apps Script', 2, 7), ('Python', 1, 12), ('Supabase', 1, 4), ('PostgreSQL', 1, 6)]),
    ('Herramientas e IA', [('Git y GitHub', 2, 24), ('Figma', 2, 12), ('Vite', 2, 12), ('IA y agentes', 2, 12)]),
]
MAX_MESES = 30

PROYECTOS = [
    {'slug': 'intranet', 'file': 'intranet-comfaoriente', 'estado': ('live', 'EN PRODUCCIÓN'), 'fecha': 'jul 2026',
     'titulo': 'Intranet Comfaoriente',
     'desc': 'Plataforma web que centraliza la información académica y administrativa del Gimnasio Campestre Comfaoriente. La desarrollé y desplegué en mi práctica del SENA.',
     'cifras': [('47', 'docentes'), ('840', 'estudiantes'), ('882', 'clases')],
     'stack': ['React', 'TypeScript', 'Firebase', 'Apps Script'], 'cta': 'abrir repositorio'},
    {'slug': 'techmarket', 'file': 'techmarket', 'estado': ('dev', 'EN DESARROLLO'), 'fecha': 'sep 2026',
     'titulo': 'TechMarket',
     'desc': 'Tienda en línea de electrónica y gaming con catálogo filtrable, carrito con validación de stock, cuentas de cliente y panel administrativo.',
     'linea': 'Interfaz diseñada en Figma antes de programar.',
     'stack': ['React', 'Vite', 'Supabase', 'Figma'], 'cta': 'abrir repositorio'},
    {'slug': 'galaxia', 'file': 'galaxia-sonora', 'estado': ('pub', 'PUBLICADO'), 'fecha': 'jul 2026',
     'titulo': 'Galaxia Sonora',
     'desc': 'Tienda virtual que reúne en un solo lugar la venta de audiolibros en español publicados en Hotmart y Etsy. Proyecto propio.',
     'linea': 'galaxiasonora.com',
     'stack': ['HTML', 'CSS', 'JavaScript'], 'cta': 'visitar sitio'},
    {'slug': 'portafolio', 'file': 'rincon-os', 'estado': ('live', 'EN LÍNEA'), 'fecha': 'oct 2026',
     'titulo': 'Portafolio RINCÓN/OS',
     'desc': 'Mi portafolio como terminal CRT animada: arranque, sonidos, consola interactiva, carruseles y panel de administración privado.',
     'linea': 'Escribe ayuda en su terminal.',
     'stack': ['HTML', 'CSS', 'JavaScript', 'Firebase'], 'cta': 'abrir portafolio'},
]

REGISTRO = [
    ('ago 2026', 'logro', 'Grado como Tecnólogo en Análisis y Desarrollo de Software', 'SENA'),
    ('ene 2026 – jul 2026', 'experiencia', 'Practicante de apoyo de sistemas', 'Gimnasio Campestre Comfaoriente, Cúcuta'),
    ('jul 2024 – hoy', 'educación', 'Ingeniería de Sistemas', 'Universidad de Pamplona'),
    ('feb 2024 – hoy', 'experiencia', 'Auxiliar de ingeniería', 'Ing. Civil Mauricio Bolívar Cuéllar, Cúcuta'),
    ('dic 2022', 'logro', 'Inglés nivel B1', 'Academia Inglés Para Todos'),
]

BOTONES = [
    ('btn-portafolio', 'Abrir portafolio', 'monitor'),
    ('btn-cv', 'Hoja de vida', 'doc'),
    ('btn-correo', 'Escribirme', 'mail'),
]

# ───────── ESTILO ─────────
C = {'glass': '#020d07', 'glass2': '#05170d', 'glass3': '#0b2817', 'ph': '#4dff91', 'hi': '#c8ffdd', 'mid': '#36c476', 'low': '#1d6e42', 'warn': '#ffc24d'}
VT, PLEX = 0.4, 0.6  # ancho de carácter (em)


def font_face(text=''):
    """Incrusta las fuentes recortadas a los caracteres que usa cada SVG."""
    import io
    from fontTools import subset
    from fontTools.ttLib import TTFont
    import re
    from html import unescape
    visible = ''.join(re.findall(r'>([^<>]*)<', text)) if '<' in text else text
    chars = ''.join(sorted(set(unescape(visible)) | set(' 0123456789')))
    def sub(name):
        font = TTFont(str(FONTS / name))
        opts = subset.Options(); opts.flavor = 'woff2'; opts.layout_features = []; opts.hinting = False; opts.desubroutinize = True; opts.name_IDs = [1, 2]; opts.notdef_outline = True
        s = subset.Subsetter(opts); s.populate(text=chars); s.subset(font)
        buf = io.BytesIO(); font.save(buf)
        return base64.b64encode(buf.getvalue()).decode()
    return (f"@font-face{{font-family:'VT';src:url(data:font/woff2;base64,{sub('vt323.woff2')}) format('woff2')}}"
            f"@font-face{{font-family:'PX';font-weight:400;src:url(data:font/woff2;base64,{sub('plex-400.woff2')}) format('woff2')}}"
            f"@font-face{{font-family:'PX';font-weight:600;src:url(data:font/woff2;base64,{sub('plex-600.woff2')}) format('woff2')}}")


BASE_CSS = f"""
.vt{{font-family:'VT','Courier New',monospace}}
.px{{font-family:'PX','Consolas','Courier New',monospace}}
.hi{{fill:{C['hi']}}} .ph{{fill:{C['ph']}}} .mid{{fill:{C['mid']}}}
.glow{{filter:url(#glow)}}
.scan{{animation:flicker 6s steps(1,end) infinite}}
.roll{{animation:roll 9s linear infinite}}
.blink{{animation:blink 1.05s steps(1,end) infinite}}
.pulse{{animation:pulse 2.4s ease-in-out infinite}}
@keyframes flicker{{0%{{opacity:.55}}7%{{opacity:.45}}8%{{opacity:.6}}43%{{opacity:.5}}44%{{opacity:.56}}71%{{opacity:.48}}72%{{opacity:.58}}}}
@keyframes roll{{from{{transform:translateY(-40%)}}to{{transform:translateY(140%)}}}}
@keyframes blink{{50%{{opacity:0}}}}
@keyframes pulse{{50%{{opacity:.3}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}
"""


def defs(w, h):
    return f"""<defs>
  <pattern id="scanp" width="4" height="3" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".5"/></pattern>
  <radialGradient id="bloom" cx="50%" cy="40%" r="75%"><stop offset="0" stop-color="{C['ph']}" stop-opacity=".09"/><stop offset=".55" stop-color="{C['ph']}" stop-opacity=".02"/><stop offset="1" stop-color="{C['ph']}" stop-opacity="0"/></radialGradient>
  <radialGradient id="vig" cx="50%" cy="50%" r="72%"><stop offset=".62" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".55"/></radialGradient>
  <linearGradient id="rollg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C['ph']}" stop-opacity="0"/><stop offset=".6" stop-color="{C['ph']}" stop-opacity=".07"/><stop offset="1" stop-color="{C['ph']}" stop-opacity="0"/></linearGradient>
  <filter id="glow" x="-10%" y="-30%" width="120%" height="160%"><feGaussianBlur stdDeviation="2.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  <clipPath id="frame"><rect x="1" y="1" width="{w-2}" height="{h-2}" rx="14"/></clipPath>
</defs>"""


def svg(w, h, title, body, css='', label=''):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(label or title)}">
<title>{escape(title)}</title>
<style>{font_face(body + title)}{BASE_CSS}{css}</style>
{defs(w, h)}
<g clip-path="url(#frame)">
<rect width="{w}" height="{h}" fill="{C['glass']}"/>
{body}
<rect width="{w}" height="{h}" fill="url(#bloom)"/>
<rect width="{w}" height="{h}" fill="url(#scanp)" class="scan" opacity=".55"/>
<rect width="{w}" height="{h*0.3:.0f}" fill="url(#rollg)" class="roll"/>
<rect width="{w}" height="{h}" fill="url(#vig)"/>
</g>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="14" fill="none" stroke="{C['low']}" stroke-width="2"/>
</svg>
"""


def t(x, y, s, size, cls='px ph', extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" class="{cls}" {extra}>{escape(s)}</text>'


def topbar(w, left, right=''):
    return (f'<line x1="0" y1="40" x2="{w}" y2="40" stroke="{C["low"]}"/>'
            + t(24, 26, left, 13, 'px hi', 'font-weight="600" letter-spacing=".5"')
            + (t(w - 24, 26, right, 12, 'px mid', 'text-anchor="end"') if right else ''))


def wrap(text, n):
    words, lines, cur = text.split(), [], ''
    for wd in words:
        if len(cur) + len(wd) + (1 if cur else 0) > n:
            lines.append(cur); cur = wd
        else:
            cur = (cur + ' ' + wd) if cur else wd
    if cur: lines.append(cur)
    return lines


# ───────── PANELES ─────────
def header():
    W, H = 960, 420
    css, body = '', [topbar(W, 'RINCÓN/OS 2.6', f'terminal de perfil   github.com/{PERFIL["usuario"]}')]
    # líneas de arranque con efecto de tecleo
    fs, cw = 14, 14 * PLEX
    delay = 0.35
    for i, (lab, val) in enumerate(ARRANQUE):
        y = 80 + i * 23
        full = lab + val
        wpx = len(full) * cw + 14
        dur = max(0.25, len(full) * 0.016)
        k = f'ty{i}'
        css += f'@keyframes {k}{{from{{transform:translateX(0);opacity:1}}99.9%{{opacity:1}}to{{transform:translateX({wpx:.1f}px);opacity:0}}}}'
        body.append(f'<text x="40" y="{y}" font-size="{fs}" class="px ph" xml:space="preserve">{escape(lab)}<tspan class="hi">{escape(val)}</tspan></text>')
        body.append(f'<g style="opacity:0;animation:{k} {dur:.2f}s steps({len(full)}) {delay:.2f}s both"><rect x="38" y="{y-15}" width="{wpx:.1f}" height="21" fill="{C["glass"]}"/><rect x="38" y="{y-13}" width="8" height="16" fill="{C["ph"]}"/></g>')
        delay += dur + 0.12
    name_at = delay + 0.15
    # osciloscopio (derecha)
    ox, oy, ow, oh = 640, 58, 288, 120
    grid = ''.join(f'<line x1="{ox+x}" y1="{oy}" x2="{ox+x}" y2="{oy+oh}" stroke="{C["ph"]}" stroke-opacity=".08"/>' for x in range(0, ow + 1, 32))
    grid += ''.join(f'<line x1="{ox}" y1="{oy+y}" x2="{ox+ow}" y2="{oy+y}" stroke="{C["ph"]}" stroke-opacity=".08"/>' for y in range(0, oh + 1, 24))
    import math
    def wave(ph, amp):
        pts = []
        for x in range(0, ow + 1, 6):
            env = math.sin(math.pi * x / ow)
            y = oy + oh / 2 + env * (math.sin(x * .05 + ph) * amp + math.sin(x * .13 - ph * 1.6) * amp * .35)
            pts.append(f'{ox+x:.1f},{y:.1f}')
        return 'M' + ' L'.join(pts)
    waves = [wave(p, a) for p, a in [(0, 18), (1.6, 26), (3.1, 14), (4.7, 30), (0, 18)]]
    body.append(f'<g><rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" fill="{C["glass2"]}" stroke="{C["low"]}"/>{grid}'
                f'<path fill="none" stroke="{C["ph"]}" stroke-width="2" class="glow" d="{waves[0]}"><animate attributeName="d" dur="3.2s" repeatCount="indefinite" values="{";".join(waves)}"/></path>'
                + t(ox + 10, oy + oh + 20, 'señal', 11, 'px mid') + t(ox + ow - 10, oy + oh + 20, 'canal abierto', 11, 'px mid', 'text-anchor="end"') + '</g>')
    # nombre
    css += f"""
.name{{animation:nameIn 1.1s cubic-bezier(.23,1,.32,1) {name_at:.2f}s both}}
.gl1{{animation:glitch 1.1s steps(1) {name_at:.2f}s both}}
.gl2{{animation:glitch2 1.1s steps(1) {name_at:.2f}s both}}
@keyframes nameIn{{0%{{opacity:0;filter:blur(6px)}}25%{{opacity:1;filter:blur(1px)}}32%{{opacity:.25}}40%{{opacity:1;filter:none}}100%{{opacity:1}}}}
@keyframes glitch{{0%{{opacity:0}}10%{{opacity:.8;transform:translateX(-7px)}}20%{{transform:translateX(5px)}}30%{{transform:translateX(-3px)}}45%,100%{{opacity:0;transform:none}}}}
@keyframes glitch2{{0%{{opacity:0}}15%{{opacity:.6;transform:translateX(6px)}}28%{{transform:translateX(-4px)}}40%,100%{{opacity:0;transform:none}}}}
.fade{{animation:fade .6s ease-out both}}
@keyframes fade{{from{{opacity:0;transform:translateY(6px)}}to{{opacity:1;transform:none}}}}
"""
    ny = 262
    for cls, fill, op in [('gl1', C['ph'], '0'), ('gl2', C['mid'], '0')]:
        body.append(f'<text x="36" y="{ny}" font-size="96" class="vt {cls}" fill="{fill}" opacity="{op}">{escape(PERFIL["nombre"])}</text>')
    body.append(f'<text x="36" y="{ny}" font-size="96" class="vt hi glow name">{escape(PERFIL["nombre"])}</text>')
    body.append(f'<g class="fade" style="animation-delay:{name_at+0.5:.2f}s">' + t(40, 298, PERFIL['rol'], 19, 'px ph glow') + '</g>')
    body.append(f'<g class="fade" style="animation-delay:{name_at+0.7:.2f}s">' + t(40, 326, PERFIL['linea'], 14, 'px mid') + '</g>')
    # línea de comandos con frases en bucle
    py = 382
    body.append(f'<line x1="0" y1="350" x2="{W}" y2="350" stroke="{C["low"]}"/>')
    prompt = 'julian@rincon-os:~$ '
    body.append(f'<text x="24" y="{py}" font-size="15" class="px hi" xml:space="preserve">{escape(prompt)}</text>')
    px0 = 24 + len(prompt) * 15 * PLEX
    cyc = 4.2 * len(COMANDOS)
    for i, cmd in enumerate(COMANDOS):
        n = len(cmd); wpx = n * 15 * PLEX + 4
        a = i / len(COMANDOS) * 100; seg = 100 / len(COMANDOS)
        p1, p2, p3, p4 = a, a + seg * .40, a + seg * .80, a + seg * .96
        css += (f'@keyframes cv{i}{{0%,{max(a-0.01,0):.2f}%{{opacity:0}}{a:.2f}%,{p4:.2f}%{{opacity:1}}{min(p4+0.01,100):.2f}%,100%{{opacity:0}}}}'
                f'@keyframes ct{i}{{0%,{p1:.2f}%{{transform:translateX(0);animation-timing-function:steps({n})}}{p2:.2f}%,{p3:.2f}%{{transform:translateX({wpx:.1f}px);animation-timing-function:steps({n})}}{p4:.2f}%,100%{{transform:translateX(0)}}}}')
        body.append(f'<g style="opacity:0;animation:cv{i} {cyc:.1f}s linear {name_at+1:.2f}s infinite">'
                    f'<text x="{px0:.1f}" y="{py}" font-size="15" class="px ph">{escape(cmd)}</text>'
                    f'<g style="animation:ct{i} {cyc:.1f}s linear {name_at+1:.2f}s infinite"><rect x="{px0-1:.1f}" y="{py-15}" width="{wpx+20:.1f}" height="21" fill="{C["glass"]}"/>'
                    f'<rect x="{px0:.1f}" y="{py-13}" width="9" height="17" fill="{C["ph"]}" class="blink"/></g></g>')
    # estado
    body.append(f'<g><rect x="{W-196}" y="366" width="10" height="10" fill="{C["ph"]}" class="pulse glow"/>' + t(W - 178, 376, 'DISPONIBLE', 13, 'px ph', 'font-weight="600" letter-spacing="1"') + '</g>')
    write('header.svg', svg(W, H, 'RINCÓN/OS: Julián Rincón', '\n'.join(body), css,
                             f'Julián Rincón. {PERFIL["rol"]} {PERFIL["linea"]} Disponible para trabajar.'))


def section_title(slug, title, sub, right):
    W, H = 960, 96
    body = [topbar(W, f'{slug}.dir', right),
            f'<text x="28" y="80" font-size="44" class="vt glow"><tspan class="mid">~/</tspan><tspan class="hi">{escape(title)}</tspan></text>',
            t(W - 28, 78, sub, 13, 'px mid', 'text-anchor="end"')]
    css = '.vt{animation:fade .7s ease-out backwards}@keyframes fade{from{opacity:.3}to{opacity:1}}'
    write(f'titulo-{slug}.svg', svg(W, H, title, '\n'.join(body), css))


def project_card(p):
    W, H = 470, 290
    st_cls, st_label = p['estado']
    st_color = {'live': C['ph'], 'dev': C['warn'], 'pub': C['hi']}[st_cls]
    b = [f'<line x1="0" y1="40" x2="{W}" y2="40" stroke="{C["low"]}"/>',
         t(20, 26, '> ' + p['file'], 13, 'px hi'),
         t(W - 20, 26, p['fecha'], 12, 'px mid', 'text-anchor="end"')]
    chip_w = len(st_label) * 10.5 * PLEX + 30
    cx = W - 20 - len(p['fecha']) * 12 * PLEX - 14 - chip_w
    b.append(f'<g><rect x="{cx:.1f}" y="13" width="{chip_w:.1f}" height="19" fill="none" stroke="{st_color}"/>'
             f'<rect x="{cx+8:.1f}" y="19.5" width="6" height="6" fill="{st_color}" class="pulse"/>'
             f'<text x="{cx+20:.1f}" y="26.5" font-size="10.5" class="px" fill="{st_color}" font-weight="600" letter-spacing=".6">{escape(st_label)}</text></g>')
    b.append(f'<text x="20" y="84" font-size="36" class="vt hi glow">{escape(p["titulo"])}</text>')
    y = 112
    for line in wrap(p['desc'], 54)[:3]:
        b.append(t(20, y, line, 13, 'px ph')); y += 20
    y = max(y, 172) + 8
    if p.get('cifras'):
        x = 20
        for num, lab in p['cifras']:
            b.append(f'<text x="{x}" y="{y+16}" font-size="30" class="vt hi glow">{num}</text>')
            nx = x + len(num) * 30 * VT + 8
            b.append(t(f'{nx:.0f}', y + 14, lab, 12, 'px mid'))
            x = nx + len(lab) * 12 * PLEX + 22
    elif p.get('linea'):
        b.append(t(20, y + 12, '+ ' + p['linea'], 12.5, 'px mid'))
    # tecnologías
    x, ty = 20, 232
    for s in p['stack']:
        w = len(s) * 11 * PLEX + 16
        b.append(f'<rect x="{x:.1f}" y="{ty}" width="{w:.1f}" height="22" fill="none" stroke="{C["low"]}"/>' + t(f'{x+8:.1f}', ty + 15, s, 11, 'px mid'))
        x += w + 6
    # llamada a la acción
    cta = p['cta']
    cw = len(cta) * 12 * PLEX
    b.append(f'<g>{t(W-38-cw, 272, cta, 12, "px hi", "font-weight=\"600\"")}<line x1="{W-38-cw:.1f}" y1="276" x2="{W-38:.1f}" y2="276" stroke="{C["hi"]}"/>'
             f'<path d="M{W-30} 263 l6 5 -6 5" fill="none" stroke="{C["hi"]}" stroke-width="2"/></g>')
    # barrido de entrada
    css = (f'.sweep{{animation:sweep 1.4s cubic-bezier(.77,0,.175,1) .3s both}}'
           f'@keyframes sweep{{from{{transform:translateY(-120px)}}to{{transform:translateY({H+40}px)}}}}')
    b.append(f'<rect x="0" y="0" width="{W}" height="90" class="sweep" fill="url(#rollg)"/>')
    write(f'p-{p["slug"]}.svg', svg(W, H, p['titulo'], '\n'.join(b), css, f'{p["titulo"]}: {p["desc"]}'))


def skills():
    W = 960
    rows = max(len(items) for _, items in HABILIDADES)
    H = 130 + rows * 46 + 40
    b = [topbar(W, 'habilidades.mod', f'{sum(len(i) for _, i in HABILIDADES)} MÓDULOS'),
         f'<text x="28" y="88" font-size="44" class="vt glow"><tspan class="mid">~/</tspan><tspan class="hi">habilidades</tspan></text>']
    css = '@keyframes charge{0%{opacity:.25}60%{opacity:1;filter:brightness(1.8)}100%{opacity:1;filter:none}}'
    colw, gap = 284, 30
    k = 0
    for ci, (cat, items) in enumerate(HABILIDADES):
        x0 = 28 + ci * (colw + gap)
        b.append(t(x0, 124, f'{cat}  {len(items)}', 12, 'px mid', 'letter-spacing=".5"'))
        b.append(f'<line x1="{x0}" y1="132" x2="{x0+colw}" y2="132" stroke="{C["low"]}"/>')
        for ri, (name, lvl, months) in enumerate(items):
            y = 158 + ri * 46
            b.append(t(x0, y, name, 14, 'px ph'))
            for q in range(3):
                fill = C['ph'] if q < lvl else 'none'
                b.append(f'<rect x="{x0+colw-40+q*14}" y="{y-10}" width="9" height="9" fill="{fill}" stroke="{C["ph"]}"/>')
            yrs, mo = divmod(months, 12)
            lab = (f'{yrs}a' if yrs else '') + (' ' if yrs and mo else '') + (f'{mo}m' if mo else '')
            bw = colw - 52
            fw = bw * min(1, months / MAX_MESES)
            b.append(f'<rect x="{x0}" y="{y+8}" width="{bw}" height="8" fill="none" stroke="{C["low"]}"/>')
            b.append(f'<g style="animation:charge .8s ease-out {0.3+k*0.07:.2f}s backwards">'
                     f'<rect x="{x0}" y="{y+8}" width="{fw:.1f}" height="8" fill="url(#segs)" class="glow"/></g>')
            b.append(t(x0 + colw, y + 16, lab, 11, 'px mid', 'text-anchor="end"'))
            k += 1
    b.append(t(28, H - 18, 'nivel: básico, intermedio o avanzado   barra: tiempo de experiencia, hasta 2 años 6 meses', 11, 'px mid'))
    body = '\n'.join(b)
    body = (f'<defs><pattern id="segs" width="8" height="8" patternUnits="userSpaceOnUse"><rect width="6" height="8" fill="{C["ph"]}"/></pattern></defs>' + body)
    write('habilidades.svg', svg(W, H, 'Habilidades', body, css,
                                 'Habilidades: ' + '; '.join(f'{c}: ' + ', '.join(n for n, _, _ in i) for c, i in HABILIDADES)))


def registro():
    W = 960
    H = 120 + len(REGISTRO) * 54 + 10
    b = [topbar(W, 'registro.log', 'formación y experiencia'),
         f'<text x="28" y="88" font-size="44" class="vt glow"><tspan class="mid">~/</tspan><tspan class="hi">trayectoria</tspan></text>']
    css = ('.row{animation:print .7s cubic-bezier(.23,1,.32,1) both}'
           '@keyframes print{0%{opacity:.35;transform:translateX(-8px)}40%{opacity:1;filter:brightness(2.2)}100%{opacity:1;filter:none;transform:none}}')
    for i, (when, kind, title, org) in enumerate(REGISTRO):
        y = 130 + i * 54
        hot = kind == 'logro'
        kw = len(kind) * 11 * PLEX + 16
        b.append(f'<g class="row" style="animation-delay:{0.3+i*0.12:.2f}s">'
                 f'<line x1="28" y1="{y-22}" x2="{W-28}" y2="{y-22}" stroke="{C["low"]}" stroke-opacity=".6"/>'
                 + t(28, y, when, 13, 'px mid')
                 + f'<rect x="228" y="{y-14}" width="{kw:.1f}" height="20" fill="none" stroke="{C["mid"] if hot else C["low"]}"/>'
                 + t(236, y, kind, 11, 'px hi' if hot else 'px mid')
                 + t(360, y - 2, title, 15, 'px hi', 'font-weight="600"')
                 + t(360, y + 17, org, 12.5, 'px mid') + '</g>')
    write('trayectoria.svg', svg(W, H, 'Trayectoria', '\n'.join(b), css,
                                 'Trayectoria: ' + '; '.join(f'{w}, {ti}, {o}' for w, _, ti, o in REGISTRO)))


ICONS = {
    'monitor': '<rect x="0" y="1" width="20" height="14" fill="none" stroke="currentColor" stroke-width="2"/><path d="M6 20h8M10 15v5" stroke="currentColor" stroke-width="2"/><path d="M4 6l3 2.5L4 11M9 11h5" fill="none" stroke="currentColor" stroke-width="1.8"/>',
    'doc': '<path d="M3 0h9l5 5v15H3z" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 0v5h5M6 11h8M6 15h8" fill="none" stroke="currentColor" stroke-width="2"/>',
    'mail': '<rect x="0" y="3" width="20" height="14" fill="none" stroke="currentColor" stroke-width="2"/><path d="M0 4l10 7 10-7" fill="none" stroke="currentColor" stroke-width="2"/>',
}


def button(slug, label, icon, solid=False):
    W, H = 236, 52
    fg = C['glass'] if solid else C['hi']
    css = '.ring{animation:ring 2.4s ease-in-out infinite}@keyframes ring{50%{stroke-opacity:.35}}'
    b = (f'<rect x="1" y="1" width="{W-2}" height="{H-2}" fill="{C["ph"] if solid else C["glass"]}" stroke="{C["ph"]}" stroke-width="2" class="ring"/>'
         f'<g transform="translate(22 16)" style="color:{fg}">{ICONS[icon]}</g>'
         f'<text x="56" y="32" font-size="16" class="px" font-weight="600" fill="{fg}">{escape(label)}</text>'
         f'<rect x="1" y="1" width="{W-2}" height="{H-2}" fill="url(#scanp)" opacity=".35"/>')
    s = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(label)}">'
         f'<title>{escape(label)}</title><style>{font_face(label)}{BASE_CSS}{css}</style>'
         f'<defs><pattern id="scanp" width="4" height="3" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".5"/></pattern></defs>{b}</svg>\n')
    write(f'{slug}.svg', s)


def footer():
    W, H = 960, 70
    msg = 'fin de transmisión. gracias por pasar.'
    b = [t(28, 42, f'julian@rincon-os:~$ {msg}', 14, 'px mid', 'xml:space="preserve"'),
         f'<rect x="{28 + (21 + len(msg)) * 14 * PLEX:.1f}" y="29" width="9" height="16" fill="{C["ph"]}" class="blink"/>',
         t(W - 28, 42, '© 2026 Julián Rincón', 12, 'px mid', 'text-anchor="end"')]
    write('pie.svg', svg(W, H, 'Fin de transmisión', '\n'.join(b)))


def serpiente_inicial():
    # Solo se crea si aún no existe: la acción la reemplaza por la serpiente real.
    if (OUT / 'serpiente.svg').exists():
        return
    W, H = 960, 120
    b = [t(28, 56, 'serpiente.exe en espera', 14, 'px hi'),
         t(28, 82, 'Aparece después de la primera sincronización de la acción.', 13, 'px mid'),
         f'<rect x="{28 + 24 * 14 * PLEX:.1f}" y="43" width="9" height="16" fill="{C["ph"]}" class="blink"/>']
    write('serpiente.svg', svg(W, H, 'Serpiente de contribuciones', '\n'.join(b)))


def write(name, content):
    OUT.mkdir(exist_ok=True)
    (OUT / name).write_text(content, encoding='utf-8')
    print(f'  {name:24} {len(content)/1024:6.1f} KB')


if __name__ == '__main__':
    header()
    section_title('proyectos', 'proyectos', 'clic en una ventana para abrirla', '4 ARCHIVOS')
    for p in PROYECTOS:
        project_card(p)
    skills()
    registro()
    for i, (slug, label, icon) in enumerate(BOTONES):
        button(slug, label, icon, solid=(i == 0))
    footer()
    serpiente_inicial()
