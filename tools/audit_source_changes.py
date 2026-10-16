"""Compare the reviewed cleaning policy with a saved previous lineage, not labels."""
from pathlib import Path
import csv
import json
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from pipeline import clean_records
from artifact_contract import read_verified_source

def main():
    records,_=read_verified_source(ROOT/'data/raw/chotot_data.json')
    clean,rejected,lineage,info=clean_records(records)
    previous=ROOT/'tmp/audit_baseline/row_lineage.csv'
    previous_ids=set()
    if previous.exists():
        with previous.open(encoding='utf-8-sig',newline='') as stream:
            previous_ids={int(r['row_id']) for r in csv.DictReader(stream) if r['status']=='kept'}
    review=rejected[rejected.quality_flags.str.contains('source_text_requires_review')].copy()
    columns=['row_id','area_m2','sale_price_vnd','rejection_reasons','source_review_evidence']
    folder=ROOT/'tmp/audit_data';folder.mkdir(parents=True,exist_ok=True)
    review[columns].to_csv(folder/'review_candidates.csv',index=False,encoding='utf-8-sig')
    current=set(clean.row_id)
    summary={'counts':info,'previous_kept_count':len(previous_ids),'newly_quarantined_ids':sorted(previous_ids-current),
             'newly_retained_ids':sorted(current-previous_ids),
             'review_candidates':review[columns].to_dict(orient='records')}
    (folder/'policy_comparison.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
