// hlidej-orchestru.mjs — jednorázový snímek stavu orchestry pro uo-shadows.
//
// PROČ TO EXISTUJE (15. 10. 2026): po resetu plánu je potřeba vidět JEDNOU
// a celé: co conductor vydal, co doběhlo, jaké PR vznikly a co je ve frontě.
// Ruční dotazy na pět endpointů se zapomínají — a stav se pak čte po paměti.
//
// POUŽITÍ: node _analyza/PRACE-2026-10-15/hlidej-orchestru.mjs
import { readFileSync } from 'node:fs';

const ORCH = 'E:/Workspaces/forge-orchestra';
const env = Object.fromEntries(readFileSync(ORCH + '/.env', 'utf8').replace(/^\uFEFF/, '')
  .split(/\r?\n/).filter((l) => l.includes('='))
  .map((l) => [l.slice(0, l.indexOf('=')).trim(), l.slice(l.indexOf('=') + 1).trim()]));
const pat = readFileSync(ORCH + '/.secrets/conductor_pat.txt', 'utf8').trim();
const api = (c) => fetch(env.FORGE_URL + c, { headers: { 'x-forge-secret': env.FORGE_SECRET } }).then((r) => r.json());

const h = await (await fetch(env.FORGE_URL + '/health')).json();
console.log('=== /health ===');
console.log('  ok=%s ready=%s running=%s time=%s', h.ok, h.ready, h.running, h.time);
for (const t of h.targets || []) {
  console.log('  cíl: %s | main_ci=%s | forge.ok=%s | selhání v řadě=%s',
    t.game_id, t.main_ci ? t.main_ci.conclusion : 'null', t.forge && t.forge.ok,
    t.forge && t.forge.selhani_v_rade);
}

const s = await api('/status');
console.log('=== běhy (nejnovější) ===');
for (const r of (s.runs || []).slice(0, 10)) {
  console.log('  #%s task=%s %-9s %s %s', r.id, r.task_id, r.status,
    (r.title || '').slice(0, 46), r.pr_url ? 'PR ' + r.pr_url : '');
}

const rm = await api('/roadmap');
const moje = (rm.roadmap || []).filter((x) => String(x.item_id).startsWith('uo-shadows/'));
console.log('=== fronta uo-shadows: %d položek ===', moje.length);
for (const x of moje) console.log('  %-34s %-8s attempts=%s', x.item_id, x.status, x.attempts);

const f = await api('/failed');
console.log('=== /failed: %d úloh ===', (f.tasks || []).length);
for (const t of (f.tasks || []).slice(0, 5)) {
  console.log('  #%s %s (pokusů: %s)', t.id, String(t.title).slice(0, 52), t.attempts);
}

// PR v herním repu — důkaz, že práce vzniká
const pr = await (await fetch('https://api.github.com/repos/ssevcikm-spec/uo-shadows/pulls?state=all&per_page=5',
  { headers: { authorization: 'Bearer ' + pat } })).json();
console.log('=== PR v herním repu (nejnovější) ===');
for (const p of (Array.isArray(pr) ? pr : []).slice(0, 5)) {
  console.log('  #%s %-9s %s', p.number, p.state, String(p.title).slice(0, 60));
}
