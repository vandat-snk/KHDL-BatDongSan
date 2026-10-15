"""Build a portable, offline dashboard from public, cleaned listing fields."""
from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parents[1]

def main():
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
    template = (ROOT / 'src/dashboard_template.html').read_text(encoding='utf-8')
    html = template.replace('__DATA_JSON__', payload)
    target = ROOT / 'outputs/DASHBOARD_BAT_DONG_SAN.html'
    target.parent.mkdir(exist_ok=True)
    target.write_text(html, encoding='utf-8')
    print(f'Dashboard: {len(records)} records; {target.stat().st_size:,} bytes')

if __name__ == '__main__':
    main()
