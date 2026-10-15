# Nguồn dữ liệu và quyền sử dụng

## Bộ dữ liệu được sử dụng

- Tên: **Vietnam Real Estate Data**, phiên bản **2**.
- Tác giả: **Duc Chung Tran, Huy Hoang Nguyen, Hong Son Ha**.
- Nơi công bố: **Mendeley Data**.
- DOI: [10.17632/5477zhnmn2.2](https://doi.org/10.17632/5477zhnmn2.2).
- Trang gốc: <https://data.mendeley.com/datasets/5477zhnmn2/2>.
- Ngày công bố theo metadata: **12/01/2021** (`2021-01-12T12:36:03.192Z`).
- Ngày nhóm tải và kiểm tra: **15/10/2026**, múi giờ Việt Nam.
- Giấy phép dữ liệu: [Creative Commons Attribution 4.0 International — CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
- Tên file gốc: `chotot_data.json`, file ID `aa75d051-79fa-4df0-9707-50382de9da4b`.
- URL tải công khai: <https://data.mendeley.com/public-files/datasets/5477zhnmn2/files/aa75d051-79fa-4df0-9707-50382de9da4b/file_downloaded>.
- Kích thước nguyên bản: **24.292.489 byte**.
- SHA-256 nguyên bản: `ef39f153f48a55af07baa86883cd9036652f6d52232fed0be6e8991c7a5bf811`.

Checksum tính tại máy **khớp hoàn toàn** checksum trong manifest API công khai của Mendeley. File JSON gốc được giữ nguyên byte tại `data/raw/chotot_data.json`. Metadata và manifest tải về được lưu bên cạnh để đối chiếu. Không sửa nội dung dữ liệu gốc.

## Quy mô thực tế và phạm vi diễn giải

Mô tả của tác giả ghi “10,000 posts”. Khi đọc file JSON phiên bản 2, nhóm đếm được **9.004 bản ghi**, hợp của **29 tên trường**. Báo cáo và sản phẩm phải dùng **9.004** làm mẫu số dữ liệu đầu vào; sự khác biệt với mô tả nguồn được công khai, không bổ sung 996 bản ghi giả định.

Đơn vị quan sát là **một bản ghi tin quảng cáo bất động sản**, không phải một giao dịch đã hoàn tất và cũng không chắc chắn là một bất động sản duy nhất. File có tên `chotot_data.json`; trang mô tả chỉ xác nhận đây là bài đăng quảng cáo tại Việt Nam. Không có tài liệu đi kèm xác nhận phương pháp lấy mẫu, thời gian đăng của từng tin hoặc quy trình xác minh nội dung. Vì vậy, không gọi đây là dữ liệu giao dịch chính thức hoặc mẫu đại diện toàn thị trường.

Trường `price` thể hiện giá được nêu trong tin; trong đồ án gọi là **giá rao**. Giá `tỷ` được đổi thành VND bằng hệ số 1.000.000.000; `triệu` bằng 1.000.000. Diện tích chuẩn hóa về m². Đây là chuẩn hóa đơn vị, không phải quy đổi tỷ giá. Không điều chỉnh giá lịch sử thành giá năm 2026.

File không cung cấp trường ngày đăng, tọa độ hay mã tin ổn định. Không suy ra biến động theo thời gian, không vẽ vị trí căn nhà chính xác, không khẳng định số lượng bất động sản duy nhất. Địa danh lấy từ nội dung địa chỉ lịch sử trong tin; không tự chuyển sang đơn vị hành chính năm 2026.

## Chất lượng dữ liệu cần nêu trong báo cáo

- Chẩn đoán trực tiếp raw cho thấy **1.886 bản ghi lặp theo bốn trường lõi** `title`, `price`, `area`, `location`, còn **7.118 tổ hợp lõi khác nhau**. Toàn bộ đối tượng JSON chỉ có 162 bản ghi lặp hoàn toàn. Hai định nghĩa này khác nhau vì nhiều trường chi tiết thay đổi dù tin lõi trùng nhau. **Pipeline cuối chọn khóa bảo thủ hơn: năm trường lõi chuẩn hóa, thêm `description`, cho 1.884 tin trùng và 7.120 tổ hợp; đây mới là số gộp trùng thực tế của pipeline.** Dùng thuật ngữ “tin trùng theo khóa nội dung”, tránh gọi là “căn nhà trùng” khi chưa có mã định danh.
- Các trường lõi đều có nội dung, nhưng điều đó không bảo đảm tính đúng đắn. Có 21 tin ghi đơn vị `đ` và tổng giá chỉ hàng trăm nghìn đồng; cần đánh dấu/quarantine nếu không thể xác minh, không tự nhân thêm 1.000 để tạo giá hợp lý.
- Chuỗi diện tích dùng dấu phẩy/dấu chấm không đồng nhất; ví dụ `90.3 m2` và `11.300 m2`. Quy tắc tách thập phân/hàng nghìn phải được công khai, các trường hợp mơ hồ phải có cờ chất lượng.
- Nhiều trường chi tiết có dấu hiệu lặp kéo dài giữa các bản ghi thuộc loại tin khác nhau. Ví dụ bản ghi thứ 3 là tin đất 500 m² nhưng vẫn có số phòng và diện tích sử dụng 89 m² giống bản ghi liền trước. Bản ghi cuối là nhà cấp 4 tại TP.HCM nhưng đồng thời chứa các trường căn hộ/văn phòng và tên phân khu không ăn khớp. **Đây là dấu hiệu nghi ngờ dữ liệu chi tiết bị lan truyền trong quá trình thu thập, chưa phải kết luận đã xác minh về lỗi của tác giả.** Không dùng trực tiếp số phòng, loại hình, pháp lý, nội thất hay các diện tích chi tiết cho kết luận chính.
- Nếu suy luận loại hình từ tiêu đề, cần ghi rõ **loại hình suy luận**, công khai quy tắc và nhóm “chưa xác định”; không xem đó là nhãn đã được xác minh.
- Phân bố địa phương không đều và không có trọng số lấy mẫu; các thống kê chỉ mô tả tập tin đã thu thập sau làm sạch. Tương quan giữa diện tích và giá không chứng minh quan hệ nhân quả.

## Cách ghi nguồn trong báo cáo

> Tran, D. C., Nguyen, H. H., & Ha, H. S. (2021). *Vietnam Real Estate Data* (Version 2) [Data set]. Mendeley Data. https://doi.org/10.17632/5477zhnmn2.2

Dưới bảng/biểu đồ nên ghi: **Nguồn: nhóm xử lý từ Vietnam Real Estate Data, v2, Mendeley Data (2021), CC BY 4.0.**

Khi chia sẻ dữ liệu đã xử lý, ghi công tác giả, dẫn DOI và giấy phép, đồng thời mô tả các thay đổi: chuẩn hóa chuỗi/đơn vị, phân tách địa chỉ, gộp tin trùng theo khóa nội dung, cách ly giá trị không xác minh được, tạo các biến dẫn xuất. Giấy phép nguồn không đồng nghĩa tác giả chứng thực đồ án của nhóm.

## Tái tải và kiểm chứng

Từ thư mục Phân tích giá rao bất động sản Việt Nam trong KHDL, chạy `python scripts/download_data.py`. Script dùng thư viện chuẩn Python, kiểm tra SHA-256 trước khi lưu, không ghi đè một file nguyên bản đã đúng checksum. Toàn bộ phân tích có thể chạy với bản dữ liệu nguyên gốc đã có trên máy, không cần tải lại.
