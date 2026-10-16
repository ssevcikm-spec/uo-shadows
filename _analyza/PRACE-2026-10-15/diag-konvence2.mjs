// Ověření pasti: co je na konci řádku s nadpisem a jak se chová `$`.
import { readFileSync } from 'node:fs';

const t = readFileSync('CONVENTIONS.md', 'utf8');
const radek = t.split('\n').find((r) => r.startsWith('## 1. '));
const znaky = [...radek];
console.log('délka řádku:', znaky.length);
console.log('posledních 5 znaků (kódy):', znaky.slice(-5).map((c) => c.charCodeAt(0)).join(' '));
console.log('obsahuje \\r?', radek.includes('\r'));

const vzory = [
  ['/^##\\s*(.*)$/', /^##\s*(.*)$/],
  ['/^##\\s*([^\\r]*)/', /^##\s*([^\r]*)/],
  ['/^##\\s*([^\\r\\n]*)/', /^##\s*([^\r\n]*)/],
];
for (const [n, re] of vzory) {
  const m = re.exec(radek);
  console.log(n, '->', m ? JSON.stringify(m[1].slice(0, 34)) : 'null');
}
