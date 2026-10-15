import fs from 'node:fs/promises';
import path from 'node:path';
import { Workbook, SpreadsheetFile } from '@oai/artifact-tool';

const ROOT = path.resolve(import.meta.dirname, '..');
const OUT = path.join(ROOT, 'outputs');
const QA = path.join(ROOT, 'tmp', 'qa_workbook');
const DATA = path.join(ROOT, 'data', 'processed', 'listings_clean.csv');
await fs.mkdir(OUT, { recursive: true });
await fs.mkdir(QA, { recursive: true });

async function readFirst(candidates) {
  for (const candidate of candidates) {
    try { return { file: candidate, value: JSON.parse(await fs.readFile(path.join(ROOT, candidate), 'utf8')) }; }
    catch (e) { if (e.code !== 'ENOENT') throw e; }
  }
  return { file: null, value: {} };
}
const analysis = await readFirst(['outputs/analysis.json', 'data/processed/analysis.json']);
const audit = { file: analysis.file, value: analysis.value.counts ?? {} };
const metadata = JSON.parse(await fs.readFile(path.join(ROOT, 'data', 'raw', 'mendeley_metadata.json'), 'utf8'));

// The pipeline's JSON preserves numeric/null types and avoids a second CSV parse.
const records = JSON.parse(await fs.readFile(path.join(ROOT,'data','processed','listings_clean.json'),'utf8'));
const names = Object.keys(records[0] ?? {});
const columns = ['row_id','listing_id','province','district','property_type','transaction_status','area_m2','sale_price_vnd','price_per_m2_vnd','price_basis','area_source','quality_flags','is_outlier_global','is_outlier_group','iqr_group','cluster'];
for (const key of columns) if (!names.includes(key)) throw new Error(`Missing required column ${key}`);
const numeric = new Set(['row_id', 'area_m2', 'sale_price_vnd', 'price_per_m2_vnd', 'cluster']);
const bools = new Set(['is_outlier_global','is_outlier_group']);
const rows = records.map(record => columns.map(key => {
  const value = record[key];
  if (value === null || value === undefined || value === '') return null;
  if (bools.has(key)) return ['true','1','yes'].includes(String(value).toLowerCase()) ? 1 : 0;
  if (numeric.has(key)) { const n = Number(value); if (!Number.isFinite(n)) throw new Error(`Non-numeric ${key}: ${value}`); return n; }
  return String(value);
}));
const n = rows.length;
if (!n) throw new Error('Empty clean dataset');
const first = 10;
const last = first + n - 1;
const prices = rows.map(r => r[7]).filter(v => typeof v === 'number');
const areas = rows.map(r => r[6]).filter(v => typeof v === 'number');
const priceAreas = rows.map(r => r[8]).filter(v => typeof v === 'number');
const mean = a => a.reduce((s,v)=>s+v,0)/a.length;
const median = a => { const v=[...a].sort((a,b)=>a-b); const m=Math.floor(v.length/2); return v.length%2?v[m]:(v[m-1]+v[m])/2; };
const provinces = [...new Set(rows.map(r => r[2]))].filter(Boolean).sort((a,b)=>rows.filter(r=>r[2]===b).length-rows.filter(r=>r[2]===a).length);
const wb = Workbook.create();
const dash = wb.worksheets.add('Dashboard');
const data = wb.worksheets.add('Du lieu');
const quality = wb.worksheets.add('Chat luong');
const C = {ink:'#183247', blue:'#214E70', teal:'#297A86', light:'#EEF4F7', gray:'#637582', orange:'#BE6A21', rule:'#C6D4DE'};
const base = (sheet, range) => { sheet.showGridLines=false; sheet.getRange(range).format.font={name:'Arial',size:10,color:C.ink}; sheet.getRange(range).format.verticalAlignment='center'; };
const title = (sheet, text, end='N') => { sheet.getRange('A2').values=[[text]]; sheet.getRange('A2').format.font={name:'Arial',size:16,bold:true,color:C.ink}; sheet.getRange(`A3:${end}3`).format.borders={bottom:{style:'thin',color:C.rule}}; };
const header = (sheet, range) => { sheet.getRange(range).format={fill:C.blue,font:{name:'Arial',size:10,bold:true,color:'#FFFFFF'},horizontalAlignment:'center',verticalAlignment:'center',wrapText:true}; sheet.getRange(range).format.rowHeight=32; };
const note = (sheet, cell, text) => { sheet.getRange(cell).values=[[text]]; sheet.getRange(cell).format.font={name:'Arial',size:10,italic:true,color:C.gray}; };
const ref = col => `'Du lieu'!$${col}$${first}:$${col}$${last}`;

base(data, `A1:R${last}`);
title(data,'Dữ liệu tin rao bất động sản đã xử lý','R');
data.getRange('A4').values=[['Nguồn: Tran, Nguyen & Ha (2021). Vietnam Real Estate Data, v2. Mendeley Data. CC BY 4.0.']];
data.getRange('A5').values=[['https://doi.org/10.17632/5477zhnmn2.2']];
note(data,'A6','Dữ liệu lịch sử được công bố 12/01/2021. Một dòng là một tin rao sau xử lý; không phải giá giao dịch hay thị trường hiện tại.');
note(data,'A7','Loại hình suy luận từ tiêu đề. Nhãn địa phương trích từ địa chỉ lịch sử. Không có ngày đăng hoặc tọa độ để phân tích thời gian/bản đồ.');
note(data,'A8','Q và R là công thức đổi đơn vị từ H và I. H/I trống nghĩa là không đủ điều kiện phân tích giá; không coi là giá bằng 0.');
const headers = ['Dòng nguồn','Mã nội dung','Tỉnh/Thành','Quận/Huyện','Loại suy luận','Trạng thái','Diện tích (m²)','Giá rao (VND)','Giá rao/m² (VND)','Cơ sở giá','Nguồn diện tích','Cờ chất lượng','Ngoại lệ toàn bộ','Ngoại lệ nhóm','Nhóm IQR','Cụm K-means','Giá rao (tỷ VND)','Giá rao/m² (triệu VND)'];
data.getRange('A9:R9').values=[headers];
data.getRange(`A${first}:P${last}`).values=rows;
data.getRange(`Q${first}:R${first}`).formulas=[[`=IF(H${first}="","",H${first}/1000000000)`,`=IF(I${first}="","",I${first}/1000000)`]];
data.getRange(`Q${first}:R${last}`).fillDown();
const table=data.tables.add(`A9:R${last}`,true,'ListingsClean');
table.showFilterButton=true;
header(data,'A9:R9');
data.getRange(`A${first}:A${last}`).setNumberFormat('0');
data.getRange(`G${first}:G${last}`).setNumberFormat('#,##0.0');
data.getRange(`H${first}:I${last}`).setNumberFormat('#,##0');
data.getRange(`M${first}:N${last}`).setNumberFormat('0');
data.getRange(`P${first}:P${last}`).setNumberFormat('0');
data.getRange(`Q${first}:R${last}`).setNumberFormat('#,##0.00');
data.getRange(`A9:R${last}`).format.rowHeight=21;
data.getRange('A9:R9').format.rowHeight=38;
for (const [col,width] of Object.entries({A:11,B:25,C:19,D:22,E:20,F:19,G:18,H:20,I:22,J:20,K:19,L:48,M:17,N:17,O:32,P:17,Q:21,R:25})) data.getRange(`${col}9:${col}${last}`).format.columnWidth=width;
data.getRange(`M${first}:N${last}`).conditionalFormats.add('cellIs',{operator:'equal',formula:1,format:{fill:'#FFF0DD',font:{color:'#A25718'}}});
data.freezePanes.freezeRows(9);
data.freezePanes.freezeColumns(2);

base(dash,'A1:O95');
dash.tabColor=C.blue;
dash.getRange('A1:O95').format.columnWidth=12;
dash.getRange('A1:O95').format.rowHeight=22;
title(dash,'Khám phá giá rao bất động sản','O');
note(dash,'A4','Mẫu tin rao lịch sử Việt Nam. Các thống kê giá dùng những tin có giá bán và diện tích đủ điều kiện.');
dash.getRange('A6:C6').values=[['Chỉ tiêu','Giá trị','Đơn vị']]; header(dash,'A6:C6');
const metrics=[
 ['Tin sau xử lý',`=COUNTA(${ref('B')})`,'tin'],
 ['Tin đủ giá',`=COUNT(${ref('H')})`,'tin'],
 ['Giá trung vị',`=MEDIAN(${ref('Q')})`,'tỷ VND'],
 ['Giá trung bình',`=AVERAGE(${ref('Q')})`,'tỷ VND'],
 ['Diện tích trung vị',`=MEDIAN(${ref('G')})`,'m²'],
 ['Giá/m² trung vị',`=MEDIAN(${ref('R')})`,'triệu VND/m²'],
];
dash.getRange('A7:A12').values=metrics.map(x=>[x[0]]); dash.getRange('B7:B12').formulas=metrics.map(x=>[x[1]]); dash.getRange('C7:C12').values=metrics.map(x=>[x[2]]);
dash.getRange('A6:A12').format.columnWidth=24; dash.getRange('B7:B8').setNumberFormat('#,##0'); dash.getRange('B9:B12').setNumberFormat('#,##0.00');
dash.getRange('B7:B12').format.font={name:'Arial',size:12,bold:true,color:C.blue};
dash.getRange('E6').values=[['Cách đọc kết quả']]; dash.getRange('E6').format.font={name:'Arial',size:12,bold:true,color:C.ink};
note(dash,'E8','Trung vị giảm ảnh hưởng của giá rao rất cao. Giá trung bình có thể bị ngoại lệ chi phối.');
note(dash,'E9','So sánh địa phương kèm số tin. Mẫu phân bố không đều, không đại diện toàn thị trường.');
note(dash,'E10','Giá/m² = giá rao toàn bộ / diện tích lấy từ trường lõi của tin.');
note(dash,'E11','Công thức và biểu đồ cập nhật khi sửa dữ liệu trong phạm vi hiện có. Thêm dòng mới: chạy lại quy trình.');

// Summary tables own business calculations and are independent from the audit tab.
dash.getRange('A51:D51').values=[['Tỉnh/Thành','Số tin','Số tin đủ giá','Giá TB (tỷ VND)']]; header(dash,'A51:D51');
const pFirst=52,pLast=pFirst+provinces.length-1;
dash.getRange(`A${pFirst}:A${pLast}`).values=provinces.map(p=>[p]);
dash.getRange(`B${pFirst}:D${pLast}`).formulas=provinces.map((p,i)=>{const r=pFirst+i;return [
 `=COUNTIFS(${ref('C')},A${r})`,
 `=COUNTIFS(${ref('C')},A${r},${ref('H')},">0")`,
 `=IF(C${r}=0,"",AVERAGEIFS(${ref('Q')},${ref('C')},A${r},${ref('H')},">0"))`
];});
dash.getRange(`B${pFirst}:C${pLast}`).setNumberFormat('#,##0'); dash.getRange(`D${pFirst}:D${pLast}`).setNumberFormat('0.00');
note(dash,`A${pLast+2}`,'Bảng theo địa phương được xếp theo số tin của lần chạy này. Cột giá là trung bình, không phải trung vị.');
dash.getRange('I51:L51').values=[['Cận dưới (tỷ)','Cận trên (tỷ)','Nhóm giá','Số tin']]; header(dash,'I51:L51');
const bounds=[0,2,4,6,8,10,12,14,16,18,20];
for(let i=0;i<bounds.length;i++){
 const r=52+i; const lo=bounds[i], hi=i===bounds.length-1?null:bounds[i+1];
 dash.getRange(`I${r}:K${r}`).values=[[lo,hi,hi===null?'Từ 20 trở lên':`${lo} đến dưới ${hi}`]];
 dash.getRange(`L${r}`).formulas=[[hi===null?`=COUNTIFS(${ref('Q')},">="&I${r},${ref('H')},">0")`:`=COUNTIFS(${ref('Q')},">="&I${r},${ref('Q')},"<"&J${r},${ref('H')},">0")`]];
}
dash.getRange('I52:J62').setNumberFormat('0'); dash.getRange('L52:L62').setNumberFormat('#,##0');
note(dash,'I64','Mười nhóm đầu rộng 2 tỷ VND. Nhóm cuối gộp toàn bộ giá từ 20 tỷ trở lên.');

// Deterministic reservoir sample for legible native scatter; all summary metrics use full data.
let seed=42; const rand=()=>{seed=(Math.imul(1664525,seed)+1013904223)>>>0;return seed/4294967296;};
const eligible=rows.map((r,i)=>({r,i})).filter(x=>x.r[6]>0&&x.r[7]>0);
const cap=Math.min(600,eligible.length);const sampled=eligible.slice(0,cap);
for(let i=cap;i<eligible.length;i++){const j=Math.floor(rand()*(i+1));if(j<cap)sampled[j]=eligible[i];}
const sFirst=Math.max(100,pLast+6),sLast=sFirst+sampled.length-1;
dash.getRange(`A${sFirst-2}`).values=[[`Mẫu scatter ngẫu nhiên có thể lặp lại: ${cap}/${eligible.length} tin, seed 42. Biến đổi log10 để thấy cả giá trị lớn.`]];
dash.getRange(`A${sFirst-1}:C${sFirst-1}`).values=[['log10(diện tích m²)','log10(giá tỷ VND)','Dòng dữ liệu']];header(dash,`A${sFirst-1}:C${sFirst-1}`);
dash.getRange(`A${sFirst}:C${sLast}`).formulas=sampled.map(x=>{const r=first+x.i;return [`=LOG10('Du lieu'!G${r})`,`=LOG10('Du lieu'!Q${r})`,`='Du lieu'!A${r}`];});
dash.getRange(`A${sFirst}:B${sLast}`).setNumberFormat('0.00');
note(dash,'A49',`Scatter dùng ${cap}/${eligible.length} tin chọn ngẫu nhiên, seed 42. Hai trục log10; mỗi 1 đơn vị tương ứng gấp 10 lần giá trị gốc.`);

function styleChart(chart,titleText,start,end,xTitle,yTitle,scatter=false){
 chart.title=titleText;chart.titleTextStyle.typeface='Arial';chart.titleTextStyle.fontSize=14;chart.hasLegend=false;
 chart.setPosition(start,end);
 chart.xAxis={axisType:scatter?'valueAxis':'textAxis',textStyle:{typeface:'Arial',fontSize:11}};
 chart.yAxis={numberFormatCode:scatter?'0.0':'0.0',numberFormatSourceLinked:false,textStyle:{typeface:'Arial',fontSize:11}};
 chart.xAxis.title.text=xTitle;chart.yAxis.title.text=yTitle;
 chart.series.items.forEach(s=>s.fill=C.teal);
}
const hist=dash.charts.add('bar',[dash.getRange('K51:K62'),dash.getRange('L51:L62')]);
styleChart(hist,'Phân bố giá rao theo nhóm','A14','G29','Nhóm giá (tỷ VND)','Số tin');
hist.yAxis.numberFormatCode='#,##0';
const top=Math.min(8,provinces.length),topLast=pFirst+top-1;
const priceChart=dash.charts.add('bar',[dash.getRange(`A51:A${topLast}`),dash.getRange(`D51:D${topLast}`)]);
styleChart(priceChart,'Giá rao trung bình tại 8 nơi nhiều tin nhất','I14','O29','Địa phương','Giá rao (tỷ VND)');
const scatter=dash.charts.add('scatter',[dash.getRange(`A${sFirst-1}:A${sLast}`),dash.getRange(`B${sFirst-1}:B${sLast}`)]);
styleChart(scatter,'Diện tích và giá rao theo thang log10','A32','G47','log10(diện tích m²)','log10(giá tỷ VND)',true);
const coverage=dash.charts.add('bar',[dash.getRange(`A51:A${topLast}`),dash.getRange(`B51:B${topLast}`)]);
styleChart(coverage,'Độ phủ dữ liệu tại 8 nơi nhiều tin nhất','I32','O47','Địa phương','Số tin');coverage.yAxis.numberFormatCode='#,##0';

base(quality,'A1:H100');quality.getRange('A1:H100').format.columnWidth=16;quality.getRange('A1:H100').format.rowHeight=23;
title(quality,'Kiểm tra chất lượng dữ liệu','H');
note(quality,'A4','Bản ghi kiểm toán từ lần chạy pipeline. Các mục có thể chồng nhau; không cộng cơ học thành số dòng bị loại.');
quality.getRange('A6:C6').values=[['Đối chiếu từ dữ liệu Excel','Giá trị','Đơn vị']];header(quality,'A6:C6');
const qRows=[
 ['Số tin sau xử lý',`=COUNTA(${ref('B')})`,'tin'],
 ['Giá rao để trống',`=COUNTBLANK(${ref('H')})`,'tin'],
 ['Cờ ngoại lệ toàn bộ',`=COUNTIFS(${ref('M')},1)`,'tin'],
 ['Cờ ngoại lệ theo nhóm',`=COUNTIFS(${ref('N')},1)`,'tin'],
 ['Tổng bin giá trừ số tin đủ giá',"=SUM('Dashboard'!L52:L62)-'Dashboard'!B8",'tin'],
];
quality.getRange('A7:A11').values=qRows.map(x=>[x[0]]);quality.getRange('B7:B11').formulas=qRows.map(x=>[x[1]]);quality.getRange('C7:C11').values=qRows.map(x=>[x[2]]);
quality.getRange('A6:A11').format.columnWidth=44;quality.getRange('B7:B11').setNumberFormat('#,##0');
quality.getRange('B11').conditionalFormats.add('cellIs',{operator:'notEqual',formula:0,format:{fill:'#FDE8E6',font:{color:'#A72828',bold:true}}});
quality.getRange('A14').values=[['Kết quả pipeline (snapshot; chạy lại pipeline để làm mới)']];quality.getRange('A14').format.font={name:'Arial',size:12,bold:true,color:C.ink};
quality.getRange('A16:B16').values=[['Mục kiểm toán','Giá trị ghi nhận']];header(quality,'A16:B16');
function flatten(value,prefix=''){
 const out=[];
 for(const [key,v]of Object.entries(value??{})){
  const k=prefix?`${prefix}.${key}`:key;
  if(v&&typeof v==='object'&&!Array.isArray(v))out.push(...flatten(v,k));
  else if(Array.isArray(v))out.push([k,JSON.stringify(v)]);
  else out.push([k,v]);
 }
 return out;
}
const auditLabels={raw_count:'Tin gốc',clean_count:'Tin đủ điều kiện sau xử lý',rejected_count:'Tin cách ly',duplicate_count:'Tin trùng theo khóa nội dung',unique_core_count:'Tổ hợp nội dung không trùng',area_recovered_count:'Diện tích khôi phục từ chuỗi giá',group_iqr_outlier_count:'Ngoại lệ IQR theo nhóm',global_iqr_outlier_count:'Ngoại lệ IQR toàn bộ',province_count:'Nhãn địa phương trích xuất',property_type_inferred_from_title:'Loại hình suy luận từ tiêu đề',transaction_assumed_sale_from_dataset_context:'Giả định bán theo ngữ cảnh bộ dữ liệu',unknown_property_type:'Chưa xác định loại hình',area_recovered_from_price_text:'Khôi phục diện tích từ chuỗi giá',dot_thousands_convention:'Diện tích: dùng dấu chấm hàng nghìn',rental_income_mentioned:'Có nhắc thu nhập cho thuê',quarantine_total_price_below_10m_vnd:'Giá toàn bộ dưới 10 triệu VND',exclude_rental_or_mixed_transaction:'Tin cho thuê hoặc lẫn bán/thuê',payment_not_confirmed_total_price:'Khoản thanh toán chưa rõ tổng giá',invalid_or_missing_area:'Diện tích thiếu hoặc không hợp lệ',sale_assumed:'Giả định tin bán',sale:'Tin bán',sale_with_rental_income:'Tin bán có nhắc thu nhập thuê'};
function auditLabel(k){const bits=k.split('.');const last=bits.at(-1);if(bits[0]==='raw_missing_fields')return `Thiếu trường gốc: ${last}`;if(bits[0]==='unparseable_unique_core_fields_before_rejection')return `Không phân tích được trước cách ly: ${last}`;return (bits[0]==='quality_flags'?'Cờ: ':bits[0]==='rejection_reasons'?'Lý do cách ly: ':bits[0]==='transaction_status'?'Trạng thái: ':'')+(auditLabels[last]??last);}
const auditFlat=flatten(audit.value).map(([k,v])=>[auditLabel(k),v]);
if(auditFlat.length)quality.getRange(`A17:B${16+auditFlat.length}`).values=auditFlat;
else quality.getRange('A17:B17').values=[['Chưa tìm thấy file audit','Xem log pipeline và bảng kiểm tra Excel ở trên']];
quality.getRange('A16:A100').format.columnWidth=53;
quality.getRange(`A17:A${16+auditFlat.length}`).format.wrapText=true;
quality.getRange(`A17:B${16+auditFlat.length}`).format.rowHeight=32;
quality.getRange('B16:B100').format.columnWidth=24;
quality.getRange('D16').values=[['Đọc đúng dữ liệu']];quality.getRange('D16').format.font={name:'Arial',size:12,bold:true,color:C.ink};
note(quality,'D18','Cờ ngoại lệ không tự động chứng minh dữ liệu sai.');
note(quality,'D20','Tin cho thuê/giá mơ hồ không được dùng như giá bán.');
note(quality,'D22','Không điền giá rao thiếu để làm đẹp phân phối.');
note(quality,'D24','Các cột chi tiết nghi lan truyền không dùng trong kết luận chính.');
note(quality,'D26','land = đất; house = nhà; apartment = căn hộ.');
note(quality,'D28','other_unknown = loại hình chưa xác định; cụm -1 = ngoại lệ theo nhóm.');
quality.freezePanes.freezeRows(16);

// Verify live recalculation by perturbing and restoring one eligible source price.
const probe=eligible[0],probeRow=first+probe.i,original=probe.r[7];
const beforeMean=dash.getRange('B10').values[0][0];
data.getRange(`H${probeRow}`).values=[[original+1000000000]];
wb.recalculate();
const changed=dash.getRange('B10').values[0][0];
const conversionChanged=data.getRange(`Q${probeRow}`).values[0][0];
if(Math.abs((changed-beforeMean)-1/prices.length)>1e-7||Math.abs(conversionChanged-(original/1e9+1))>1e-7)throw new Error('Formula perturbation failed');
data.getRange(`H${probeRow}`).values=[[original]];
wb.recalculate();
const expected=[n,prices.length,median(prices)/1e9,mean(prices)/1e9,median(areas),median(priceAreas)/1e6];
const actual=dash.getRange('B7:B12').values.map(x=>x[0]);
expected.forEach((v,i)=>{if(Math.abs(actual[i]-v)>Math.max(1e-6,Math.abs(v)*1e-9))throw new Error(`Metric mismatch ${i}: ${actual[i]} versus ${v}`);});
const a=analysis.value.overall;
const analysisExpected=[analysis.value.counts.clean_count,analysis.value.counts.clean_count,a.median_price_vnd/1e9,a.mean_price_vnd/1e9,a.median_area_m2,a.median_price_per_m2_vnd/1e6];
analysisExpected.forEach((v,i)=>{if(Math.abs(actual[i]-v)>Math.max(1e-6,Math.abs(v)*1e-9))throw new Error(`analysis.json mismatch ${i}`);});
const formulaErrors=await wb.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A|#NUM!|#NULL!|#SPILL!|#CALC!',options:{useRegex:true,maxResults:40},summary:'Final formula error scan',maxChars:6000});
const detail=await wb.inspect({kind:'table',range:'Dashboard!A6:D12',include:'values,formulas',tableMaxRows:10,tableMaxCols:4,maxChars:5000});
await fs.writeFile(path.join(QA,'formula_scan.ndjson'),formulaErrors.ndjson);
await fs.writeFile(path.join(QA,'metrics.ndjson'),detail.ndjson);
for(const [sheet,range,file]of [['Dashboard','A1:O49','dashboard.png'],['Du lieu','A1:I23','data.png'],['Chat luong','A1:H32','quality.png']]){
 const preview=await wb.render({sheetName:sheet,range,scale:1.5,format:'png'});
 await fs.writeFile(path.join(QA,file),new Uint8Array(await preview.arrayBuffer()));
}
const output=await SpreadsheetFile.exportXlsx(wb);await output.save(path.join(OUT,'DO_AN_BAT_DONG_SAN.xlsx'));
const validation={row_count:n,price_count:prices.length,metrics_expected:expected,metrics_analysis:analysisExpected,metrics_actual:actual,live_perturbation_pass:true,analysis_reconciliation_pass:true,chart_count:dash.charts.items.length,source_doi:metadata.doi,audit_file:audit.file,analysis_file:analysis.file,analysis_top_level_keys:Object.keys(analysis.value),formula_error_scan:formulaErrors.ndjson,source_ranges:{rows:[first,last],scatter:[sFirst,sLast]},built_at:'2026-10-15'};
await fs.writeFile(path.join(QA,'validation.json'),JSON.stringify(validation,null,2));
console.log(JSON.stringify({output:path.join(OUT,'DO_AN_BAT_DONG_SAN.xlsx'),rows:n,charts:dash.charts.items.length,metrics:actual,audit:audit.file,qa:QA}));
