"""Compare rules on development IDs only. This is not an accuracy evaluation."""
import csv, hashlib, json, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
import pipeline as p

def main():
    folder=ROOT/'docs/manual_validation';private=folder/'private'
    packet=json.loads((private/'development_packet.json').read_text())
    manifest=json.loads((folder/'sample_manifest.json').read_text())
    allowed={r['row_id'] for r in manifest['sample'] if r['split']=='development'}
    assert {r['row_id'] for r in packet}==allowed
    baseline={int(r['row_id']):r for r in json.loads((private/'baseline_predictions.json').read_text()) if int(r['row_id']) in allowed}
    raw=[{'title':r['title'],'description':r['description'],'price':r['raw_price'],'area':r['raw_area']} for r in packet]
    clean,rejected,lineage,_=p.clean_records(raw)
    byid={int(r['row_id']):{**r,'new_status':state} for frame,state in [(clean,'kept'),(rejected,'rejected')] for r in frame.to_dict('records')}
    results=[]
    for i,r in enumerate(packet,1):
        new=byid[i];old=baseline[r['row_id']]
        results.append({'row_id':r['row_id'],'split':'development','old_status':'rejected' if old['group']=='rejected' else 'kept','new_status':new['new_status'],
            'old_property':old['property_type'],'new_property':new['property_type'],
            'old_transaction':old['transaction_status'],'new_transaction':new['transaction_status'],
            'old_flags':';'.join(f for f in old['quality_flags'].split(';') if f not in ('unknown_district','unknown_province','province_alias_normalized')),'new_flags':';'.join(f for f in new['quality_flags'].split(';') if f not in ('unknown_district','unknown_province','province_alias_normalized')),
            'old_reasons':old.get('rejection_reasons',''),'new_reasons':new.get('rejection_reasons',''),
            'new_evidence':new['source_review_evidence']})
    with (folder/'DEVELOPMENT_RULE_DIFF.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(results[0]));w.writeheader();w.writerows(results)
    changes=[r for r in results if any(r['old_'+k]!=r['new_'+k] for k in ['status','property','transaction','flags','reasons'])]
    print(json.dumps({'scope':'120 development rows only; no independent accuracy','n':len(results),'changed':len(changes),'changes':changes},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
