# Phân công tiếp quản, kiểm chứng và phát triển đồ án

Cập nhật 16/10/2026. Tài liệu này thay toàn bộ phân công/dàn ý cũ; báo cáo theo sáu chương giảng viên yêu cầu.

Đề tài: **Phân tích giá rao bất động sản Việt Nam**. Mục tiêu duy nhất: xây dựng quy trình có thể chạy lại để khám phá và so sánh giá rao trong mẫu tin lịch sử sau kiểm tra chất lượng. Làm sạch, trực quan, K-means và SQL cùng phục vụ mục tiêu này.

## 1. Trách nhiệm và cách ghi nhận đóng góp

Mã và sản phẩm hiện có do trợ lý chuẩn bị, sửa và kiểm tra. Giao một phần cho thành viên là giao trách nhiệm học, tiếp quản, tự kiểm chứng, bảo trì và cải tiến; không ghi ngược rằng thành viên đã tự hoàn thành phần đó trước khi thực hiện.

Ba trạng thái phải tách rõ: **bản nền đã có → thành viên tự kiểm chứng → cải tiến được nghiệm thu**. Hiện chưa tự xác nhận bước hai/ba cho ai. Không lấy kế hoạch làm thành tích; đóng góp cuối được chứng minh bằng commit, tài liệu, log, đọc chéo và khả năng giải thích, không tự gán 33,33% đã hoàn thành.

| Thành viên | Trách nhiệm chính | Chủ trì viết | Kiểm chéo |
|---|---|---|---|
| Võ Văn Đạt — N23DCCN078 | Tích hợp, thuật toán, database/SQL, kiểm thử và phiên bản | Chương 3–4 | Nhi kiểm dữ liệu/DB; Quỳnh kiểm luồng sử dụng |
| Nguyễn Thị Yến Nhi — N23DCCN112 | Nguồn, từ điển, làm sạch, nhãn, lý thuyết và giới hạn | Chương 1–2 | Đạt kiểm kỹ thuật/công thức; Quỳnh kiểm cách giải thích |
| Hứa Như Quỳnh — N23DCCN118 | EDA, dashboard, Excel, nghiệm thu, demo và trình bày | Chương 5–6; ghép định dạng | Đạt kiểm số; Nhi kiểm diễn giải và giới hạn |

Đạt cung cấp lý thuyết NumPy/SQLite/tích hợp cho Nhi viết Chương 2; Nhi cung cấp từ điển/quy tắc cho Đạt viết Chương 3–4; Quỳnh cung cấp thiết kế giao diện và ví dụ vận hành cho Đạt. Cả ba duyệt kết luận; không viết ba phần độc lập rồi ghép máy móc.

## 2. Phân toàn bộ công việc trợ lý đã làm để tiếp quản

Mốc đối chiếu `20261016T015620Z-f2e661a6`: 9.004 dòng nguồn, 1.884 trùng, 184 cách ly, 6.936 giữ; 29 test Python đạt. Đây là kết quả một phiên bản, không phải hằng số cần ép các lần chạy sau khớp.

| Bản nền đã có | File/sản phẩm để học và tiếp quản | Chính; phối hợp |
|---|---|---|
| Chọn nguồn công khai; metadata, giấy phép, checksum; đối chiếu slide/đăng ký | `scripts/download_data.py`, metadata/manifest trong `data/raw`, `references/DATA_SOURCE.md`, `DOI_CHIEU_SLIDE.md`, `registration.json` | Nhi; Đạt vận hành tải |
| Chuẩn hóa Unicode, số/đơn vị giá/diện tích/địa phương; khôi phục diện tích được ghi rõ trong chuỗi giá | `normalize`, `parse_number`, `parse_area`, `parse_price`, `parse_location` trong `src/pipeline.py` | Nhi; Đạt hỗ trợ sửa mã |
| Suy luận loại hình/giao dịch; phát hiện mâu thuẫn nội dung và chuyển nhượng hoạt động kinh doanh | `classify_title`, `clean_records`, `src/source_checks.py` | Nhi |
| Gộp trùng năm trường; cách ly có lý do và truy nguyên dòng | `data/processed/listings_clean.*`, `listings_rejected.csv`, `row_lineage.csv`, `tools/audit_source_changes.py` | Nhi; Đạt tích hợp |
| IQR, độ nhạy, trung vị, Spearman, bootstrap, tổng hợp theo tỉnh/loại/diện tích | `add_outlier_flags`, `summarize_groups`, `sensitivity_table`, `outputs/analysis.json`, `outputs/tables` | Nhi phụ trách chính sách/giả định; Quỳnh đối soát/diễn giải |
| Code NumPy K-means++/Lloyd; log/Z-score, k=2–5, silhouette và ARI theo seed | `kmeans`, `sampled_silhouette`, `adjusted_rand_index`, `cluster_records`; bảng `cluster_*` | Đạt; Nhi kiểm đầu vào |
| Database ba bảng, khóa/ràng buộc, SQL, index, benchmark, kiểm toàn vẹn | `build_database`, `sql/01_schema.sql`, `02_queries.sql`, `03_indexes.sql`, `scripts/demo_sql.py`, `outputs/real_estate.sqlite`, `sql_benchmark.json` | Đạt; Nhi kiểm kết quả |
| Tám hình Matplotlib có dữ liệu/đơn vị | `make_charts`, `outputs/charts/01_*` đến `08_*` | Quỳnh; Nhi kiểm thống kê, Đạt hỗ trợ mã |
| Dashboard ngoại tuyến: KPI, lọc, rỗng, phân trang/tìm kiếm, CSV, lấy mẫu scatter; mở bằng trình duyệt | `src/dashboard_template.html`, `tools/build_dashboard.py`, `outputs/DASHBOARD_BAT_DONG_SAN.html`, `MO_DASHBOARD.cmd` | Quỳnh |
| Excel ba trang/bốn biểu đồ; công thức đơn giá/tổng hợp; thử sửa đầu vào, rà lỗi | `tools/build_workbook.mjs`, `outputs/DO_AN_BAT_DONG_SAN.xlsx`, `workbook_build.json`, `workbook_test_results.json` | Quỳnh; Đạt hỗ trợ môi trường dựng |
| Kiểm đúng nguồn; hash mã/đầu ra; staging, giữ byte khi Git checkout và phát hiện sản phẩm cũ | `src/artifact_contract.py`, `.gitattributes`, `main`/`generate_outputs`, `outputs/run_manifest.json`, các `*_build.json` | Đạt |
| Lệnh chạy thống nhất, verifier đối soát, bản sao chỉ có nguồn | `scripts/run_project.py`, `tools/verify_delivery.py`, `tools/check_portability.py`, README, `AUDIT_RESULTS.json`, `DELIVERY_CHECK.json`, `portability_check.json` | Đạt |
| Test parser/làm sạch/toán phân cụm/CSDL/provenance/dashboard | `tests/test_pipeline.py`, `test_source_checks.py`: Nhi/Đạt; `test_artifact_contract.py`: Đạt; `test_dashboard.mjs`: Quỳnh | Đạt điều phối; mỗi người bảo trì test phần mình |
| Mẫu 60 tin; nhật ký UI; bằng chứng ảnh và giới hạn xác nhận | `tools/create_manual_review.py`, `docs/MAU_KIEM_TRA_DU_LIEU.csv`, `KIEM_THU_THUC_TE.md`, `outputs/visual_review.json` | Nhi điều phối nhãn; Quỳnh điều phối UI; cả ba kiểm tin |
| Biên bản rà soát, ma trận sáu chương, phân công, bàn giao và kịch bản | `docs/RA_SOAT_KY_THUAT.md`, `DOI_CHIEU_YEU_CAU_BAO_CAO.md`, tài liệu này, `BAN_GIAO_VA_KIEM_TRA.md`, `KICH_BAN_THUYET_TRINH_VA_HOI_DAP.md` | Nhi kiểm nội dung; Đạt kiểm kỹ thuật; Quỳnh ghép/định dạng |
| Trích xuất slide, dựng/xuất bản thảo cũ và ảnh biểu đồ | `tools/extract_course.py`, `build_report.py`, `render_report_with_word.ps1`, `render_dashboard_charts.mjs`, `docs/BAO_CAO_DO_AN.*` | Đạt tiếp quản công cụ; Quỳnh tiếp quản trình bày. Bản thảo cũ chưa dùng nộp; bộ dựng cũ đã khóa chạy trực tiếp |

## 3. Võ Văn Đạt: công việc cụ thể

Slide trọng tâm: Z-score Chương 2; K-means Chương 4 phần 2; quan hệ, khóa, SQL/index Chương 5. Trang cụ thể theo `references/DOI_CHIEU_SLIDE.md`.

| Mã | Nhiệm vụ | Bàn giao và nghiệm thu | Người kiểm |
|---|---|---|---|
| D01 | Clone thư mục riêng hoặc dùng máy khác; tạo môi trường Python, tải đúng nguồn và chạy theo README | `docs/NGHIEM_THU_MOI_TRUONG.md`: môi trường thực, lệnh/log, mã thoát, run_id, phần chạy/bỏ qua. Không gọi bản sao cùng Python là đã cài trên máy khác | Nhi thực hiện lại tải/kiểm và một truy vấn |
| D02 | Đọc luồng điều khiển; vẽ kiến trúc, luồng dữ liệu và ERD ba bảng; mô tả từng mô-đun | `docs/THIET_KE_VA_MODULE.md`: sơ đồ khớp code, ví dụ một dòng đi qua hệ thống, hợp đồng dữ liệu, hash/staging/lỗi; không dựng phân quyền chưa có | Nhi đối chiếu quy tắc; Quỳnh đối chiếu demo |
| D03 | Tự giải thích K-means và làm một vòng lặp tay trên ví dụ nhỏ ghi rõ chỉ để minh họa | `docs/THUC_NGHIEM_KMEANS.md`: biến/log/Z-score/Euclid/tâm/dừng, k/inertia/silhouette/n, seed/ARI, đặc điểm cụm ở đơn vị gốc; phân biệt thí nghiệm mới với kết quả đã có | Nhi kiểm mẫu/giả định; Quỳnh kiểm hình |
| D04 | Mở DB, chạy bốn truy vấn, đọc plan và so kết quả trước/sau index | `docs/THUC_NGHIEM_SQL.md`: schema, SQL/tham số, kết quả/hash, plan, thời gian phân tán, môi trường. Giữ cả kết quả không nhanh hơn; dữ liệu thử tải phải ghi riêng | Nhi chạy lại truy vấn và đối chiếu CSV |
| D05 | Tích hợp thay đổi đã review; dựng đầu ra và kiểm bản cuối | Log/commit, test phù hợp, `AUDIT_RESULTS.json` cùng run_id; Excel dựng/đối soát hoặc ghi rõ chưa cập nhật. Không sửa manifest bằng tay | Nhi kiểm dữ liệu; Quỳnh kiểm UI/Excel |
| D06 | Viết Chương 3–4; cung cấp phần kỹ thuật cho Nhi viết Chương 2 | Thiết kế khớp mã/DB; mỗi mô-đun có file/hàm, đầu vào, bước xử lý, đầu ra, lỗi, ví dụ; mã đầy đủ ở repo | Nhi và Quỳnh đọc chéo |

Đạt còn kiểm 20 tin và đọc chéo 20 tin theo Mục 6.

## 4. Nguyễn Thị Yến Nhi: công việc cụ thể

Slide trọng tâm: ý nghĩa/phạm vi KHDL Chương 1; thiếu/nhiễu/không nhất quán/ngoại lệ, biến đổi, lấy mẫu và chọn thuộc tính Chương 2. IQR, bootstrap, silhouette/ARI cần giải thích và tài liệu bổ sung khi sử dụng.

| Mã | Nhiệm vụ | Bàn giao và nghiệm thu | Người kiểm |
|---|---|---|---|
| N01 | Xác minh DOI/v2/tác giả/giấy phép/metadata; đơn vị quan sát; chênh lệch mô tả 10.000 với 9.004 dòng; lý do bỏ trường chi tiết nghi lan truyền | `docs/NGUON_VA_TU_DIEN_DU_LIEU.md`: từ điển cột, kiểu/đơn vị/nguồn/giới hạn, ví dụ thực và trích dẫn | Đạt kiểm checksum; Quỳnh đọc như người mới |
| N02 | Lập bảng đầy đủ quy tắc làm sạch và hàm tương ứng | `docs/QUY_TAC_VA_VI_DU_DU_LIEU.md`: trước/sau, lý do, số tin tác động có thể chồng nhau, ví dụ dễ loại nhầm; đối soát nguồn = trùng + cách ly + giữ | Quỳnh truy nguyên 10 ví dụ; Đạt kiểm hàm |
| N03 | Điều phối nhãn 60 tin; tự kiểm phần mình; tập hợp và giải quyết bất đồng | CSV có hai lượt đọc; `docs/KET_QUA_KIEM_TRA_NHAN.md`: đồng thuận/bất đồng/không đủ bằng chứng theo nhóm; không dùng regex điền nhãn rồi gọi là người kiểm | Cả hai bạn ký phần thực kiểm |
| N04 | Đọc sensitivity; phân biệt cách ly mâu thuẫn với IQR giữ trong EDA; rà thêm tin 638, 7811, 335, 8262, 300, 588, 8535 | Bảng quyết định và cụm số/chữ minh họa; ghi chưa xác minh khi còn mơ hồ; so n/trung vị khi đổi điều kiện | Đạt tính lại; Quỳnh kiểm diễn giải |
| N05 | Khi có lỗi thật, mô tả lỗi trước, phối hợp sửa parser/nhận diện và bổ sung hồi quy cả trường hợp không được loại nhầm | Commit/test và bảng chuyển trạng thái có lý do; Đạt dựng lại đầu ra. Không sửa raw hoặc tự đặt lại giá suy đoán | Đạt review mã; Quỳnh đối soát KPI |
| N06 | Viết Chương 1–2; cung cấp quy tắc/từ điển cho Chương 3–4 | Chương 1 đủ thực tiễn/nghiên cứu/một mục tiêu/phạm vi ứng dụng; Chương 2 có cơ chế kỹ thuật, công thức đọc được, tham số, ví dụ gắn với code | Đạt kiểm kỹ thuật/công thức; Quỳnh kiểm lập luận |

## 5. Hứa Như Quỳnh: công việc cụ thể

Slide trọng tâm: Chương 3 về cột/scatter/histogram/nhãn/chú thích; Chương 2 về tổng hợp/tạo biến; Chương 1 về truyền đạt và tư duy phản biện. Phân biệt histogram với cột đếm khoảng giá không đều.

| Mã | Nhiệm vụ | Bàn giao và nghiệm thu | Người kiểm |
|---|---|---|---|
| Q01 | Đọc tám hình/bảng gốc, xác định câu hỏi mỗi hình; tính độc lập n và ít nhất ba trung vị từ CSV | `docs/DOI_CHIEU_SO_LIEU_TRUC_QUAN.md`: bộ lọc, mẫu số, giá trị gốc/hiển thị, sai số; không kết luận diện tích lớn giá cao nếu số không hỗ trợ | Đạt tính lại; Nhi kiểm giới hạn |
| Q02 | Mở trình duyệt thật, thực hiện NEW01–NEW07 trong nhật ký UI; kiểm lọc/tìm/CSV/phân trang/rỗng khi giao diện cho phép | Cập nhật `docs/KIEM_THU_THUC_TE.md`: người/ngày/run_id, mong đợi/thực tế, ảnh có bộ lọc. Trạng thái không tạo được qua UI chỉ ghi test tự động, không dựng thao tác giả | Đạt đối soát CSV; Nhi kiểm mẫu số |
| Q03 | Mở Excel thật, kiểm ba trang/bốn biểu đồ/lọc/sắp xếp; trên bản sao tạm thử đổi giá/diện tích và ô trống/0/chữ | `docs/NGHIEM_THU_EXCEL.md`: công thức/số trước-sau, hiểu IQR/cụm snapshot; không lưu đè workbook chuẩn bằng dữ liệu thử | Đạt kiểm công thức; Nhi kiểm ngữ nghĩa |
| Q04 | Lập demo nguồn → sạch/lineage → biểu đồ → lọc/CSV → cụm → SQL; chụp ảnh sau chốt dữ liệu | `docs/DEMO_VA_DANH_MUC_MINH_CHUNG.md`, ảnh `docs/minh_chung/`: mã hình, nguồn, run_id, n, đơn vị, bộ lọc, bảng số liệu tương ứng | Đạt kiểm phiên bản; Nhi kiểm nguồn |
| Q05 | Thử màn hình laptop/cửa sổ hẹp; ghi lỗi đọc nhãn, trạng thái lọc, thiếu mẫu; cải thiện có mục đích | Nhật ký trước/sau; cập nhật test dashboard nếu hành vi đổi; không thay nghĩa KPI để làm đẹp | Đạt review tích hợp; Nhi thử sử dụng |
| Q06 | Viết Chương 5–6, ghép định dạng và cập nhật kịch bản bảo vệ cũ | Demo có dữ liệu; kết luận có bằng chứng/giới hạn; Word căn đều, caption/dẫn chiếu, mục lục/danh mục, Equation bản địa, in đậm chọn lọc | Cả nhóm duyệt số/kết luận |

## 6. Chia chính xác 60 tin và kiểm chéo

Mẫu `docs/MAU_KIEM_TRA_DU_LIEU.csv` có sáu nhóm × mười tin, seed 42; các ô người kiểm hiện trống. Phân theo row_id, không theo thứ tự Excel sau sắp xếp.

| Người kiểm chính | 20 row_id được giao | Người đọc lần hai |
|---|---|---|
| Đạt | 683, 7164, 709, 6266, 4208, 4167, 6570, 750, 2331, 7826, 7103, 3879, 3589, 5900, 7485, 1802, 4266, 4759, 5093, 8387 | Nhi |
| Nhi | 6677, 7133, 2980, 4588, 3696, 1915, 6181, 8271, 8773, 634, 8572, 3788, 6510, 3133, 5906, 6469, 3427, 8107, 1071, 8151 | Quỳnh |
| Quỳnh | 6244, 7533, 2123, 5517, 8096, 8957, 3739, 1437, 4288, 3008, 5755, 3111, 78, 2512, 2604, 1140, 5418, 7452, 8879, 7363 | Đạt |

1. row_id là vị trí trong mảng JSON nguồn tính từ 1, không phải số dòng văn bản/mã giao dịch. Đọc năm trường lõi của đúng tin; không dùng trường chi tiết nghi lan truyền làm đáp án chuẩn.
2. Người đầu điền `human_property_type`, `human_transaction`, `human_price_area_status`, `reviewer`, `reviewed_on`, `evidence_note`. Loại dùng `land/house/apartment/other_unknown`; giao dịch dùng nhãn định nghĩa trong N02 hoặc `insufficient_evidence`; trạng thái số dùng `consistent/conflict/ambiguous/insufficient_evidence`. `consistent` chỉ nghĩa các trường được đọc không mâu thuẫn rõ, không xác nhận tài sản hay giá giao dịch.
3. Người thứ hai đọc nguồn độc lập trước khi xem kết luận lượt đầu; ghi nhận xét riêng trong `docs/NHAT_KY_KIEM_TRA_CHEO.md`, điền `second_reviewer`, `agreement` là `agree/disagree/insufficient_evidence`. Không ghi đè kết luận đầu để che bất đồng.
4. Nhi tập hợp; hai người thảo luận với người thứ ba làm trọng tài khi cần. Giữ kết luận đầu, kết luận sau thảo luận và lý do; không ép tin mơ hồ thành nhãn chắc chắn.
5. Mỗi người đọc thêm 2–3 ví dụ trọng điểm/cực trị ở N04, ghi riêng không cộng vào mẫu ngẫu nhiên. Mẫu phân tầng đều không tự cho tỷ lệ chính xác toàn bộ 6.936 tin; chỉ báo kết quả theo mẫu/nhóm và phương pháp phù hợp.
6. Nếu run_id đổi, giữ nhãn cũ để truy nguyên và đối chiếu lại trạng thái; không gọi bộ tạo mẫu để xóa kết quả đã điền.

## 7. Cải tiến phát triển để chuyên nghiệp hơn

Đây là **việc chưa triển khai**, không phải tính năng/kết quả đã có. P0 làm trước; sau đó chọn P1 theo thời gian; P2 chỉ làm khi không ảnh hưởng bản báo cáo cuối.

| Mã/ưu tiên | Chủ trì; phối hợp | Việc phát triển cụ thể | Sản phẩm và tiêu chí đánh giá |
|---|---|---|---|
| I01 — P0 | Nhi; cả nhóm | Bộ đối chiếu 60 tin hai người đọc; quy tắc nhãn/bất đồng; thêm mẫu có chủ đích về tiền trả trước, giá đơn vị, chiều ngang dễ nhầm | Bảng lỗi/mơ hồ theo nhóm; sửa quy tắc có test chống loại nhầm, không gọi đây là nhãn chuẩn thị trường |
| I02 — P0 | Quỳnh; Đạt | Nghiệm thu trình duyệt/Excel thật, demo thống nhất, ảnh có bảng số và run_id | Q02–Q04 có tên/ngày/bằng chứng, số khớp; phân biệt kiểm bằng công cụ với thao tác thật |
| I03 — P0 | Đạt; Nhi | Nghiệm thu cài mới/môi trường độc lập; hướng dẫn lỗi; khóa phiên bản bàn giao | Log cài/chạy thực, hash/phiên bản. Thiếu runtime Excel phải ghi giới hạn, không tự xác nhận workbook đã tạo lại |
| I04 — P1 | Đạt; Nhi | CI chạy unit test mỗi PR; tích hợp tải nguồn/kiểm hash/dựng dashboard thành luồng riêng do nhóm kích hoạt | Cấu hình và lần chạy thật; unit test không cần file riêng laptop; phân biệt lỗi mạng/code. Không yêu cầu gói dựng Excel nội bộ trên CI công khai |
| I05 — P1 | Nhi; Đạt | Phân loại cảnh báo rõ hơn: mâu thuẫn tiền, đơn giá, trả trước, kích thước, nhiều căn trong một tin | Bộ đối chiếu I01, test hồi quy, bảng đổi trạng thái và độ nhạy; không đổi ngưỡng chỉ để n/trung vị đẹp |
| I06 — P1 | Quỳnh; Đạt | Bộ lọc nhóm diện tích và xuất tóm tắt bộ lọc đang xem | Lọc đồng bộ KPI/biểu đồ/bảng/CSV; xuất kèm run_id/n/đơn vị/điều kiện; test biên khoảng, lọc kết hợp/rỗng. Hiện chưa có bộ lọc này |
| I07 — P1 | Quỳnh; Nhi | So sánh tỉnh trong cùng loại bất động sản, luôn kèm n/giới hạn | Bảng/biểu đồ trả lời câu hỏi cụ thể; ngưỡng mẫu rõ; đối chiếu CSV; không coi kiểm soát một thuộc tính là loại hết nhiễu |
| I08 — P1 | Đạt; Quỳnh | SQL nhiều khối đo; cân nhắc index hiện có với covering index và đánh đổi lưu/ghi | Cùng SQL/tham số/kết quả, plan, thời gian phân tán, dung lượng và chi phí ghi nếu đo; giữ cả kết quả không nhanh hơn, chỉ đổi khi có bằng chứng |
| I09 — P2 | Đạt; Nhi | Độ nhạy K-means với thêm seed, có/không nhóm mơ hồ | ARI/inertia/silhouette/n/scaler, tâm và cỡ cụm; không chọn k vì hình đẹp hoặc gọi ổn định là accuracy |
| I10 — P2 | Nhi; Quỳnh | Khảo sát nguồn mới có ngày/ID/quyền sử dụng rõ cho nghiên cứu sau | Hồ sơ nguồn và kiểm thử thí điểm; dataset/lần chạy riêng, không trộn thời điểm hay hứa có xu hướng/bản đồ khi chưa có biến |

Ước lượng xếp lịch, không phải hạn cam kết: mỗi P0 khoảng một buổi/người; P1 một đến hai buổi chủ trì kèm review; P2 ước lượng sau chốt phạm vi. Chưa có ngày nộp xác nhận. Ưu tiên ít cải tiến có bằng chứng hơn nhiều tính năng chưa nghiệm thu.

Mỗi thí nghiệm ghi: vấn đề/giả thuyết → phiên bản trước → thay đổi → dữ liệu/cách đo → kết quả cả tốt/xấu → giữ/bỏ và lý do → người kiểm. Tăng số test đơn thuần không chứng minh chất lượng tăng.

## 8. Nội dung sáu chương và trách nhiệm viết

| Chương/chủ trì | Nội dung bắt buộc | Phối hợp và bằng chứng |
|---|---|---|
| 1 — Nhi | Tên/vấn đề; ý nghĩa thực tiễn; ý nghĩa cộng đồng nghiên cứu; mục tiêu duy nhất; đối tượng/người dùng; phạm vi ứng dụng/giới hạn lịch sử | Cả nhóm chốt phạm vi; Đạt xác nhận vận hành. Câu hỏi con phục vụ cùng mục tiêu, không tự nhận thuật toán mới/mẫu đại diện |
| 2 — Nhi | Lý thuyết và kỹ thuật thật sự dùng: parse/Unicode/regex, thiếu/trùng/IQR, thống kê/độ nhạy, Python/pandas/NumPy/Matplotlib, K-means, SQLite/index, HTML/CSS/JS, Excel và provenance/kiểm thử | Đạt cung cấp thuật toán/SQL/tích hợp; Quỳnh DOM/SVG/Excel/trực quan. Mỗi nền tảng có cơ chế, I/O, tham số, lý do, giới hạn, ví dụ số và liên hệ mã; công thức đúng dạng toán |
| 3 — Đạt | Phân tích yêu cầu; kiến trúc/luồng; dữ liệu ba bảng, khóa/ràng buộc/index; thiết kế giao diện/trạng thái lọc/lỗi | Nhi cung cấp từ điển/quy tắc; Quỳnh thiết kế sử dụng. Sơ đồ kèm ví dụ dữ liệu, ERD khớp SQL; không dựng phân quyền chưa có |
| 4 — Đạt | Hiện thực tải/kiểm nguồn, làm sạch/lineage, IQR/thống kê, K-means, DB/SQL, hình, dashboard/CSV, Excel, tích hợp/kiểm tra | Nhi soạn dữ liệu/làm sạch, Quỳnh dashboard/Excel. Mỗi mô-đun: file/hàm, đầu vào, thuật toán, đầu ra, lỗi, ví dụ; mã dài để repo/phụ lục |
| 5 — Quỳnh | Cài/chạy/môi trường, demo nguồn đến sản phẩm, kết quả cuối, thí nghiệm/benchmark, kiểm thử/nghiệm thu, cải tiến nhóm thật sự làm | Đạt cung cấp log/SQL/K-means/tái lập; Nhi kiểm nhãn/độ nhạy. Ảnh có dữ liệu/bộ lọc/n/đơn vị/run_id và bảng tương ứng; ghi phần chưa kiểm |
| 6 — Quỳnh, cả nhóm duyệt | Trả lời mục tiêu, độ tin cậy có điều kiện, vận hành/tích hợp/ứng dụng đến đâu, giới hạn và hướng phát triển | Nhi chốt giới hạn dữ liệu; Đạt chốt kỹ thuật. Mỗi nhận định dẫn bằng chứng, tách kết quả/kế hoạch; không kết luận chung “chính xác, ứng dụng rộng rãi” |

Nhi thống nhất tham khảo/nguồn dẫn; Đạt kiểm phiên bản/mã/SQL và phụ lục kỹ thuật; Quỳnh ghép bìa, tóm tắt viết sau cùng, mục lục/danh mục, caption, căn đều hai bên và Equation bản địa. Nhóm xác nhận trường/lớp/giảng viên/ngày nộp/STT 22 hay 47, không tự điền.

Caption thống nhất `Hình 1: ...`, `Bảng 1: ...`, hoặc theo chương nếu chọn từ đầu. Mỗi hình có dữ liệu minh họa; hình/bảng đều được dẫn và phân tích trong thân chương. Không viết thành danh sách việc làm, không giới thiệu công nghệ qua loa hai đến ba dòng. Đối chiếu chi tiết tại [yêu cầu báo cáo](DOI_CHIEU_YEU_CAU_BAO_CAO.md).

## 9. Thứ tự làm và quy ước GitHub

| Mốc | Đạt | Nhi | Quỳnh | Điều kiện chuyển mốc |
|---|---|---|---|---|
| A — Tiếp quản | D01–D02 | N01–N02 | Q01–Q03 | Mỗi người chạy/mở được phần mình, hiểu cùng phạm vi |
| B — Kiểm chứng | 20 tin + đọc chéo, D03–D04 | 20 tin + đọc chéo, N03–N04 | 20 tin + đọc chéo, Q02–Q04 | Nhãn/UI có bằng chứng, lỗi được ghi thật |
| C — Cải tiến | I03, chọn I04 hoặc I08 | I01, chọn I05 | I02, chọn I06 hoặc I07 | P0 xong, P1 có review/test/kết quả trước-sau |
| D — Chốt dữ liệu | D05, dựng/đối soát | Chốt quy tắc/nhãn/số | Chụp ảnh cuối/so Excel | Một bộ kết quả thống nhất, giới hạn rõ |
| E — Viết/đọc chéo | Chương 3–4, phụ lục | Chương 1–2, nguồn | Chương 5–6, ghép | Cả ba đọc toàn văn, số liệu/hình/demo khớp |
| F — Nộp/bảo vệ | Demo kỹ thuật/đóng gói | Dữ liệu/lý thuyết | Trực quan/kết luận | Mỗi người giải thích được phần mình và luồng chung |

Đợt cập nhật của trợ lý push trực tiếp `main` theo yêu cầu người dùng. Với công việc sau này, đề xuất dùng `feat/dat-...`, `feat/nhi-...`, `feat/quynh-...`, commit có mã task (ví dụ `N05: ...`), PR để đọc chéo rồi merge. Quy ước này chưa đồng nghĩa đã cấu hình branch protection/CI hoặc gửi lời mời thành viên.

Cập nhật từ main trước khi bắt đầu; không force-push lịch sử chung. Một người tích hợp đầu ra cuối vì các lần chạy khác run_id/timing dễ xung đột. Raw lớn, `.venv`, `node_modules`, `tmp`, file khóa Office không đưa lên Git.

## 10. Nhật ký và tiêu chí đóng việc

Khi thực hiện, ghi vào `docs/NHAT_KY_KIEM_TRA_CHEO.md` theo mẫu sau; hiện chưa tự tạo kết quả/ngày/ký xác nhận cho thành viên.

```text
Mã nhiệm vụ:
Người làm / người kiểm chéo:
Ngày, commit, run_id:
Đầu vào và bước/lệnh:
Mong đợi / kết quả thực:
File minh chứng:
Lỗi hoặc giới hạn:
Giữ/bỏ thay đổi và lý do:
Trạng thái: chưa làm / đang làm / chờ kiểm / đạt / cần sửa
```

- [ ] Mỗi phần bản nền có người tự hiểu/kiểm chứng, không nhận kế hoạch thành kết quả.
- [ ] 60 tin có hai lượt đọc, giữ bất đồng; tin cực trị ghi riêng.
- [ ] UI/Excel mới có thao tác thật; không dùng xác nhận 7.001 tin cho bản 6.936 tin.
- [ ] Cải tiến được chọn có mã, minh chứng, đánh giá trước-sau; chưa có không viết như đã triển khai.
- [ ] CSV/JSON/DB/dashboard/Excel/bảng/hình/báo cáo dùng bộ kết quả tương ứng, kiểm lại sau sửa code.
- [ ] Giải thuật có code; SQL có DB/truy vấn thật; không thổi phồng thời gian/độ chính xác.
- [ ] Sáu chương đủ nội dung, căn đều, công thức đọc được, caption/dẫn chiếu/nguồn đồng bộ.
- [ ] Mỗi người có log/commit hoặc tài liệu, đọc chéo, phần viết và khả năng bảo vệ thực tế.

Đọc cùng: [rà soát](RA_SOAT_KY_THUAT.md), [yêu cầu sáu chương](DOI_CHIEU_YEU_CAU_BAO_CAO.md), [nhật ký UI](KIEM_THU_THUC_TE.md), [README](../README.md), [đối chiếu slide](../references/DOI_CHIEU_SLIDE.md).
