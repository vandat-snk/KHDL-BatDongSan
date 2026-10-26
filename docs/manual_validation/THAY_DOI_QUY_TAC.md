# Sửa quy tắc từ mẫu phát triển

Ngày 26/10/2026. Căn cứ: 120 nhận xét AI và các ca hồi quy đã biết. Không có nhãn người đọc độc lập; không tính accuracy.

| Vấn đề | Bằng chứng phát triển/hồi quy | Thay đổi và giới hạn |
|---|---|---|
| Nhầm chung cư trong câu so sánh hoặc địa điểm lân cận | 8148; ca tổng hợp bán đất gần chung cư | Câu “chung cư hay nhà” trả other_unknown và cờ rà soát; bỏ từ loại trong một số cụm lân cận/xây tương lai. Không lấy mô tả tự động ghi đè loại. |
| Viết dính/chính tả hẹp | 8764,8314,8459; hồi quy2331 | Sửa nội bộ các cụm Bánđất, ĐấtBán, đat, cho thê, hoạc khi phân loại; nguồn gốc không đổi. Không fuzzy match toàn văn. |
| Thiếu nhãn dãy trọ | 8592,7088,5494,3934 | Nhận dãy trọ/dãy phòng trọ là house; nhận biến thể dạy trọ đã gặp. CCMN được nhận apartment; dạng viết tắt khác vẫn có thể bỏ sót. |
| Cách ly vì “tiện cho thuê” | 3370 | Bỏ cụm công năng khỏi kiểm giao dịch; tin bán có thể giữ nhưng vẫn mang cờ chênh diện tích. “Bán hoặc cho thuê” vẫn bị cách ly. |
| Giá tổng thực ra tiền trả trước | 7028,7121;7030 đã bị loại từ trước | Khi khoản thanh toán ban đầu được ghi rõ và bằng giá lõi (dung sai1%), cách ly với lý do riêng. Không loại mọi tin hỗ trợ vay. Chưa nới quy tắc title trả trước cũ cho các tin3862/653, chờ người đọc xác nhận chính sách. |
| Giá trên100/1000m2 | 8891; đối chứng3251 | Cách ly khi giá lõi bằng giá cho một khối diện tích nhưng diện tích lõi khác khối. Nếu tổng đã được chuyển đúng hoặc diện tích đúng một khối, không loại theo quy tắc này. Không tự đổi sào/công. |
| Mâu thuẫn nhỏ hơn5lần bị bỏ qua | 5494,3370,8929,6515,4413 | Thêm cờ mềm cho một khai báo số rõ chênh trên1%; vẫn giữ tin và số lõi. Ngưỡng1% là bộ lọc rà soát, không phải sai số đo được chứng minh. Chênh >=5lần vẫn dùng chính sách cách ly cũ. |
| Đọc giá kép thành tiền tỷ phần đầu | 8592,5903,7767,2491 | Nhận phần triệu3chữ số sau khoảng trắng; phần1–2chữ số còn mơ hồ thì bỏ phép so giá đó, không tạo mâu thuẫn giả từ tiền tố. |

Các giới hạn chưa sửa: nhiều lô trong một tin; nhãn chỉ thấy trong mô tả; office/tòa dịch vụ; số gần đúng; giá/diện tích khác ý nghĩa; tin bán nhưng tiêu đề chỉ nói cho thuê; đơn vị vùng miền. Các trường hợp này được ghi nhận riêng, không ép thành nhãn đúng.

DEVELOPMENT_RULE_DIFF.csv chỉ so các trường loại/giao dịch/giữ-cách ly/cờ/lý do trên120 tin. Bỏ ba cờ địa lý khỏi phép so vì packet đọc tin không đưa location vào hàm làm sạch thử nghiệm. Không chạy IQR/K-means ở đây. Đây là kiểm tác động trong development, không phải kết quả tái chạy toàn bộ9004 tin.
