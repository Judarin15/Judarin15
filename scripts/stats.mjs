// Genera assets/estadisticas.svg con tus datos reales de GitHub (estética RINCÓN/OS).
// Lo ejecuta la acción .github/workflows/rincon-os.yml una vez al día.
// Local:  GITHUB_TOKEN=xxx node scripts/stats.mjs
// Prueba sin red:  MOCK=ruta/datos.json node scripts/stats.mjs
// Marcador inicial: node scripts/stats.mjs --placeholder
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const ROOT = join(HERE, '..');
const LOGIN = process.env.LOGIN || 'Judarin15';
const C = { glass: '#020d07', glass2: '#05170d', ph: '#4dff91', hi: '#c8ffdd', mid: '#36c476', low: '#1d6e42' };
const SHADES = ['#4dff91', '#36c476', '#c8ffdd', '#1d8f4f', '#7dffb2', '#1d6e42'];
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const b64 = (f) => readFileSync(join(HERE, 'fonts', f)).toString('base64');

const QUERY = `query($login:String!){user(login:$login){
  followers{totalCount}
  repositories(ownerAffiliations:OWNER,isFork:false,privacy:PUBLIC,first:100,orderBy:{field:PUSHED_AT,direction:DESC}){
    totalCount nodes{stargazerCount languages(first:10,orderBy:{field:SIZE,direction:DESC}){edges{size node{name}}}}}
  contributionsCollection{contributionCalendar{totalContributions weeks{contributionDays{contributionCount date}}}}
}}`;

async function fetchData() {
  if (process.env.MOCK) return JSON.parse(readFileSync(process.env.MOCK, 'utf8'));
  const token = process.env.GITHUB_TOKEN;
  if (!token) throw new Error('Falta GITHUB_TOKEN');
  const r = await fetch('https://api.github.com/graphql', {
    method: 'POST',
    headers: { Authorization: `bearer ${token}`, 'Content-Type': 'application/json', 'User-Agent': 'rincon-os-stats' },
    body: JSON.stringify({ query: QUERY, variables: { login: LOGIN } })
  });
  const j = await r.json();
  if (!r.ok || j.errors) throw new Error('GitHub respondió: ' + JSON.stringify(j.errors || j));
  return j.data;
}

function summarize(d) {
  const u = d.user;
  const repos = u.repositories.nodes;
  const stars = repos.reduce((a, r) => a + r.stargazerCount, 0);
  const langs = {};
  repos.forEach((r) => r.languages.edges.forEach((e) => { langs[e.node.name] = (langs[e.node.name] || 0) + e.size; }));
  const total = Object.values(langs).reduce((a, b) => a + b, 0) || 1;
  let top = Object.entries(langs).sort((a, b) => b[1] - a[1]);
  const rest = top.slice(5).reduce((a, [, v]) => a + v, 0);
  top = top.slice(0, 5).map(([n, v]) => [n, v / total]);
  if (rest) top.push(['Otros', rest / total]);
  const days = u.contributionsCollection.contributionCalendar.weeks.flatMap((w) => w.contributionDays);
  // racha actual (si hoy aún no hay aportes, cuenta desde ayer)
  let streak = 0, i = days.length - 1;
  if (i >= 0 && days[i].contributionCount === 0) i--;
  for (; i >= 0 && days[i].contributionCount > 0; i--) streak++;
  let best = 0, run = 0;
  days.forEach((x) => { run = x.contributionCount > 0 ? run + 1 : 0; best = Math.max(best, run); });
  const last30 = days.slice(-30).map((x) => x.contributionCount);
  return {
    contributions: u.contributionsCollection.contributionCalendar.totalContributions,
    repos: u.repositories.totalCount, stars, followers: u.followers.totalCount,
    streak, best, langs: top, last30
  };
}

function render(s, placeholder = false) {
  const W = 960, H = 300;
  const now = new Date().toLocaleString('es-CO', { timeZone: 'America/Bogota', dateStyle: 'medium', timeStyle: 'short' });
  const t = (x, y, str, size, cls, extra = '') => `<text x="${x}" y="${y}" font-size="${size}" class="${cls}" ${extra}>${esc(str)}</text>`;
  let b = `<line x1="0" y1="40" x2="${W}" y2="40" stroke="${C.low}"/>`
    + t(24, 26, 'estadisticas.dat', 13, 'px hi', 'font-weight="600"')
    + t(W - 24, 26, placeholder ? 'esperando primera sincronización' : `sincronizado ${now}`, 12, 'px mid', 'text-anchor="end"')
    + `<text x="28" y="88" font-size="44" class="vt glow"><tspan class="mid">~/</tspan><tspan class="hi">actividad</tspan></text>`;
  if (placeholder) {
    b += t(28, 140, 'Ejecuta la acción "RINCÓN/OS" en la pestaña Actions para cargar tus datos reales.', 14, 'px ph')
      + t(28, 166, 'Después se actualiza sola todos los días.', 14, 'px mid')
      + `<rect x="28" y="190" width="12" height="18" fill="${C.ph}" class="blink"/>`;
  } else {
    const cells = [
      [s.contributions, 'contribuciones en el último año'],
      [s.repos, 'repositorios públicos'],
      [s.streak, s.streak === 1 ? 'día de racha actual' : 'días de racha actual'],
      [s.best, 'mejor racha del año']
    ];
    cells.forEach(([v, lab], k) => {
      const x = 28 + k * 150, y = 154;
      b += `<g class="pop" style="animation-delay:${0.3 + k * 0.12}s">`
        + `<text x="${x}" y="${y}" font-size="54" class="vt hi glow">${esc(v)}</text>`
        + lab.split(' ').reduce((acc, w) => { const l = acc[acc.length - 1]; (l + ' ' + w).trim().length > 17 ? acc.push(w) : acc[acc.length - 1] = (l + ' ' + w).trim(); return acc; }, [''])
          .map((ln, j) => t(x, y + 22 + j * 16, ln, 11.5, 'px mid')).join('')
        + '</g>';
    });
    // últimos 30 días
    const mx = Math.max(1, ...s.last30), bx = 28, by = 270, bw = 572;
    b += t(bx, 236, 'últimos 30 días', 11.5, 'px mid');
    s.last30.forEach((v, k) => {
      const h = v ? 4 + (v / mx) * 22 : 2;
      const x = bx + k * (bw / 30);
      b += `<rect x="${x.toFixed(1)}" y="${(by - h).toFixed(1)}" width="${(bw / 30 - 4).toFixed(1)}" height="${h.toFixed(1)}" fill="${v ? C.ph : C.low}" class="bar" style="animation-delay:${0.6 + k * 0.025}s;transform-origin:0 ${by}px"/>`;
    });
    // lenguajes
    const lx = 650, lw = 282;
    b += t(lx, 118, 'lenguajes en mis repositorios', 11.5, 'px mid');
    let acc = 0;
    s.langs.forEach(([n, p], k) => {
      const w = Math.max(2, lw * p);
      b += `<rect x="${(lx + acc).toFixed(1)}" y="128" width="${(w - 2).toFixed(1)}" height="12" fill="${SHADES[k % SHADES.length]}" class="seg" style="animation-delay:${0.4 + k * 0.1}s;transform-origin:${(lx + acc).toFixed(1)}px 0"/>`;
      acc += w;
      const y = 166 + k * 21;
      b += `<rect x="${lx}" y="${y - 9}" width="10" height="10" fill="${SHADES[k % SHADES.length]}"/>`
        + t(lx + 18, y, n, 13, 'px ph') + t(lx + lw, y, (p * 100).toFixed(1) + '%', 12, 'px mid', 'text-anchor="end"');
    });
  }
  const css = `@font-face{font-family:'VT';src:url(data:font/woff2;base64,${b64('vt323.woff2')}) format('woff2')}
@font-face{font-family:'PX';font-weight:400;src:url(data:font/woff2;base64,${b64('plex-400.woff2')}) format('woff2')}
@font-face{font-family:'PX';font-weight:600;src:url(data:font/woff2;base64,${b64('plex-600.woff2')}) format('woff2')}
.vt{font-family:'VT','Courier New',monospace}.px{font-family:'PX','Consolas','Courier New',monospace}
.hi{fill:${C.hi}}.ph{fill:${C.ph}}.mid{fill:${C.mid}}.glow{filter:url(#glow)}
.pop{animation:pop .7s cubic-bezier(.23,1,.32,1) both}@keyframes pop{0%{opacity:.35;transform:translateY(8px)}40%{opacity:1;filter:brightness(2)}100%{opacity:1;transform:none;filter:none}}
.bar{animation:grow .6s cubic-bezier(.23,1,.32,1) both}@keyframes grow{from{transform:scaleY(.15)}to{transform:scaleY(1)}}
.seg{animation:seg .8s cubic-bezier(.23,1,.32,1) both}@keyframes seg{from{opacity:.3}to{opacity:1}}
.scan{animation:flicker 6s steps(1,end) infinite}@keyframes flicker{0%{opacity:.55}7%{opacity:.45}8%{opacity:.6}43%{opacity:.5}44%{opacity:.56}}
.roll{animation:roll 9s linear infinite}@keyframes roll{from{transform:translateY(-40%)}to{transform:translateY(140%)}}
.blink{animation:blink 1.05s steps(1,end) infinite}@keyframes blink{50%{opacity:0}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}`;
  const label = placeholder ? 'Estadísticas de GitHub: pendientes de sincronizar'
    : `Estadísticas de GitHub: ${s.contributions} contribuciones en el último año, ${s.repos} repositorios públicos, racha actual de ${s.streak} días. Lenguajes: ${s.langs.map(([n, p]) => `${n} ${(p * 100).toFixed(0)}%`).join(', ')}.`;
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(label)}">
<title>Actividad en GitHub</title><style>${css}</style>
<defs>
<pattern id="scanp" width="4" height="3" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity=".5"/></pattern>
<radialGradient id="bloom" cx="50%" cy="40%" r="75%"><stop offset="0" stop-color="${C.ph}" stop-opacity=".09"/><stop offset="1" stop-color="${C.ph}" stop-opacity="0"/></radialGradient>
<radialGradient id="vig" cx="50%" cy="50%" r="72%"><stop offset=".62" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".55"/></radialGradient>
<linearGradient id="rollg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${C.ph}" stop-opacity="0"/><stop offset=".6" stop-color="${C.ph}" stop-opacity=".07"/><stop offset="1" stop-color="${C.ph}" stop-opacity="0"/></linearGradient>
<filter id="glow" x="-10%" y="-30%" width="120%" height="160%"><feGaussianBlur stdDeviation="2.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<clipPath id="frame"><rect x="1" y="1" width="${W - 2}" height="${H - 2}" rx="14"/></clipPath>
</defs>
<g clip-path="url(#frame)"><rect width="${W}" height="${H}" fill="${C.glass}"/>
${b}
<rect width="${W}" height="${H}" fill="url(#bloom)"/>
<rect width="${W}" height="${H}" fill="url(#scanp)" class="scan" opacity=".55"/><rect width="${W}" height="${H * 0.3}" fill="url(#rollg)" class="roll"/><rect width="${W}" height="${H}" fill="url(#vig)"/></g>
<rect x="1" y="1" width="${W - 2}" height="${H - 2}" rx="14" fill="none" stroke="${C.low}" stroke-width="2"/>
</svg>
`;
}

const placeholder = process.argv.includes('--placeholder');
const svg = placeholder ? render(null, true) : render(summarize(await fetchData()));
mkdirSync(join(ROOT, 'assets'), { recursive: true });
writeFileSync(join(ROOT, 'assets', 'estadisticas.svg'), svg);
console.log('assets/estadisticas.svg', (svg.length / 1024).toFixed(1), 'KB');
