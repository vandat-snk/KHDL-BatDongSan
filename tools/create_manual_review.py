"""Create an unlabelled, stratified review worksheet; never fabricate human labels."""
from pathlib import Path
import csv
import json
import sys
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from artifact_contract import validate_core_outputs


def main():
    manifest=validate_core_outputs(ROOT)
    clean=pd.read_csv(ROOT/'data/processed/listings_clean.csv',keep_default_na=False)
    rejected=pd.read_csv(ROOT/'data/processed/listings_rejected.csv',keep_default_na=False)
    groups={
        'retained_explicit_sale':clean[clean.transaction_status.eq('sale')],
        'retained_assumed_sale':clean[clean.transaction_status.eq('sale_assumed')],
        'retained_unknown_type':clean[clean.property_type.eq('other_unknown')],
        'retained_numeric_uncertainty':clean[clean.quality_flags.str.contains('dot_thousands|source_dimension')],
        'quarantined_source_conflict':rejected[rejected.quality_flags.str.contains('source_text_requires_review')],
        'quarantined_other':rejected[~rejected.quality_flags.str.contains('source_text_requires_review')],
    }
    rng=np.random.default_rng(42);seen=set();rows=[]
    for group,frame in groups.items():
        pool=frame[~frame.row_id.isin(seen)]
        selected=pool.iloc[rng.choice(len(pool),min(10,len(pool)),replace=False)]
        for row in selected.to_dict('records'):
            seen.add(row['row_id'])
            rows.append({'run_id':manifest['run_id'],'sampling_group':group,'row_id':row['row_id'],
                         'machine_property_type':row['property_type'],'machine_transaction':row['transaction_status'],
                         'area_m2':row['area_m2'],'sale_price_vnd':row['sale_price_vnd'],
                         'machine_flags':row['quality_flags'],'machine_reasons':row.get('rejection_reasons',''),
                         'human_property_type':'','human_transaction':'','human_price_area_status':'',
                         'reviewer':'','reviewed_on':'','evidence_note':'','second_reviewer':'','agreement':''})
    destination=ROOT/'docs/MAU_KIEM_TRA_DU_LIEU.csv'
    if destination.exists():
        with destination.open(encoding='utf-8-sig',newline='') as stream: previous=list(csv.DictReader(stream))
        manual_fields=('human_property_type','human_transaction','human_price_area_status','reviewer','reviewed_on','evidence_note','second_reviewer','agreement')
        if any(any(r.get(field) for field in manual_fields) for r in previous):
            raise ValueError('Manual work already exists; preserve it instead of overwriting review labels.')
    with destination.open('w',encoding='utf-8-sig',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    print(json.dumps({'review_rows':len(rows),'labels_filled':False,'run_id':manifest['run_id']}))


if __name__=='__main__': main()
