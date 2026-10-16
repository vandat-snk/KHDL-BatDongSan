"""Prepare report evidence from verified artifacts without regenerating analysis.

The assistant's text review is separate from human labels and from pipeline rules.
Run with the project's Python from any working directory.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import sqlite3
import statistics
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from verify_delivery import verify


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def read_csv(path):
    with (ROOT / path).open(encoding="utf-8-sig", newline="") as stream:
        return list(csv.DictReader(stream))


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def table(headers, rows):
    def escape(value):
        return str(value).replace("|", "/").replace("\n", " ")
    return "\n".join(["| " + " | ".join(map(escape, headers)) + " |",
                      "| " + " | ".join(["---"] * len(headers)) + " |"] +
                     ["| " + " | ".join(map(escape, row)) + " |" for row in rows])


# Authored after reading each sampled title/description. These are qualitative
# assistant interpretations, not outputs of an automatic classifier or gold labels.
REVIEW = """683|land|sale|ambiguous|200 m² cho hai lô; mô tả 670 triệu/lô: chưa biết giá thuộc một hay hai lô.
7164|house|sale|no_explicit_conflict|88 m²; 4,9 tỷ khớp nội dung.
709|house|sale|rounded_or_definition|60 so với 60,05 m²; 9,2 so với 9,19 tỷ: làm tròn.
6266|house|sale|ambiguous|58 m² so với kích thước 4×16: có thể khác định nghĩa diện tích.
4208|house|sale|no_explicit_conflict|140 m²; 23,85 tỷ khớp nội dung.
4167|land|sale|insufficient_evidence|10.000 m²; 1,05 tỷ chưa có xác nhận số độc lập trong mô tả.
6570|house|sale|ambiguous|63 m² so với kích thước 5×12: chưa biết diện tích nào được đo.
750|house|sale|rounded_or_definition|74 so với 73,2 m²; 4,199 tỷ.
2331|house|mixed_sale_rental|ambiguous|Tiêu đề bán hoạc cho thê: biến thể chính tả có thể bỏ lọt tín hiệu cho thuê.
7826|house|sale|insufficient_evidence|56 m²; 650 triệu chưa được mô tả xác nhận độc lập.
7103|land|sale|ambiguous|5×27=135 m²; 1,35 tỷ khớp lô chính nhưng mô tả nhiều sản phẩm.
3879|land|sale|no_explicit_conflict|50 m² × 60 triệu/m² = 3 tỷ; mức 59–60 triệu/m² là khoảng rao.
3589|house|sale|no_explicit_conflict|45 m²; 5 tầng; 3,95 tỷ khớp nội dung.
5900|apartment|sale|no_explicit_conflict|Mô tả chung cư, 65 m²; 2,7 tỷ. Tiêu đề viết C.Cư nên nhãn máy chưa rõ.
7485|land|sale|insufficient_evidence|570 triệu được nêu; 75 m² chưa xác nhận độc lập.
1802|house|sale|ambiguous|62 m² so với 4,5×15=67,5: định nghĩa diện tích chưa rõ.
4266|land|sale|no_explicit_conflict|100 m² thổ cư + 400 m² cây trồng = 500 m²; 2 tỷ.
4759|house|sale|no_explicit_conflict|Mô tả nhà ba tầng, 34 m²; 1,52 tỷ. Tiêu đề thiếu ký tự nhà.
5093|house|sale|conflict|Giá lõi 9,7 tỷ so với mô tả 9,9 tỷ; 5,2×20=104 m². Chưa biết giá đúng.
8387|land|sale|ambiguous|105 so với 5,4×19,5=105,3 m²; nhiều đề nghị trong mô tả.
6677|house|sale|no_explicit_conflict|Mô tả nhà bốn tầng 34 m²; 3,12 tỷ; nhãn máy chưa rõ.
7133|apartment|sale|ambiguous|61 m²; 22 triệu ở trường giá, tiêu đề thanh toán 300 triệu; chưa xác định giá tổng.
2980|land|sale|conflict|2.400 m², lõi 460 triệu; mô tả 360 triệu/1.000 m²: cơ sở giá mâu thuẫn.
4588|apartment|sale|ambiguous|Lõi 75 m²/2,65 tỷ; mô tả nhiều căn 57/68/87 m², kèm điều kiện thanh toán.
3696|house|sale|no_explicit_conflict|Mô tả một trệt ba lầu; 3,7×15=55,5 m²; 3,6 tỷ; nhãn máy chưa rõ.
1915|house|sale|no_explicit_conflict|Mô tả nhà 50 m², năm tầng; 4,1 tỷ; nhãn máy chưa rõ.
6181|house|sale|rounded_or_definition|90 m² đất, 67,5 m² xây dựng, 291 m² sàn: các khái niệm khác nhau.
8271|other_unknown|sale_assumed|insufficient_evidence|Căn ba phòng ngủ và view chưa đủ xác định chắc loại hình từ nội dung.
8773|house|sale|no_explicit_conflict|Villa 192 m²; 3 tỷ 260 triệu khớp 3,26 tỷ; nhãn máy chưa rõ.
634|land|sale|conflict|Hai lô, lõi 140 m²; mô tả 10×20=200 m²: chưa biết diện tích áp dụng.
8572|land|sale|no_explicit_conflict|20×60=1.200 m²; 1,8 tỷ; dấu chấm theo quy ước hàng nghìn.
3788|land|sale|rounded_or_definition|1.000 so với 1.004 m²; 19,5 tỷ: chênh lệch nhỏ nhưng giữ nguyên nguồn.
6510|land|sale|rounded_or_definition|1.860 so với 1.860,2 m²; kích thước gần đúng 46×40; 900 triệu.
3133|land|sale|rounded_or_definition|1.260 m² pháp lý và 1.450 m² hiện trạng; lõi dùng hiện trạng, không chứng thực pháp lý.
5906|land|sale|insufficient_evidence|1.023 m²; 350 triệu khớp tiêu đề, thiếu xác nhận bổ sung.
6469|land|sale|ambiguous|270 triệu/1.000 m²; mô tả nhiều lô 15×70, 20×50, 10×100.
3427|land|sale_assumed|ambiguous|1.000 m² so với 27×39=1.053; giá 3,1 tỷ; chưa rõ định nghĩa diện tích.
8107|land|sale|no_explicit_conflict|2,4 ha = 24.000 m²; 40 tỷ.
1071|land|sale|no_explicit_conflict|1.000 m² tổng; 100 m² thổ cư là thành phần; 340 triệu khớp tiêu đề.
8151|land|sale|conflict|Lõi 18.000 m²; mô tả 180.000 m² và một mẫu tám; không tự sửa số 0.
6244|house|sale|conflict|Giá lõi 3 triệu so với nội dung trên 3 tỷ.
7533|land|sale|conflict|33 triệu ở giá lõi; mô tả 33 triệu/m²: giá đơn vị khác giá tổng.
2123|land|sale|conflict|2,35 triệu so với 2,35 tỷ; 57 so với 57,1 m².
5517|land|sale|conflict|47 m² ở lõi so với 4 m² trong mô tả; chưa quyết định nguồn nào đúng.
8096|land|sale|ambiguous|360 triệu/sào, hai sào ba; không tự đổi sào thành m² khi thiếu quy ước địa phương.
8957|house|sale|conflict|16,6 tỷ so với 1,66 tỷ trong nội dung.
3739|apartment|sale|ambiguous|16,8–18,5 triệu/m², thêm phí/VAT; không xác định tổng giá từ trường giá lõi.
1437|land|sale|ambiguous|700 triệu/sào và diện tích 1.400 m²; giá theo sào chưa xác định tổng.
4288|land|sale|ambiguous|820 triệu/công; 1.000 m² so với 12×90; cách ly bảo thủ, chưa chứng minh giá tổng sai.
3008|house|sale|conflict|350 tỷ ở lõi so với 3,5 tỷ; mô tả diện tích 42/47 m².
5755|house|sale|conflict|8 triệu so với 800 triệu; 120 m² so với 12×10,5.
3111|land|sale|ambiguous|1,75 tỷ; mô tả nhiều lô từ 1,7 tỷ và trả góp: cách ly bảo thủ, chưa chứng minh giá sai.
78|land|sale|insufficient_evidence|3,2 triệu/60 m² ở lõi quá thấp theo ngưỡng; nội dung không cho phép sửa thành tỷ.
2512|land|sale|conflict|1,5 triệu so với 1,5 tỷ trong mô tả.
2604|house|sale|insufficient_evidence|2,6 triệu/50 m²; thiếu căn cứ chọn một tổng giá khác.
1140|land|sale|insufficient_evidence|3,15 triệu/560 m²; 11,5×50=575; thiếu tổng giá được xác nhận.
5418|house|mixed_sale_rental|conflict|Tiêu đề cho thuê, mô tả bán; 60 so với 59,2 m² đất và 108,2 m² sử dụng.
7452|land|sale|conflict|460.000 đồng so với 460 triệu trong mô tả.
8879|land|sale|ambiguous|720 ngàn/m² so với giá lõi 720.000 đồng; dấu số diện tích chưa rõ.
7363|land|sale|conflict|800.000 đồng so với 800 triệu; diện tích 280 so với 282 m².
"""


def main():
    verified = verify(require_workbook=True)
    a = read_json("outputs/analysis.json")
    if a['run_id'] != '20261016T015620Z-f2e661a6':
        raise ValueError('This authored review belongs to the 2026-10-16 snapshot. Review the text and examples before using another run.')
    records = read_csv("data/processed/listings_clean.csv")
    sample = read_csv("docs/MAU_KIEM_TRA_DU_LIEU.csv")
    assert all(row['run_id'] == a['run_id'] for row in sample)
    source = read_json("data/raw/chotot_data.json")
    reviewed = {}
    for line in REVIEW.strip().splitlines():
        rid, kind, transaction, consistency, note = line.split("|", 4)
        reviewed[int(rid)] = (kind, transaction, consistency, note)
    assert len(reviewed) == 60 and set(reviewed) == {int(r['row_id']) for r in sample}
    assert len(source) == a['counts']['raw_count']
    retained = {int(r['row_id']) for r in records}
    review_rows = []
    for row in sample:
        rid = int(row['row_id'])
        kind, transaction, consistency, note = reviewed[rid]
        review_rows.append(dict(run_id=a['run_id'], row_id=rid,
            sampling_group=row['sampling_group'], pipeline_state='retained' if rid in retained else 'quarantined',
            machine_property_type=row['machine_property_type'], assistant_property_type=kind,
            machine_transaction=row['machine_transaction'], assistant_transaction_interpretation=transaction,
            assistant_text_consistency=consistency, evidence_note=note,
            reviewer='Codex assistant; not a human gold label', reviewed_on='2026-10-16'))
    with (ROOT/'docs/DOI_CHIEU_60_TIN_TRO_LY.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(review_rows[0]));writer.writeheader();writer.writerows(review_rows)

    db=sqlite3.connect(f"{(ROOT/'outputs/real_estate.sqlite').as_uri()}?mode=ro",uri=True)
    independent={}
    for field, key in [('area_m2','median_area_m2'),('sale_price_vnd','median_price_vnd'),('price_per_m2_vnd','median_price_per_m2_vnd')]:
        csv_median=statistics.median(float(r[field]) for r in records)
        n=db.execute('SELECT COUNT(*) FROM listings').fetchone()[0]
        mid=db.execute(f'SELECT {field} FROM listings ORDER BY {field} LIMIT ? OFFSET ?', (2 if n%2==0 else 1,(n-1)//2)).fetchall()
        sql_median=statistics.mean(x[0] for x in mid)
        assert math.isclose(csv_median,sql_median,rel_tol=1e-12)
        assert math.isclose(csv_median,a['overall'][key],rel_tol=1e-12)
        independent[field]={'csv_statistics_median':csv_median,'sqlite_ordered_median':sql_median,'analysis_median':a['overall'][key]}
    queries=[]
    statement_buffer=''
    for line in (ROOT/'sql/02_queries.sql').read_text(encoding='utf-8').splitlines(keepends=True):
        statement_buffer += line
        if sqlite3.complete_statement(statement_buffer):
            queries.append(statement_buffer)
            statement_buffer=''
    assert len(queries) == 4, 'SQL demo must have four complete statements'
    benchmark=read_json('outputs/sql_benchmark.json')
    sql_evidence=[]
    for i,statement in enumerate(queries):
        if not statement.strip():continue
        cursor=db.execute(statement,benchmark['parameters'] if i==3 else ())
        if cursor.description is None:
            continue
        result=cursor.fetchall()
        result_hash=hashlib.sha256(json.dumps(result,separators=(',',':')).encode()).hexdigest()
        if i == 3:
            assert result_hash == benchmark['before']['result_sha256'] == benchmark['after']['result_sha256']
        sql_evidence.append({'query_number':i+1,'columns':[d[0] for d in cursor.description], 'result_count':len(result),
                             'result_sha256':result_hash,'first_five_rows':result[:5]})
    integrity=db.execute('PRAGMA integrity_check').fetchone()[0]
    foreign_keys=db.execute('PRAGMA foreign_key_check').fetchall()
    assert integrity=='ok' and not foreign_keys
    db.close()
    # Deliberately selected caution cases; not a representative estimate or a rule change.
    caution_ids={rid for rid,(_,_,status,_) in reviewed.items() if rid in retained and status in {'conflict','ambiguous'}} | ({8535}&retained)
    alternative=[r for r in records if int(r['row_id']) not in caution_ids]
    sensitivity={'scope':'Assistant-selected caution subset; illustrative sensitivity only; main outputs unchanged',
                 'excluded_row_ids':sorted(caution_ids),'n':len(alternative),
                 'median_price_vnd':statistics.median(float(r['sale_price_vnd']) for r in alternative),
                 'median_area_m2':statistics.median(float(r['area_m2']) for r in alternative),
                 'median_price_per_m2_vnd':statistics.median(float(r['price_per_m2_vnd']) for r in alternative)}
    inputs=['outputs/run_manifest.json','outputs/analysis.json','outputs/sql_benchmark.json','outputs/workbook_test_results.json',
            'docs/MAU_KIEM_TRA_DU_LIEU.csv','data/processed/listings_clean.csv','outputs/real_estate.sqlite']
    evidence={'checked_at_utc':datetime.now(timezone.utc).isoformat(),'core_run_id':a['run_id'],
        'scope':'Additional assistant checks and authored handover; not student completion or human label accuracy',
        'verified_delivery':verified,'independent_medians':independent,'read_only_sql_queries':sql_evidence,
        'assistant_review_rows':len(review_rows),'assistant_selected_sensitivity':sensitivity,
        'input_sha256':{p:sha(p) for p in inputs},'review_csv_sha256':sha('docs/DOI_CHIEU_60_TIN_TRO_LY.csv'),
        'tool_sha256':sha('tools/prepare_handover_evidence.py'),
        'not_verified':['Native Excel UI recalculation: UI actions failed to enter file path',
                        'Browser layout of the 6936-row version: file URL blocked by browser policy',
                        'Fresh pip installation on another machine','Human gold labels','Final six-chapter Word report']}
    (ROOT/'outputs/ASSISTANT_CHECKS.json').write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8')
    stamp=f"Ngày kiểm 16/10/2026; run_id `{a['run_id']}`. Người thực hiện: trợ lý Codex."
    def doc(name,body):
        (ROOT/'docs'/name).write_text(body.strip()+'\n',encoding='utf-8')

    doc('KET_QUA_KIEM_TRA_NHAN.md', f'''# Rà soát nội dung tin bằng trợ lý

{stamp}

Đã đọc tiêu đề và mô tả của 60 tin trong mẫu có sẵn, lưu diễn giải từng tin tại [CSV rà soát](DOI_CHIEU_60_TIN_TRO_LY.csv). Có 40 tin giữ và 20 tin cách ly. Sáu tầng lấy mười tin mỗi tầng; đây không phải mẫu ngẫu nhiên đồng tỷ lệ.

Đây là một lượt đọc bằng trợ lý, không phải hai người gán nhãn độc lập, không phải xác minh thực địa. Không điền thay các cột `human_*` trong mẫu gốc. Không tính precision/accuracy hoặc tỷ lệ lỗi toàn bộ dữ liệu từ mẫu này. `no_explicit_conflict` chỉ nghĩa chưa thấy mâu thuẫn rõ trong văn bản, không chứng thực giao dịch.

## Phát hiện cần nêu khi viết

| Dòng nguồn | Quan sát | Cách diễn giải |
| --- | --- | --- |
| 5900, 4759, 6677, 3696, 1915, 6181, 8773 | Mô tả có thể cung cấp loại hình mà tiêu đề viết tắt/thiếu từ | Nhãn chỉ từ tiêu đề có thể bỏ sót; chưa sửa thành bộ phân loại đã kiểm chứng |
| 2331 | Biến thể bán/cho thuê trong tiêu đề | Quy tắc từ khóa có thể bỏ lọt chính tả |
| 5093 | 9,7 tỷ so với 9,9 tỷ | Kiểm tra tỷ lệ chênh lớn không bắt mọi sai khác |
| 8151 | 18.000 so với 180.000 m² | Không tự chọn số đúng hoặc xóa một số 0 |
| 683, 2980, 7133, 4588 | Giá/lô, giá/diện tích hoặc điều kiện thanh toán | Giá tổng có thể chưa được xác định chắc chắn |
| 4288, 3111 | Bị cách ly theo chính sách bảo thủ | Không gọi là chứng minh tin sai/giả |
| 3133, 6181 | Đất, xây dựng, sàn, pháp lý, thực tế khác nhau | Không coi mọi diện tích trong cùng mô tả là cùng đại lượng |

Đã đọc thêm bảy tin trọng điểm ngoài mẫu: 638 (20 triệu/m² khác tổng giá), 7811 (860 tỷ so với 860 triệu), 335 (2 m² so với 2 ha), 8262 (3m2×5 là biểu thức kích thước chưa rõ), 300 (nhiều lô/diện tích), 588 (sang quán ngoài phạm vi), 8535 (6 m² so với mô tả 55/60 m²). Tin ngoài mẫu không được cộng vào mẫu 60 để tính tỷ lệ.

## Độ nhạy bổ sung

Thử loại riêng {len(caution_ids)} tin giữ được trợ lý chọn do nghi vấn giá/diện tích/giao dịch, gồm cả 8535 ngoài mẫu; còn {len(alternative)} tin. Trung vị diện tích {sensitivity['median_area_m2']:g} m²; giá {sensitivity['median_price_vnd']/1e9:.6g} tỷ; đơn giá {sensitivity['median_price_per_m2_vnd']/1e6:.8g} triệu/m². Danh sách ID và giá trị chưa làm tròn ở `outputs/ASSISTANT_CHECKS.json`.

Đây là phân tích tình huống có chủ đích, không phải sửa bộ dữ liệu chính hay ước lượng độ lệch. Chưa loại hết tin đáng ngờ. Trung vị ít thay đổi cũng không chứng minh nhãn từng tin đúng. Báo cáo phải giữ giới hạn này; chưa được khẳng định toàn bộ 6.936 tin đã xác minh.

Nhóm không bắt buộc đọc lại 60 tin. Nếu muốn công bố độ chính xác nhãn hoặc nghiên cứu riêng về bộ nhận diện, khi đó mới cần một thiết kế gán nhãn người thật độc lập.
''')

    doc('DOI_CHIEU_SO_LIEU_TRUC_QUAN.md', f'''# Đối soát số liệu và danh mục hình cho báo cáo

{stamp}

Đã đọc lại CSV bằng `csv` + `statistics` của Python và tính trung vị riêng bằng SQLite sắp thứ tự; cả hai khớp `analysis.json`. Kiểm toàn bộ bản ghi với JSON/DB/workbook do verifier thực hiện, không chỉ ba ô mẫu.

{table(['Biến', 'CSV / SQLite / analysis cùng giá trị', 'Đơn vị'], [(k, v['csv_statistics_median'], 'm²' if k=='area_m2' else 'VND/m²' if k=='price_per_m2_vnd' else 'VND') for k,v in independent.items()])}

9.004 = 1.884 trùng + 184 cách ly + 6.936 giữ. Loại IQR theo nhóm còn 6.676; chỉ tiêu đề bán rõ có 3.030; TP.HCM có 3.277; căn hộ TP.HCM có 239. Các trạng thái này đã được kiểm bằng JavaScript thực trong DOM mô phỏng; kiểm bố cục trình duyệt bản mới vẫn còn chờ.

## Dữ liệu minh họa kèm hình

{table(['Tên hình đề xuất', 'File ảnh trong outputs/charts', 'Bảng/dữ liệu đối chiếu'], [
('Hình: Phân bố tổng giá rao','01_price_distribution.png','listings_clean.csv: sale_price_vnd; 50 khoảng thang gốc và 35 khoảng log10, mỗi biểu đồ n=6.936'),
('Hình: Diện tích và giá rao','02_area_price_scatter.png','listings_clean.csv: area_m2, sale_price_vnd; hai trục log'),
('Hình: Trung vị đơn giá theo tỉnh','03_province_medians.png','outputs/tables/province_summary.csv; ghi n/ngưỡng mẫu'),
('Hình: Đơn giá theo loại suy luận','04_type_boxplot.png','listings_clean.csv: property_type, price_per_m2_vnd'),
('Hình: Độ phủ mẫu','05_sample_coverage.png','province_summary.csv; số tin không phải thị phần'),
('Hình: Độ nhạy chính sách','06_cleaning_sensitivity.png','outputs/tables/sensitivity.csv'),
('Hình: Phân nhóm thăm dò','07_exploratory_clusters.png','cluster_summary.csv và listings_clean.csv: cluster'),
('Hình: Tương quan Spearman','08_spearman_correlation.png','outputs/analysis.json: spearman')])}

Đánh lại số Hình/Bảng thống nhất theo thứ tự xuất hiện trong báo cáo. Mỗi hình phải có bảng số hoặc dữ liệu minh họa, nguồn, đơn vị, n và bộ lọc. Hình scatter tĩnh và scatter dashboard có thể dùng mẫu vẽ khác nhau; KPI dùng toàn bộ mẫu lọc. Không diễn giải số điểm trên ảnh là tổng số tin.

## Kịch bản demo gọn

1. Nêu nguồn v2 năm 2021 và mục tiêu khám phá giá rao lịch sử; mở `references/DATA_SOURCE.md`.
2. Nêu bảng 9.004 → 6.936 và ví dụ cách ly 638; mở lineage và CSV rà soát.
3. Mở dashboard, tải lại trang, xác nhận 6.936 / 2,25 tỷ / 32,3 triệu/m² / 70 m²; chọn TP.HCM rồi căn hộ: 239 tin. Đặt lại bộ lọc, bỏ IQR: 6.676 tin. Xuất CSV và nêu điều kiện lọc.
4. Mở workbook: ba trang/bốn biểu đồ; giải thích công thức và các cột snapshot. Không dùng thay đổi ô Excel để khẳng định đã chạy lại K-means.
5. Giải thích k=2 và 6.676 tin fit; mở bảng trials. Chạy SQL theo README và nêu kết quả benchmark thật.
6. Kết thúc bằng ứng dụng học tập/phân tích mẫu, chưa dùng định giá thị trường hoặc khuyến nghị đầu tư.

Ảnh dashboard đưa vào bản nộp cần chụp thực tế từ bản cuối. Không tạo ảnh giả thay bằng chứng vận hành. Có thể dùng tám hình dữ liệu đã có, kèm bảng trên, để viết phần phân tích ngay.
''')

    c=a['clustering']
    doc('THUC_NGHIEM_KMEANS_VA_SQL.md', f'''# Bằng chứng K-means và SQL đã chuẩn bị

{stamp}

## K-means: kết quả đã có của lần chạy chính

Mã: `src/pipeline.py`, các hàm `kmeans`, `sampled_silhouette`, `adjusted_rand_index`, `cluster_records`. NumPy thực hiện khởi tạo K-means++ và vòng Lloyd; không chỉ vẽ cụm bằng tay.

Đặc trưng là ln(diện tích m²), ln(đơn giá VND/m²), sau đó Z-score với độ lệch chuẩn tổng thể. Đơn giá được tính từng tin bằng giá tổng chia diện tích. Fit {c['fit_count']} tin, loại {c['excluded_group_outliers']} cờ IQR nhóm khỏi fit; EDA mặc định vẫn giữ các tin này. Seed {c['seed']}, mười lần khởi tạo, tối đa 150 vòng; silhouette lấy mẫu {c['silhouette_sample_size']}.

Trung bình log: {c['log_means']}; độ lệch chuẩn: {c['log_std']}. Cần giữ scaler cùng phiên bản đầu vào, không đổi đơn vị mà dùng scaler cũ.

{table(['k','silhouette mẫu','inertia','cụm nhỏ nhất'],[(r['k'],r['silhouette_sample'],r['inertia'],r['min_cluster_size']) for r in c['trials']])}

Chọn k={c['chosen_k']} theo kết quả khảo sát này. Inertia giảm khi thêm cụm nên không dùng riêng inertia để kết luận k tốt nhất. Seed 7 và 42 có ARI=1 với kết quả chính; đây là ổn định của phép chia trên cùng dữ liệu/thiết lập, không phải accuracy hay kiểm định nhãn thị trường.

{table(['Cụm','n','Trung vị diện tích m²','Giá tỷ VND','Đơn giá triệu VND/m²'],[(r['cluster'],r['n'],r['median_area_m2'],r['median_price_vnd']/1e9,r['median_price_per_m2_vnd']/1e6) for r in c['summary']])}

Ví dụ Lloyd để học, KHÔNG phải kết quả dữ liệu thật: bốn điểm trong không gian đầu vào giả định (−1;−1), (−1;0), (1;0), (1;1), hai tâm đầu (−1;−1),(1;1). Gán hai điểm đầu vào cụm 1, hai điểm sau vào cụm 2; tâm cập nhật (−1;−0,5),(1;0,5); gán lại không đổi và tổng bình phương khoảng cách bằng 1. Dấu chấm phẩy ngăn tọa độ, dấu phẩy là thập phân. Ví dụ chỉ minh họa Lloyd, không mô phỏng bước log/Z-score của dữ liệu thật. Khi đưa công thức vào Word dùng Equation, giải thích khoảng cách Euclid và trung bình theo từng tọa độ.

## SQL: kiểm đọc lại độc lập

Ba bảng `provinces`, `property_types`, `listings`; khóa ngoại từ listings, UNIQUE ID, CHECK diện tích dương, giá tối thiểu, đơn giá dương và giá ≈ diện tích × đơn giá. SQLite phải bật `PRAGMA foreign_keys=ON` trên mỗi kết nối có ghi. Chế độ đọc kiểm này dùng `mode=ro`, không đổi database chuẩn.

Đã thực thi bốn truy vấn `sql/02_queries.sql`; số dòng trả về lần lượt {[q['result_count'] for q in sql_evidence]}. Năm dòng đầu mỗi kết quả và tên cột được lưu trong `outputs/ASSISTANT_CHECKS.json`. Toàn vẹn: `{integrity}`; lỗi khóa ngoại: {foreign_keys}. AVG trong SQL là trung bình, không được ghi nhãn trung vị. Ba trung vị đã tính độc lập bằng ORDER BY và đối chiếu CSV.

Benchmark nguồn: `outputs/sql_benchmark.json`; cùng truy vấn, tham số {benchmark['parameters']}, LIMIT 100. Trước: quét bảng và B-tree tạm; sau: `idx_listings_search(province_id,type_id,price_per_m2_vnd,row_id)`, tận dụng cột bằng trước cột khoảng/sắp xếp. Hai tập 100 kết quả có cùng SHA `{benchmark['before']['result_sha256']}`.

{table(['Trạng thái','Trung vị ms','P10 ms','P90 ms'],[(key,benchmark[key]['median_ms'],benchmark[key]['p10_ms'],benchmark[key]['p90_ms']) for key in ['before','after']])}

Tỷ số trước/sau {benchmark['median_speedup']:.6g}; lần này độ trễ trung vị không cải thiện. Không chạy lại để chọn con số đẹp. Quy trình có 10 warmup, 51 lượt đo mỗi pha, tuần tự warm-cache, không ngẫu nhiên hóa, dữ liệu nhỏ. Kết luận có thể chứng minh đổi kế hoạch truy vấn và bảo toàn kết quả; chưa chứng minh tăng tốc ứng dụng thực tế. Index còn có chi phí ghi/lưu trữ.

Nhóm chỉ cần đọc, giải thích và dẫn chứng; không bị giao chạy lại thí nghiệm này như một nhiệm vụ chưa làm.
''')
    print(json.dumps({'status':'prepared','core_run_id':a['run_id'],'assistant_review_rows':60,'independent_medians':'matched','sql_queries':len(sql_evidence),'caution_sensitivity':sensitivity},ensure_ascii=False,indent=2))
    return 0


if __name__=='__main__':
    raise SystemExit(main())
