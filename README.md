# Đồ án phân tích giá rao bất động sản Việt Nam

**Đề tài chính:** Xây dựng bộ dữ liệu về bất động sản, xử lý và trực quan hóa dữ liệu và rút ra các ý nghĩa (STT 22 hoặc 47 trong danh sách môn học).

Nhóm gồm Võ Văn Đạt (N23DCCN078), Nguyễn Thị Yến Nhi (N23DCCN112), Hứa Như Quỳnh (N23DCCN118).

## Mở kết quả ngay

1. Mở `outputs/DASHBOARD_BAT_DONG_SAN.html` bằng Edge hoặc Chrome, hoặc nhấp đôi `MO_DASHBOARD.cmd`. Không cần mạng hoặc cài Python để xem.
2. Mở `outputs/DO_AN_BAT_DONG_SAN.xlsx` bằng Excel để xem bảng tính và các biểu đồ có thể chỉnh sửa.
3. Đọc `docs/BAO_CAO_DO_AN.docx`: bản thảo báo cáo có kết quả thực từ pipeline. Nhóm bổ sung tên trường, lớp, giảng viên, thời hạn và phần cải tiến của mình trước khi nộp.
4. Đọc `docs/PHAN_CONG_VA_NOI_DUNG_BAO_CAO.md` để nhận nhiệm vụ tìm hiểu, kiểm chứng và cải tiến; `docs/KICH_BAN_THUYET_TRINH_VA_HOI_DAP.md` để luyện bảo vệ.

## Phạm vi và bằng chứng

Phần chính đáp ứng Chương 1–3: xác định câu hỏi, kiểm tra chất lượng, xử lý thiếu và trùng, chuẩn hóa đơn vị, gắn cờ ngoại lệ, phân tích và trực quan hóa. Phần mở rộng có **code K-means chạy ra nhãn cụm** và **database SQLite thực, câu SQL và đo truy vấn trước/sau index**. Hai phần này là bổ sung; không đổi đề tài sang dự đoán giá hoặc tối ưu dữ liệu lớn.

Nguồn là Vietnam Real Estate Data v2 trên Mendeley Data, DOI `10.17632/5477zhnmn2.2`, CC BY 4.0, công bố 12/01/2021. File thực tế có **9.004 dòng**, khác mô tả khoảng 10.000 của nguồn. Giá là **giá rao**, không phải giá giao dịch; không diễn giải thành tình hình thị trường năm 2026. Xem `references/DATA_SOURCE.md` để biết tác giả, URL tải, checksum và giới hạn. Không có ngày từng tin hoặc tọa độ đáng tin cậy nên không dựng chuỗi thời gian hay bản đồ căn nhà.

## Cấu trúc

| Thư mục | Nội dung |
|---|---|
| `data/raw` | File nguồn nguyên trạng, metadata và manifest để kiểm chứng |
| `data/processed` | Dữ liệu sạch, dòng loại, ánh xạ từng dòng nguồn sang kết quả |
| `src` | Pipeline Python và mã dashboard |
| `scripts/download_data.py` | Tải lại nguồn và kiểm tra SHA-256 |
| `sql` | DDL, truy vấn minh họa và phần tối ưu index |
| `outputs` | Dashboard, Excel, kết quả JSON, bảng CSV, biểu đồ và database |
| `docs` | Báo cáo, phân công, nội dung cần có và kịch bản bảo vệ |
| `references` | Nguồn dữ liệu và đối chiếu từng trang slide |
| `tests` | Kiểm thử những quy tắc xử lý quan trọng |
| `tools` | Tạo dashboard, báo cáo và workbook từ kết quả pipeline |
| `tmp` | Ảnh và log dùng kiểm tra nội bộ, không cần nộp |

## Chạy lại phân tích trên Windows

Chạy PowerShell trong thư mục đề tài `E:\VanDat_\KHDL\Phân tích giá rao bất động sản Việt Nam`. Python 3.11 trở lên được khuyến nghị.

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe src\pipeline.py
.\.venv\Scripts\python.exe tools\build_dashboard.py
.\.venv\Scripts\python.exe tools\build_report.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe scripts\demo_sql.py
```

Nguồn đã có sẵn nên các bước phân tích chạy ngoại tuyến sau khi cài thư viện. Nếu cần tải lại:

```powershell
.\.venv\Scripts\python.exe scripts\download_data.py
```

Pipeline chỉ tái tạo các kết quả của đồ án; giữ nguyên dữ liệu gốc. Tên cột, quy tắc, seed và các số đo được lưu cùng kết quả. Đọc thông báo lỗi thay vì sử dụng kết quả cũ nếu một bước thất bại.

Workbook được tạo bằng `@oai/artifact-tool` của runtime Codex. `tools/build_workbook.mjs` lưu toàn bộ cách tạo. Việc tạo lại workbook cần Node và gói này; môi trường Python riêng không cài nó. File Excel bàn giao mở được độc lập, các công thức và biểu đồ gắn với dữ liệu trong workbook. Khi thay nguồn, chạy lại pipeline và tạo lại workbook qua Codex để các bảng chụp kết quả cũng được cập nhật.

Nếu có Node.js 22 trở lên, chạy `node tests/test_dashboard.mjs` để kiểm tra mã dashboard với DOM mô phỏng. Đây là kiểm thử bộ lọc, KPI, phân trang, CSV và liên kết; không thay thế việc mở dashboard trong trình duyệt để kiểm tra bố cục.

## Cách kiểm chứng trước khi nộp

- Tổng dòng giữ + dòng trùng + dòng loại phải bằng 9.004; mỗi dòng nguồn xuất hiện đúng một lần trong nhật ký.
- Chọn ít nhất 30 dòng thuộc nhiều cách ghi giá để kiểm tra tay phép đổi đơn vị và đơn giá. Nhóm tự ghi nhận kết quả kiểm tra này; không xem kiểm thử tự động là kiểm tra nhãn thủ công.
- Đối chiếu cùng số tin và trung vị giữa CSV, Excel, dashboard và báo cáo khi chưa lọc. Không nhầm trung bình với trung vị, hoặc trung bình các tỷ số với tỷ số của tổng.
- Thử bộ lọc tỉnh, loại, bỏ ngoại lệ và mẫu rỗng; đồ thị, bảng và CSV xuất phải dùng cùng tập tin.
- Đọc `references/DOI_CHIEU_SLIDE.md` để giải thích mỗi kỹ thuật bằng nội dung môn học. K-means chỉ phân cụm; không phải hệ thống dự đoán giá nhà.
- Với SQL, so sánh cùng câu truy vấn và tham số, kế hoạch thực thi, kết quả và trung vị thời gian. Dataset nhỏ không đủ để khẳng định hiệu quả trên dữ liệu lớn.

Các tệp báo cáo là bản thảo có kết quả đã chạy. Đóng góp cải tiến và mức độ hiểu bài của từng thành viên cần được nhóm thực hiện, xác minh và cập nhật trung thực.
