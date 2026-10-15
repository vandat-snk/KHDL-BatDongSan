# Bàn giao đồ án phân tích giá rao bất động sản Việt Nam

Toàn bộ sản phẩm nằm trong `E:\VanDat_\KHDL\Phân tích giá rao bất động sản Việt Nam`. File đăng ký đề tài ban đầu được giữ ở thư mục KHDL bên ngoài dự án.

## Những phần đã có

| Sản phẩm | Vị trí |
|---|---|
| Bản thảo báo cáo Word 19 trang và bản Markdown | `docs/BAO_CAO_DO_AN.docx`, `docs/BAO_CAO_DO_AN.md` |
| Excel với 3 trang tính và 4 biểu đồ chỉnh sửa được | `outputs/DO_AN_BAT_DONG_SAN.xlsx` |
| Dashboard ngoại tuyến có bộ lọc và xuất CSV | `outputs/DASHBOARD_BAT_DONG_SAN.html` |
| Pipeline xử lý dữ liệu, phân cụm, biểu đồ và SQL | `src/pipeline.py` |
| Nguồn nguyên trạng và dữ liệu đã xử lý | `data/raw`, `data/processed` |
| 8 biểu đồ tĩnh và các bảng thống kê | `outputs/charts`, `outputs/tables` |
| Database SQLite thực và truy vấn minh họa | `outputs/real_estate.sqlite`, `sql` |
| Demo chạy các câu SQL trên database | `scripts/demo_sql.py` |
| Phân công theo tên và MSSV, dàn ý báo cáo chi tiết | `docs/PHAN_CONG_VA_NOI_DUNG_BAO_CAO.md` |
| Kịch bản trình bày 10 phút và câu hỏi bảo vệ | `docs/KICH_BAN_THUYET_TRINH_VA_HOI_DAP.md` |
| Đối chiếu trang slide và nguồn có giấy phép | `references/DOI_CHIEU_SLIDE.md`, `references/DATA_SOURCE.md` |

## Kết quả kiểm tra

- Đối soát 9.004 dòng nguồn bằng 7.001 tin giữ, 1.884 dòng trùng và 119 dòng cách ly.
- File nguồn khớp SHA-256 công bố và không bị sửa.
- Chạy lại pipeline thành công sau khi chuyển vào thư mục đề tài.
- 12 kiểm thử Python đạt; kiểm tra gộp trùng, đọc đơn vị, ngoại lệ, địa lý, phân cụm và ràng buộc database.
- Dashboard thực thi mã JavaScript với DOM mô phỏng: 6 trường hợp lọc, mẫu rỗng, phân trang, xuất CSV, nhãn cụm và liên kết đạt.
- Excel không có lỗi công thức trong kiểm tra đã thực hiện; giá trị lưu khớp kết quả Python, đã thử thay giá và khôi phục để kiểm tra cập nhật công thức.
- Đã xem kết xuất 19 trang Word bằng Microsoft Word, ảnh của 3 trang tính và 4 biểu đồ SVG của dashboard.
- Database kiểm tra toàn vẹn và khóa ngoại đạt; truy vấn trước/sau index có kết quả và hash giống nhau.

Chi tiết kiểm tra giữa các định dạng được lưu trong `outputs/DELIVERY_CHECK.json`. Các ảnh và log nội bộ ở `tmp`, không cần nộp cùng báo cáo.

## Các bước ba thành viên cần hoàn thiện

Đạt tìm hiểu pipeline, phân cụm và SQL; Nhi kiểm chứng nguồn, cách đọc giá diện tích và gộp trùng; Quỳnh kiểm tra biểu đồ, bộ lọc và diễn giải kết quả. Sản phẩm cần nộp, thí nghiệm cải tiến và tiêu chí nghiệm thu của từng bạn nằm trong tài liệu phân công.

Nhóm cần bổ sung tên trường, lớp học phần, giảng viên, ngày nộp và STT đăng ký. Kiểm tra thủ công nhãn loại hình, giao dịch và các tin bị cách ly chưa được thay thế bằng kiểm thử tự động. Không ghi phần cải tiến chưa làm thành kết quả đã thực hiện.

Việc kiểm tra bố cục toàn trang dashboard trong trình duyệt bị giới hạn bởi lỗi công cụ trình duyệt. Mã xử lý và từng biểu đồ đã được kiểm tra; nhóm mở `MO_DASHBOARD.cmd` trên máy để xác nhận bố cục, thao tác và tải CSV. Chưa kiểm tra trực tiếp trong giao diện Microsoft Excel; cấu trúc XLSX, công thức, biểu đồ và giá trị lưu đã được đối chiếu.

Nguồn công bố năm 2021, không có ngày của từng tin. Kết quả là phân tích giá rao trong mẫu nghiên cứu lịch sử, không đại diện cho giá giao dịch hoặc thị trường năm 2026.
