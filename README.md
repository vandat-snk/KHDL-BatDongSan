# Phân tích giá rao bất động sản Việt Nam

Đồ án Nhập môn Khoa học dữ liệu về xây dựng, xử lý, trực quan hóa dữ liệu bất động sản và rút ra ý nghĩa; STT đăng ký 22 hoặc 47 cần nhóm xác nhận.

Nhóm: Võ Văn Đạt (N23DCCN078), Nguyễn Thị Yến Nhi (N23DCCN112), Hứa Như Quỳnh (N23DCCN118).

## Mục tiêu và phạm vi

Mục tiêu duy nhất là giúp người phân tích khám phá và so sánh đặc điểm giá rao trong một mẫu tin bất động sản lịch sử bằng quy trình có thể chạy lại và kiểm chứng.

Nguồn là Vietnam Real Estate Data v2 trên Mendeley Data, DOI [10.17632/5477zhnmn2.2](https://doi.org/10.17632/5477zhnmn2.2), CC BY 4.0, công bố 12/01/2021. File thực tế có 9.004 bản ghi. Một dòng là một tin rao; chưa xác nhận là một bất động sản duy nhất hoặc một giao dịch. Không diễn giải kết quả thành thị trường năm 2026. Không có ngày từng tin hoặc tọa độ xác minh để dựng chuỗi thời gian hay vị trí căn nhà.

Phần chính bám Chương 1–3 môn học. K-means và SQLite là công cụ mở rộng phục vụ khám phá cùng tập tin: có code phân cụm, database thực, SQL và benchmark. Không triển khai dự đoán giá hoặc khuyến nghị đầu tư. Xem [nguồn dữ liệu](references/DATA_SOURCE.md) và [đối chiếu slide](references/DOI_CHIEU_SLIDE.md).

## Trạng thái báo cáo

Kết quả và các sửa đổi ngày 16/10/2026: [biên bản rà soát kỹ thuật](docs/RA_SOAT_KY_THUAT.md). Bản sau rà soát có 6.936 tin, khác 7.001 tin của bản nền. Nhóm dùng số liệu cùng mã lần chạy khi demo và viết báo cáo.

`docs/BAO_CAO_DO_AN.docx` và `.md` là bản thảo cũ, trước khi nhận yêu cầu sáu chương của giảng viên. Giữ lại để đối chiếu; chưa đáp ứng cấu trúc/định dạng mới và chưa dùng làm bản nộp. Đợt rà soát này ưu tiên sửa và kiểm chứng code, chưa tạo báo cáo Word mới.

Chuẩn biên soạn tiếp theo nằm trong [đối chiếu yêu cầu báo cáo](docs/DOI_CHIEU_YEU_CAU_BAO_CAO.md): Giới thiệu → Cơ sở lý thuyết → Phân tích và thiết kế → Hiện thực → Demo và vận hành → Kết luận. [Phân công cập nhật](docs/PHAN_CONG_VA_NOI_DUNG_BAO_CAO.md) đã rút gọn: trợ lý hoàn tất kiểm tra/tài liệu kỹ thuật; nhóm tập trung viết sáu chương, hiểu kết quả và một buổi tổng duyệt/chụp ảnh. Không giao lại 60 tin cho ba thành viên. Ghi việc thực làm vào [nhật ký](docs/NHAT_KY_KIEM_TRA_CHEO.md). `tools/build_report.py` của bản thảo cũ đã tạm khóa chạy trực tiếp để tránh ghi đè báo cáo bằng cấu trúc và số liệu cũ.

Hồ sơ có thể dùng ngay khi viết:

- [Nguồn, từ điển, quy tắc, thiết kế và mô-đun](docs/NGUON_QUY_TAC_VA_THIET_KE.md).
- [Bằng chứng K-means và SQL](docs/THUC_NGHIEM_KMEANS_VA_SQL.md).
- [Đối soát số liệu, dữ liệu kèm tám hình và kịch bản demo](docs/DOI_CHIEU_SO_LIEU_TRUC_QUAN.md).
- [Rà soát nội dung 60 tin bằng trợ lý](docs/KET_QUA_KIEM_TRA_NHAN.md), [CSV riêng](docs/DOI_CHIEU_60_TIN_TRO_LY.csv). Đây không phải nhãn người thật hoặc đo accuracy; vẫn có tin mơ hồ lọt qua quy tắc.
- [Phạm vi nghiệm thu Excel](docs/NGHIEM_THU_EXCEL.md) và bằng chứng máy đọc được `outputs/ASSISTANT_CHECKS.json`.

Tái kiểm/chuẩn bị lại hồ sơ của đúng mốc này: `.\.venv\Scripts\python.exe -X utf8 tools\prepare_handover_evidence.py`. Công cụ đối soát đầu ra hiện có và thực thi bốn SQL ở chế độ đọc; không chạy lại pipeline/benchmark hoặc tạo báo cáo Word. Tài liệu đọc tin được viết riêng cho mốc đã ghi; nếu run_id thay đổi, công cụ yêu cầu rà lại thay vì gắn kết quả cũ cho phiên bản mới.

## Mở sản phẩm đã có

1. Nhấp đôi `MO_DASHBOARD.cmd` để mở dashboard bằng Edge/Chrome, hoặc dùng Ctrl+O trong trình duyệt chọn `outputs/DASHBOARD_BAT_DONG_SAN.html`. Không cần Python hay mạng để xem.
2. Mở `outputs/DO_AN_BAT_DONG_SAN.xlsx` bằng Excel. Workbook có dữ liệu, công thức và bốn biểu đồ; xem giới hạn tạo lại bên dưới.
3. Đọc [phân công kỹ thuật](docs/PHAN_CONG_VA_NOI_DUNG_BAO_CAO.md), [kịch bản bảo vệ](docs/KICH_BAN_THUYET_TRINH_VA_HOI_DAP.md) và [nhật ký kiểm thử người dùng](docs/KIEM_THU_THUC_TE.md). Số liệu nền phải đối chiếu lại sau khi sửa quy tắc.

## Cấu trúc dự án

| Vị trí | Nội dung |
|---|---|
| `data/raw` | Nguồn nguyên trạng, metadata/manifest; JSON lớn không nằm trên Git |
| `data/processed` | Dữ liệu sạch, tin cách ly và trạng thái mỗi dòng nguồn |
| `src` | Pipeline Python và mẫu dashboard HTML/CSS/JavaScript |
| `scripts` | Tải nguồn, demo SQL và lệnh chạy dự án |
| `sql` | Schema ba bảng, truy vấn minh họa, chỉ mục |
| `outputs` | JSON kết quả, bảng CSV, biểu đồ, database, dashboard, Excel và kiểm tra đầu ra |
| `tools` | Công cụ dựng/kiểm tra sản phẩm |
| `tests` | Kiểm thử đơn vị và tích hợp |
| `docs` | Tài liệu kiểm tra, phân công, yêu cầu mới và bản thảo báo cáo cũ |
| `references` | Nguồn dữ liệu, đăng ký, đối chiếu slide |
| `tmp` | Kết quả kiểm tra cục bộ; không phải điều kiện để clone và chạy phân tích |

## Cài và chạy từ bản clone trên Windows

Yêu cầu Python 3.11 trở lên. Cài thư viện và tải nguồn lần đầu cần mạng. Mở PowerShell tại thư mục gốc repo; nếu ở máy ban đầu:

```powershell
cd "E:\VanDat_\KHDL\Phân tích giá rao bất động sản Việt Nam"
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Nếu clone ở máy khác, chuyển vào đường dẫn bản clone của bạn. Mã chính xác định thư mục dự án theo vị trí file.

Chạy quy trình và kiểm chứng bằng một lệnh:

```powershell
.\.venv\Scripts\python.exe -X utf8 scripts\run_project.py
```

Lệnh mặc định kiểm/tải đúng dữ liệu nguồn trước, rồi chạy pipeline, dựng dashboard, kiểm thử và đối soát phần cốt lõi. Nó không tạo lại báo cáo. Nếu một bước thất bại, đọc lỗi và xử lý; không dùng file cũ trong `outputs` để khẳng định lần chạy mới thành công.

File `data/raw/chotot_data.json` không được đưa lên GitHub. Tải riêng khi cần:

```powershell
.\.venv\Scripts\python.exe -X utf8 scripts\download_data.py
```

Khi nguồn đã có đúng checksum và thư viện đã cài, chạy ngoại tuyến:

```powershell
.\.venv\Scripts\python.exe -X utf8 scripts\run_project.py --skip-download
```

`--skip-download` chỉ bỏ bước truy cập tải nguồn, không phải cách bỏ kiểm chứng checksum của pipeline. `--skip-tests` là lựa chọn chủ động bỏ chạy test; kết quả phải ghi trạng thái bỏ qua, không coi là kiểm thử đạt.

## Chạy từng bước để tìm hiểu code

Chạy tuần tự từ thư mục repo:

```powershell
.\.venv\Scripts\python.exe -X utf8 scripts\download_data.py
.\.venv\Scripts\python.exe -X utf8 src\pipeline.py
.\.venv\Scripts\python.exe -X utf8 tools\build_dashboard.py
.\.venv\Scripts\python.exe -X utf8 -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -X utf8 scripts\demo_sql.py
.\.venv\Scripts\python.exe -X utf8 tools\verify_delivery.py --core-only
.\MO_DASHBOARD.cmd
```

Pipeline tái tạo dữ liệu sạch, thống kê, phân cụm, biểu đồ, database và SQL. Dashboard dùng dữ liệu vừa xử lý. Các bước này không tự tạo lại workbook hoặc bản báo cáo cũ.

Nếu có Node.js 22 trở lên:

```powershell
node tests/test_dashboard.mjs
```

Test JavaScript dùng DOM mô phỏng để kiểm bộ lọc, KPI, mẫu rỗng, phân trang, CSV và liên kết; không thay thế kiểm tra bố cục trong trình duyệt. Xem phân biệt xác nhận người dùng và kiểm tra tự động tại `docs/KIEM_THU_THUC_TE.md`.

## Excel và phạm vi đối soát

`tools/build_workbook.mjs` dùng Node và `@oai/artifact-tool` của runtime Codex. `pip install -r requirements.txt` không cài gói này. Môi trường Python thông thường có thể tái tạo phần cốt lõi, nhưng chưa đủ để tạo lại chính xác workbook bàn giao. File Excel có sẵn mở độc lập bằng Excel.

Nếu runtime có sẵn phụ thuộc này, chạy toàn bộ và tạo lại workbook:

```powershell
.\.venv\Scripts\python.exe -X utf8 scripts\run_project.py --workbook
```

Hoặc chạy riêng `node tools/build_workbook.mjs`, rồi đối soát đầy đủ:

```powershell
.\.venv\Scripts\python.exe -X utf8 tools\verify_delivery.py --require-workbook
```

`--core-only` không xác nhận Excel đã cập nhật. Chế độ yêu cầu workbook phải báo lỗi nếu workbook/metadata không khớp lần chạy hiện tại. Không tự cài phụ thuộc nội bộ từ một nguồn không xác định.

Workbook gồm cột snapshot và các công thức gắn với vùng dữ liệu hiện tại. Không giả định sửa một ô giá sẽ tạo lại mọi biến dẫn xuất, nhãn cụm, cờ ngoại lệ và bảng snapshot. Khi thay dữ liệu hoặc quy tắc, chạy lại và dựng lại workbook rồi kiểm chứng; không chỉnh riêng từng sản phẩm để ép số khớp nhau.

## Bằng chứng kiểm tra và cách nghiệm thu

Kết quả kiểm tra mới ở `outputs/AUDIT_RESULTS.json`; trạng thái được gắn với đầu vào/đầu ra và nội dung code của lần kiểm tra. Đọc trạng thái từng phần: kiểm tra cốt lõi thành công không có nghĩa Excel, báo cáo, nhãn dữ liệu hoặc mọi bố cục UI đã được xác nhận. Không lấy `outputs/DELIVERY_CHECK.json` cũ làm bằng chứng cho code đã thay đổi.

`.gitattributes` giữ nguyên byte của mã, dữ liệu và metadata có hash khi Git thêm hoặc checkout file, tránh thay dấu xuống dòng làm sai SHA-256 giữa Windows và máy khác. Nếu sửa nội dung, vẫn phải chạy lại quy trình và dựng sản phẩm liên quan; không sửa hash bằng tay.

- Đối soát số tin giữ + trùng + cách ly bằng số dòng nguồn; mỗi dòng có một trạng thái trong lineage.
- Kiểm tra tay cách quy đổi giá/diện tích trên mẫu nguồn, cả trường hợp mơ hồ và cách ly. Không tự tạo tỷ lệ chính xác nhãn khi chưa có nhãn do người kiểm tra cung cấp.
- So sánh số tin, đơn vị và trung vị giữa CSV, database, dashboard, Excel và tài liệu cuối; phân biệt trung bình với trung vị.
- IQR là cờ ngoại lệ để kiểm độ nhạy; K-means phân nhóm thăm dò. Các cụm không phải nhãn thị trường đã được xác minh.
- SQL phải dùng cùng truy vấn/tham số và kết quả tương đương trước/sau index. Thời gian tùy máy; không dùng một lần chạy nhỏ để khẳng định hiệu quả mọi truy vấn.
- Chỉ ghi công việc và cải tiến nhóm thật sự thực hiện. Thí nghiệm trong tài liệu phân công còn là kế hoạch đến khi có kết quả.
- Bản báo cáo mới cần sáu chương và hình/bảng có dữ liệu minh họa theo [yêu cầu biên soạn](docs/DOI_CHIEU_YEU_CAU_BAO_CAO.md).
