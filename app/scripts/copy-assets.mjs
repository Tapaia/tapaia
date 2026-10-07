// Copies the pixel art and fonts from design/mockups-v2 into public/ (single source of truth for the art).
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const here = path.dirname(fileURLToPath(import.meta.url));
const src = path.resolve(here, '../../design/mockups-v2');
const pub = path.resolve(here, '../public');
for (const d of ['assets', 'fonts']) {
  fs.mkdirSync(path.join(pub, d), { recursive: true });
  for (const f of fs.readdirSync(path.join(src, d))) fs.copyFileSync(path.join(src, d, f), path.join(pub, d, f));
}
// official logo: design/logo/opt4-refined/D-hybrid -> public/brand
const logo = path.resolve(here, '../../design/logo/opt4-refined/D-hybrid');
fs.mkdirSync(path.join(pub, 'brand'), { recursive: true });
for (const f of fs.readdirSync(logo)) fs.copyFileSync(path.join(logo, f), path.join(pub, 'brand', f.replace(/^D-hybrid/, 'logo')));
console.log('copied art + fonts from design/mockups-v2 and the logo from design/logo');
