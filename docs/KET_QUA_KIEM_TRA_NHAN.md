# Rà soát nội dung tin bằng trợ lý

Ngày kiểm 16/10/2026; run_id `20261016T015620Z-f2e661a6`. Người thực hiện: trợ lý Codex.

Đã đọc tiêu đề và mô tả của 60 tin trong mẫu có sẵn, lưu diễn giải từng tin tại [CSV rà soát](DOI_CHIEU_60_TIN_TRO_LY.csv). Có 40 tin giữ và 20 tin cách ly. Sáu tầng lấy mười tin mỗi tầng; đây không phải mẫu ngẫu nhiên đồng tỷ lệ.

Đây là một lượt đọc bằng trợ lý, không phải hai người gán nhãn độc lập, không phải xác minh thực địa. Không điền thay các cột `human_*` trong mẫu gốc. Không tính precision/accuracy hoặc tỷ lệ lỗi toàn bộ dữ liệu từ mẫu này. `no_explicit_conflict` chỉ nghĩa chưa thấy mâu thuẫn rõ trong văn bản, không chứng thực giao dịch.

## Phát hiện cần nêu khi viết

| Dòng nguồn | Quan sát | Cách diễn giải |
| --- | --- | --- |
| 5900, 4759, 6677, 3696, 1915, 6181, 8773 | Mô tả có thể cung cấp loại hình mà tiêu đề viết tắt/thiếu từ | Nhãn chỉ từ tiêu đề có thể bỏ sót; chưa sửa thành bộ phân loại đã kiểm chứng |
| 2331 | Biến thể bán/cho thuê trong tiêu đề | Quy tắc từ khóa có thể bỏ lọt chính tả |
| 5093 | 9,7 tỷ so với 9,9 tỷ | Kiểm tra tỷ lệ chênh lớn không bắt mọi sai khác |
| 8151 | 18.000 so với 180.000 m² | Không tự chọn số đúng hoặc xóa một số 0 |
| 683, 2980, 7133, 4588 | Giá/lô, giá/diện tích hoặc điều kiện thanh toán | Giá tổng có thể chưa được xác định chắc chắn |
| 4288, 3111 | Bị cách ly theo chính sách bảo thủ | Không gọi là chứng minh tin sai/giả |
| 3133, 6181 | Đất, xây dựng, sàn, pháp lý, thực tế khác nhau | Không coi mọi diện tích trong cùng mô tả là cùng đại lượng |

Đã đọc thêm bảy tin trọng điểm ngoài mẫu: 638 (20 triệu/m² khác tổng giá), 7811 (860 tỷ so với 860 triệu), 335 (2 m² so với 2 ha), 8262 (3m2×5 là biểu thức kích thước chưa rõ), 300 (nhiều lô/diện tích), 588 (sang quán ngoài phạm vi), 8535 (6 m² so với mô tả 55/60 m²). Tin ngoài mẫu không được cộng vào mẫu 60 để tính tỷ lệ.

## Độ nhạy bổ sung

Thử loại riêng 16 tin giữ được trợ lý chọn do nghi vấn giá/diện tích/giao dịch, gồm cả 8535 ngoài mẫu; còn 6920 tin. Trung vị diện tích 70 m²; giá 2.25 tỷ; đơn giá 32.360781 triệu/m². Danh sách ID và giá trị chưa làm tròn ở `outputs/ASSISTANT_CHECKS.json`.

Đây là phân tích tình huống có chủ đích, không phải sửa bộ dữ liệu chính hay ước lượng độ lệch. Chưa loại hết tin đáng ngờ. Trung vị ít thay đổi cũng không chứng minh nhãn từng tin đúng. Báo cáo phải giữ giới hạn này; chưa được khẳng định toàn bộ 6.936 tin đã xác minh.

Nhóm không bắt buộc đọc lại 60 tin. Nếu muốn công bố độ chính xác nhãn hoặc nghiên cứu riêng về bộ nhận diện, khi đó mới cần một thiết kế gán nhãn người thật độc lập.
