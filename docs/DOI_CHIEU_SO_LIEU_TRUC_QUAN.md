# Đối soát số liệu và danh mục hình cho báo cáo

Ngày kiểm 16/10/2026; run_id `20261016T015620Z-f2e661a6`. Người thực hiện: trợ lý Codex.

Đã đọc lại CSV bằng `csv` + `statistics` của Python và tính trung vị riêng bằng SQLite sắp thứ tự; cả hai khớp `analysis.json`. Kiểm toàn bộ bản ghi với JSON/DB/workbook do verifier thực hiện, không chỉ ba ô mẫu.

| Biến | CSV / SQLite / analysis cùng giá trị | Đơn vị |
| --- | --- | --- |
| area_m2 | 70.0 | m² |
| sale_price_vnd | 2250000000.0 | VND |
| price_per_m2_vnd | 32320512.82051282 | VND/m² |

9.004 = 1.884 trùng + 184 cách ly + 6.936 giữ. Loại IQR theo nhóm còn 6.676; chỉ tiêu đề bán rõ có 3.030; TP.HCM có 3.277; căn hộ TP.HCM có 239. Các trạng thái này đã được kiểm bằng JavaScript thực trong DOM mô phỏng; kiểm bố cục trình duyệt bản mới vẫn còn chờ.

## Dữ liệu minh họa kèm hình

| Tên hình đề xuất | File ảnh trong outputs/charts | Bảng/dữ liệu đối chiếu |
| --- | --- | --- |
| Hình: Phân bố tổng giá rao | 01_price_distribution.png | listings_clean.csv: sale_price_vnd; 50 khoảng thang gốc và 35 khoảng log10, mỗi biểu đồ n=6.936 |
| Hình: Diện tích và giá rao | 02_area_price_scatter.png | listings_clean.csv: area_m2, sale_price_vnd; hai trục log |
| Hình: Trung vị đơn giá theo tỉnh | 03_province_medians.png | outputs/tables/province_summary.csv; ghi n/ngưỡng mẫu |
| Hình: Đơn giá theo loại suy luận | 04_type_boxplot.png | listings_clean.csv: property_type, price_per_m2_vnd |
| Hình: Độ phủ mẫu | 05_sample_coverage.png | province_summary.csv; số tin không phải thị phần |
| Hình: Độ nhạy chính sách | 06_cleaning_sensitivity.png | outputs/tables/sensitivity.csv |
| Hình: Phân nhóm thăm dò | 07_exploratory_clusters.png | cluster_summary.csv và listings_clean.csv: cluster |
| Hình: Tương quan Spearman | 08_spearman_correlation.png | outputs/analysis.json: spearman |

Đánh lại số Hình/Bảng thống nhất theo thứ tự xuất hiện trong báo cáo. Mỗi hình phải có bảng số hoặc dữ liệu minh họa, nguồn, đơn vị, n và bộ lọc. Hình scatter tĩnh và scatter dashboard có thể dùng mẫu vẽ khác nhau; KPI dùng toàn bộ mẫu lọc. Không diễn giải số điểm trên ảnh là tổng số tin.

## Kịch bản demo gọn

1. Nêu nguồn v2 năm 2021 và mục tiêu khám phá giá rao lịch sử; mở `references/DATA_SOURCE.md`.
2. Nêu bảng 9.004 → 6.936 và ví dụ cách ly 638; mở lineage và CSV rà soát.
3. Mở dashboard, tải lại trang, xác nhận 6.936 / 2,25 tỷ / 32,3 triệu/m² / 70 m²; chọn TP.HCM rồi căn hộ: 239 tin. Đặt lại bộ lọc, bỏ IQR: 6.676 tin. Xuất CSV và nêu điều kiện lọc.
4. Mở workbook: ba trang/bốn biểu đồ; giải thích công thức và các cột snapshot. Không dùng thay đổi ô Excel để khẳng định đã chạy lại K-means.
5. Giải thích k=2 và 6.676 tin fit; mở bảng trials. Chạy SQL theo README và nêu kết quả benchmark thật.
6. Kết thúc bằng ứng dụng học tập/phân tích mẫu, chưa dùng định giá thị trường hoặc khuyến nghị đầu tư.

Ảnh dashboard đưa vào bản nộp cần chụp thực tế từ bản cuối. Không tạo ảnh giả thay bằng chứng vận hành. Có thể dùng tám hình dữ liệu đã có, kèm bảng trên, để viết phần phân tích ngay.
