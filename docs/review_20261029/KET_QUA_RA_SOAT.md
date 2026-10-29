# Rà soát tiểu luận và mã nguồn trước khi nộp

Ngày 29/10/2026. Đối chiếu tệp người dùng gửi với nhánh GitHub `improve-data-validation`, commit `549df1aa0fcb46b011863a02930241807489e91b`. Mã phân tích của nhánh này đã được đồng bộ vào `main`; quy tắc nhận diện, 180 ID lấy mẫu và các nhãn công khai không thay đổi trong lượt rà soát.

## Nhận định

Bản người dùng gửi có nội dung phân tích tốt nhưng chưa nên nộp nguyên trạng vì cách tổ chức kết quả, đánh số bảng, tài liệu tham khảo và một số mô tả hiện thực còn thiếu nhất quán. Bản `BAO_CAO_TIEU_LUAN_DA_RA_SOAT` đã sửa các điểm này, bám sáu chương và phạm vi khám phá giá rao lịch sử. Đây là nhận định về chất lượng hồ sơ theo yêu cầu được cung cấp, không phải điểm chấm hoặc cam kết điểm của giảng viên.

## Những điểm đã sửa

| Vấn đề ở bản gửi | Cách hoàn thiện |
|---|---|
| Hai bảng bổ sung chưa có số/tên; kết quả mới nằm sau kết luận | Đưa toàn bộ vào Chương 5; đánh số liên tục 24 bảng |
| Dẫn trang PDF, slide và giáo trình | Bỏ các dẫn này; giữ nguồn dữ liệu, tài liệu chính thức và bài báo gốc; đánh lại 11 tài liệu tham khảo |
| Mô tả đổi đặc trưng phân cụm là hướng chưa thực hiện | Nêu rõ thí nghiệm đã chạy, bổ sung bảng ARI và hình từ cùng số liệu |
| Chưa có bảng theo tầng ngay trong tiểu luận | Thêm kết quả ba nhóm baseline, số khớp/số xác định và độ bao phủ |
| Phân tích 405 nhóm chỉ được nhắc đến | Thêm sáu ô so sánh cùng loại và khoảng diện tích giữa hai thành phố, kèm Q1–Q3 và n |
| Mô tả cờ kiểm nguồn còn theo bản cũ | Xác nhận cờ ở dòng 5093; nêu chính xác 8151/8535 vẫn chưa được nhận diện đầy đủ |
| Danh mục và tham chiếu trang cũ | Dựng lại mục lục, danh mục hình/bảng, cập nhật trường trong Word |
| Tên nguồn đoạn K-means còn dẫn SQL | Đổi về đúng hàm thực thi |
| Repo chính chưa có nhánh cải tiến | Đồng bộ main theo kiểu fast-forward, bảo toàn bản thảo người dùng đang sửa |
| Clone Windows làm đổi byte của tài liệu đã khóa | Bảo toàn xuống dòng trong Git; khôi phục đúng byte đã commit khi khác biệt chỉ là CRLF/LF, không thay hash quy tắc |
| Metadata bản báo cáo không khớp Markdown đã qua Git | Gắn metadata với đúng Word/PDF/Markdown bản nộp, kiểm hash byte thực tế |

## Phạm vi kiểm thực tế

| Lớp | Kết quả |
|---|---|
| GitHub | Đọc main và nhánh cải tiến; pin commit chứa kết quả mới |
| Mã Python | Chạy đủ 45 test, không lỗi; hai lỗi quyền thư mục tạm của lần thử sandbox đầu đã được giải quyết bằng thư mục tạm trong workspace, không sửa thuật toán |
| JavaScript | Kiểm code thật trên DOM tối giản: bộ lọc, KPI, mẫu rỗng, tìm kiếm, CSV, phân trang, cụm và liên kết |
| Nguồn/làm sạch | Đúng SHA-256; 9.004 = 1.884 trùng + 209 cách ly + 6.911 giữ; kiểm lại chính sách trên nguồn |
| Sản phẩm | Đối soát từng dòng CSV/JSON/database/workbook, trung vị và hash; SQLite integrity/FK đạt |
| Nhãn công khai | Tính lại 60 dòng và các tỷ lệ từng tầng; đúng các ID evaluation, không trùng development |
| Phân nhóm | Tính lại 405 nhóm, 41 nhóm đủ điều kiện, 4.594 tin trong các nhóm đủ điều kiện |
| Phân cụm bổ sung | Chạy lại 65 phép fit; so CSV số với rtol 10⁻⁸, atol 10⁻⁵; khớp số liệu đã lưu |
| Báo cáo | 39 trang; 6 chương, 11 hình, 24 bảng, 8 công thức bản địa; đã xem toàn bộ PNG của bản cuối |

Lượt tái tính nhãn dùng giá trị tham chiếu công khai trong `evaluation_rows.csv`. Tệp gán nhãn XLSX riêng không được cung cấp trong bản clone, nên không tái kiểm lịch sử chỉnh 17 tin hoặc tính độc lập của người gán nhãn. Không được biến phép kiểm số liệu công khai này thành một lượt xác minh nhãn người mới.

## Nội dung khoa học cần giữ khi nộp

Chỉ số 8/8 quyết định đã xác định khớp chỉ bao phủ 8/60 = 13,33%; 52 tin còn review. Loại tài sản khớp 43/58, giao dịch 28/45. Các số này mô tả bộ tham chiếu một người ban đầu và AI hiệu chỉnh, không phải accuracy toàn nguồn. Những trường sale_assumed/other_unknown không bị tính thành nhãn cụ thể đã đúng.

Đơn giá là biến giá chia diện tích, nên quan hệ với diện tích có ràng buộc toán học. Hệ số diện tích–giá toàn mẫu gần 0 nhưng khác trong nhóm; không suy ra diện tích không liên quan đến giá hoặc quan hệ nhân quả. Trong các ô được so sánh, nhà tại Hà Nội có trung vị cao hơn TP.HCM nhưng căn hộ 30–60 m² có thứ tự ngược lại. Vị trí/chất lượng và ý nghĩa diện tích chưa được kiểm soát.

Cụm K-means lặp lại tốt trong các phép thử seed và mẫu con đã làm, nhưng ARI giảm còn 0,0071 khi đổi sang thang gốc và 0,1833 khi đổi sang log tổng giá. Không gán tên phân khúc cao cấp/bình dân. Silhouette ở các hình học khác nhau không phải thước đo tuyệt đối để chọn cách biến đổi.

SQL lưu một lần đo có trung vị 3,5297 ms trước và 0,6029 ms sau chỉ mục. Câu lệnh, tham số, plan và hash kết quả kiểm được; không suy thành tốc độ ổn định trên mọi máy. Không lựa chọn lại lần đo thuận lợi để thay số của run đã công bố.

## Có nên phát triển thêm

Để hoàn thiện tiểu luận trong phạm vi hiện tại, phần có thể kiểm bằng mã và phần biên tập đã hoàn thành. Không cần thêm mô hình dự đoán giá, backend, đăng nhập hoặc nhiều bảng nghiệp vụ để làm bài có vẻ lớn hơn; các phần đó cần dữ liệu và đánh giá khác, làm mục tiêu bị loãng.

Nếu có thời gian bổ sung bằng chứng, ưu tiên chất lượng tham chiếu: người đọc xác nhận 17 sửa đổi có AI hỗ trợ, làm rõ các tin review khi nguồn cho phép, hoặc có một mẫu mới do hai người đọc độc lập theo tiêu chí thống nhất. Không ép mọi trường mơ hồ thành usable/exclude để tăng độ bao phủ. Nếu dùng evaluation hiện tại để sửa quy tắc, cần holdout mới trước khi tuyên bố cải thiện.

Ưu tiên tiếp theo là xác nhận các bộ lọc bản hiện hành trong trình duyệt thật và việc tính lại công thức trong Microsoft Excel thật. Các kiểm DOM, cached value và Artifact Tool hiện có đã được ghi đúng phạm vi; chưa được đổi thành nghiệm thu UI.

Nếu phát triển nghiên cứu sau môn học, nên tìm nguồn có quyền sử dụng rõ, ngày từng tin và nghĩa diện tích thống nhất; kiểm tin gần trùng rồi mới xây dựng dự báo. Với SQL, bổ sung các khối đo có thứ tự ngẫu nhiên, dung lượng chỉ mục và chi phí ghi nếu muốn nghiên cứu hiệu năng sâu hơn.

## Tệp và lệnh bàn giao

Bản Word/PDF cần dùng là `docs/BAO_CAO_TIEU_LUAN_DA_RA_SOAT`. Bộ số liệu chính vẫn là `20261027T065401Z-5c8df2cc`; ngày 29/10 là ngày rà soát và tái kiểm. Tệp đầu vào tại E:\UsersData được giữ nguyên.

Các lệnh từ repo, trong môi trường có thư viện:

```powershell
python tools/verify_final_report.py
python tools/verify_delivery.py --require-workbook
python scripts/verify_validation_freeze.py
python tools/recheck_extensions.py
```

Ba lệnh đầu không chạy lại phân tích chính. Lệnh cuối tạo kết quả so sánh dưới `tmp/recheck_extensions`, không thay nhãn hoặc kết quả đã công bố. Thông báo lịch sử về baseline trong công cụ khóa quy tắc không thay trạng thái run hiện hành; công cụ đó chỉ kiểm byte các tệp nằm trong giao thức khóa.
