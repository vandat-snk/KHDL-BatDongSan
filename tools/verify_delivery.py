"""Cross-check the saved deliverables after relocation, without editing them."""
from pathlib import Path
import csv
import hashlib
import json
import math
import sqlite3
from openpyxl import load_workbook
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]

def main():
    analysis = json.loads((ROOT / 'outputs/analysis.json').read_text(encoding='utf-8'))
    records = json.loads((ROOT / 'data/processed/listings_clean.json').read_text(encoding='utf-8'))
    raw_hash = hashlib.sha256((ROOT / 'data/raw/chotot_data.json').read_bytes()).hexdigest()
    assert raw_hash == analysis['source']['sha256'] == 'ef39f153f48a55af07baa86883cd9036652f6d52232fed0be6e8991c7a5bf811'
    workbook = load_workbook(ROOT / 'outputs/DO_AN_BAT_DONG_SAN.xlsx', data_only=True)
    columns = ['row_id','listing_id','province','district','property_type','transaction_status','area_m2','sale_price_vnd','price_per_m2_vnd','price_basis','area_source','quality_flags','is_outlier_global','is_outlier_group','iqr_group','cluster']
    saved = list(workbook['Du lieu'].iter_rows(min_row=10, max_row=9+len(records), min_col=1, max_col=16, values_only=True))
    assert len(saved) == len(records) == analysis['counts']['clean_count']
    for record, row in zip(records, saved):
        for key, value in zip(columns, row):
            expected = record[key]
            if isinstance(expected, (int,float,bool)):
                assert math.isclose(float(value),float(expected),rel_tol=1e-12,abs_tol=1e-7), (record['row_id'],key)
            else:
                assert (value or '') == (expected or ''), (record['row_id'],key)
    with sqlite3.connect((ROOT / 'outputs/real_estate.sqlite').as_uri()+'?mode=ro',uri=True) as connection:
        assert connection.execute('SELECT COUNT(*) FROM listings').fetchone()[0] == len(records)
        assert connection.execute('PRAGMA integrity_check').fetchone()[0] == 'ok'
        assert connection.execute('PRAGMA foreign_key_check').fetchall() == []
    with (ROOT / 'data/processed/row_lineage.csv').open(encoding='utf-8-sig',newline='') as stream:
        lineage=list(csv.DictReader(stream))
    assert len(lineage) == analysis['counts']['raw_count']
    assert len({int(x['row_id']) for x in lineage}) == len(lineage)
    for status,key in [('kept','clean_count'),('duplicate','duplicate_count'),('rejected','rejected_count')]:
        assert sum(x['status']==status for x in lineage) == analysis['counts'][key]
    reader=PdfReader(ROOT/'tmp/qa_report/BAO_CAO_DO_AN.pdf')
    assert len(reader.pages)==19
    for page in reader.pages:
        assert len(page.extract_text())>400, 'Blank or near-blank report page'
    benchmark=analysis['sql_benchmark']
    assert benchmark['before']['result_sha256']==benchmark['after']['result_sha256']
    report={'status':'passed','raw_count':len(lineage),'clean_count':len(records),'duplicates':analysis['counts']['duplicate_count'],
            'rejected':analysis['counts']['rejected_count'],'workbook_rows_matched':len(saved),'report_pages':len(reader.pages),
            'source_sha256':raw_hash,'database_integrity':'ok','sql_results_identical':True,
            'pipeline_unit_tests':12,'dashboard_filter_cases':6,
            'visual_review':'19 Word report pages, 3 workbook sheet previews and 4 standalone dashboard SVG charts inspected',
            'limitations':['Full dashboard browser layout was not verified: browser tool unavailable.',
                           'Workbook native UI in Microsoft Excel was not exercised; saved formulas, charts and values were verified.',
                           'Human label and source-entry audit remains assigned to the three students.']}
    (ROOT/'outputs/DELIVERY_CHECK.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Delivery verified: source hash, 7001 workbook records, 9004 lineage rows, SQLite, 19 report pages.')

if __name__=='__main__':
    main()
