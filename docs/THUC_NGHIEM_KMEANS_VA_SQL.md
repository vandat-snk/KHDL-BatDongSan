# Bằng chứng K-means và SQL đã chuẩn bị

Ngày kiểm 16/10/2026; run_id `20261016T015620Z-f2e661a6`. Người thực hiện: trợ lý Codex.

## K-means: kết quả đã có của lần chạy chính

Mã: `src/pipeline.py`, các hàm `kmeans`, `sampled_silhouette`, `adjusted_rand_index`, `cluster_records`. NumPy thực hiện khởi tạo K-means++ và vòng Lloyd; không chỉ vẽ cụm bằng tay.

Đặc trưng là ln(diện tích m²), ln(đơn giá VND/m²), sau đó Z-score với độ lệch chuẩn tổng thể. Đơn giá được tính từng tin bằng giá tổng chia diện tích. Fit 6676 tin, loại 260 cờ IQR nhóm khỏi fit; EDA mặc định vẫn giữ các tin này. Seed 20261015, mười lần khởi tạo, tối đa 150 vòng; silhouette lấy mẫu 1000.

Trung bình log: [4.479549822987997, 16.95778661256449]; độ lệch chuẩn: [1.0808908075842054, 1.4597753825359123]. Cần giữ scaler cùng phiên bản đầu vào, không đổi đơn vị mà dùng scaler cũ.

| k | silhouette mẫu | inertia | cụm nhỏ nhất |
| --- | --- | --- | --- |
| 2 | 0.6231025757482119 | 6277.213200241327 | 961 |
| 3 | 0.4735672438790726 | 3852.476617826341 | 456 |
| 4 | 0.39393035208081195 | 2983.807390074934 | 306 |
| 5 | 0.37942034448803824 | 2465.1049285179347 | 122 |

Chọn k=2 theo kết quả khảo sát này. Inertia giảm khi thêm cụm nên không dùng riêng inertia để kết luận k tốt nhất. Seed 7 và 42 có ARI=1 với kết quả chính; đây là ổn định của phép chia trên cùng dữ liệu/thiết lập, không phải accuracy hay kiểm định nhãn thị trường.

| Cụm | n | Trung vị diện tích m² | Giá tỷ VND | Đơn giá triệu VND/m² |
| --- | --- | --- | --- | --- |
| 1 | 961 | 500.0 | 0.88 | 2.3 |
| 2 | 5715 | 63.0 | 2.35 | 39.189189189189186 |

Ví dụ Lloyd để học, KHÔNG phải kết quả dữ liệu thật: bốn điểm trong không gian đầu vào giả định (−1;−1), (−1;0), (1;0), (1;1), hai tâm đầu (−1;−1),(1;1). Gán hai điểm đầu vào cụm 1, hai điểm sau vào cụm 2; tâm cập nhật (−1;−0,5),(1;0,5); gán lại không đổi và tổng bình phương khoảng cách bằng 1. Dấu chấm phẩy ngăn tọa độ, dấu phẩy là thập phân. Ví dụ chỉ minh họa Lloyd, không mô phỏng bước log/Z-score của dữ liệu thật. Khi đưa công thức vào Word dùng Equation, giải thích khoảng cách Euclid và trung bình theo từng tọa độ.

## SQL: kiểm đọc lại độc lập

Ba bảng `provinces`, `property_types`, `listings`; khóa ngoại từ listings, UNIQUE ID, CHECK diện tích dương, giá tối thiểu, đơn giá dương và giá ≈ diện tích × đơn giá. SQLite phải bật `PRAGMA foreign_keys=ON` trên mỗi kết nối có ghi. Chế độ đọc kiểm này dùng `mode=ro`, không đổi database chuẩn.

Đã thực thi bốn truy vấn `sql/02_queries.sql`; số dòng trả về lần lượt [20, 4, 20, 100]. Năm dòng đầu mỗi kết quả và tên cột được lưu trong `outputs/ASSISTANT_CHECKS.json`. Toàn vẹn: `ok`; lỗi khóa ngoại: []. AVG trong SQL là trung bình, không được ghi nhãn trung vị. Ba trung vị đã tính độc lập bằng ORDER BY và đối chiếu CSV.

Benchmark nguồn: `outputs/sql_benchmark.json`; cùng truy vấn, tham số [38, 2, 33911924.93946731, 78358108.1081081], LIMIT 100. Trước: quét bảng và B-tree tạm; sau: `idx_listings_search(province_id,type_id,price_per_m2_vnd,row_id)`, tận dụng cột bằng trước cột khoảng/sắp xếp. Hai tập 100 kết quả có cùng SHA `adee9406ef35f1fbe5221ae1093158eaef954f3b948b39cd5e953245ffff1e1b`.

| Trạng thái | Trung vị ms | P10 ms | P90 ms |
| --- | --- | --- | --- |
| before | 0.6484 | 0.5834 | 1.0437 |
| after | 0.7788 | 0.1976 | 1.3754 |

Tỷ số trước/sau 0.832563; lần này độ trễ trung vị không cải thiện. Không chạy lại để chọn con số đẹp. Quy trình có 10 warmup, 51 lượt đo mỗi pha, tuần tự warm-cache, không ngẫu nhiên hóa, dữ liệu nhỏ. Kết luận có thể chứng minh đổi kế hoạch truy vấn và bảo toàn kết quả; chưa chứng minh tăng tốc ứng dụng thực tế. Index còn có chi phí ghi/lưu trữ.

Nhóm chỉ cần đọc, giải thích và dẫn chứng; không bị giao chạy lại thí nghiệm này như một nhiệm vụ chưa làm.
