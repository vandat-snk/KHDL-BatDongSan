// Execute the actual offline dashboard script in a minimal DOM.
// This checks data/filter/export integration, not browser rendering or native UI.
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const root = path.resolve(import.meta.dirname, '..');
const html = fs.readFileSync(path.join(root, 'outputs/DASHBOARD_BAT_DONG_SAN.html'), 'utf8');
const script = html.match(/<script>([\s\S]+)<\/script>/)[1];
const analysis = JSON.parse(fs.readFileSync(path.join(root, 'outputs/analysis.json'), 'utf8'));
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
assert.equal(elements.get('price').textContent, '2,2');
assert.equal(elements.get('ppm').textContent, '32');
assert.equal(elements.get('area').textContent, '70');
elements.get('outliers').checked = true; evaluate('update()');
check('exclude precomputed group IQR', analysis.counts.clean_count-analysis.counts.group_iqr_outlier_count);
elements.get('reset').onclick();
elements.get('status').value='confirmed'; evaluate('update()');
check('explicit sale titles only', analysis.counts.transaction_status.sale);
elements.get('reset').onclick();
elements.get('province').value='Tp Hồ Chí Minh'; evaluate('update()');
check('HCMC', analysis.province_summary.find(r=>r.province==='Tp Hồ Chí Minh').n);
elements.get('type').value='apartment'; evaluate('update()');
check('HCMC apartments', analysis.province_type_summary.find(r=>r.province==='Tp Hồ Chí Minh' && r.property_type==='apartment').n);
elements.get('province').value='not-an-actual-province'; evaluate('update()');
check('empty selection',0);
assert.equal(elements.get('price').textContent,'—');
assert.ok(elements.get('hist').innerHTML.includes('Không có dữ liệu phù hợp'));
elements.get('reset').onclick();
elements.get('next').onclick();
assert.equal(elements.get('page').textContent,'Trang 2/351');
elements.get('search').value='Hà Nội'; elements.get('search').oninput();
const expectedSearch=evaluate('DATA.filter(d=>(d.province+" "+d.district+" "+typeName(d.property_type)).toLocaleLowerCase("vi").includes("hà nội")).length');
assert.equal(evaluate('tableRows.length'),expectedSearch);
elements.get('download').onclick();
assert.equal(downloaded,'bat_dong_san_da_loc.csv');
const exported = await exportedBlob.text();
assert.equal(exported.split('\r\n').length,expectedSearch+1);
assert.ok(!exported.includes('Đường '), 'No street address in exported clean data');
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
fs.writeFileSync(path.join(out,'validation.json'),JSON.stringify({status:'passed',scope:'Actual JS in minimal DOM; browser rendering unavailable',findings,exported_search_rows:expectedSearch,clustered_rows:clustered},null,2));
console.log(`Dashboard integration checks passed: ${findings.length} filter cases, pagination, empty state, CSV, cluster coverage, links.`);
