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
console.log('copied art + fonts from design/mockups-v2');
