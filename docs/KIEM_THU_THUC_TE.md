# Nhật ký kiểm thử thực tế

> Cập nhật 16/10/2026: các xác nhận 7.001 tin bên dưới thuộc bản nền. Sau rà soát còn 6.936 tin; chưa tự ghi người dùng đã kiểm bản mới. Bảng mới ở cuối tài liệu.

Ngày ghi nhận: 15/10/2026.

Các trường hợp dashboard dưới đây do người dùng thao tác trên trình duyệt và xác nhận kết quả trong cuộc trò chuyện. Ảnh màn hình trạng thái mặc định đã được cung cấp. Chưa có ảnh riêng cho từng trạng thái lọc; nhóm có thể bổ sung khi lập phụ lục báo cáo.

| Mã | Thao tác | Kết quả mong đợi | Kết quả ghi nhận | Trạng thái |
|---|---|---|---|---|
| UI01 | Mở dashboard với bộ lọc mặc định | 7.001 tin; trung vị giá 2,2 tỷ đồng; đơn giá 32 triệu đồng/m²; diện tích 70 m² | Khớp ảnh màn hình người dùng cung cấp | Đạt |
| UI02 | Đặt lại rồi chọn Tp Hồ Chí Minh | 3.295 tin | Người dùng xác nhận khớp | Đạt |
| UI03 | Đặt lại rồi chọn Căn hộ | 377 tin | Người dùng xác nhận khớp | Đạt |
| UI04 | Đặt lại rồi bật bỏ ngoại lệ IQR | 6.734 tin | Người dùng xác nhận khớp | Đạt |
| UI05 | Đặt lại rồi chỉ giữ tiêu đề có dấu hiệu bán rõ | 3.055 tin | Người dùng xác nhận khớp | Đạt |
| UI06 | Đặt lại bộ lọc | 7.001 tin | Người dùng xác nhận khớp | Đạt |
| CSV01 | Lọc Tp Hồ Chí Minh, tìm kiếm để trống, tải CSV | 3.295 bản ghi không tính tiêu đề; địa phương đồng nhất | Người dùng xác nhận khớp | Đạt |
| SQL01 | Chạy scripts/demo_sql.py | Bốn truy vấn trả kết quả; kiểm tra database là ok | Người dùng xác nhận khớp | Đạt |
| DATA01 | Kiểm tra thủ công dòng nguồn số 1 | Giá 2.380.000.000 đồng; diện tích 100 m²; đơn giá 23.800.000 đồng/m² | Chưa nhận kết quả từ người dùng | Chờ kiểm tra |

Các xác nhận về số tin chưa chứng minh toàn bộ biểu đồ, xuất CSV hoặc nội dung tin rao đều đúng. Những phần đó được kiểm tra riêng. Đây là nhật ký thao tác; không thay thế việc đánh giá nhãn loại hình, giao dịch và các dòng bị cách ly.

## Nghiệm thu giao diện sau rà soát 16/10/2026

Phiên bản dữ liệu `20261016T015620Z-f2e661a6`. Các kết quả dưới đã được test JavaScript trên DOM mô phỏng, đang chờ thành viên thao tác trình duyệt và ghi tên/ngày xác nhận.

| Mã | Thao tác | Kết quả mong đợi | Xác nhận trình duyệt bản mới |
|---|---|---|---|
| NEW01 | Mở trang/đặt lại | 6.936 tin; giá trung vị 2,25 tỷ; đơn giá hiển thị 32,3 triệu/m²; diện tích 70 m² | Chờ |
| NEW02 | Chọn Tp Hồ Chí Minh | 3.277 tin | Chờ |
| NEW03 | Thêm loại Căn hộ tại Tp Hồ Chí Minh | 239 tin | Chờ |
| NEW04 | Đặt lại, bỏ ngoại lệ IQR | 6.676 tin | Chờ |
| NEW05 | Đặt lại, chỉ giữ tiêu đề có dấu hiệu bán rõ | 3.030 tin | Chờ |
| NEW06 | Đặt lại, tìm Hà Nội trong ô bảng | Bảng/CSV 1.014 tin; KPI toàn bộ vẫn 6.936 | Chờ |
| NEW07 | Đặt lại, tới trang 2 rồi tải CSV | Phân trang đổi dòng hiển thị; CSV chứa toàn bộ bảng đang lọc, không chỉ 20 dòng trang hiện tại | Chờ |

Sau mỗi lần thay quy tắc và chạy pipeline mới, đọc lại `analysis.json` và test dashboard; không dùng cố định bảng này nếu mã lần chạy đã khác. Ảnh báo cáo cần chụp bản cuối và ghi dữ liệu/bộ lọc cùng chú thích.
