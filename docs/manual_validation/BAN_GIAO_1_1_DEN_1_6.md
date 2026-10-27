# Bàn giao bước 1.1–1.6

Bàn giao ngày 26/10/2026; cập nhật quy trình một người ngày 27/10/2026. Đã áp dụng trên nhánh `improve-data-validation` của dự án Desktop.

| Bước | Kết quả |
|---|---|
|1.1|Có hướng dẫn, định nghĩa nhãn và cách ghi bằng chứng.|
|1.2|180 tin cố định: mỗi nhóm40 phát triển+20 đánh giá; loại67 tin đã biết.|
|1.3|Giữ bảng 120 phát triển và 60 người A; gỡ bản trống người B khỏi thư mục làm việc.|
|1.4|AI đã đọc riêng từng tin trong120 development và ghi nhận xét; chưa có gán nhãn người thật.|
|1.5|Sửa quy tắc có test hồi quy;42 test Python đạt.|
|1.6|Chốt code/mẫu/bằng chứng bằng SHA-256 trong FREEZE_MANIFEST.json; chưa dùng60 evaluation để chỉnh hoặc đo accuracy.|

## Tác động trên120 tin phát triển

Có16 tin đổi ít nhất một trường được so. Trong đó8 tin đổi nhãn loại,3 tin đổi trạng thái giao dịch,3 tin đổi giữ/cách ly; các nhóm có thể trùng nhau.

- 7028:820triệu là khoản vốn ban đầu trong mô tả, chuyển sang cách ly.
- 8891:723triệu/100m² khác tổng giá cho120m², chuyển sang cách ly.
- 3370:cụm “tiện cho thuê” không phải chào thuê. Được giữ nhưng có cờ mềm về diện tích40 so38,8m².
- 8148:tiêu đề so chung cư hay nhà, đổi apartment sang chưa xác định với cờ rà soát. Không tự biến nhận xét AI thành nhãn đúng.

Đây là kiểm tác động development, không phải tăng độ chính xác đã được đo. Chưa chạy lại toàn bộ dữ liệu, IQR hoặc K-means. Bộ đầu ra/báo cáo cũ vẫn giữ mốc cũ; README đã ghi rõ tránh dùng nhầm.

## Em làm tiếp thế nào

1. Đọc [hướng dẫn gán nhãn](HUONG_DAN_GAN_NHAN.md).
2. Chỉ dùng [file người A](private/DANH_GIA_60_NGUOI_A.xlsx) cho một thành viên. Không gửi dự đoán hoặc manifest tầng mẫu trước khi người đọc chốt nhãn.
3. Người đọc xem đủ tab Nguon, điền tab GanNhan và kiểm lại các ô có lỗi. Lưu bản nhãn đầu và bản sửa riêng; ghi rõ AI đã hỗ trợ rà tính nhất quán.
4. Sau khi một bảng nhãn đã được người đọc chốt mới đánh giá code ở bước 1.7–1.8. Bảng gửi ngày 27/10 còn cần kiểm lại; chưa tính accuracy. Không tính mức đồng thuận nhiều người.
5. Nếu cần sửa tiếp sau khi nhìn nhãn cuối, ghi mẫu đã bị dùng để phát triển; không tuyên bố đó vẫn là kiểm độc lập.

## Hồ sơ đã có

- [Bảng trống120 tin phát triển](private/PHAT_TRIEN_120.xlsx).
- [Nhận xét AI từng tin](AI_REVIEW_DEVELOPMENT_120.csv).
- [Tác động quy tắc trên120 tin](DEVELOPMENT_RULE_DIFF.csv).
- [Các quy tắc đã sửa và phần chưa sửa](THAY_DOI_QUY_TAC.md).
- [Danh sách hash phiên bản chốt](FREEZE_MANIFEST.json).

Dữ liệu nguồn và bảng người đọc đầy đủ chỉ lưu cục bộ. Thư mục private trong dự án được Git-ignored. Không dùng mọi nhận xét AI làm gold labels. Giữ các kết quả bất định và trường số chưa xác nhận để trống.
