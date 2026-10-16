// Diagnostika: proč parser sekcí nevidí nadpisy CONVENTIONS.md?
import { readFileSync } from 'node:fs';

const t = readFileSync('CONVENTIONS.md', 'utf8');
const radky = t.split('\n');

// 1) přesné bajty prvních znaků souboru (BOM?)
console.log('prvních 6 znaků (kódy):', [...t.slice(0, 6)].map((c) => c.charCodeAt(0)).join(' '));
console.log('prvních 6 znaků (repr):', JSON.stringify(t.slice(0, 6)));

// 2) najdi první řádek s '##' a vypiš jeho kódy
const idx = radky.findIndex((r) => r.startsWith('##'));
const radek = radky[idx];
console.log('řádek', idx + 1, 'kódy znaků:', [...radek.slice(0, 8)].map((c) => c.charCodeAt(0)).join(' '));
console.log('řádek repr:', JSON.stringify(radek.slice(0, 40)));

// 3) testy vzorů
const vzory = {
  '^##\\s*(.*)$': /^##\s*(.*)$/,
  '^##\\s*(.*)': /^##\s*(.*)/,
  '^##\\s*(.+)$': /^##\s*(.+)$/,
  'startsWith ##': null,
};
for (const [nazev, re] of Object.entries(vzory)) {
  if (!re) { console.log(nazev, '->', radek.startsWith('##')); continue; }
  const m = re.exec(radek);
  console.log(nazev, '->', m ? 'MATCH: ' + JSON.stringify(m[1].slice(0, 30)) : 'null');
}

// 4) kolik sekcí najde funkční varianta
let sekce = 0;
for (const r of radky) if (/^##\s*(.+)$/.test(r)) sekce++;
console.log('sekcí (varianta .+):', sekce);
