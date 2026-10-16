# Rà soát kỹ thuật trước khi viết báo cáo

Ngày: 16/10/2026. Phiên bản dữ liệu đang đối chiếu: `20261016T015620Z-f2e661a6`. Đây là biên bản rà soát và hướng dẫn tiếp quản, không phải bản báo cáo tiểu luận.

## Kết luận rà soát

Bản nền có lỗi cần sửa, nên đợt này chưa viết báo cáo hoàn chỉnh theo đúng yêu cầu của người dùng. Đã sửa các vấn đề về diễn giải dữ liệu, công thức Excel, cách trình bày biểu đồ và tái lập đầu ra. Trạng thái kiểm tra thực tế được ghi ở `outputs/AUDIT_RESULTS.json`; kiểm tra bằng bản sao nguồn ở `outputs/portability_check.json`. Nếu chạy pipeline lần nữa, phải đối chiếu mã lần chạy trước khi dùng các con số trong biên bản này.

Mục tiêu của đề tài tiếp tục là khám phá và so sánh đặc điểm giá rao trong mẫu tin lịch sử có kiểm tra chất lượng. Không thêm dự báo giá, tài khoản, giao dịch hoặc 32 bảng chỉ để tăng quy mô.

## Các vấn đề đã sửa

| Vấn đề tại bản nền | Cách sửa | Bằng chứng |
|---|---|---|
| Chuỗi số hỗn hợp và thành phần giá âm/lặp đơn vị có thể được đọc sai | Kiểm cấu trúc dấu phân cách; thành phần giá phải không âm và đi theo đơn vị giảm dần | `tests/test_source_checks.py`, `tests/test_pipeline.py` |
| Giá đơn vị trong mô tả có thể bị dùng như tổng giá; trường lõi và nội dung có thể mâu thuẫn lớn | Cách ly trường hợp không giải quyết được; lưu lý do và cụm số minh họa; không tự nhân/sửa giá | `src/source_checks.py`, CSV cách ly và lineage |
| “nha trang” có thể bị nhận là nhà; sang quán có thể bị coi là bán bất động sản | Loại cụm địa danh khỏi bước suy luận loại; phát hiện chuyển nhượng hoạt động/thuê mặt bằng | Kiểm thử hồi quy và tin nguồn 300, 588 |
| “DT: 3m2 x 5” bị so sánh số 3 với tổng diện tích | Nhận diện biểu thức kích thước, chỉ gắn cờ cần kiểm tra; không lấy chiều ngang làm diện tích | Kiểm thử biểu thức kích thước và tin 8262 |
| Pipeline có thể gắn DOI cho một JSON tùy ý | Kiểm SHA-256 và cấu trúc đúng bản công bố trước khi ghi đầu ra | `src/artifact_contract.py` và kiểm thử nguồn bị thay |
| Dùng nhầm đầu ra của lần chạy cũ | Manifest theo lần chạy, hash mã nguồn/đầu ra; dashboard và workbook có hồ sơ dựng riêng | `run_manifest.json`, `dashboard_build.json`, `workbook_build.json` |
| Lỗi giữa chừng có thể để đầu ra chưa hoàn chỉnh | Tạo trong thư mục tạm, chỉ bắt đầu chuyển sang đầu ra chính khi tạo thành công; manifest xuất cuối | Kiểm thử mô phỏng lỗi tạo biểu đồ. Việc chuyển nhiều file không phải một giao dịch filesystem; manifest phát hiện trạng thái không đồng bộ nếu bị gián đoạn lúc chuyển |
| Excel lưu sẵn đơn giá, thay giá/diện tích không tính lại đúng | Cột I tính H/G; Q/R đổi đơn vị; S giữ diện tích hợp lệ. Phân biệt công thức với cờ IQR/cụm snapshot | Kiểm sửa giá/diện tích và tám trường hợp đầu vào không hợp lệ trong bộ dựng; đối soát lại giá trị đã xuất |
| Các khoảng giá không đều bị gọi là histogram | Dashboard và Excel gọi đúng là cột đếm tin theo nhóm; không diễn giải là mật độ | Nhãn và chú thích trong sản phẩm |
| Vẽ mẫu theo bước cố định có thể trùng cấu trúc thứ tự nguồn | Reservoir sampling có seed 42; thống kê dùng toàn bộ mẫu đang lọc | Test tính lặp lại và số điểm; ghi cỡ mẫu trên hình |
| Tìm kiếm bảng khiến người dùng hiểu nhầm KPI cũng đổi | Ghi rõ tìm kiếm chỉ tác động bảng/CSV; bộ lọc phía trên tác động toàn dashboard | Test tìm kiếm và số dòng CSV |
| CSV xử lý nhãn cụm -1 như chuỗi công thức | Phân biệt giá trị số với chuỗi; số âm giữ kiểu số, chuỗi công thức được vô hiệu hóa | Test xuất CSV |
| Clone không có raw, hướng dẫn chạy sai thứ tự; verifier cần PDF tạm và ghi sẵn kết quả đạt | Thêm lệnh chạy thống nhất, kiểm nguồn trước; bỏ phụ thuộc PDF; lưu kết quả test thực tế theo mã lần chạy | Bản sao nguồn chạy đạt và bài kiểm thiếu nguồn |
| Liên kết Excel có thể dẫn tới workbook cũ sau khi chỉ chạy Python | Chỉ hiện liên kết mở Excel khi hồ sơ workbook khớp lần chạy hiện tại | Bộ dựng dashboard kiểm provenance workbook |
| Git tự chuẩn hóa dấu xuống dòng, làm byte của file trong commit khác bản đã tính hash | Thêm `.gitattributes` giữ byte của mã/dữ liệu/metadata; chấp nhận CRLF là dấu xuống dòng khi rà khoảng trắng; kiểm trực tiếp blob đã stage và bản checkout | 30 hash của mã/đầu ra lõi phải khớp trước push; không sửa manifest để hợp thức hóa |

## Kết quả dữ liệu sau sửa

| Chỉ tiêu | Bản nền | Bản sau rà soát |
|---|---:|---:|
| Dòng nguồn | 9.004 | 9.004 |
| Trùng năm trường lõi | 1.884 | 1.884 |
| Cách ly | 119 | 184 |
| Giữ phân tích | 7.001 | 6.936 |
| Trung vị tổng giá rao | 2,20 tỷ VND | 2,25 tỷ VND |
| Trung vị đơn giá | 32,00 triệu VND/m² | 32,3205 triệu VND/m² |
| Trung vị diện tích | 70 m² | 70 m² |
| Ngoại lệ IQR theo nhóm, vẫn giữ trong EDA mặc định | 267 | 260 |
| Tin dùng cho K-means | 6.734 | 6.676 |

Đối soát: 9.004 = 1.884 + 184 + 6.936. Có thêm 65 tin cách ly. Lý do có thể chồng nhau, không cộng số lượt lý do để suy ra số dòng. “Cách ly” nghĩa là không đủ điều kiện theo chính sách, không có nghĩa đã xác nhận tin giả hoặc biết chắc giá nào đúng.

Ví dụ số có thể dùng để giải thích quy tắc; trợ lý đã đọc lại nguồn của bốn dòng dưới trong lượt bổ sung:

| Dòng nguồn | Mâu thuẫn quan sát | Quyết định |
|---|---|---|
| 638 | Trường giá 20 triệu VND, diện tích 143 m², mô tả nêu 20tr/m2 | Không dùng 20 triệu như tổng giá; cách ly, không tự đặt lại thành 2,86 tỷ |
| 7811 | Trường giá 860 tỷ VND, tiêu đề nêu 860tr | Cách ly mâu thuẫn quy mô tiền; không tự chọn số đúng |
| 335 | Trường diện tích 2 m², tiêu đề nêu 2 ha | Cách ly mâu thuẫn đơn vị |
| 8262 | Diện tích lõi 16 m², mô tả ghi “DT: 3m2 x 5” | Không kết luận diện tích bằng 3 m²; giữ cờ cần kiểm tra biểu thức kích thước |

## Kiểm tra đã thực hiện và giới hạn

- 29 bài kiểm thử Python chạy đạt, không có lỗi/bỏ qua; số thực thi lưu theo mã lần chạy và hash file test.
- JavaScript thật được chạy trong DOM tối giản: sáu trạng thái lọc, KPI, phân trang, mẫu rỗng, tìm kiếm, CSV, mẫu scatter, độ phủ cụm và liên kết. Đây không phải tự động thao tác trình duyệt đầy đủ.
- Verifier so từng bản ghi CSV/JSON/database, kiểm phép chia giá–diện tích, lineage và bản ghi trùng, ba trung vị độc lập, hash đầu ra, toàn vẹn database và khóa ngoại. Excel được kiểm riêng khi có bản dựng cùng phiên bản.
- Bản sao không có `.venv`, `node_modules`, đầu ra cũ hoặc PDF tạm đã chạy lại và tạo dữ liệu/nhãn giống hệt. Dùng cùng Python đã cài thư viện; chưa có bằng chứng cài pip mới trên máy khác hoặc tải mạng khác.
- Kiểm nguồn bằng SHA-256 chứng minh đúng file công bố, không chứng minh từng giá trị trong file đúng sự thật.
- 3.891 tin vẫn được giả định là bán theo ngữ cảnh nguồn; 1.120 tin chưa xác định loại. Nhãn là suy luận; chưa công bố precision/accuracy.
- 36 tin giữ lại có biểu thức kích thước cần xem tay; 328 tin có quy ước dấu chấm hàng nghìn cần so độ nhạy. Các trường hợp khác vẫn có thể lọt qua regex.
- Có tin rất bất thường vẫn được giữ và gắn cờ IQR. Không coi tập “sạch” là đã chứng thực diện tích, pháp lý hoặc giao dịch. Nên đối chiếu cả các tin cực trị, ví dụ dòng 8535 có diện tích lõi 6 m² và mô tả nêu các diện tích khác; không thể xác nhận đúng trường nào bằng test số học.
- K-means là phân nhóm thăm dò, không có nhãn chuẩn; độ ổn định seed không phải độ chính xác thị trường. Spearman không chứng minh nhân quả; đơn giá chứa diện tích trong mẫu số.

## Cách đọc minh họa SQL

Ba bảng thực là `provinces`, `property_types`, `listings`, có khóa và ràng buộc. Trước index, kế hoạch quét bảng và dùng B-tree tạm để sắp xếp; sau index, dùng `idx_listings_search`. Hai kết quả 100 dòng có cùng SHA-256.

Ở lần chạy dữ liệu ghi trên biên bản, trung vị trước là 0,6484 ms, sau là 0,7788 ms; tỷ số trước/sau khoảng 0,833. Kết quả này không chứng minh cải thiện độ trễ. Dữ liệu nhỏ, phép đo tuần tự và trạng thái máy làm thời gian dao động; bản chạy kiểm tái lập có thể cho tốc độ khác. Giữ số đo thật, giải thích kế hoạch truy vấn và giới hạn, không chọn lại chỉ để có tỷ số đẹp. Khi chạy lại, lấy số đo từ `outputs/sql_benchmark.json` của chính lần đó.

## Lượt bổ sung do trợ lý thực hiện để giảm việc nhóm

Ngày 16/10/2026, cùng run_id: đọc 60 tin mẫu và bảy tin trọng điểm; lưu diễn giải riêng, không điền nhãn người thật trong mẫu gốc. Đã tính ba trung vị độc lập bằng CSV thư viện chuẩn và SQLite ORDER BY, chạy bốn truy vấn chỉ đọc, kiểm toàn vẹn/FK và đối soát workbook. Bằng chứng bổ sung: `outputs/ASSISTANT_CHECKS.json`; tái kiểm bằng `tools/prepare_handover_evidence.py`.

Rà soát nội dung thấy các tin giữ vẫn có mâu thuẫn/mơ hồ: ví dụ 5093 giá 9,7/9,9 tỷ, 8151 diện tích 18.000/180.000 m², 2331 biến thể bán/cho thuê; một số mô tả rõ loại hình hơn tiêu đề. Đây là giới hạn của các quy tắc bảo thủ, không được kết luận mọi tin giữ đã xác minh. Không tự sửa raw, giá đúng suy đoán hoặc biến nhãn trợ lý thành gold labels.

Thử độ nhạy riêng khi bỏ 16 tin giữ do trợ lý chọn có nghi vấn, còn 6.920; trung vị giá 2,25 tỷ và diện tích 70 m², đơn giá 32,36078133 triệu/m². Đây là tình huống có chủ đích, không phải ước lượng tỷ lệ lỗi/toàn bộ độ lệch hay bộ dữ liệu chính mới. Xem [kết quả đọc tin](KET_QUA_KIEM_TRA_NHAN.md) và [CSV 60 tin](DOI_CHIEU_60_TIN_TRO_LY.csv). Không bắt nhóm kiểm lại 60 tin nếu không công bố độ chính xác nhãn.

Đã chuẩn bị [nguồn/quy tắc/thiết kế/mô-đun](NGUON_QUY_TAC_VA_THIET_KE.md), [K-means/SQL](THUC_NGHIEM_KMEANS_VA_SQL.md), [đối soát số liệu, hình và demo](DOI_CHIEU_SO_LIEU_TRUC_QUAN.md). Kiểm tính lại bằng Artifact Tool có bằng chứng; thử thao tác Excel thật chưa mở được workbook do công cụ nhập không có hiệu lực, xem [phạm vi Excel](NGHIEM_THU_EXCEL.md). Công cụ browser chặn URL file cục bộ, chưa xác nhận bố cục bản mới. Không dùng đường vòng để vượt chặn hoặc ghi các kiểm UI này là đạt.

## Nhóm còn làm trước bản báo cáo cuối

1. Đạt hiểu/viết Chương 3–4; Nhi Chương 1–2 và nguồn/thông tin hành chính; Quỳnh Chương 5–6, định dạng. Dùng hồ sơ có sẵn, không giao lại kiểm SHA, lập từ điển, chạy SQL/thống kê hoặc thí nghiệm đã làm.
2. Một buổi tổng duyệt dashboard/Excel trên máy demo và chụp ảnh có dữ liệu. Xác nhận 7.001 tin cũ không áp dụng cho bản 6.936; chưa thao tác phần nào thì ghi phần đó chưa xác nhận.
3. Cả ba đọc chéo, giải thích kết quả và giới hạn; hoàn thiện sáu chương, căn đều, caption/Equation và số liệu đúng phiên bản. Bản Word cũ chưa dùng nộp.

[Phân công rút gọn](PHAN_CONG_VA_NOI_DUNG_BAO_CAO.md) thay các task và cải tiến bắt buộc cũ; theo dõi việc thực làm ở [nhật ký](NHAT_KY_KIEM_TRA_CHEO.md). Tính năng mới là tùy chọn sau khi báo cáo/demo ổn. Nếu cần thay quy tắc/code thì có hồi quy và dựng/đối soát lại đầu ra liên quan trước khi chốt số; không sửa riêng Excel để ép khớp.
