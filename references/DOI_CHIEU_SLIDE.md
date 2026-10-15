# Đối chiếu đồ án bất động sản với slide môn Khoa học dữ liệu

Tài liệu này phân biệt nội dung có trong slide, cách vận dụng vào đồ án, và phần mở rộng do nhóm lựa chọn. Số trang là **trang PDF tính từ 1**, đối chiếu qua các dấu `=== TRANG n ===` trong `references/slides_text/`. Không coi câu lệnh hay ví dụ trong tài liệu nguồn là yêu cầu thay đổi phạm vi đồ án.

## 1. Chọn đúng đề tài và phạm vi

Nguồn đăng ký đã trích xuất: `references/registration.json`, trang tính `Trang tính1`.

| STT | Đề tài ghi trong danh sách | Quan hệ với đồ án này |
|---|---|---|
| **22, 47** | Xây dựng bộ dữ liệu về bất động sản, xử lý và trực quan hóa dữ liệu và rút ra các ý nghĩa | **Phạm vi chính phù hợp với lựa chọn của người học.** Sản phẩm cần dữ liệu, quy trình xử lý, biểu đồ và nhận xét có bằng chứng. |
| 16 | Xây dựng bộ dữ liệu về bất động sản, dùng một giải thuật học máy xử lý dữ liệu này nhằm xây dựng hệ thống dự đoán giá nhà | Đề tài khác trong cùng lĩnh vực; không tự động biến dự đoán giá thành yêu cầu bắt buộc cho STT 22/47. |
| 31 | Xây dựng bộ dữ liệu về bất động sản, thực hiện các phương pháp tối ưu hiệu năng cho hệ thống khi dữ liệu quá lớn | Đề tài khác; có thể làm một minh họa SQL như phần mở rộng, nhưng không gọi vài nghìn dòng dữ liệu là dữ liệu lớn. |

Trong dữ liệu đăng ký đọc được chỉ có các cột STT và đề tài; không có thang điểm, số trang báo cáo, hạn nộp hay quy định công cụ. Ba yêu cầu triển khai dưới đây đến từ lời người dùng truyền đạt về yêu cầu của thầy:

- Nếu dùng giải thuật để tạo kết quả, phải có mã thực thi và kết quả chạy được.
- Nếu cần trực quan hóa, có thể dùng bất kỳ công cụ phù hợp, kể cả Excel.
- Nếu trình bày tối ưu SQL, phải tạo cơ sở dữ liệu và có SQL minh họa thực tế.

Tên đề xuất cho phần chính: **Xây dựng, xử lý và trực quan hóa bộ dữ liệu bất động sản để khám phá các yếu tố liên quan đến giá nhà**. Nếu bộ dữ liệu ở nước ngoài, phải ghi địa bàn, thời gian và đơn vị tiền tệ của dữ liệu đó trong tiêu đề phụ và phần giới hạn; không suy diễn thành kết quả cho thị trường Việt Nam hiện tại.

## 2. Ma trận đối chiếu nội dung cốt lõi

“Cốt lõi” dưới đây là phạm vi đề xuất để đáp ứng đề tài STT 22/47, không phải thang điểm chính thức của giảng viên.

| File slide | Trang PDF | Nội dung thực sự có trong slide | Vận dụng cụ thể và bằng chứng nên đưa vào báo cáo | Phạm vi |
|---|---:|---|---|---|
| `Chuong 1 - Mo dau.pdf` | 3–5 | Khoa học dữ liệu nhằm trích xuất tri thức, hiểu hiện tượng; phân biệt hiểu biết và dự đoán | Đặt 3–5 câu hỏi phân tích, mỗi kết luận dẫn tới bảng/biểu đồ; kết luận về mối liên hệ trong mẫu dữ liệu | Cốt lõi |
| `Chuong 1 - Mo dau.pdf` | 12 | Kỹ năng định lượng, kỹ thuật, tư duy hoài nghi, hợp tác và truyền đạt | Phân công 3 thành viên có sản phẩm và người kiểm tra chéo; nêu giới hạn dữ liệu và cách phản biện kết luận | Cốt lõi |
| `Chuong 2 - Chuan bi du lieu.pdf` | 3, 5 | Dữ liệu thô có thể thiếu, nhiễu, không nhất quán; nguồn file/CSDL và dữ liệu có cấu trúc | Lưu bản dữ liệu gốc bất biến, URL nguồn, ngày tải, quyền sử dụng; mô tả mỗi dòng là gì và từ điển cột | Cốt lõi |
| `Chuong 2 - Chuan bi du lieu.pdf` | 6–8 | Dữ liệu thiếu; bỏ qua, xử lý tay, thay thế bằng hằng số/mode/trung bình toàn cục hoặc cục bộ/giá trị dự đoán; ngăn thiếu bằng ràng buộc | Lập bảng thiếu trước/sau, phân biệt thiếu thật với “không có tiện ích”, quy tắc riêng theo cột; lưu cờ và số dòng chịu tác động | Cốt lõi |
| `Chuong 2 - Chuan bi du lieu.pdf` | 9–10 | Khái niệm outlier; phát hiện theo phân bố, khoảng cách, mật độ và độ lệch | Kiểm tra miền hợp lệ và gắn cờ giá/diện tích khác biệt; xem biểu đồ và dữ liệu gốc trước khi quyết định; nêu tác động của việc giữ/loại | Cốt lõi |
| `Chuong 2 - Chuan bi du lieu.pdf` | 11–13 | Giảm nhiễu bằng hồi quy/phân cụm; phát hiện không nhất quán qua siêu dữ liệu, ràng buộc, kiểm tra của nhà phân tích; biến đổi tự động | Chuẩn kiểu số/ngày, cách viết nhãn, đơn vị, kiểm tra ID và bản ghi lặp; nhật ký xử lý có lý do. Chỉ cần dùng phương pháp phù hợp, không bắt buộc hồi quy/phân cụm để làm sạch | Cốt lõi ở xử lý nhất quán |
| `Chuong 2 - Chuan bi du lieu.pdf` | 14–17 | Vì sao cần co giãn; Min–Max, Z-score, độ lệch chuẩn | Giữ biến có đơn vị gốc để diễn giải; minh họa cột đã chuẩn hóa nếu dùng khoảng cách/phân cụm, ghi công thức và tham số | Cốt lõi ở giải thích; thực thi co giãn khi có nhu cầu |
| `Chuong 2 - Chuan bi du lieu.pdf` | 18–19 | Lấy mẫu tĩnh: có/không thay thế, thiên vị, phân tầng | Phân tích toàn bộ dữ liệu nếu đủ nhỏ; nếu lấy mẫu để vẽ, ghi seed, kích thước và lý do, không lấy mẫu rồi bỏ quên sai lệch | Khi cần |
| `Chuong 2 - Chuan bi du lieu.pdf` | 23–24, 26–27 | Lựa chọn thuộc tính, giảm số hàng/cột và mất thông tin; PCA/SVD/LSA được nêu | Chọn biến giá, diện tích, vị trí, chất lượng, số phòng/năm xây phù hợp dữ liệu; loại ID khỏi phép đo khoảng cách. Không bắt buộc PCA | Cốt lõi ở chọn biến |
| `Chuong 2 - Chuan bi du lieu.pdf` | 28–29 | Tổng hợp, khái quát hóa, tạo thuộc tính mới, rời rạc hóa, mã hóa phân loại/one-hot | Tạo tuổi nhà theo năm bán, nhóm diện tích, chỉ số giá trên đơn vị diện tích với định nghĩa rõ; tổng hợp theo khu vực | Cốt lõi |
| `Chuong 3 - Truc quan hoa du lieu.pdf` | 3–4, 6–7 | Trực quan hóa phục vụ phân tích, trình bày, giải thích; Visual Data Mining; Matplotlib | Xây bộ biểu đồ trả lời câu hỏi nghiên cứu; dashboard và hình xuất phục vụ báo cáo; công cụ do nhóm lựa chọn | Cốt lõi |
| `Chuong 3 - Truc quan hoa du lieu.pdf` | 14–15 | Bar chart cho dữ liệu phân loại | So sánh trung vị giá và số mẫu theo khu vực/loại nhà; sắp xếp dễ đọc, ghi ngưỡng số mẫu khi cần | Cốt lõi |
| `Chuong 3 - Truc quan hoa du lieu.pdf` | 16–18 | Scatter plot cho mối quan hệ giữa hai biến | Biểu đồ diện tích–giá, có màu theo chất lượng/khu vực nếu phù hợp; mô tả xu hướng và điểm khác biệt | Cốt lõi |
| `Chuong 3 - Truc quan hoa du lieu.pdf` | 22–25 | Histogram, phân phối tần suất, mật độ và binning hai chiều | Phân phối giá/diện tích trước và sau xử lý; ghi đơn vị, số bin hoặc cách chọn bin; có thể thêm trục log để đọc dữ liệu lệch | Cốt lõi |
| `Chuong 3 - Truc quan hoa du lieu.pdf` | 26–30 | Tiêu đề, nhãn trục, văn bản và chú thích | Mỗi hình có tiêu đề, đơn vị, chú giải, nguồn, số mẫu và ghi chú xử lý; đánh số hình để trích dẫn trong báo cáo | Cốt lõi |
| `Chuong 3 - Truc quan hoa du lieu.pdf` | 8–13 | Biểu đồ đường thường dùng cho chuỗi thời gian | Chỉ vẽ khi có thời điểm thực; ví dụ giá trung vị theo năm bán và số giao dịch theo năm, ghi rõ là mẫu giao dịch quan sát được | Khi dữ liệu có thời gian |
| `Chuong 3 - Truc quan hoa du lieu.pdf` | 19–21 | Trực quan hóa lỗi/độ bất định | Thanh sai số hoặc khoảng tin cậy khi có phương pháp tính phù hợp; mô tả cách tính và giả định, không chỉ thêm vùng màu trang trí | Mở rộng |
| `Chuong 3 - Truc quan hoa du lieu.pdf` | 38–40 | Dữ liệu địa lý; Basemap được giới thiệu ở trang 39 | Bản đồ chỉ khi dữ liệu có tọa độ hoặc ranh giới có nguồn hợp lệ; nếu chỉ có tên khu vực, biểu đồ theo khu vực đã phù hợp | Mở rộng có điều kiện |

## 3. Ma trận phần mở rộng

| File slide | Trang PDF | Nội dung thực sự có trong slide | Cách triển khai phù hợp | Điều kiện và mức độ |
|---|---:|---|---|---|
| `Chương 4 - Hoc may - 2.pdf` | 41, 44–51 | Học không giám sát; khoảng cách, trọng tâm; K-means, các bước gán cụm/cập nhật tâm và điều kiện dừng | Phân nhóm các căn nhà theo một số biến số đã chuẩn hóa; có code, seed, lựa chọn k, bảng mô tả từng cụm, biểu đồ và kiểm tra hội tụ | Mở rộng sát slide; cụm là cấu trúc tính toán, tên cụm do nhóm diễn giải |
| `Chương 4 - Hoc may - 2.pdf` | 52–53 | Ví dụ K-means với k=2 | Có thể kèm một ví dụ nhỏ tự tính một vòng lặp để giải thích được khi vấn đáp | Mở rộng giáo dục |
| `Chương 4 - Hoc may - 2.pdf` | 54–60 | HAC và các cách đo Single/Complete/Centroid/Group Average | So sánh với K-means nếu nhóm đủ thời gian, ưu tiên mẫu vừa phải do chi phí tính toán | Mở rộng thêm, không bắt buộc |
| `Chuong 4 - Hoc may.pdf` | 6; `Chương 4 - Hoc may - 2.pdf` trang 3 | Phân biệt phân lớp đầu ra rời rạc và hồi quy đầu ra liên tục | Nếu thử dự đoán giá, xác định là hồi quy; baseline và sai số phải phù hợp biến giá | Phần phụ, không thay thế EDA |
| `Chuong 4 - Hoc may.pdf` | 8–32, 36–40 | Cây quyết định và kNN được trình bày chủ yếu cho **phân lớp** | Không khẳng định slide đã dạy chi tiết DecisionTreeRegressor/KNeighborsRegressor; nếu dùng biến thể hồi quy cần ghi rõ là mở rộng có tài liệu bổ sung | Mở rộng ngoài phần trình bày chi tiết |
| `Chương 4 - Hoc may - 1.pdf` | 6–10, 13–15, 18–20 | Đánh giá thực nghiệm; hold-out; k-fold; tập validation; overfitting/underfitting | Chia train/test trước thao tác học tham số; chỉ tối ưu trên train/validation; khóa test đến lần đánh giá cuối | Bắt buộc về phương pháp nếu làm dự đoán |
| `Chuong 4 - Hoc may.pdf` | 41; `Chương 4 - Hoc may - 2.pdf` trang 40 | Accuracy, Precision, Recall, F-measure cho phân lớp | Chỉ dùng khi đầu ra là nhãn phân lớp; với giá liên tục, dùng MAE/RMSE/R² như kiến thức mở rộng và dẫn nguồn riêng | Không dùng sai chỉ số |
| `Chuong 5 - Co so du lieu va SQL - 1.pdf` | 3–4, 23–32 | Nhóm lệnh SQL, INSERT/SELECT/WHERE/GROUP BY/ORDER BY; tạo DB/bảng, khóa chính/khóa ngoại/UNIQUE | Tạo DB thật, bảng nhà và bảng khu vực, nhập dữ liệu; truy vấn tổng hợp giá và số mẫu theo khu vực; mô tả sơ đồ và ràng buộc | Mở rộng SQL có minh chứng |
| `Chuong 5 - Co so du lieu va SQL - 1.pdf` | 13–17, 36–38 | Hàm tổng hợp; index và đánh đổi giữa đọc nhanh với chi phí ghi | Đo cùng truy vấn trước/sau index trên điều kiện lọc phù hợp; ghi số dòng, thiết bị, số lần đo, kế hoạch truy vấn và kết quả tương đương | Nếu tuyên bố tối ưu thì phải chạy thật |
| `Chuong 5 - Co so du lieu va SQL - 1.pdf` | 39–45 | View và ví dụ truy vấn/tổng hợp | View thống kê theo khu vực để tái sử dụng; phân biệt view với bảng vật lý | Mở rộng nhẹ |
| `Chuong 5 - Co so du lieu va SQL - 2.pdf` | 36–40 | Ví dụ tối ưu truy vấn, có JOIN/tìm theo ID ở 37–38, JOIN/tìm theo NAME ở 39, không JOIN/tìm theo NAME ở 40 | So sánh phương án trên DB của nhóm, bảo đảm cùng nghĩa và cùng kết quả; không mặc định JOIN hoặc index luôn nhanh hơn | Phương pháp đối chiếu; tốc độ phải đo |
| `Chuong 6 - He khuyen nghi.pdf` | 5–10, 12–17 | Hồ sơ người dùng, lọc nội dung, lọc cộng tác và vấn đề dữ liệu thưa | Nếu gợi ý nhà tương tự theo diện tích/vị trí/chất lượng, giải thích là dựa vào thuộc tính; không gọi là lọc cộng tác khi chưa có đánh giá hoặc hành vi người dùng | Mở rộng tùy chọn, không cần cho STT 22/47 |

Các thuật ngữ như **IQR, boxplot, Spearman/Pearson heatmap, bootstrap CI cho trung vị, silhouette, MAE/RMSE/R²** có thể hữu ích cho đồ án nhưng không được trình bày chi tiết trong các trang slide đã trích xuất ở trên. Nếu sử dụng, ghi rõ là kỹ thuật bổ sung, giải thích công thức/cách tính và dẫn nguồn chuyên môn riêng. Min–Max và Z-score được nêu trực tiếp trong Chương 2; K-means có các bước thuật toán trực tiếp trong Chương 4 phần 2.

## 4. Các điểm cần hiểu đúng để bảo vệ đồ án

### Dữ liệu thiếu và chất lượng dữ liệu

- Một ô trống có thể có nghĩa “không biết” hoặc “không có tiện ích”. Phải xem mô tả nguồn trước khi thay thế; ví dụ không có garage khác với chưa biết diện tích garage.
- Không điền giá bán thiếu bằng trung bình rồi dùng dòng ấy để suy ra phân phối giá hoặc đánh giá mô hình. Dòng không có biến mục tiêu có thể bị loại khỏi phân tích giá, với số lượng và lý do được ghi lại.
- Median imputation là lựa chọn bổ sung hợp lý với biến lệch nhưng không được nêu tên trực tiếp ở trang 8. Nếu dùng, nói rõ vì sao ưu tiên trung vị, tập nào được dùng để tính và có cờ đánh dấu giá trị được điền.
- Chỉ số giá/diện tích phải ghi mẫu số cụ thể: diện tích đất, diện tích sàn hay diện tích sinh hoạt. Kiểm tra mẫu số dương, hữu hạn và dùng đơn vị nhất quán; không đổi tên diện tích sinh hoạt thành diện tích đất.
- Giữ raw và cleaned riêng, có nhật ký thay đổi; bảng chất lượng trước/sau phải có số dòng, số cột, thiếu, trùng, miền giá trị lỗi và số outlier được gắn cờ. Các mục có thể chồng nhau nên không cộng cơ học thành tổng số dòng loại.

### Ngoại lệ, chuẩn hóa và trực quan hóa

- Outlier không tự động là lỗi: nhà rất lớn/đắt có thể hợp lệ. Dùng gắn cờ và phân tích độ nhạy; nếu loại cần quy tắc, ví dụ và số dòng cụ thể. Chương 2 trang 9–10 là cơ sở cho kiểm tra outlier, **không chỉ định riêng quy tắc IQR 1,5 lần**.
- Chuẩn hóa cách viết nhãn/đơn vị để dữ liệu nhất quán khác với co giãn số bằng Min–Max/Z-score. Hai thao tác cần được trình bày riêng.
- Với phân tích mô tả, đơn vị gốc giúp người đọc hiểu giá/diện tích; chuẩn hóa không phải điều kiện để mọi biểu đồ đúng. Với khoảng cách Euclidean/K-means, co giãn giúp biến có độ lớn lớn không chi phối toàn bộ.
- Nếu làm học máy, imputer/scaler/encoder phải fit trên train rồi áp dụng lên validation/test. Nếu chỉ mô tả toàn bộ dữ liệu, có thể tính thống kê trên tập phân tích nhưng phải nói rõ mục đích.
- Biểu đồ đường cần trục có thứ tự/thời gian đúng; không nối các khu vực thành “xu hướng thời gian”. Bản đồ cần tọa độ/ranh giới thật; không gán tọa độ giả để có bản đồ.
- Giá nhà thường lệch, nên báo cáo cả trung vị và trung bình, số mẫu, khoảng tứ phân vị; công bố xử lý outlier và log-transform nếu có. Tương quan diện tích–giá không chứng minh diện tích gây ra toàn bộ chênh lệch giá.

### Đánh giá và tính trung thực của kết luận

- Đồ án EDA được đánh giá thực chất bằng khả năng truy nguyên nguồn, độ nhất quán xử lý, biểu đồ phù hợp và nhận xét có số liệu; không cần Accuracy cho phần này.
- Với hồi quy, báo cáo MAE/RMSE theo cùng đơn vị tiền tệ và R² trên test, so với baseline đơn giản. Test không tham gia chọn mô hình, tham số, cột hay ngưỡng dựa trên kết quả. Các chỉ số này là phần mở rộng ngoài nội dung chỉ số phân lớp trong slide.
- Với K-means, không dùng Accuracy nếu không có nhãn đúng. Mô tả số lượng và đặc điểm cụm, so sánh các giá trị k, độ ổn định theo seed; silhouette/inertia là chỉ số bổ sung cần giải thích. Nhãn “cao cấp/bình dân” là diễn giải của nhóm, không phải chân lý thị trường.
- Với SQL, đo nhiều lượt trên cùng dữ liệu và kết quả; có thể không cải thiện trên dữ liệu nhỏ. Nêu cả thời gian, execution plan và chi phí chỉ mục. Nếu nhân bản dữ liệu để benchmark, gắn nhãn **dữ liệu tổng hợp chỉ phục vụ thử tải** và không trộn vào kết quả phân tích bất động sản.
- Nội dung khoảng tin cậy được nhắc ở Chương 1 trang 34. Khi mở rộng nên dùng cách diễn giải thống kê chuẩn: quy trình lấy mẫu tạo khoảng sẽ bao phủ tham số thật ở tỷ lệ đã chọn khi lặp lại theo giả định; không coi khoảng tin cậy của giá trung bình là khoảng chứa 95% tất cả giá nhà.
- Dữ liệu lịch sử tại một địa bàn chỉ hỗ trợ kết luận trong phạm vi mẫu và giai đoạn quan sát. Không đưa lời khuyên đầu tư hoặc dự báo thị trường Việt Nam từ dữ liệu nước ngoài/historical.

## 5. Danh sách bằng chứng tối thiểu nên có trong báo cáo

1. Trang xác định tên đề tài, phạm vi, câu hỏi nghiên cứu và ánh xạ vào Chương 1–3.
2. Nguồn dữ liệu, điều kiện sử dụng, thời gian/địa bàn, kích thước, từ điển và ví dụ bản ghi.
3. Sơ đồ luồng raw → kiểm tra → xử lý → dữ liệu phân tích → biểu đồ → nhận xét; bảng quy tắc xử lý có lý do và số dòng bị tác động.
4. Bảng chất lượng trước/sau; ví dụ thiếu/không nhất quán/outlier; minh họa co giãn khi có nhu cầu.
5. Bộ biểu đồ gồm phân phối giá/diện tích, quan hệ diện tích–giá, so sánh theo vị trí/nhóm thuộc tính. Mỗi hình trả lời một câu hỏi, có đơn vị và số mẫu.
6. Các kết luận định lượng liên kết trực tiếp tới hình/bảng, phân biệt mô tả, suy luận và giới hạn.
7. Phần mở rộng đặt riêng, có code/DB/SQL và log thực nghiệm tương ứng với tuyên bố. Không lấy độ phức tạp làm lý do thay thế chất lượng của phần chính.
8. Hướng dẫn chạy lại từ dữ liệu gốc; phiên bản thư viện, seed và file đầu ra; phân công 3 thành viên, sản phẩm mỗi người, kiểm tra chéo và việc cải tiến còn lại.

Lưu ý khả năng đọc nguồn: `Chuong 4 - Hoc may - Naive Bayes.pdf` có 6 trang nhưng phần trích xuất văn bản trống (khả năng là ảnh). Tài liệu đối chiếu này **không suy đoán** nội dung từng trang của file đó; các nhận định về Naïve Bayes, nếu cần, có thể tham chiếu `Chuong 4 - Hoc may.pdf` trang 33–35 và `Chương 4 - Hoc may - 2.pdf` trang 4–6. Các trang chỉ có hình khác cũng không được gán công thức chi tiết chưa kiểm chứng.
