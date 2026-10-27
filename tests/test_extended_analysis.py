import importlib.util
from pathlib import Path
import tempfile
import unittest
import pandas as pd

SPEC=importlib.util.spec_from_file_location('extended',Path(__file__).resolve().parents[1]/'scripts/complete_analysis.py')
m=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(m)

class ExtendedTests(unittest.TestCase):
    def test_missing_reference_is_unscored_not_zero(self):
        self.assertIsNone(m.compare_numeric(0,None,1))
        self.assertFalse(m.compare_numeric(None,100,1))
        self.assertTrue(m.compare_numeric(100000000.01,100000000,1))
        self.assertFalse(m.compare_numeric(3200000,3200000000,1))
        self.assertIsNone(m.ratio(0,0))

    def test_abstention_and_review_do_not_inflate_match_rate(self):
        labels=pd.DataFrame([dict(row_id=1,property='other',transaction='sale',basis='total',price=100,
            area=10,conflict='no',usability='review')])
        clean=pd.DataFrame([dict(row_id=1,property_type='other_unknown',transaction_status='sale_assumed',
            price_basis='total',sale_price_vnd=100,area_m2=10)])
        sample=pd.DataFrame([dict(row_id=1,group='kept_assumed',risk='ordinary')])
        with tempfile.TemporaryDirectory() as folder:
            result=m.evaluation(labels,clean,clean.iloc[:0],sample,Path(folder))
        metrics={r['field']:r for r in result['metrics'] if r['group']=='all_sample'}
        self.assertEqual(metrics['property']['n_match'],0)
        self.assertEqual(metrics['transaction']['n_match'],0)
        self.assertEqual(metrics['status']['n_resolved'],0)
        self.assertIsNone(metrics['status']['match_rate_resolved'])
        self.assertEqual(metrics['price']['n_match'],1)

    def test_missing_prediction_id_fails_instead_of_dropping_row(self):
        labels=pd.DataFrame([dict(row_id=2)])
        clean=pd.DataFrame([dict(row_id=1)])
        sample=pd.DataFrame([dict(row_id=2,group='kept_assumed',risk='ordinary')])
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaisesRegex(ValueError,'missing'):
                m.evaluation(labels,clean,clean.iloc[:0],sample,Path(folder))

if __name__=='__main__':unittest.main()
