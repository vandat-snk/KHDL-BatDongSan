# Nhật ký nhiệm vụ và kiểm tra chéo

Khởi tạo mẫu ngày 16/10/2026. Đây là bảng giao việc, chưa phải bằng chứng thành viên đã hoàn thành. Không điền ngày nghiệm thu, chữ ký hoặc kết quả đạt khi chưa thực hiện.

Phạm vi, file tiếp quản và tiêu chí chi tiết theo [phân công chính thức](PHAN_CONG_VA_NOI_DUNG_BAO_CAO.md). Mỗi task có thể cần nhiều bản ghi; ghi commit/run_id của đúng lần kiểm.

## 1. Theo dõi nhiệm vụ bắt buộc

| Task | Người phụ trách | Người kiểm chéo | Trạng thái ban đầu | Minh chứng/commit/ngày nghiệm thu |
|---|---|---|---|---|
| D01 — Môi trường và chạy lại | Đạt | Nhi | Chờ thành viên thực hiện | |
| D02 — Thiết kế và mô-đun | Đạt | Nhi, Quỳnh | Chờ thành viên thực hiện | |
| D03 — K-means | Đạt | Nhi, Quỳnh | Chờ thành viên thực hiện | |
| D04 — DB/SQL | Đạt | Nhi | Chờ thành viên thực hiện | |
| D05 — Tích hợp bản cuối | Đạt | Nhi, Quỳnh | Chờ chốt thay đổi | |
| D06 — Chương 3–4 | Đạt | Nhi, Quỳnh | Chưa viết theo cấu trúc mới | |
| N01 — Nguồn/từ điển | Nhi | Đạt, Quỳnh | Chờ thành viên thực hiện | |
| N02 — Quy tắc/ví dụ | Nhi | Đạt, Quỳnh | Chờ thành viên thực hiện | |
| N03 — Nhãn/đối chiếu | Nhi điều phối, cả ba kiểm | Theo vòng kiểm chéo | Chưa có nhãn người kiểm trong mẫu | |
| N04 — Độ nhạy/tin trọng điểm | Nhi | Đạt, Quỳnh | Chờ thành viên thực hiện | |
| N05 — Sửa quy tắc nếu có lỗi | Nhi | Đạt, Quỳnh | Chỉ thực hiện khi có lỗi xác định | |
| N06 — Chương 1–2 | Nhi | Đạt, Quỳnh | Chưa viết theo cấu trúc mới | |
| Q01 — Đối soát trực quan | Quỳnh | Đạt, Nhi | Chờ thành viên thực hiện | |
| Q02 — Dashboard trình duyệt | Quỳnh | Đạt, Nhi | Chờ kiểm phiên bản 6.936 tin | |
| Q03 — Excel thực tế | Quỳnh | Đạt, Nhi | Chờ thao tác trong Excel | |
| Q04 — Demo/ảnh minh chứng | Quỳnh | Đạt, Nhi | Chờ chốt phiên bản | |
| Q05 — Khả năng sử dụng | Quỳnh | Đạt, Nhi | Chờ thử và ghi lỗi | |
| Q06 — Chương 5–6/định dạng | Quỳnh | Đạt, Nhi | Chưa viết theo cấu trúc mới | |

## 2. Theo dõi cải tiến

| Task | Chủ trì | Trạng thái | Giả thuyết/commit/kết quả/quyết định |
|---|---|---|---|
| I01 — Bộ đối chiếu nhãn | Nhi | P0: chưa thực hiện | |
| I02 — Nghiệm thu/demo thật | Quỳnh | P0: chưa thực hiện | |
| I03 — Môi trường độc lập | Đạt | P0: chưa thực hiện | |
| I04 — CI kiểm thử | Đạt | P1: chưa triển khai | |
| I05 — Cảnh báo chất lượng | Nhi | P1: chưa triển khai | |
| I06 — Lọc diện tích/xuất tóm tắt | Quỳnh | P1: chưa triển khai | |
| I07 — So sánh trong cùng loại | Quỳnh | P1: chưa triển khai | |
| I08 — Benchmark/index | Đạt | P1: chưa triển khai | |
| I09 — Độ nhạy K-means mở rộng | Đạt | P2: tùy thời gian | |
| I10 — Nguồn dữ liệu mới | Nhi | P2: khảo sát cho hướng phát triển | |

## 3. Mẫu ghi nghiệm thu một task

Sao chép khối sau mỗi khi có lần kiểm mới; không sửa bản ghi cũ thành kết quả mới.

```text
Mã task / lần kiểm:
Người làm / người kiểm chéo:
Ngày thực hiện:
Commit và run_id:
Môi trường và đầu vào:
Bước/lệnh thực hiện:
Mong đợi:
Kết quả thực:
File minh chứng:
Lỗi/giới hạn còn lại:
Quyết định và lý do:
Trạng thái: đang làm / chờ kiểm / đạt / cần sửa
```

## 4. Mẫu đọc nhãn độc lập và xử lý bất đồng

Người đọc thứ hai kiểm nguồn trước khi đọc kết luận đầu, lưu nhãn độc lập vào bảng này rồi đối chiếu. Chưa có kết quả nào được tự điền. Giữ cả hai kết luận nếu bất đồng; người thứ ba và hai người đọc thống nhất quyết định cuối khi có đủ bằng chứng.

| row_id/run_id | Người đọc 2/ngày | Loại hình độc lập | Giao dịch độc lập | Trạng thái giá/diện tích độc lập | Cụm số/chữ làm bằng chứng | So với lượt 1 | Kết luận sau thảo luận/người thứ ba |
|---|---|---|---|---|---|---|---|

Không đưa nguyên văn số điện thoại/địa chỉ chi tiết vào nhật ký công khai khi chỉ cần cụm số/chữ để giải thích quy tắc. Tin đọc thêm có chủ đích phải ghi nhãn “ngoài mẫu 60”.
