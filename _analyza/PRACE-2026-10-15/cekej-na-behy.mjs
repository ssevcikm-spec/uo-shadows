// cekej-na-behy.mjs — počká, až orchestra doběhne nové běhy, a vypíše výsledek.
//
// PROČ: po opravě zadání je potřeba vidět, jestli další pokus projde — a čekat
// v konverzaci je drahé. Tenhle skript čeká sám a hlásí JEN změny.
//
// POUŽITÍ: node _analyza/PRACE-2026-10-15/cekej-na-behy.mjs [minuty]
import { readFileSync } from 'node:fs';

const ORCH = 'E:/Workspaces/forge-orchestra';
const env = Object.fromEntries(readFileSync(ORCH + '/.env', 'utf8').replace(/^\uFEFF/, '')
  .split(/\r?\n/).filter((l) => l.includes('='))
  .map((l) => [l.slice(0, l.indexOf('=')).trim(), l.slice(l.indexOf('=') + 1).trim()]));
const api = (c) => fetch(env.FORGE_URL + c, { headers: { 'x-forge-secret': env.FORGE_SECRET } }).then((r) => r.json());

const minuty = Number(process.argv[2] || 10);
const start = await api('/status');
const videno = new Map((start.runs || []).map((r) => [r.id, r.status]));
console.log('výchozí stav: %d běhů v historii, čekám na nové (%d min)', videno.size, minuty);

let kdykoli = false;
const konec = Date.now() + minuty * 60_000;
while (Date.now() < konec) {
  await new Promise((x) => setTimeout(x, 25_000));
  const s = await api('/status');
  for (const r of s.runs || []) {
    const stary = videno.get(r.id);
    if (stary === undefined || (stary === 'running' && r.status !== 'running')) {
      videno.set(r.id, r.status);
      kdykoli = true;
      const znacka = r.status === 'success' ? '✔' : (r.status === 'failed' || r.status === 'failure' ? '✘' : '…');
      console.log('%s #%s task=%s [%s] %s %s', znacka, r.id, r.task_id, r.status,
        String(r.title || '').slice(0, 50), r.pr_url ? 'PR ' + r.pr_url : '');
      if (r.summary) console.log('     %s', String(r.summary).slice(0, 200));
    }
  }
  const h = await (await fetch(env.FORGE_URL + '/health')).json();
  process.stdout.write('  tik=' + h.last_cron_min + 'min ready=' + h.ready + ' running=' + h.running + '\r');
}

const rm = await api('/roadmap');
const moje = (rm.roadmap || []).filter((x) => String(x.item_id).startsWith('uo-shadows/'));
console.log('\n=== fronta uo-shadows (%d) ===', moje.length);
for (const x of moje) console.log('  %s -> %s (pokusů %s)', x.item_id, x.status, x.attempts);
console.log(kdykoli ? '\nběhem čekání se něco stalo (viz výš)' : '\nběhem čekání se NIC nového nevydalo');
