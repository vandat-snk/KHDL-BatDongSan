"""Development/regression examples, NEVER independent accuracy measurement."""
import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import pipeline as p

class DevelopmentRuleTests(unittest.TestCase):
    def check(self,text,area=120,price=723e6,title='Bán đất'):
        return p.check_source_consistency({'title':title,'description':text},area,price,'total',p.parse_number,p.normalize)

    def test_nearby_apartment_not_asset(self):
        for text,expected in [('Bán đất gần chung cư A','land'),('Bán nhà đối diện căn hộ A','house'),('Bán căn hộ gần chung cư A','apartment'),('Bán đất xây căn hộ','land')]:
            self.assertEqual(p.classify_title(text)[0],expected,text)

    def test_comparison_not_confident_apartment(self):
        kind,_,flags=p.classify_title('1,95 tỷ mua chung cư hay nhà 2tầng 64m2 sàn sổ đỏ')
        self.assertEqual(kind,'other_unknown');self.assertIn('ambiguous_property_comparison_requires_review',flags)

    def test_narrow_spelling_and_rental_typo(self):
        for text in ['Bánđất 1041M2','ĐấtBán gấp 102 m2','chính chủ bán lô đat 1900m2']:
            kind,tx,flags=p.classify_title(text);self.assertEqual((kind,tx),('land','sale'));self.assertIn('title_spelling_normalized',flags)
        self.assertEqual(p.classify_title('Nhà bán hoạc cho thê')[1],'ambiguous_mixed')

    def test_rental_suitability_and_real_rent(self):
        self.assertEqual(p.classify_title('Bán nhà tiện cho thuê 1,2tỷ')[1],'sale')
        self.assertEqual(p.classify_title('Bán nhà phù hợp để cho thuê')[1],'sale')
        self.assertEqual(p.classify_title('Bán hoặc cho thuê nhà')[1],'ambiguous_mixed')
        self.assertEqual(p.classify_title('Bán nhà đang cho thuê 30tr')[1],'sale_with_rental_income')
        self.assertEqual(p.classify_title('Cho thuê nhà tiện cho thuê lại')[1],'rental')

    def test_room_building_and_mini_apartment(self):
        for title in ['Bán dãy trọ 12P','bán dãy phòng trọ doanh thu 15 triệu/tháng','cần bán dạy trọ 5p']:
            self.assertEqual(p.classify_title(title)[0],'house')
        self.assertEqual(p.classify_title('CCMN Nam Thăng Long')[0],'apartment')
        self.assertEqual(p.classify_title('Bán đất xây nhà trọ')[0],'land')

    def test_block_price_requires_same_area(self):
        self.assertIn('unresolved_block_unit_price_from_source_text',self.check('Giá 723tr/100m2')[0])
        self.assertNotIn('unresolved_block_unit_price_from_source_text',self.check('Giá 723tr/100m2',area=100)[0])
        self.assertNotIn('unresolved_block_unit_price_from_source_text',self.check('Giá 723tr/100m2',price=867.6e6)[0])
        self.assertEqual(self.check('Giá 5.5 tỷ trọn sổ (2.74 tỷ/1000m2)',area=2005,price=5.5e9)[0],[])

    def test_deposit_same_as_total_not_financing_in_general(self):
        for text,price in [('Vốn ban đầu chỉ từ 10% (820tr)',820e6),('Chỉ cần thanh toán 40% tầm 508tr',508e6)]:
            self.assertIn('core_price_matches_initial_payment',self.check(text,price=price)[0])
        for text,price in [('Giá bán 2.7tỷ có thể trả trước 460Tr',2.7e9),('Không cần trả trước 820tr',820e6),('Hỗ trợ vay 70%',820e6),('Trả trước 1ty5',1e9)]:
            self.assertNotIn('core_price_matches_initial_payment',self.check(text,price=price)[0])

    def test_moderate_discrepancy_flag_not_replacement(self):
        reasons,flags,ev=self.check('Giá 4 tỷ',price=3.6e9)
        self.assertEqual(reasons,[]);self.assertIn('source_price_discrepancy_requires_review',flags)
        self.assertEqual(ev[0]['numeric_phrase'],'4 tỷ')
        self.assertIn('source_area_discrepancy_requires_review',self.check('DT: 38.8m2',area=40)[1])
        self.assertNotIn('source_area_discrepancy_requires_review',self.check('Diện tích đất: 45m2, diện tích sử dụng 70m2',area=45)[1])
        self.assertNotIn('source_price_discrepancy_requires_review',self.check('Giá 2.350 tỷ',price=2.35e9)[1])

    def test_spaced_compound_is_not_a_prefix_price_conflict(self):
        for text,price in [('Giá 1 tỷ 780',1.78e9),('Giá 1 tỷ 250',1.25e9),('Giá 4 tỷ 5',4.5e9),('Giá 7ty 1',7.1e9),('Giá 3 tỷ 950',3.95e9)]:
            reasons,flags,_=self.check(text,price=price)
            self.assertNotIn('price_conflict_from_description',reasons,text)
            self.assertNotIn('source_price_discrepancy_requires_review',flags,text)

    def test_full_clean_preserves_numeric_values_when_flagged(self):
        rows=[{'title':'Bán nhà','price':'3,6 tỷ- 76.9 m2','area':'- 76.9 m2','location':'Hà Nội','description':'Giá 4 tỷ'}]
        clean,rejected,_,_=p.clean_records(rows)
        self.assertEqual(len(rejected),0);self.assertEqual(clean.iloc[0].sale_price_vnd,3.6e9)
        self.assertIn('source_price_discrepancy_requires_review',clean.iloc[0].quality_flags)

if __name__=='__main__':unittest.main()
