# Phạm vi kiểm chứng Excel

Ngày ghi nhận 16/10/2026; run_id `20261016T015620Z-f2e661a6`. Trợ lý thực hiện kiểm bằng mã và thử mở giao diện; chưa có xác nhận thao tác Excel thật của thành viên.

## Những gì đã kiểm được

- Đối soát đủ 6.936 dòng và KPI workbook với CSV/JSON/SQLite bằng verifier; metadata/hash đúng phiên bản.
- Workbook có ba trang và bốn biểu đồ; công thức/cache được kiểm riêng.
- Artifact Tool tính lại sau sửa giá và diện tích trên bản thử, kiểm tám đầu vào không hợp lệ và quét lỗi công thức. Bằng chứng: `outputs/workbook_test_results.json`.
- Cột I tính đơn giá từ H/G khi cả hai là số dương; Q/R chuyển tỷ/triệu, S nhận diện tích hợp lệ. Dashboard Excel tính các KPI động từ vùng công thức tương ứng.
- Cờ IQR/nhãn cụm và các bảng snapshot không chạy lại K-means khi sửa ô. Đổi nguồn/quy tắc cần dựng pipeline và workbook lại.

Đã thử dùng Microsoft Excel mở bản sao `tmp/native_excel/KHDL_QA.xlsx`. Hộp Open hiển thị nhưng lệnh nhập không làm xuất hiện đường dẫn; chưa mở được workbook trong lượt thao tác này. Do đó **chưa xác nhận** tính lại, lọc/sắp xếp hoặc bố cục bằng Microsoft Excel thật. Không dùng kiểm của Artifact Tool để điền trạng thái Excel thật là đạt. Workbook gốc trong outputs không bị sửa bởi thử UI này.

## Một bước tổng duyệt ngắn cho nhóm

Quỳnh mở `outputs/DO_AN_BAT_DONG_SAN.xlsx` bằng Excel trên máy demo, xem ba trang/bốn biểu đồ và đối chiếu KPI 6.936 tin, 2,25 tỷ, 70 m², 32,32051282 triệu/m². Chụp một màn hình có số liệu nếu dùng trong báo cáo.

Nếu cần minh họa tính lại, tạo bản sao riêng rồi kiểm dòng dữ liệu Excel 10: G10=100, H10=2.380.000.000, I10=23.800.000. Đổi H10 thành 3.380.000.000 thì I10 mong đợi 33.800.000; hoặc phục hồi H10 và đổi G10 thành 200 thì I10=11.900.000. Chỉ thử trong bản sao, không lưu dữ liệu minh họa đè workbook chuẩn. Không cần lặp tám trường hợp lỗi đã có kiểm bằng công cụ, trừ khi thấy lỗi thực tế.

| Người/ngày/run_id | Mở trang/biểu đồ và KPI | Thử tính lại nếu có | Ảnh/ghi chú |
| --- | --- | --- | --- |
| Chờ nhóm ghi kết quả thực | Chưa xác nhận Excel thật | Chưa xác nhận Excel thật | Không ký thay |

Đây là phần tổng duyệt sử dụng cuối cùng, không phải yêu cầu kiểm lại từng dòng hoặc dựng workbook từ đầu.
