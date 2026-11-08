# Hướng dẫn tái lập và kiểm chứng

Tài liệu này mô tả cách kiểm tra bộ kết quả đã bàn giao và cách tạo một lần chạy mới. Thực hiện lệnh từ thư mục gốc repo. Bộ bàn giao dùng mã lần chạy `20261027T065401Z-5c8df2cc`.

## 1. Môi trường

- Python 3.11 trở lên; cài các thư viện trong [requirements.txt](../requirements.txt).
- Node.js 22 trở lên để kiểm JavaScript và dùng công cụ dựng workbook.
- Git để clone repo; mạng để cài thư viện và tải nguồn lần đầu.
- Trình duyệt để mở dashboard, Microsoft Excel để mở workbook có sẵn.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Python đủ để chạy phần cốt lõi. Công cụ dựng workbook cần thêm `@oai/artifact-tool` từ runtime cung cấp công cụ này; `pip install` không cài phụ thuộc Node đó. Repo không chứa thư viện hay liên kết thư viện riêng của máy tác giả.

## 2. Kiểm tra bộ kết quả có sẵn

Nên kiểm bộ bàn giao trước khi chạy lại pipeline vì một lần chạy mới sẽ thay mã lần chạy và các sản phẩm cốt lõi.

```powershell
.\.venv\Scripts\python.exe -X utf8 -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -X utf8 tools\verify_final_report.py
```

Nếu có Node.js:

```powershell
node tests/test_dashboard.mjs
```

Kiểm đầy đủ dữ liệu nguồn, CSV/JSON, database, dashboard và workbook:

```powershell
.\.venv\Scripts\python.exe -X utf8 scripts\download_data.py
.\.venv\Scripts\python.exe -X utf8 tools\verify_delivery.py --require-workbook
```

Lệnh tải nguồn kiểm SHA-256 trước khi lưu và kiểm lại tệp đã có. Nếu checksum khác, công cụ dừng để giữ nguyên bản cần kiểm tra. `verify_delivery.py` ghi kết quả vào `outputs/DELIVERY_CHECK.json` và `outputs/AUDIT_RESULTS.json`.

| Phép kiểm | Phạm vi |
|---|---|
| `unittest` | Quy tắc xử lý, hợp đồng dữ liệu, lấy mẫu, phân tích mở rộng và các trường hợp hồi quy |
| `test_dashboard.mjs` | Chạy JavaScript thật trong DOM mô phỏng; kiểm bộ lọc, KPI, phân trang và xuất CSV |
| `verify_delivery.py` | Hash, lineage, số liệu và từng bản ghi giữa CSV/JSON/SQLite; với `--require-workbook` kiểm thêm Excel |
| `verify_final_report.py` | Sáu chương, 24 bảng, 11 hình, tám Equation, căn đều và hash khớp hồ sơ đã xem ảnh trang |

Kiểm tự động không được diễn giải thành nghiệm thu bố cục trên mọi trình duyệt hoặc tương tác trực tiếp trong Microsoft Excel. Các trạng thái đó được ghi riêng trong [hồ sơ kiểm thực tế](KIEM_THU_THUC_TE.md).

## 3. Tái chạy phần cốt lõi

Dùng một bản clone riêng nếu muốn giữ nguyên bộ kết quả đã nộp.

```powershell
.\.venv\Scripts\python.exe -X utf8 scripts\run_project.py
```

Thứ tự thực thi:

1. Tải hoặc kiểm tra dữ liệu nguồn.
2. Chạy pipeline: làm sạch, truy nguyên, thống kê, phân cụm, biểu đồ và SQLite.
3. Dựng dashboard từ kết quả mới.
4. Chạy kiểm thử Python; chạy kiểm JavaScript nếu tìm thấy Node.js.
5. Chạy demo SQL và đối soát sản phẩm cốt lõi.

Các tùy chọn:

| Tùy chọn | Ý nghĩa |
|---|---|
| `--skip-download` | Dùng nguồn đã có để chạy ngoại tuyến; pipeline vẫn kiểm checksum |
| `--node <đường-dẫn>` | Chỉ định tệp thực thi Node.js khi chưa có trong PATH |
| `--workbook` | Dựng lại Excel; yêu cầu Node.js và `@oai/artifact-tool` |
| `--skip-tests` | Chủ động bỏ kiểm thử; không được xem lần chạy đó là đã kiểm thử đạt |

Lệnh mặc định không tạo lại báo cáo, workbook hoặc phần phân tích mở rộng. Các sản phẩm cũ còn trên đĩa có thể thuộc mã lần chạy trước; phải đọc metadata để xác định phiên bản.

## 4. Chạy từng bước

```powershell
.\.venv\Scripts\python.exe -X utf8 scripts\download_data.py
.\.venv\Scripts\python.exe -X utf8 src\pipeline.py
.\.venv\Scripts\python.exe -X utf8 tools\build_dashboard.py
.\.venv\Scripts\python.exe -X utf8 -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -X utf8 scripts\demo_sql.py
.\.venv\Scripts\python.exe -X utf8 tools\verify_delivery.py --core-only
.\MO_DASHBOARD.cmd
```

Kiểm riêng bằng `python -m unittest` không cập nhật `outputs/python_test_results.json`; bộ điều phối `run_project.py` mới ghi bằng chứng cho lượt test của nó. `--core-only` chủ động bỏ kiểm Excel.

## 5. Dữ liệu và truy nguyên

| Tệp | Vai trò |
|---|---|
| `data/raw/chotot_data.json` | Nguồn nguyên byte, được tải riêng và Git-ignored |
| `data/raw/mendeley_metadata.json` | Metadata bộ dữ liệu |
| `data/raw/mendeley_file_manifest.json` | Manifest tệp nguồn |
| `data/processed/listings_clean.csv` và `.json` | 6.911 tin giữ ở bộ bàn giao |
| `data/processed/listings_rejected.csv` | 209 tin cách ly và lý do |
| `data/processed/row_lineage.csv` | Trạng thái của cả 9.004 dòng nguồn |
| `outputs/run_manifest.json` | Mã lần chạy, hash nguồn, mã xử lý và sản phẩm |
| `outputs/dashboard_build.json` và `workbook_build.json` | Liên kết sản phẩm dẫn xuất với lần chạy cốt lõi |

SHA-256 nguồn được kiểm:

```text
ef39f153f48a55af07baa86883cd9036652f6d52232fed0be6e8991c7a5bf811
```

`.gitattributes` giữ nguyên byte các tệp được băm khi Git thêm hoặc checkout. Khi thay quy tắc, cần chạy lại và kiểm lại sản phẩm liên quan; không sửa hash để chấp nhận thay đổi nội dung chưa được đánh giá.

## 6. Phân tích mở rộng

Để tính lại và đối chiếu phần mở rộng của **bộ bàn giao hiện hành** bằng các giá trị tham chiếu công khai:

```powershell
.\.venv\Scripts\python.exe -X utf8 tools\recheck_extensions.py
```

Công cụ tính lại đối chiếu 60 tin, bảng nhóm và 65 phép fit; kết quả kiểm ghi vào `tmp/recheck_extensions/`. Công cụ yêu cầu bộ cốt lõi vẫn khớp mã lần chạy của phần mở rộng. Thực hiện bước này trước khi tái tạo pipeline.

Bản tham chiếu công khai nằm trong `outputs/extended/evaluation_rows.csv`. Tính lại từ các giá trị này không xác nhận độc lập nhãn người đọc hay tái tạo được lịch sử sửa của workbook nhãn gốc.

Để tạo phân tích mở rộng mới từ workbook nhãn được nhóm giữ riêng, chạy sau pipeline:

```powershell
.\.venv\Scripts\python.exe -X utf8 scripts\complete_analysis.py --labels docs/manual_validation/private/DANH_GIA_60_DA_SUA_CO_HO_TRO_AI.xlsx
.\.venv\Scripts\python.exe -X utf8 tools\build_dashboard.py
```

Thư mục `docs/manual_validation/private/` chứa văn bản nguồn và thông tin đọc tin, không có trong bản clone công khai. Cần cung cấp tệp XLSX thực tế vào đúng vị trí trước khi dùng lệnh có `--labels`.

Mẫu và quy tắc đã khóa nằm trong `docs/manual_validation/`. README tại thời điểm khóa được lưu ở `docs/manual_validation/history/`; việc biên tập README gốc không thay hồ sơ đã khóa. Các tỷ lệ đối chiếu mô tả mẫu phân tầng và chưa phải độ chính xác toàn nguồn; AI không được tính là người gán nhãn độc lập thứ hai.

## 7. Dựng lại và kiểm workbook

Workbook có sẵn mở độc lập bằng Excel. Để dựng lại bằng môi trường đã cung cấp `@oai/artifact-tool`:

```powershell
node tools/build_workbook.mjs
.\.venv\Scripts\python.exe -X utf8 tools\verify_delivery.py --require-workbook
```

Hoặc dùng `scripts/run_project.py --workbook` để tạo một lần chạy cốt lõi mới kèm workbook.

Workbook chứa cả công thức và các bảng snapshot. Sửa một ô giá/diện tích trong Excel không tự tính lại mọi nhãn cụm, cờ ngoại lệ và bảng tổng hợp. Khi thay dữ liệu hoặc quy tắc xử lý, dựng lại workbook từ pipeline và đối soát cùng mã lần chạy.

## 8. Báo cáo và hồ sơ lịch sử

Bản báo cáo được liên kết trong README là `BAO_CAO_TIEU_LUAN_DA_RA_SOAT.docx/.pdf`. Hồ sơ tương ứng nằm trong `docs/review_20261029/QA_REPORT.json` và `outputs/report_build.json`.

- Bản đã rà soát có 39 trang, sáu chương, 11 hình, 24 bảng và tám Equation; số liệu khớp bộ kết quả bàn giao.
- `tools/verify_final_report.py` mặc định kiểm lại cấu trúc và hash của hồ sơ, không tạo báo cáo hay suy ra đã xem ảnh trang trong một lượt kiểm mới.
- `docs/review_20261029/build_reviewed_report.py` cần tệp báo cáo đầu vào đúng checksum. Các công cụ dựng báo cáo cũ phục vụ bản lịch sử, không dùng để ghi đè bản đã rà soát.
- Khi đổi số liệu, phải cập nhật nội dung, xuất lại PDF, xem từng trang và cập nhật metadata/QA đúng bản mới.
- Các bản `BAO_CAO_DO_AN`, `BAO_CAO_TIEU_LUAN_6_CHUONG` và hồ sơ rà soát ngày trước được giữ để đối chiếu; số liệu lịch sử có thể khác bộ bàn giao hiện hành.

Nếu một phép kiểm thất bại, đọc nguyên nhân, đối chiếu mã lần chạy và hash trước khi khẳng định sản phẩm còn đồng bộ. Bằng chứng cũ chỉ có giá trị đối với đúng đầu vào, mã xử lý và đầu ra được ghi trong hồ sơ đó.
