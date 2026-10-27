"""Freeze a stratified 120/60 audit sample without opening evaluation labels.

Run once against the OLD saved baseline; refuses to overwrite reader work.
Uses only the standard library. Raw text and reader packets stay Git-ignored.
"""
import argparse, csv, hashlib, json, random
from collections import defaultdict, Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SHA = 'ef39f153f48a55af07baa86883cd9036652f6d52232fed0be6e8991c7a5bf811'
KNOWN_EXTRA = {638,7811,335,8262,300,588,8535,2331,5093,8151}
LABELS = ['transaction_label','property_label','price_basis','verified_price_vnd',
          'area_basis','verified_area_m2','conflict_status','usability','evidence','reviewer','reviewed_on']

def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as f:return list(csv.DictReader(f))
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write_csv(path, rows, fields):
    with path.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
def select(candidates, excluded, seed=42):
    """Equal rotation over nonempty type × risk strata, then 2:1 split per stratum.

    Each group has 60 sampled canonical IDs. Probability differs by stratum.
    Round-robin randomizes stratum order once, then shuffles IDs within strata.
    """
    rng=random.Random(seed); chosen=[]; allocation=[]
    for group in ['kept_assumed','kept_other','rejected']:
        strata=defaultdict(list)
        for row in candidates:
            if row['group']==group and int(row['row_id']) not in excluded:
                strata[(row['property_type'],row['risk'])].append(row)
        keys=sorted(strata);rng.shuffle(keys)
        for key in keys:
            strata[key].sort(key=lambda x:int(x['row_id']));rng.shuffle(strata[key])
        assert sum(map(len,strata.values()))>=60,group
        picks=defaultdict(list)
        while sum(map(len,picks.values()))<60:
            for key in keys:
                if strata[key] and sum(map(len,picks.values()))<60:picks[key].append(strata[key].pop())
        # Largest-remainder allocation gives exactly 20 evaluation rows per group.
        quotas={k:len(v)//3 for k,v in picks.items()}
        order=sorted(picks,key=lambda k:(-(len(picks[k])%3),keys.index(k)))
        for k in order[:20-sum(quotas.values())]:quotas[k]+=1
        for key,rows in picks.items():
            rng.shuffle(rows)
            total=sum(r['group']==group and (r['property_type'],r['risk'])==key and int(r['row_id']) not in excluded for r in candidates)
            allocation.append({'group':group,'property_type':key[0],'risk':key[1],'eligible_n':total,'sample_n':len(rows),'development_n':len(rows)-quotas[key],'evaluation_n':quotas[key]})
            for i,row in enumerate(rows):chosen.append({**row,'split':'evaluation' if i<quotas[key] else 'development'})
    return sorted(chosen,key=lambda r:int(r['row_id'])),allocation

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--raw',type=Path,default=ROOT/'data/raw/chotot_data.json');args=ap.parse_args()
    dest=ROOT/'docs/manual_validation';private=dest/'private';manifest=dest/'sample_manifest.json'
    if manifest.exists() or private.exists():raise SystemExit('Sample already exists; never overwrite frozen IDs or reader work. Use a separate versioned project copy.')
    assert sha(args.raw)==SOURCE_SHA,'Unexpected raw source'
    records=json.loads(args.raw.read_text(encoding='utf-8'))
    excluded=set(KNOWN_EXTRA)
    for name in ['DOI_CHIEU_60_TIN_TRO_LY.csv','MAU_KIEM_TRA_DU_LIEU.csv']:
        for row in read_csv(ROOT/'docs'/name):excluded.add(int(row['row_id']))
    candidates=[]
    baseline={}
    for filename,state in [('listings_clean.csv','kept'),('listings_rejected.csv','rejected')]:
        path=ROOT/'data/processed'/filename;baseline[filename]=sha(path)
        for row in read_csv(path):
            group='rejected' if state=='rejected' else ('kept_assumed' if row['transaction_status']=='sale_assumed' else 'kept_other')
            risk='flagged' if row.get('is_outlier_group','').lower()=='true' or any(s in row['quality_flags'] for s in ['dot_thousands','source_','area_recovered','ambiguous']) else 'ordinary'
            candidates.append({**row,'group':group,'risk':risk})
    chosen,allocation=select(candidates,excluded)
    assert len(chosen)==len({r['row_id'] for r in chosen})==180
    assert Counter(r['split'] for r in chosen)=={'development':120,'evaluation':60}
    private.mkdir(parents=True)
    baseline_run=json.loads((ROOT/'outputs/run_manifest.json').read_text())['run_id']
    data={'schema_version':1,'seed':42,'baseline_run_id':baseline_run,'source_sha256':SOURCE_SHA,'baseline_sha256':baseline,'excluded_known_ids':sorted(excluded),'allocation':allocation,
          'method':'Randomized round-robin balanced type × risk strata within three groups; largest-remainder evaluation allocation. NOT self-weighting. Exact duplicates absent; near-duplicate leakage not ruled out.',
          'sample':[{'row_id':int(r['row_id']),'split':r['split'],'group':r['group'],'property_type':r['property_type'],'risk':r['risk']} for r in chosen]}
    manifest.write_text(json.dumps(data,ensure_ascii=False,indent=2))
    (private/'baseline_predictions.json').write_text(json.dumps(chosen,ensure_ascii=False,indent=2))
    packets={}
    fields=['row_id','title','description','raw_price','raw_area']+LABELS
    for split in ['development','evaluation']:
        packet=[]
        for r in chosen:
            if r['split']!=split:continue
            raw=records[int(r['row_id'])-1]
            packet.append({'row_id':int(r['row_id']),'title':raw.get('title',''),'description':raw.get('description',''),'raw_price':raw.get('price',''),'raw_area':raw.get('area',''),**{k:'' for k in LABELS}})
        random.Random(42 if split=='development' else 43).shuffle(packet)
        packets[split]=packet
        copies=['development_blank'] if split=='development' else ['evaluation_reader_A']
        for name in copies:write_csv(private/(name+'.csv'),packet,fields)
        (private/(split+'_packet.json')).write_text(json.dumps(packet,ensure_ascii=False,indent=2))
    print(json.dumps({'n':len(chosen),'split':dict(Counter(r['split'] for r in chosen)),'excluded':len(excluded),'allocation':allocation},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
