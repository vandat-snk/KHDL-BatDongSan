# Nhật ký bàn giao và đọc chéo

Cập nhật 16/10/2026. Thay bảng 18 task và 10 cải tiến cũ theo [phân công rút gọn](PHAN_CONG_VA_NOI_DUNG_BAO_CAO.md). Không coi việc trợ lý làm là sinh viên đã thực hiện.

## Bằng chứng trợ lý đã hoàn tất

| Phần kiểm/chuẩn bị | Kết quả hoặc giới hạn | Minh chứng |
| --- | --- | --- |
| Nguồn, checksum, quy tắc, từ điển, kiến trúc và mô-đun | Hồ sơ đã chuẩn bị, có ví dụ số và mã tương ứng | `NGUON_QUY_TAC_VA_THIET_KE.md`, `references/DATA_SOURCE.md` |
| Dữ liệu và đa sản phẩm | 9.004 = 1.884 + 184 + 6.936; đối soát CSV/JSON/DB/Excel và provenance | `outputs/AUDIT_RESULTS.json`, `ASSISTANT_CHECKS.json` |
| Thống kê độc lập | Trung vị CSV thư viện chuẩn khớp SQLite sắp thứ tự và analysis | `DOI_CHIEU_SO_LIEU_TRUC_QUAN.md`, `ASSISTANT_CHECKS.json` |
| Nội dung mẫu tin | Đã đọc 60 tin mẫu và bảy tin trọng điểm; vẫn có bất định/bỏ sót | `DOI_CHIEU_60_TIN_TRO_LY.csv`, `KET_QUA_KIEM_TRA_NHAN.md`; không phải nhãn người thật |
| K-means và SQL | Tài liệu tham số/k/seed/cụm; chạy lại bốn truy vấn đọc; giải thích benchmark không tăng tốc | `THUC_NGHIEM_KMEANS_VA_SQL.md`, `ASSISTANT_CHECKS.json` |
| Test mã, JavaScript, workbook | 29 Python đạt; logic JS và tính lại Artifact Tool đạt | `python_test_results.json`, `dashboard_test_results.json`, `workbook_test_results.json` |
| Bố cục browser và tính lại Excel thật | Chưa xác nhận: công cụ browser chặn file URL, công cụ Excel không nhập được đường dẫn | `KIEM_THU_THUC_TE.md`, `NGHIEM_THU_EXCEL.md` |
| Cài trên máy khác | Chưa xác nhận; mới chạy bản sao nguồn cùng Python đã cài | `outputs/portability_check.json` |
| Kịch bản/ảnh dữ liệu/dàn ý sáu chương | Đã chuẩn bị bảng đối chiếu và script demo; ảnh UI cuối do nhóm chụp khi tổng duyệt | `DOI_CHIEU_SO_LIEU_TRUC_QUAN.md`, `DOI_CHIEU_YEU_CAU_BAO_CAO.md` |

Ngày và run_id gắn trong từng bằng chứng. Nếu đổi code/quy tắc/nguồn thì kiểm và dựng lại các sản phẩm liên quan; bảng này không xác nhận vô thời hạn.

## Việc nhóm còn lại

| Mã | Người làm | Sản phẩm cần có | Người đọc chéo | Trạng thái hiện tại |
| --- | --- | --- | --- | --- |
| DAT-01 | Đạt | Hiểu luồng và ví dụ dữ liệu | Nhi/Quỳnh trao đổi | Chưa nhận xác nhận thành viên |
| DAT-02 | Đạt | Chương 3 từ hồ sơ thiết kế có sẵn | Quỳnh | Chờ viết theo yêu cầu mới |
| DAT-03 | Đạt | Chương 4; cung cấp kỹ thuật cho Chương 2 | Quỳnh/Nhi | Chờ viết theo yêu cầu mới |
| DAT-04 | Đạt | Tổng duyệt kỹ thuật; đọc Chương 1–2 | Cả nhóm | Chờ |
| NHI-01 | Nhi | Hiểu nguồn, giới hạn và ba ví dụ | Đạt/Quỳnh trao đổi | Chưa nhận xác nhận thành viên |
| NHI-02 | Nhi | Chương 1 | Đạt | Chờ viết theo yêu cầu mới |
| NHI-03 | Nhi | Chương 2 và nguồn tham khảo | Đạt/Quỳnh | Chờ viết theo yêu cầu mới |
| NHI-04 | Nhi | Thông tin bìa/lớp/thầy/STT; đọc Chương 5–6 | Cả nhóm | Chờ |
| QUYNH-01/02 | Quỳnh | Một buổi demo UI/Excel và ba ảnh có dữ liệu | Đạt kiểm phiên bản, Nhi kiểm diễn giải | Chờ thao tác bản cuối |
| QUYNH-03 | Quỳnh | Chương 5–6 | Nhi | Chờ viết theo yêu cầu mới |
| QUYNH-04 | Quỳnh | Ghép định dạng, đọc Chương 3–4 | Cả ba duyệt toàn văn | Chờ |

Không bắt buộc gán lại 60 nhãn hoặc chạy lại các thí nghiệm đã có. Cải tiến tùy chọn chỉ ghi thành đóng góp sau khi triển khai/đánh giá thật; chưa có thì đưa vào hướng phát triển.

## Mẫu ghi việc thật đã hoàn thành

```text
Mã việc / người làm / người đọc chéo:
Ngày, commit hoặc phiên bản tài liệu, run_id dữ liệu:
Phần đã viết hoặc đã thao tác:
Bằng chứng / file / trang báo cáo:
Góp ý nhận được và cách sửa:
Giới hạn còn lại:
Trạng thái: đang làm / chờ đọc chéo / hoàn tất
```

Không điền thay chữ ký, ngày hoặc xác nhận của thành viên. Dữ liệu cá nhân/liên hệ trong raw không cần sao chép vào nhật ký công khai.
