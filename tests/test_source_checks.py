"""Source inconsistency checks preserve uncertainty rather than repairing guesses."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import pipeline as p

class SourceConsistencyTests(unittest.TestCase):
    def check(self,title='Bán đất',description='',area=100,price=2_000_000_000,basis='total'):
        return p.check_source_consistency({'title':title,'description':description},area,price,basis,p.parse_number,p.normalize)

    def test_explicit_unit_price_mistaken_as_total_is_quarantined(self):
        reasons,_,evidence=self.check(description='Giá chỉ 20tr/m2',area=143,price=20_000_000)
        self.assertIn('unresolved_price_basis_from_source_text',reasons)
        self.assertEqual(evidence[0]['numeric_phrase'],'20tr/m2')
        self.assertNotIn('unresolved_price_basis_from_source_text',self.check(description='Giá chỉ 20tr/m2',area=143,price=2_860_000_000)[0])

    def test_explicit_core_unit_price_already_converted_is_not_rejected(self):
        self.assertEqual(self.check(description='Giá bán 20 triệu/m2',area=143,price=2_860_000_000,basis='per_m2')[0],[])

    def test_title_currency_scale_conflict_is_quarantined(self):
        reasons,_,evidence=self.check(title='Bán nhà 860tr',area=40,price=860_000_000_000)
        self.assertIn('price_conflict_from_title',reasons)
        self.assertEqual(evidence[0]['numeric_phrase'],'860tr')

    def test_rental_income_and_downpayment_quotes_are_not_total_price(self):
        for title,description in [('Bán nhà 4 tỷ đang cho thuê 30tr','Giá thuê 30 triệu/tháng'),('Bán nhà 4 tỷ trả trước 500tr','Thanh toán giá 500 triệu')]:
            self.assertEqual(self.check(title=title,description=description,price=4_000_000_000)[0],[])

    def test_hectare_scale_conflict_not_nearby_park(self):
        self.assertIn('area_unit_conflict_from_title',self.check(title='2ha đất cần bán',area=2)[0])
        self.assertEqual(self.check(title='Bán đất gần công viên 2ha',area=100)[0],[])

    def test_description_gross_area_conflict_preserves_evidence(self):
        reasons,_,evidence=self.check(description='Diện tích đất: 500 m2',area=3)
        self.assertIn('area_conflict_from_source_text',reasons)
        self.assertIn('500 m2',[x['numeric_phrase'] for x in evidence])
        self.assertEqual(self.check(description='Diện tích 100 m2 và diện tích 20 m2',area=100)[0],[])

    def test_business_transfer_and_foreign_price_not_normal_sales(self):
        self.assertIn('outside_scope_business_or_lease_transfer',self.check(title='Sang quán cà phê')[0])
        self.assertIn('currency_conflict_from_source_text',self.check(description='Giá bán: 50000 USD')[0])
        self.assertEqual(self.check(title='Bán căn hộ',description='Nội thất phong cách sang trọng')[0],[])

    def test_width_in_dimension_expression_is_not_total_area(self):
        reasons,flags,_=self.check(description='DT: 3m2 x 5 (1 trệt 1 lầu)',area=16)
        self.assertNotIn('area_conflict_from_source_text',reasons)
        self.assertIn('source_dimension_expression_requires_review',flags)

    def test_place_name_nha_trang_is_not_a_house_label(self):
        self.assertEqual(p.classify_title('Bán đất nền ven nha trang')[0],'land')
        self.assertEqual(p.classify_title('Bán nhà tại nha trang')[0],'house')

    def test_price_component_and_grouping_validation(self):
        for price in ['1 tỷ -200 triệu','1 tỷ 2 tỷ','200 triệu 1 tỷ','1,23.45 triệu','1.23,45 triệu']:
            self.assertIsNone(p.parse_price(price)[0],price)
        self.assertEqual(p.parse_price('1 tỷ 200 triệu')[0],1_200_000_000)
        self.assertEqual(p.parse_number('1.234,5')[0],1234.5)
        self.assertEqual(p.parse_number('1,234.5')[0],1234.5)

if __name__=='__main__': unittest.main()
