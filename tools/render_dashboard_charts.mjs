// Visual QA for the actual SVG chart markup; this is not a browser screenshot.
import fs from 'node:fs/promises';
import path from 'node:path';
import sharp from 'sharp';
const folder=path.resolve(import.meta.dirname,'../tmp/qa_dashboard');
for (const name of ['hist','scatter','provinces','boxes']) {
  const svg=await fs.readFile(path.join(folder,name+'.svg'));
  await sharp(svg,{density:150}).flatten({background:'#ffffff'}).png().toFile(path.join(folder,name+'.png'));
}
console.log('Rendered four dashboard chart SVGs.');
