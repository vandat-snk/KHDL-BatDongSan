"""Build a portable, offline dashboard from public, cleaned listing fields."""
from pathlib import Path
import csv
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from artifact_contract import validate_core_outputs, validate_derivative, register_derivative

def main():
    manifest = validate_core_outputs(ROOT)
    with (ROOT / 'data/processed/listings_clean.csv').open(encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    fields = ['row_id', 'province', 'district', 'property_type', 'transaction_status', 'area_m2',
              'sale_price_vnd', 'price_per_m2_vnd', 'is_outlier_group', 'cluster']
    records = []
    for row in rows:
        record = {k: row.get(k, '') for k in fields}
        for k in ['row_id', 'area_m2', 'sale_price_vnd', 'price_per_m2_vnd', 'cluster']:
            record[k] = float(record[k]) if record[k] not in ('', 'nan', 'None') else None
        record['is_outlier_group'] = str(record['is_outlier_group']).lower() in ('true', '1', '1.0')
        records.append(record)
    payload = json.dumps(records, ensure_ascii=False, separators=(',', ':'), allow_nan=False).replace('<', '\\u003c')
    metadata = {'run_id': manifest['run_id'], 'source_sha256': manifest['source_sha256'],
                'record_count': len(records)}
    meta_json = json.dumps(metadata, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
    template = (ROOT / 'src/dashboard_template.html').read_text(encoding='utf-8')
    try:
        validate_derivative(ROOT, 'workbook', manifest)
        workbook_link = '<a href="DO_AN_BAT_DONG_SAN.xlsx">Mở Excel cùng phiên bản dữ liệu</a>'
    except ValueError:
        workbook_link = '<span>Excel chưa được đối soát với lần chạy này; xem hướng dẫn tạo lại.</span>'
    html = template.replace('__DATA_JSON__', payload).replace('__META_JSON__', meta_json).replace('__WORKBOOK_LINK__', workbook_link)
    extended_path = ROOT / 'outputs/extended/results.json'
    if extended_path.exists():
        extended = json.loads(extended_path.read_text(encoding='utf-8'))
        if extended.get('core_run_id') == manifest['run_id'] and (ROOT / 'outputs/extended/summary.html').exists():
            html = html.replace('</body>', '<p style="padding:16px;text-align:center"><a href="extended/summary.html">Xem kiểm nhãn, so sánh theo nhóm và độ nhạy phân cụm</a></p></body>')
    target = ROOT / 'outputs/DASHBOARD_BAT_DONG_SAN.html'
    target.parent.mkdir(exist_ok=True)
    target.write_text(html, encoding='utf-8')
    register_derivative(ROOT, 'dashboard', target)
    print(f'Dashboard: {len(records)} records; {target.stat().st_size:,} bytes')

if __name__ == '__main__':
    main()
