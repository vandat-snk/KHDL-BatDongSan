"""Evaluate locked rules and run descriptive extensions, without tuning rules on labels.

python scripts/complete_analysis.py --labels path/to/reviewed.xlsx
Outputs are supplementary and bind to a validated core run and label SHA-256.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import openpyxl

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
import pipeline as p
from artifact_contract import validate_core_outputs, file_sha256


def ratio(n, d):
    return n / d if d else None


def compare_numeric(pred, reference, atol):
    if pd.isna(reference):
        return None
    return bool(pd.notna(pred) and np.isclose(pred, reference, rtol=1e-6, atol=atol))


def load_labels(path, sample):
    rows = list(openpyxl.load_workbook(path, data_only=True)['GanNhan'].values)[1:]
    labels = pd.DataFrame(rows, columns=['row_id','title','raw_price','raw_area','transaction','property','basis',
        'price','area_basis','area','conflict','usability','evidence','reviewer','reviewed_on'])
    expected = set(sample.loc[sample.split.eq('evaluation'), 'row_id'])
    if len(labels) != 60 or labels.row_id.duplicated().any() or set(labels.row_id) != expected:
        raise ValueError('Labels must contain exactly the 60 locked evaluation IDs, once each.')
    allowed = {'transaction': {'sale','rental','mixed','transfer','unknown'},
        'property': {'house','land','apartment','other','unknown'},
        'basis': {'total','per_m2','per_block','partial_payment','rental','transfer','foreign','unknown'},
        'conflict': {'yes','no','uncertain'}, 'usability': {'usable','review','exclude'}}
    for key, values in allowed.items():
        if not labels[key].isin(values).all():
            raise ValueError('Invalid or missing category: ' + key)
    return labels


def evaluation(labels, clean, rejected, sample, folder):
    pred = pd.concat([clean.assign(pred_status='kept'), rejected.assign(pred_status='rejected')], ignore_index=True)
    join = labels.merge(pred, on='row_id', validate='one_to_one').merge(
        sample[['row_id','group','risk']], on='row_id', validate='one_to_one')
    if len(join) != len(labels):
        raise ValueError('Evaluation IDs missing from current nonduplicate outputs')
    # other_unknown merges two different classes: treat it as abstention, never as a correct "other".
    join['pred_property'] = join.property_type.replace({'other_unknown':'abstain'})
    join['pred_transaction'] = join.transaction_status.map({'sale':'sale','sale_with_rental_income':'sale',
        'sale_assumed':'abstain','rental':'rental','rental_or_ambiguous':'abstain','ambiguous_mixed':'mixed'})
    join['property_match'] = [None if ref == 'unknown' else a == ref for a, ref in zip(join.pred_property,join.property)]
    join['transaction_match'] = [None if ref == 'unknown' else a == ref for a, ref in zip(join.pred_transaction,join.transaction)]
    join['basis_match'] = [None if ref == 'unknown' else a == ref for a, ref in zip(join.price_basis,join.basis)]
    join['price_match'] = [compare_numeric(a,b,1) for a,b in zip(join.sale_price_vnd,join.price)]
    join['area_match'] = [compare_numeric(a,b,1e-6) for a,b in zip(join.area_m2,join.area)]
    join['status_match'] = [None if ref=='review' else a==('kept' if ref=='usable' else 'rejected')
                            for a,ref in zip(join.pred_status,join.usability)]
    metrics=[]
    groups=[('all_sample',join)]+list(join.groupby('group',sort=True))
    for name, frame in groups:
        for key in ['property','transaction','basis','price','area','status']:
            scored=frame[key+'_match'].dropna()
            metrics.append({'group':name,'field':key,'n_sample':len(frame),'n_resolved':len(scored),
                'n_match':int(scored.sum()),'n_unresolved':len(frame)-len(scored),
                'match_rate_resolved':ratio(int(scored.sum()),len(scored)),
                'resolved_coverage':ratio(len(scored),len(frame))})
    public_cols=['row_id','group','risk','property','pred_property','property_match','transaction','pred_transaction',
        'transaction_match','basis','price_basis','basis_match','price','sale_price_vnd','price_match','area',
        'area_m2','area_match','conflict','usability','pred_status','status_match']
    join[public_cols].to_csv(folder/'evaluation_rows.csv',index=False,encoding='utf-8-sig')
    pd.DataFrame(metrics).to_csv(folder/'evaluation_metrics.csv',index=False,encoding='utf-8-sig')
    for ref, machine in [('property','pred_property'),('transaction','pred_transaction'),('usability','pred_status')]:
        pd.crosstab(join[ref],join[machine]).to_csv(folder/f'confusion_{ref}.csv',encoding='utf-8-sig')
    return {'metrics':metrics,'usability_counts':join.usability.value_counts().to_dict(),
        'prediction_abstentions':{'property':int(join.pred_property.eq('abstain').sum()),'transaction':int(join.pred_transaction.eq('abstain').sum())},
        'scope':'One human initial annotator; 17 rows edited by AI at user request. Human reconfirmation of AI edits not recorded. Not independent human gold.',
        'policy':'Unknown reference values and review decisions are unscored, not errors or matches. Model abstention against resolved labels is not a match. Numeric checks include parsed values of quarantined rows; they do not validate retention decisions. Tolerance rtol=1e-6; price atol=1 VND; area atol=1e-6 m2.',
        'limits':'Balanced sample is not self-weighting; report baseline sampling groups separately. No population accuracy or inter-rater agreement. Title-only class predictions have less context than full-text annotation.'}


def stratification(clean, folder):
    table=p.summarize_groups(clean,['province','property_type','area_band'])
    table['enough_for_comparison']=table.n.ge(30) & table.province.ne('Chưa xác định') & table.property_type.ne('other_unknown')
    base=clean.loc[~clean.is_outlier_group]
    filtered=p.summarize_groups(base,['province','property_type','area_band'])[
        ['province','property_type','area_band','n','median_price_per_m2_vnd']].rename(columns={
            'n':'n_without_group_outliers','median_price_per_m2_vnd':'median_without_group_outliers'})
    table=table.merge(filtered,on=['province','property_type','area_band'],how='left',validate='one_to_one')
    table['median_change_pct']=100*(table.median_without_group_outliers/table.median_price_per_m2_vnd-1)
    table.to_csv(folder/'province_type_area_summary.csv',index=False,encoding='utf-8-sig')
    correlations=[]
    for keys in [['property_type'],['province','property_type']]:
        for name,g in clean.groupby(keys,sort=True):
            if len(g)<30:continue
            name=name if isinstance(name,tuple) else (name,)
            correlations.append({**dict(zip(keys,name)),'n':len(g),
                'spearman_area_total':float(g[['area_m2','sale_price_vnd']].rank().corr().iloc[0,1])})
    pd.DataFrame(correlations).to_csv(folder/'within_group_correlations.csv',index=False,encoding='utf-8-sig')
    top=table[table.enough_for_comparison].head(12).sort_values('median_price_per_m2_vnd')
    p.chart_setup()
    fig,ax=p.plt.subplots(figsize=(11,7))
    med=top.median_price_per_m2_vnd/1e6
    ax.errorbar(med,np.arange(len(top)),xerr=np.array([med-top.q1_price_per_m2_vnd/1e6,
        top.q3_price_per_m2_vnd/1e6-med]),fmt='o',color='#214E70',capsize=3)
    ax.set_yticks(np.arange(len(top)),[f'{r.province} | {r.property_type} | {r.area_band} m² (n={r.n})' for r in top.itertuples()])
    ax.set_xlabel('Trung vị và khoảng tứ phân vị giá rao (triệu VND/m²)')
    ax.set_title('12 nhóm có nhiều tin nhất trong các nhóm đủ n ≥ 30')
    fig.tight_layout();fig.savefig(folder/'stratified_prices.png',dpi=160);p.plt.close(fig)
    eligible=table[table.enough_for_comparison]
    return {'group_count':len(table),'eligible_groups':len(eligible),'eligible_rows':int(eligible.n.sum()),
        'total_rows':len(clean),'top_groups':top.to_dict('records'),
        'limits':'Descriptive convenience sample only. n>=30 is a display threshold, not evidence of representativeness. Area semantic types remain mixed; inferred property labels may be wrong. IQR bars describe spread, not confidence intervals.'}


def clustering(clean, folder):
    configs=[('log_z_no_outliers',False,'log_z'),('log_z_all',True,'log_z'),
             ('raw_z_no_outliers',False,'raw_z'),('log_robust_no_outliers',False,'log_robust'),
             ('log_total_no_outliers',False,'log_total')]
    trials=[];models={}
    for scenario,include,transform in configs:
        sub=clean if include else clean.loc[~clean.is_outlier_group]
        features=['area_m2','sale_price_vnd' if transform=='log_total' else 'price_per_m2_vnd']
        x=sub[features].to_numpy(float)
        if transform.startswith('log'):x=np.log(x)
        if transform=='log_robust':
            center=np.median(x,axis=0);scale=np.quantile(x,.75,axis=0)-np.quantile(x,.25,axis=0)
        else:center=x.mean(axis=0);scale=x.std(axis=0)
        if np.any(scale==0):raise ValueError('Constant clustering feature')
        x=(x-center)/scale
        for k in range(2,6):
            for seed in [7,42,2026]:
                lab,_,inertia=p.kmeans(x,k,seed=seed)
                reason=''
                try:
                    sil=p.sampled_silhouette(x,lab,seed=123,sample_size=500)
                except ValueError as exc:
                    if str(exc)!='silhouette_sample_requires_two_to_n_minus_one_clusters':raise
                    sil=None;reason='Random silhouette sample contains fewer than two clusters; score unavailable.'
                trials.append({'scenario':scenario,'k':k,'seed':seed,'n':len(sub),
                    'silhouette':sil,'score_note':reason,'inertia':inertia,'min_cluster_n':int(np.bincount(lab,minlength=k).min())})
                models[(scenario,k,seed)]=pd.Series(lab,index=sub.row_id)
        print('Completed cluster scenario: '+scenario,flush=True)
    trial=pd.DataFrame(trials);trial.to_csv(folder/'cluster_robustness_trials.csv',index=False,encoding='utf-8-sig')
    stability=[]
    for scenario,_,_ in configs:
        for k in range(2,6):
            ref=models[(scenario,k,42)]
            for seed in [7,2026]:
                stability.append({'scenario':scenario,'k':k,'seed':seed,'n':len(ref),
                    'ari_vs_seed42':p.adjusted_rand_index(ref.to_numpy(),models[(scenario,k,seed)].to_numpy())})
    pd.DataFrame(stability).to_csv(folder/'cluster_seed_stability.csv',index=False,encoding='utf-8-sig')
    primary_k=int(json.loads((ROOT/'outputs/analysis.json').read_text())['clustering']['chosen_k'])
    reference=models[('log_z_no_outliers',primary_k,42)]
    sensitivity=[]
    for scenario,_,_ in configs:
        alternate=models[(scenario,primary_k,42)];common=reference.index.intersection(alternate.index)
        sensitivity.append({'scenario':scenario,'fixed_k':primary_k,'n_common':len(common),
            'ari_on_common_rows':p.adjusted_rand_index(reference.loc[common].to_numpy(),alternate.loc[common].to_numpy())})
    pd.DataFrame(sensitivity).to_csv(folder/'cluster_feature_sensitivity.csv',index=False,encoding='utf-8-sig')
    # Subsample refits compare only IDs present in both fits, at the primary k.
    sub=clean.loc[~clean.is_outlier_group];resamples=[]
    for seed in [7,42,2026,2027,2028]:
        subset=sub.sample(frac=.8,random_state=seed).sort_values('row_id')
        x=np.log(subset[['area_m2','price_per_m2_vnd']].to_numpy(float));x=(x-x.mean(0))/x.std(0)
        lab,_,_=p.kmeans(x,primary_k,seed=seed)
        resamples.append({'seed':seed,'n':len(subset),'k':primary_k,
            'ari_vs_full_common_rows':p.adjusted_rand_index(reference.loc[subset.row_id].to_numpy(),lab)})
    pd.DataFrame(resamples).to_csv(folder/'cluster_subsample_stability.csv',index=False,encoding='utf-8-sig')
    means=trial.groupby(['scenario','k']).silhouette.agg(['mean','min','max']).reset_index()
    fig,ax=p.plt.subplots(figsize=(8,5))
    for name,g in means.groupby('scenario'):
        ax.plot(g.k,g['mean'],'o-',label=name);ax.fill_between(g.k,g['min'],g['max'],alpha=.12)
    ax.set(xticks=[2,3,4,5],xlabel='Số cụm k',ylabel='Silhouette trên tối đa 500 tin',title='Độ nhạy với ngoại lệ và cách biến đổi đặc trưng')
    ax.legend(fontsize=8);fig.tight_layout();fig.savefig(folder/'cluster_robustness.png',dpi=160);p.plt.close(fig)
    return {'primary_k':primary_k,'n_fits':len(trials)+len(resamples),'silhouette_sample_seed':123,
        'mean_silhouettes':means.astype(object).where(means.notna(),None).to_dict('records'),'feature_sensitivity':sensitivity,
        'seed_ari_min':min(r['ari_vs_seed42'] for r in stability),'subsample':resamples,
        'limits':'ARI compares partitions on identical IDs against log-z without outliers, refit with seed 42 at the core chosen k. Silhouette depends on geometry and sample; unavailable single-cluster sample scores are not zero. Scores across transformations are descriptive, not a universal selection criterion. Repeated seeds/subsamples are not independent external validation.'}


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--labels',type=Path,required=True);args=ap.parse_args()
    manifest=validate_core_outputs(ROOT)
    freeze=json.loads((ROOT/'docs/manual_validation/FREEZE_MANIFEST.json').read_text())
    for rel,sha in freeze['sha256'].items():
        if file_sha256(ROOT/rel)!=sha:raise ValueError('Frozen file changed: '+rel)
    sample=pd.DataFrame(json.loads((ROOT/'docs/manual_validation/sample_manifest.json').read_text())['sample'])
    labels=load_labels(args.labels,sample)
    clean=pd.read_csv(ROOT/'data/processed/listings_clean.csv');rejected=pd.read_csv(ROOT/'data/processed/listings_rejected.csv')
    folder=ROOT/'outputs/extended';folder.mkdir(exist_ok=True)
    results={'core_run_id':manifest['run_id'],'source_sha256':manifest['source_sha256'],
        'labels_sha256':file_sha256(args.labels),'script_sha256':file_sha256(Path(__file__)),
        'evaluation':evaluation(labels,clean,rejected,sample,folder),
        'stratification':stratification(clean,folder),'clustering':clustering(clean,folder)}
    (folder/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2,allow_nan=False),encoding='utf-8')
    print('Extensions completed for '+manifest['run_id'])


if __name__=='__main__':main()
