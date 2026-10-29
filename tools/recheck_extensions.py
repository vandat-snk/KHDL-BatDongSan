"""Recompute the published extensions without modifying the checked Git revision."""
import sys, json, hashlib, importlib.util
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'tmp/recheck_extensions'
BASE.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'src'))
from artifact_contract import validate_core_outputs, file_sha256
manifest=validate_core_outputs(ROOT)
freeze=json.loads((ROOT/'docs/manual_validation/FREEZE_MANIFEST.json').read_text(encoding='utf-8'))
for relative,digest in freeze['sha256'].items():
    assert file_sha256(ROOT/relative)==digest, 'Frozen input changed: '+relative
spec=importlib.util.spec_from_file_location('extensions',ROOT/'scripts/complete_analysis.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
clean=pd.read_csv(ROOT/'data/processed/listings_clean.csv')
saved=json.loads((ROOT/'outputs/extended/results.json').read_text(encoding='utf-8'))
assert saved['core_run_id']==manifest['run_id']
assert saved['script_sha256']==file_sha256(ROOT/'scripts/complete_analysis.py')
out=BASE/'recomputed_extensions';out.mkdir(exist_ok=True)
sample=pd.DataFrame(json.loads((ROOT/'docs/manual_validation/sample_manifest.json').read_text())['sample'])
rows=pd.read_csv(ROOT/'outputs/extended/evaluation_rows.csv')
assert set(rows.row_id)==set(sample.loc[sample.split.eq('evaluation'),'row_id']) and len(rows)==60
assert set(sample[sample.split.eq('development')].row_id).isdisjoint(set(rows.row_id))
labels=rows.rename(columns={'price':'price','area':'area'})[['row_id','property','transaction','basis','price','area','conflict','usability']]
rejected=pd.read_csv(ROOT/'data/processed/listings_rejected.csv')
evaluation=m.evaluation(labels,clean,rejected,sample,out)
assert evaluation['metrics']==saved['evaluation']['metrics']
strat=m.stratification(clean,out)
assert (strat['group_count'],strat['eligible_groups'],strat['eligible_rows'])==(405,41,4594)
def compare_csv(name, numeric):
    left=pd.read_csv(ROOT/'outputs/extended'/name)
    right=pd.read_csv(out/name)
    assert left.shape==right.shape,(name,left.shape,right.shape)
    for col in left:
        if col in numeric:
            assert np.allclose(left[col].to_numpy(float),right[col].to_numpy(float),equal_nan=True,rtol=1e-8,atol=1e-5),(name,col)
        else:assert left[col].fillna('').tolist()==right[col].fillna('').tolist(),(name,col)
compare_csv('evaluation_metrics.csv',{'n_sample','n_resolved','n_match','n_unresolved','match_rate_resolved','resolved_coverage'})
compare_csv('province_type_area_summary.csv',set(pd.read_csv(out/'province_type_area_summary.csv').select_dtypes('number').columns))
cluster=m.clustering(clean,out)
assert cluster['n_fits']==65
for name in ['cluster_robustness_trials.csv','cluster_seed_stability.csv','cluster_feature_sensitivity.csv','cluster_subsample_stability.csv']:
    compare_csv(name,set(pd.read_csv(out/name).select_dtypes('number').columns))
result={'status':'passed','checked_revision':'549df1aa0fcb46b011863a02930241807489e91b',
    'core_run_id':saved['core_run_id'],'evaluation_rows_recomputed':60,
    'reference_scope':'Recomputed against the public reference values; original private annotation XLSX not supplied. No independent annotation validation.',
    'stratification':{k:strat[k] for k in ['group_count','eligible_groups','eligible_rows']},
    'cluster_fits_recomputed':65,'numeric_tolerance':{'rtol':1e-8,'atol':1e-5},
    'source_files':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT/'scripts/complete_analysis.py',ROOT/'outputs/extended/results.json']}}
(BASE/'extended_audit.json').write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
