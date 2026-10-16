// Execute the actual offline dashboard script in a minimal DOM.
// This checks data/filter/export integration, not browser rendering or native UI.
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
const root = path.resolve(import.meta.dirname, '..');
const html = fs.readFileSync(path.join(root, 'outputs/DASHBOARD_BAT_DONG_SAN.html'), 'utf8');
const script = html.match(/<script>([\s\S]+)<\/script>/)[1];
const analysis = JSON.parse(fs.readFileSync(path.join(root, 'outputs/analysis.json'), 'utf8'));
const manifest = JSON.parse(fs.readFileSync(path.join(root, 'outputs/run_manifest.json'), 'utf8'));
const cleaned = JSON.parse(fs.readFileSync(path.join(root, 'data/processed/listings_clean.json'), 'utf8'));
const build = JSON.parse(fs.readFileSync(path.join(root, 'outputs/dashboard_build.json'), 'utf8'));
assert.equal(build.core_run_id, manifest.run_id, 'Dashboard must use the current core run');
assert.equal(build.sha256, createHash('sha256').update(html).digest('hex'), 'Dashboard content must match build evidence');
const elements = new Map([...html.matchAll(/\bid="([^"]+)"/g)].map(m => [m[1], {
  value: '', checked: false, textContent: '', innerHTML: '', disabled: false,
  options: [], handlers: {}, add(o) { this.options.push(o); },
  addEventListener(event, handler) { this.handlers[event] = handler; }
}]));
let exportedBlob = null, downloaded = null;
const context = vm.createContext({
  Intl, Blob, console, setTimeout: callback => callback(),
  Option: function(text, value) { this.text = text; this.value = value; },
  URL: { createObjectURL(blob) { exportedBlob = blob; return 'blob:validation'; }, revokeObjectURL() {} },
  document: { getElementById(id) { assert.ok(elements.has(id), `Unknown element ${id}`); return elements.get(id); },
    createElement() { return {click() { downloaded = this.download; }}; } }
});
vm.runInContext(script, context, {timeout: 10000});
const evaluate = code => vm.runInContext(code, context, {timeout: 10000});
const count = () => evaluate('filtered.length');
const findings = [];
function check(label, expected) {
  assert.equal(count(), expected, label);
  assert.equal(evaluate('tableRows.length'), expected, `${label}: table uses same rows`);
  for (const id of ['hist', 'scatter', 'provinces', 'boxes']) {
    assert.ok(!/(?:cx|cy|x|y|width|height)="(?:NaN|Infinity)/.test(elements.get(id).innerHTML), `${label}: invalid SVG ${id}`);
  }
  findings.push({label, count: expected});
}
check('baseline', analysis.counts.clean_count);
assert.equal(elements.get('price').textContent, evaluate(`fmt(${analysis.overall.median_price_vnd}/1e9,3)`));
assert.equal(elements.get('ppm').textContent, evaluate(`fmt(${analysis.overall.median_price_per_m2_vnd}/1e6)`));
assert.equal(elements.get('area').textContent, evaluate(`fmt(${analysis.overall.median_area_m2})`));
assert.equal(evaluate('META.run_id'), manifest.run_id);
assert.equal(evaluate('META.source_sha256'), manifest.source_sha256);
assert.equal(evaluate('DATA.length'), cleaned.length);
const byId = new Map(cleaned.map(d=>[d.row_id,d]));
for (const record of evaluate('DATA')) {
  const expected = byId.get(record.row_id);
  assert.ok(expected, `Missing source row ${record.row_id}`);
  for (const key of Object.keys(record)) assert.equal(record[key], expected[key], `Row ${record.row_id}, ${key}`);
}
assert.ok(!html.includes('aria-label="Histogram'), 'Unequal intervals are categorical counts');
elements.get('outliers').checked = true; evaluate('update()');
check('exclude precomputed group IQR', analysis.counts.clean_count-analysis.counts.group_iqr_outlier_count);
elements.get('reset').onclick();
elements.get('status').value='confirmed'; evaluate('update()');
check('explicit sale titles only', analysis.counts.transaction_status.sale || 0);
elements.get('reset').onclick();
elements.get('province').value='Tp Hồ Chí Minh'; evaluate('update()');
check('HCMC', analysis.province_summary.find(r=>r.province==='Tp Hồ Chí Minh').n);
elements.get('type').value='apartment'; evaluate('update()');
check('HCMC apartments', analysis.province_type_summary.find(r=>r.province==='Tp Hồ Chí Minh' && r.property_type==='apartment')?.n || 0);
elements.get('province').value='not-an-actual-province'; evaluate('update()');
check('empty selection',0);
assert.equal(elements.get('price').textContent,'—');
assert.ok(elements.get('hist').innerHTML.includes('Không có dữ liệu phù hợp'));
assert.ok(elements.get('scatter-note').textContent.includes('Không có dữ liệu phù hợp'));
elements.get('reset').onclick();
elements.get('next').onclick();
assert.equal(elements.get('page').textContent,`Trang 2/${Math.ceil(cleaned.length/20)}`);
const originalMetric = elements.get('n').textContent;
elements.get('search').value='Hà Nội'; elements.get('search').oninput();
const expectedSearch=evaluate('DATA.filter(d=>(d.province+" "+d.district+" "+typeName(d.property_type)).toLocaleLowerCase("vi").includes("hà nội")).length');
assert.equal(evaluate('tableRows.length'),expectedSearch);
assert.equal(elements.get('n').textContent,originalMetric, 'Search affects only table and CSV');
elements.get('download').onclick();
assert.equal(downloaded,'bat_dong_san_da_loc.csv');
const exported = await exportedBlob.text();
assert.equal(exported.split('\r\n').length,expectedSearch+1);
assert.ok(!exported.includes('Đường '), 'No street address in exported clean data');
assert.equal(evaluate('csvCell(-1)'), '"-1"', 'Negative numeric cluster labels stay numeric in CSV');
for (const text of ['=SUM(1,2)', '+SUM(1,2)', '-1+2', '@SUM(1,2)', ' =SUM(1,2)', '\t=SUM(1,2)']) {
  const result=evaluate(`csvCell(${JSON.stringify(text)})`);
  assert.equal(result[1], "'", `Escape formula text ${JSON.stringify(text)}`);
}
const sampleIds = evaluate('JSON.stringify(reservoirSample(DATA,1800,42).map(d=>d.row_id))');
assert.equal(sampleIds,evaluate('JSON.stringify(reservoirSample(DATA,1800,42).map(d=>d.row_id))'), 'Scatter repeats for a fixed seed');
assert.equal(JSON.parse(sampleIds).length, Math.min(1800,cleaned.length));
assert.equal(new Set(JSON.parse(sampleIds)).size, JSON.parse(sampleIds).length);
if (cleaned.length>1800) {
  assert.notEqual(sampleIds,evaluate('JSON.stringify(DATA.slice(0,1800).map(d=>d.row_id))'), 'Avoid selecting only source prefix');
  assert.notEqual(sampleIds,evaluate('JSON.stringify(reservoirSample(DATA,1800,43).map(d=>d.row_id))'), 'Seed must affect sample');
}
elements.get('reset').onclick();
const clustered=evaluate('DATA.filter(d=>d.cluster>0).length');
assert.equal(clustered,analysis.clustering.fit_count);
assert.ok(!elements.get('clusters').innerHTML.includes('Cụm -1'));
for (const match of html.matchAll(/href="(?!https?:)([^"#]+)"/g)) {
  assert.ok(fs.existsSync(path.resolve(root, 'outputs', match[1])), `Missing artifact link ${match[1]}`);
}
const out=path.join(root,'tmp/qa_dashboard'); fs.mkdirSync(out,{recursive:true});
for (const id of ['hist','scatter','provinces','boxes']) {
  const height=['provinces','boxes'].includes(id)?350:320;
  const svg=`<svg xmlns="http://www.w3.org/2000/svg" width="580" height="${height}" viewBox="0 0 580 ${height}"><style>text{font-family:Arial;fill:#526779;font-size:11px}.gridline{stroke:#e7eef3}.empty{font-size:17px;text-anchor:middle}</style>${elements.get(id).innerHTML}</svg>`;
  fs.writeFileSync(path.join(out,id+'.svg'),svg);
}
const evidence={status:'passed',core_run_id:manifest.run_id,
  test_file_sha256:createHash('sha256').update(fs.readFileSync(import.meta.filename)).digest('hex'),
  dashboard_sha256:build.sha256,scope:'Actual JS in minimal DOM; does not validate browser layout',
  findings,exported_search_rows:expectedSearch,clustered_rows:clustered};
fs.writeFileSync(path.join(out,'validation.json'),JSON.stringify(evidence,null,2));
fs.writeFileSync(path.join(root,'outputs/dashboard_test_results.json'),JSON.stringify(evidence,null,2));
console.log(`Dashboard integration checks passed: ${findings.length} filter cases, pagination, empty state, CSV, cluster coverage, links.`);
