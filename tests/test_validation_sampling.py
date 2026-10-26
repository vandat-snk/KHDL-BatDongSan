import importlib.util,unittest,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('prepare',ROOT/'scripts/prepare_manual_validation.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class SamplingTests(unittest.TestCase):
    def test_reproducible_disjoint_balanced_sample_with_exclusions(self):
        rows=[]
        for gi,g in enumerate(['kept_assumed','kept_other','rejected']):
            for i in range(150):rows.append({'row_id':str(gi*1000+i+1),'group':g,'property_type':['land','house','apartment'][i%3],'risk':'flagged' if i%2 else 'ordinary'})
        a,alloc=m.select(rows,{1,1001,2001});b,_=m.select(rows,{1,1001,2001})
        self.assertEqual(a,b);self.assertEqual(len(a),180);self.assertEqual(len({r['row_id'] for r in a}),180)
        self.assertFalse({1,1001,2001}&{int(r['row_id']) for r in a})
        for g in ['kept_assumed','kept_other','rejected']:
            self.assertEqual(sum(r['group']==g and r['split']=='development' for r in a),40)
            self.assertEqual(sum(r['group']==g and r['split']=='evaluation' for r in a),20)
        self.assertTrue(all(r['sample_n']<=r['eligible_n'] for r in alloc))

    def test_small_stratum_is_not_duplicated(self):
        rows=[]
        for gi,g in enumerate(['kept_assumed','kept_other','rejected']):
            for i in range(80):rows.append({'row_id':str(gi*1000+i),'group':g,'property_type':'rare' if i==0 else 'house','risk':'ordinary'})
        selected,alloc=m.select(rows,set())
        self.assertEqual(sum(r['property_type']=='rare' for r in selected),3)
        self.assertEqual(sum(r['split']=='evaluation' for r in selected),60)

    def test_frozen_membership_and_ai_only_development(self):
        import csv
        folder=ROOT/'docs/manual_validation';data=json.loads((folder/'sample_manifest.json').read_text());rows=data['sample']
        dev={r['row_id'] for r in rows if r['split']=='development'};ev={r['row_id'] for r in rows if r['split']=='evaluation'}
        self.assertEqual((len(dev),len(ev)),(120,60));self.assertFalse(dev&ev)
        self.assertFalse((dev|ev)&set(data['excluded_known_ids']))
        with (folder/'AI_REVIEW_DEVELOPMENT_120.csv').open(encoding='utf-8-sig') as f:notes=list(csv.DictReader(f))
        self.assertEqual({int(r['row_id']) for r in notes},dev);self.assertTrue(all('AI' in r['reviewer'] for r in notes))
if __name__=='__main__':unittest.main()
