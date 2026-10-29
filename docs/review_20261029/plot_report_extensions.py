from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'docs/review_20261029/assets'
OUT.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'axes.spines.top':False,'axes.spines.right':False})
table=pd.read_csv(ROOT/'outputs/extended/province_type_area_summary.csv')
rows=[]
for kind,band in [('house','(30,60]'),('house','(60,100]'),('apartment','(30,60]')]:
    for province in ['Hà Nội','Tp Hồ Chí Minh']:
        selected=table[(table.province==province)&(table.property_type==kind)&(table.area_band==band)]
        assert len(selected)==1 and selected.iloc[0]['n']>=30
        rows.append(selected.iloc[0])
small=pd.DataFrame(rows)
small.to_csv(OUT/'conditional_comparison.csv',index=False,encoding='utf-8-sig')
fig,ax=plt.subplots(figsize=(9,4.6))
for i,(province,color) in enumerate([('Hà Nội','#214e70'),('Tp Hồ Chí Minh','#b36b25')]):
    s=small[small.province==province]
    med=s.median_price_per_m2_vnd.to_numpy()/1e6
    low=s.q1_price_per_m2_vnd.to_numpy()/1e6
    high=s.q3_price_per_m2_vnd.to_numpy()/1e6
    y=np.arange(3)+(i-.5)*.18
    ax.errorbar(med,y,xerr=np.vstack([med-low,high-med]),fmt='o',capsize=4,color=color,label=province)
    for yy,nn in zip(y,s.n):ax.annotate(f'n={nn}',(high[list(y).index(yy)],yy),xytext=(7,0),textcoords='offset points',fontsize=9,va='center',color=color)
ax.set_yticks(np.arange(3),['Nhà · 30 < A ≤ 60 m²','Nhà · 60 < A ≤ 100 m²','Căn hộ · 30 < A ≤ 60 m²'])
ax.set_xlabel('Trung vị và khoảng Q1–Q3 của đơn giá rao (triệu VND/m²)')
ax.set_xlim(0,180);ax.invert_yaxis();ax.legend(loc='lower right')
ax.grid(axis='x',alpha=.18)
fig.tight_layout();fig.savefig(OUT/'conditional_comparison.png',dpi=180);plt.close(fig)

ari=pd.read_csv(ROOT/'outputs/extended/cluster_feature_sensitivity.csv')
names=['Mốc log + Z-score, bỏ IQR','Giữ ngoại lệ','Thang gốc + Z-score','Log + trung vị/IQR','Log diện tích + log tổng giá']
fig,ax=plt.subplots(figsize=(8.7,4.4))
ax.barh(np.arange(5),ari.ari_on_common_rows,color=['#596a79','#214e70','#b36b25','#214e70','#214e70'],height=.62)
ax.set_yticks(np.arange(5),names);ax.invert_yaxis()
for y,v in enumerate(ari.ari_on_common_rows):ax.text(v+.018,y,f'{v:.4f}'.replace('.',','),va='center',fontsize=10)
ax.set_xlim(0,1.13);ax.set_xlabel('ARI trên 6.652 ID chung, cố định k=2 và seed 42')
ax.grid(axis='x',alpha=.18)
fig.tight_layout();fig.savefig(OUT/'cluster_feature_ari.png',dpi=180);plt.close(fig)
print('Two figures and supporting numeric table generated from verified saved results.')
