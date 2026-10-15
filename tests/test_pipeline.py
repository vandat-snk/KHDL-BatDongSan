"""Meaningful checks for parsing, leakage-free cleaning and deterministic math."""
import importlib.util
from pathlib import Path
import unittest
import sqlite3
import numpy as np

MODULE = Path(__file__).resolve().parents[1] / "src/pipeline.py"
SPEC = importlib.util.spec_from_file_location("pipeline", MODULE)
p = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(p)


class ParserTests(unittest.TestCase):
    def test_mixed_decimal_and_thousand_notation(self):
        self.assertEqual(p.parse_area("- 2.246 m2")[0], 2246)
        self.assertIn("dot_thousands_convention", p.parse_area("2.246 m²")[1])
        self.assertEqual(p.parse_area("- 90.3 m2")[0], 90.3)
        self.assertEqual(p.parse_area("0,5 ha")[0], 5000)
        self.assertEqual(p.parse_price("2,38 tỷ- 100 m2")[0], 2380000000)
        self.assertEqual(p.parse_price("1.000 triệu- 900 m2")[0], 1000000000)
        self.assertEqual(p.parse_price("1 tỷ 200 triệu")[0], 1200000000)

    def test_price_per_m2_is_only_explicit(self):
        price, basis, _ = p.parse_price("25 triệu/m²- 80 m2", 80)
        self.assertEqual(price, 2e9)
        self.assertEqual(basis, "per_m2")
        self.assertEqual(p.parse_price("25 triệu- 80 m2", 80)[0], 25e6)
        self.assertIsNone(p.parse_price("25 triệu/m2")[0])

    def test_empty_zero_and_ambiguous_do_not_become_data(self):
        for value in ("", "liên hệ", "1 tỷ 950", "-5 triệu", "0 đ"):
            self.assertIsNone(p.parse_price(value)[0])
        for value in ("", "0 m2", "-5 m2", "50-70 m2"):
            self.assertIsNone(p.parse_area(value)[0])


class CleaningTests(unittest.TestCase):
    def row(self, **kwargs):
        result = {"title": "Bán đất", "price": "2 tỷ- 100 m2", "area": "- 100 m2", "location": "Quận A, Tỉnh B", "description": "Một tin gốc"}
        result.update(kwargs)
        return result

    def test_reconciliation_lineage_and_no_imputation(self):
        rows = [self.row(), self.row(), self.row(title="Bán nhà", area="GIÁ TỐT"), self.row(title="Bán lô khác", price="500.000 đ- 100 m2"), self.row(title="Cho thuê căn hộ", price="20 triệu- 100 m2"), self.row(title="Thiếu diện tích", price="2 tỷ", area="")]
        clean, rejected, lineage, info = p.clean_records(rows)
        self.assertEqual(info["raw_count"], len(clean) + len(rejected) + info["duplicate_count"])
        self.assertEqual(len(clean), 2)
        self.assertEqual(info["duplicate_count"], 1)
        self.assertEqual(lineage.loc[lineage.row_id.eq(2), "canonical_row_id"].iloc[0], 1)
        self.assertIn("area_recovered_from_price_text", clean.iloc[1].quality_flags)
        self.assertNotIn("title", clean.columns)
        self.assertTrue(np.allclose(clean.area_m2 * clean.price_per_m2_vnd, clean.sale_price_vnd))

    def test_detail_fields_never_override_core(self):
        record = self.row(**{"Diện tích đất:": "9999 m2", "Giá/m2:": "999 tỷ/m2"})
        clean, _, _, _ = p.clean_records([record])
        self.assertEqual(clean.iloc[0].area_m2, 100)
        self.assertEqual(clean.iloc[0].sale_price_vnd, 2e9)

    def test_conflict_is_quarantined(self):
        _, rejected, _, _ = p.clean_records([self.row(), self.row(title="Bán khác", area="200 m2")])
        self.assertIn("area_conflict_between_core_fields", rejected.iloc[0].rejection_reasons)

    def test_rental_income_and_mixed_status(self):
        self.assertEqual(p.classify_title("Bán nhà hiện đang cho thuê 30tr")[1], "sale_with_rental_income")
        self.assertEqual(p.classify_title("Cho thuê hoặc bán đất")[1], "ambiguous_mixed")
        self.assertEqual(p.classify_title("Cho thuê căn hộ cao cấp")[1], "rental")

    def test_geography_requires_explicit_valid_tokens(self):
        self.assertEqual(len(p.PROVINCES_2021), 63)
        for address in ("Đường Nguyễn Văn Bứa", "D6", "Duong go xoai", "ấp 4", "quận 8"):
            province, district, flags = p.parse_location(address)
            self.assertEqual(province, "Chưa xác định")
            self.assertEqual(district, "Chưa xác định")
            self.assertIn("unknown_province", flags)
        self.assertEqual(p.parse_location("Đường A, Quận 9, TP HCM.")[:2], ("Tp Hồ Chí Minh", "Quận 9"))
        self.assertEqual(p.parse_location("Đường A, tỉnh Long An")[:2], ("Long An", "Chưa xác định"))

    def test_kmeans_is_deterministic_and_finds_separated_clouds(self):
        rng = np.random.default_rng(7)
        x = np.r_[rng.normal(-3, .1, (40, 2)), rng.normal(3, .1, (40, 2))]
        a, ca, ia = p.kmeans(x, 2)
        b, cb, ib = p.kmeans(x, 2)
        np.testing.assert_array_equal(a, b)
        np.testing.assert_allclose(ca, cb)
        self.assertEqual(ia, ib)
        self.assertGreater(p.sampled_silhouette(x, a), .95)
        self.assertEqual(len(set(a[:40])), 1)
        self.assertNotEqual(a[0], a[-1])

    def test_iqr_flags_do_not_drop_records(self):
        rows = [self.row(title=f"Bán đất {i}", price=f"{1+i/100} tỷ- 100 m2", location="Huyện Đức Hòa, Long An") for i in range(40)]
        rows.append(self.row(title="Bán đất đặc biệt", price="100 tỷ- 100 m2", location="Huyện Đức Hòa, Long An"))
        clean, _, _, _ = p.clean_records(rows)
        flagged, bounds, _ = p.add_outlier_flags(clean)
        self.assertEqual(len(flagged), 41)
        self.assertTrue(flagged.iloc[-1].is_outlier_group)
        self.assertEqual(bounds.iloc[0].level, "province_type")

    def test_database_constraints_enforce_price_area_consistency(self):
        conn = sqlite3.connect(":memory:")
        conn.executescript(p.SCHEMA_SQL)
        conn.execute("INSERT INTO provinces VALUES (1, 'Long An')")
        conn.execute("INSERT INTO property_types VALUES (1, 'land')")
        values = (1, "hash", 1, 1, "Huyện Đức Hòa", "sale", 100., 1e9, 1e7, 0, 1)
        conn.execute("INSERT INTO listings VALUES (?,?,?,?,?,?,?,?,?,?,?)", values)
        self.assertEqual(conn.execute("PRAGMA integrity_check").fetchone()[0], "ok")
        with self.assertRaises(sqlite3.IntegrityError):
            conn.execute("UPDATE listings SET area_m2=0 WHERE row_id=1")
        with self.assertRaises(sqlite3.IntegrityError):
            conn.execute("UPDATE listings SET price_per_m2_vnd=1 WHERE row_id=1")
        with self.assertRaises(sqlite3.IntegrityError):
            conn.execute("UPDATE listings SET province_id=999 WHERE row_id=1")
        conn.close()

    def test_partition_stability_does_not_depend_on_label_names(self):
        self.assertEqual(p.adjusted_rand_index(np.array([0, 0, 1, 1]), np.array([9, 9, 3, 3])), 1)
        self.assertLess(p.adjusted_rand_index(np.array([0, 0, 1, 1]), np.array([0, 1, 0, 1])), 0)


if __name__ == "__main__":
    unittest.main()
