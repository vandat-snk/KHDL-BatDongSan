# Bàn giao và trạng thái kiểm tra kỹ thuật

Ngày cập nhật: 16/10/2026. Thư mục dự án: `E:\VanDat_\KHDL\Phân tích giá rao bất động sản Việt Nam`. Kết quả xử lý các phát hiện và số liệu sau sửa nằm trong [biên bản rà soát kỹ thuật](RA_SOAT_KY_THUAT.md).

## Phạm vi và quyết định của đợt rà soát

Đồ án phục vụ một mục tiêu: khám phá và so sánh đặc điểm giá rao trong mẫu tin bất động sản lịch sử sau xử lý có thể kiểm chứng. K-means và SQL là công cụ trong luồng phân tích này; không mở thành đề tài định giá, khuyến nghị đầu tư hoặc hệ thống giao dịch.

Người dùng yêu cầu kiểm tra toàn bộ trước: nếu code cần chỉnh thì chưa viết báo cáo. Đã phát hiện các vấn đề kỹ thuật và điểm chưa phù hợp yêu cầu báo cáo; đợt này tập trung sửa, chạy kiểm thử và đối soát. Không tạo bản báo cáo Word mới.

`docs/BAO_CAO_DO_AN.docx` và `.md` là bản thảo cũ giữ để tham khảo. Chúng chưa đáp ứng yêu cầu mới và không phải bản để nộp. Công cụ dựng bản thảo cũ không nằm trong lệnh chạy dự án mặc định.

## Sản phẩm và cách kiểm chứng

| Thành phần | Vị trí | Cách kiểm tra |
|---|---|---|
| Quy trình và kết quả phân tích | `src/pipeline.py`, `outputs/analysis.json` | Chạy lại từ nguồn đúng checksum; đọc chính sách, số dòng, thống kê và nhãn |
| Truy xuất dữ liệu | `data/processed/listings_clean.csv`, `listings_rejected.csv`, `row_lineage.csv` | Mỗi dòng nguồn có trạng thái duy nhất; tin cách ly có lý do; đơn vị và biến dẫn xuất nhất quán |
| Biểu đồ và bảng | `outputs/charts`, `outputs/tables` | Dùng kết quả cuối; nhãn trục, đơn vị, số mẫu và điều kiện lọc rõ ràng |
| Dashboard ngoại tuyến | `outputs/DASHBOARD_BAT_DONG_SAN.html` | Mở bằng trình duyệt; thử lọc, mẫu rỗng, phân trang, CSV; so với phân tích |
| Database và SQL | `outputs/real_estate.sqlite`, `sql`, `outputs/sql_benchmark.json` | Đối chiếu toàn bộ dòng; kiểm tra toàn vẹn/khóa ngoại; truy vấn và tham số trước/sau index cùng kết quả |
| Kiểm thử | `tests` | Chạy bằng môi trường dự án; số test và trạng thái lấy từ lần chạy thật |
| Tích hợp | `scripts/run_project.py`, `tools/verify_delivery.py` | Tạo/kiểm nguồn trước xử lý; các bước chạy nối tiếp; đánh dấu lỗi hoặc bỏ qua, không ghi đạt giả |
| Bằng chứng kiểm tra mới | `outputs/AUDIT_RESULTS.json` và manifest của quy trình | Dùng trạng thái và dấu vết của lần kiểm tra hiện tại; không dùng báo cáo kiểm tra cũ để đại diện code mới |
| Excel | `outputs/DO_AN_BAT_DONG_SAN.xlsx` | Chỉ xác nhận cập nhật khi đã dựng lại và đối soát workbook/metadata với lần chạy cuối |
| Báo cáo | `docs/BAO_CAO_DO_AN.docx`, `.md` | Bản thảo cũ, cần viết lại sau khi đóng các vấn đề kỹ thuật |

Chi tiết lệnh chạy và phụ thuộc ở README. Bản clone không chứa JSON nguồn lớn; bước tải/kiểm nguồn phải diễn ra trước pipeline. `tmp` là tài liệu cục bộ, không được yêu cầu có sẵn để kiểm chứng phần cốt lõi từ bản clone.

## Những vấn đề được phát hiện ở bản nền

| Vấn đề | Hệ quả cần xử lý |
|---|---|
| Hướng dẫn trước đây chạy pipeline trước downloader, trong khi raw bị Git bỏ qua | Thành viên clone mới có thể lỗi thiếu nguồn; hướng dẫn mới và lệnh tích hợp phải kiểm/tải nguồn trước |
| Pipeline từng chỉ ghi checksum của file đang dùng | Cần kiểm đúng bản nguồn trước xử lý, tránh gắn DOI nguồn công khai cho một file đã bị sửa |
| Dữ liệu đầu ra cũ có thể còn sau khi lần chạy mới lỗi | Cần gắn đầu ra với nguồn, phiên bản code và lần chạy; đối soát bằng dữ liệu thật thay vì chỉ đếm file |
| Kiểm tra bàn giao cũ phụ thuộc PDF tạm và số 19 trang cố định, ghi sẵn số test/đánh giá thị giác | Không dùng làm bằng chứng tự động mới. Kết quả kiểm thử phải được thực thi hoặc ghi rõ chưa chạy; báo cáo/layout là phạm vi riêng |
| Tạo lại Excel cần gói `@oai/artifact-tool` không được cài qua pip | Nêu rõ giới hạn tái lập. Chạy phần cốt lõi không tự chứng minh Excel cập nhật; có chế độ yêu cầu workbook riêng |
| Nhãn loại hình, giao dịch và chuỗi số có thể bị suy luận sai | Cần sửa quy tắc có hồi quy và công khai hạn chế; chưa có gán nhãn thủ công thì không đưa tỷ lệ chính xác |
| Báo cáo cũ dùng cấu trúc khác yêu cầu mới | Giữ bản cũ, lập ma trận sáu chương; chưa viết lại trong đợt sửa code |

Các thay đổi và số liệu cuối phải lấy từ `outputs/analysis.json`, manifest và `outputs/AUDIT_RESULTS.json` sau kiểm tra. Bảng này ghi nhận lý do rà soát, không tự tuyên bố mọi vấn đề đã đóng.

## Bằng chứng đã có và giới hạn

Trước đợt sửa, 12 kiểm thử Python đã chạy đạt; kiểm tra JavaScript trên DOM mô phỏng đạt các trường hợp lọc, mẫu rỗng, CSV, phân trang và liên kết. Đó là kết quả của bản nền, cần chạy lại sau sửa. Không dùng số test nền làm hằng số nghiệm thu.

Người dùng đã cung cấp ảnh dashboard mặc định và xác nhận các bộ lọc, CSV và demo SQL khớp số mong đợi của bản nền; nhật ký nằm trong `docs/KIEM_THU_THUC_TE.md`. Những xác nhận này là bằng chứng người dùng thao tác phiên bản đó, không chứng minh code mới có cùng số liệu hoặc mọi bản ghi được đọc đúng. Sau khi thay quy tắc, cần thử lại UI với số mới.

Bộ Excel đã có ba trang tính và bốn biểu đồ; việc kiểm tra cấu trúc/công thức/giá trị lưu khác với trực tiếp thao tác mọi chức năng trong Microsoft Excel. Khi sửa dữ liệu giá trong workbook, không giả định các cột snapshot hoặc nhãn cụm/cờ ngoại lệ được huấn luyện lại.

Kiểm tra tự động không xác minh sự thật của mọi tin rao. Chưa có nhãn con người thì chưa thể công bố độ chính xác loại hình/giao dịch, giá đúng thực tế hay giá giao dịch. Thời gian SQL chỉ có ý nghĩa với máy, truy vấn, tham số và lần đo đã ghi.

## Phần báo cáo chưa đáp ứng yêu cầu mới

Rà soát trực tiếp bản Word cũ cho thấy có 14 bảng và 6 hình nhưng chưa có caption đánh số cho các bảng; thân bài chưa đặt căn đều hai bên; công thức chưa được trình bày thành Equation bản địa của Word. Chương 2–5 hiện là nguồn → làm sạch → kết quả → phần mở rộng, không theo lý thuyết → thiết kế → hiện thực → demo.

Cần bổ sung diễn giải kỹ thuật sâu, kiến trúc và thiết kế CSDL khớp ba bảng thực tế, minh họa các mô-đun, demo dữ liệu thật, đánh số và dẫn chiếu hình/bảng đồng bộ. Ví dụ giảng viên về 32 bảng hoặc hai mức đối tượng không phải yêu cầu phải dựng thêm bảng/tài khoản.

[Ma trận yêu cầu sáu chương](DOI_CHIEU_YEU_CAU_BAO_CAO.md) là chuẩn cho bản viết lại. Chương 6 phải trả lời về độ tin cậy có điều kiện, vận hành, tích hợp và phạm vi ứng dụng bằng bằng chứng; không kết luận chung chung.

## Công việc ba thành viên tiếp tục

| Thành viên | Trọng tâm tiếp quản |
|---|---|
| Võ Văn Đạt | Chạy quy trình sau sửa, đọc manifest/kiểm thử; giải thích pipeline, K-means, database và benchmark; thử bản clone theo README |
| Nguyễn Thị Yến Nhi | Kiểm tra tay các chuỗi giá/diện tích, loại hình và giao dịch; đối chiếu tin trùng/cách ly; ghi nhãn và lý do thực tế |
| Hứa Như Quỳnh | Kiểm thử dashboard/CSV với số liệu cuối; đối chiếu bảng/biểu đồ; chuẩn bị ảnh demo có dữ liệu và quy tắc định dạng báo cáo |

Nhóm cần bổ sung trường, lớp, giảng viên và STT đăng ký. Các thí nghiệm cải tiến trong phân công cũ vẫn là việc cần thực hiện cho đến khi có sản phẩm thật. Sau khi code và đầu ra được kiểm chứng, cập nhật phân công viết báo cáo theo sáu chương mới rồi mới biên soạn bản Word hoàn chỉnh.
