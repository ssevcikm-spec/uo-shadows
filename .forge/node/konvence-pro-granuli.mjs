// konvence-pro-granuli.mjs — vybere z CONVENTIONS.md JEN to, co granule potřebuje.
//
// PROČ (naměřeno 15. 10. 2026):
//   `.github/workflows/agent.yml:227` posílá aideru `--read CONVENTIONS.md` CELÝ.
//   Soubor má 13 600 znaků ≈ 4 488 tokenů a jde do KAŽDÉHO requestu — tedy
//   56 % limitu 8 000 (Groq, `gpt-4-oss-120b`). U granulí, které píšou jeden
//   soubor s pár funkcemi, je přitom potřeba jen zlomek: konvence Godotu 4
//   a past na typy. Zbytek limitu padá na text, který se té granule netýká.
//
// CO POSÍLÁ VŽDY: sekce 1–1h (GDScript a pasti, které shazují PARSOVÁNÍ — bez
//   nich agent vyrobí kód, který se vůbec nenačte) a sekci „Ověření".
// CO PŘIDÁ PODLE KONTEXTU: sekce, jejichž téma se v granulи objevuje (UI, mapa,
//   soubory/JSON, co agent nesmí měnit).
//
// POUŽITÍ:
//   node .forge/node/konvence-pro-granuli.mjs --grain engine.input
//   node .forge/node/konvence-pro-granuli.mjs --grain ui.hud --vystup /tmp/k.md
//   node .forge/node/konvence-pro-granuli.mjs --zmer        # jen změří úsporu
//
// VÝSTUP: cesta k vygenerovanému souboru (výchozí `.forge/node/.konvence-<grain>.md`).

import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..', '..');
const KONVENCE = join(ROOT, 'CONVENTIONS.md');
const PLAN = join(ROOT, '.forge', 'roadmap.json');

const arg = (n, d = '') => { const i = process.argv.indexOf(n); return i >= 0 ? process.argv[i + 1] : d; };
const grain = arg('--grain');
const vystup = arg('--vystup', grain ? join(ROOT, '.forge', 'node', `.konvence-${grain.replace(/[^\w.-]/g, '_')}.md`) : '');

// Sekce se hledají podle nadpisu `## …` — text se dělí tak, jak je v souboru.
const text = readFileSync(KONVENCE, 'utf8');
// ⚠ SOUBOR JE CRLF A JS `$` NETREFÍ PŘED `\r` (na rozdíl od Pythonu).
// Naměřeno 15. 10. 2026: `/^##\s*(.*)$/` na řádku `## 1. …\r` vrátí **null**,
// takže parser našel 1 „sekci" a filtr poslal 147 znaků místo celého souboru —
// tichá ztráta kontextu, kterou by nikdo nepoznal. Konce řádků se proto
// normalizují PŘED dělením.
const radky = text.replace(/\r\n/g, '\n').split('\n');
const sekce = [];
let cur = null;
for (const r0 of radky) {
  // Pozor: soubor má nadpisy `## 1.` i `##1b.` (bez mezery) — vzor proto nesmí
  // mezeru vyžadovat. Naměřeno 15. 10. 2026: s `\s+` se našla JEDNA sekce
  // a filtr posílal 147 znaků místo celého souboru (tichá ztráta kontextu).
  const r = r0;
  const m = /^##\s*(.*)$/.exec(r);
  if (m) { cur = { nazev: m[1], radky: [] }; sekce.push(cur); }
  else if (cur) cur.radky.push(r);
  else { (sekce[0] = sekce[0] || { nazev: '(úvod)', radky: [] }).radky.push(r); }
}
const najdi = (re) => sekce.filter((s) => re.test(s.nazev));

// --- které sekce vždy (past na parsování = kód se vůbec nenačte)
const VZDY = [
  /^1\.\s/,        // typy a :=
  /^1b\./, /^1c\./, /^1d\./, /^1e\./, /^1f\./, /^1g\./, /^1h\./,
];
// --- co podle kontextu granule
const KONTEXT = [
  { re: /^4\.\s/, kdy: (t) => /Level|mapa|mřížk|walkable|marker|cell_w|iso/i.test(t) },
  { re: /^5\.\s/, kdy: () => true },                       // co agent nesmí měnit — vždy
  { re: /^6\.\s/, kdy: () => true },                       // styl — vždy (krátké)
  { re: /^7\.\s/, kdy: () => true },                       // ověření — vždy
  { re: /^1c\.|^1e\./, kdy: (t) => /json|data|ConfigFile|save|load/i.test(t) },
];

function vyber(g) {
  const kontext = [g.id, g.title, g.prompt, (g.owns || []).join(' ')].join(' ');
  const vybrane = [];
  for (const s of sekce) {
    if (VZDY.some((re) => re.test(s.nazev))) { vybrane.push(s); continue; }
    if (KONTEXT.some((k) => k.re.test(s.nazev) && k.kdy(kontext))) { vybrane.push(s); continue; }
  }
  return vybrane;
}

const tokeny = (s) => Math.round(s.length / 3.03);

// POZOR: `console.log` formátuje jen když počet argumentů ODPOVÍDÁ počtu `%`
// značek; s argumentem navíc vypíše format string doslova (naměřeno 15. 10. 2026
// — tabulka pak hlásila „0 znaků" a vypadalo to jako vada filtru).
const f = (vzor, ...a) => vzor.replace(/%[-+ 0#]*\d*(?:\.\d+)?[sdifjoO]/g, () => String(a.shift()));

if (process.argv.includes('--zmer') || !grain) {
  const plan = JSON.parse(readFileSync(PLAN, 'utf8'));
  const vsechny = plan.grains.filter((g) => g.done !== true);
  console.log(f('CONVENTIONS.md celý: %d znaků ≈ %d tokenů', text.length, tokeny(text)));
  console.log('');
  console.log(f('%-22s %8s %8s %8s   %s', 'granule', 'znaků', 'tokenů', 'úspora', 'sekce'));
  for (const g of vsechny) {
    const v = vyber(g);
    const telo = v.map((s) => '## ' + s.nazev + '\n' + s.radky.join('\n')).join('\n');
    console.log(f('%-22s %8d %8d %7d%%   %s', g.id, telo.length, tokeny(telo),
      Math.round(100 - (telo.length / text.length) * 100), v.length + '/' + sekce.length));
  }
  if (!grain) process.exit(0);
}

const plan = JSON.parse(readFileSync(PLAN, 'utf8'));
const g = plan.grains.find((x) => x.id === grain);
if (!g) { console.error(`CHYBA: granule '${grain}' v plánu není`); process.exit(2); }

const vybrane = vyber(g);
const hlavicka = [
  `<!-- Vygenerováno .forge/node/konvence-pro-granuli.mjs pro granuli ${g.id}.`,
  '     NEPIŠ DO TOHOHLE SOUBORU — je to výřez z CONVENTIONS.md. -->',
  '',
].join('\n');
const telo = hlavicka + vybrane.map((s) => '## ' + s.nazev + '\n' + s.radky.join('\n').replace(/\s+$/, '')).join('\n\n');
writeFileSync(vystup, telo, 'utf8');
console.log('granule %s: %d sekcí z %d · %d znaků ≈ %d tokenů (celý soubor %d t)',
  g.id, vybrane.length, sekce.length, telo.length, tokeny(telo), tokeny(text));
console.log(vystup);
