# Kịch bản trình bày 10 phút và câu hỏi bảo vệ

> Cập nhật ngày 15/10/2026: kịch bản này thuộc bản nền trước đợt rà soát code và yêu cầu báo cáo sáu chương. Chưa dùng nguyên trạng làm kịch bản cuối. Lấy số liệu từ lần chạy đã kiểm chứng sau cùng; sắp xếp phần trình bày theo [yêu cầu báo cáo mới](DOI_CHIEU_YEU_CAU_BAO_CAO.md). Không dùng số cũ hoặc mô tả chức năng chưa được hiện thực.

**Nhóm:** Võ Văn Đạt — N23DCCN078; Nguyễn Thị Yến Nhi — N23DCCN112; Hứa Như Quỳnh — N23DCCN118.

**Thông điệp chính:** từ dữ liệu quảng cáo bất động sản có nhiều vấn đề, nhóm xây dựng một quy trình xử lý có thể kiểm chứng và dùng biểu đồ để trả lời các câu hỏi trong phạm vi mẫu. Phần chính gắn Chương 1–3; K-means và SQL là mở rộng có thực thi.

Đây là kịch bản để tập, chưa phải bằng chứng nhóm đã tự thực hiện mọi công việc. Trước khi bảo vệ, mỗi người phải chạy lại và xác nhận phần được giao trong [kế hoạch phân công](PHAN_CONG_VA_NOI_DUNG_BAO_CAO.md). Thay các vị trí cần số liệu bằng kết quả thật từ `outputs/analysis.json` và output cuối; không đọc số ước đoán theo hình. Các câu nói dưới đây là gợi ý, có thể diễn đạt tự nhiên theo hiểu biết của người nói.

## 1. Chuẩn bị demo

- Mở sẵn báo cáo/biểu đồ, Excel và `outputs/DASHBOARD_BAT_DONG_SAN.html`; kiểm tra chúng dùng cùng tập dữ liệu và bộ lọc ban đầu.
- Mở một ví dụ raw → processed → lineage; chọn dòng không chứa số điện thoại hoặc thông tin liên hệ trong mô tả khi trình chiếu.
- Nếu trình bày phần mở rộng, mở mã K-means, DB/SQL và bảng benchmark đã chạy. Không dành giờ bảo vệ để cài thư viện hoặc chờ tải mạng.
- Chuẩn bị ảnh minh chứng dự phòng từ sản phẩm thật để dùng khi máy chiếu hoặc ứng dụng gặp lỗi. Giữ dữ liệu gốc để kiểm chứng khi thầy hỏi.
- Đánh dấu nguồn và đơn vị dưới biểu đồ; không dùng ảnh số liệu không khớp lần chạy cuối.

## 2. Kịch bản 10 phút, mỗi người 3 phút 20 giây

| Thời gian | Người trình bày | Nội dung/slide gợi ý | Hành động và câu chuyển |
|---|---|---|---|
| 00:00–00:40 | Quỳnh | 1. Bài toán và tên nhóm | Nói tên đề tài; nêu mục tiêu xử lý, trực quan hóa và rút ý nghĩa |
| 00:40–01:10 | Quỳnh | 2. Câu hỏi và phạm vi | Nêu 3 câu hỏi chính; giải thích đây là giá rao lịch sử trong mẫu |
| 01:10–01:50 | Quỳnh | 3. Phân phối | Chỉ một phát hiện có số liệu từ histogram; giải thích trung vị/trục log |
| 01:50–02:35 | Quỳnh | 4. Quan hệ/so sánh | Nêu diện tích–giá và một so sánh giá/m², kèm n/giới hạn |
| 02:35–03:20 | Quỳnh | 5. Dashboard và kết luận EDA | Demo một bộ lọc; chỉ số mẫu thay đổi; chuyển sang nguồn/làm sạch |
| 03:20–04:00 | Nhi | 6. Nguồn có thể kiểm chứng | Mendeley v2, DOI/CC BY, 9.004 dòng thực; giải thích quảng cáo khác giao dịch |
| 04:00–04:45 | Nhi | 7. Vấn đề dữ liệu | Hai ví dụ thật về giá/đơn vị và trường chi tiết nghi ngờ; không đọc cả JSON |
| 04:45–05:35 | Nhi | 8. Quy tắc và kiểm toán | Một dòng trước/sau; chính sách trùng/cách ly; bảng số dòng cuối và lineage |
| 05:35–06:15 | Nhi | 9. Outlier và độ nhạy | Giải thích IQR gắn cờ; nêu kết quả độ nhạy chỉ sau khi nhóm đã chạy |
| 06:15–06:40 | Nhi | 10. Giới hạn dữ liệu | Không ngày/ID/tọa độ; không suy rộng; chuyển sang cách tái lập |
| 06:40–07:25 | Đạt | 11. Luồng và khả năng tái lập | Chỉ raw → pipeline → CSV/Excel/dashboard; môi trường và lệnh theo README |
| 07:25–08:20 | Đạt | 12. K-means nếu dùng | Biến, scaler, k/seed; một kết quả mô tả cụm; không gọi là dự đoán giá |
| 08:20–09:15 | Đạt | 13. SQLite/SQL nếu dùng | DB thật, truy vấn trước/sau index, plan và số đo thực; nêu giới hạn dữ liệu nhỏ |
| 09:15–10:00 | Đạt | 14. Đóng góp và kết thúc | Mỗi người một đóng góp đã kiểm chứng; 2 kết luận, giới hạn và cải tiến có thể làm |

Tổng thời lượng: Quỳnh **200 giây**, Nhi **200 giây**, Đạt **200 giây**. Nếu không trình bày mở rộng, Đạt dùng khoảng 07:25–09:15 để giải thích một quy tắc trong mã, chứng minh CSV–Excel–dashboard khớp và demo tái lập; không thêm kết quả học máy/SQL chưa có.

Khoảng 10–12 slide chính thường dễ theo dõi hơn 14 slide riêng. Có thể gộp các mục liên quan trong bảng; bảng đánh số nội dung, không bắt buộc số lượng slide. Giữ một phát hiện chính mỗi slide.

## 3. Lời nói gợi ý ở các đoạn quan trọng

**Quỳnh mở bài:** “Nhóm em chọn xây dựng, xử lý và trực quan hóa dữ liệu bất động sản. Mục tiêu là làm cho dữ liệu quảng cáo có thể phân tích được, sau đó trả lời các câu hỏi về phân phối giá rao, diện tích và khác biệt giữa những nhóm tin có đủ số mẫu. Phần chính bám Chương 1–3 của môn học.”

**Quỳnh khi giải thích biểu đồ:** “Hình này dùng tập [tên tập/bộ lọc thực], gồm [n thực] tin. Trục giá có đơn vị [đơn vị thực]. Trung vị là [giá trị thực], trong khi trung bình là [giá trị thực], cho thấy [nhận xét đúng theo kết quả]. Đây là mô tả các tin trong mẫu, chưa phải mức giá của toàn thị trường.”

**Quỳnh chuyển sang Nhi:** “Các hình chỉ có ý nghĩa khi dữ liệu đầu vào và quy tắc xử lý rõ ràng. Nhi sẽ trình bày nguồn, những vấn đề đã phát hiện và cách nhóm kiểm chứng dữ liệu.”

**Nhi về nguồn:** “Bộ dữ liệu Vietnam Real Estate Data được ba tác giả công bố trên Mendeley, phiên bản 2, giấy phép CC BY 4.0. Mô tả nguồn ghi 10.000 tin, nhưng file thực tế có 9.004 bản ghi. Nhóm dùng số đếm của file và công khai khác biệt này; checksum bản tải khớp manifest nguồn.”

**Nhi về chất lượng:** “Ô có giá trị chưa chắc là dữ liệu đúng. Một số trường chi tiết tiếp tục xuất hiện ở các tin có nội dung không ăn khớp, nên nhóm không sử dụng chúng để khẳng định số phòng hay pháp lý. Với giá hoặc diện tích không xác minh được, nhóm lưu trạng thái rà soát/cách ly thay vì tự sửa theo kỳ vọng.”

**Nhi về ngoại lệ:** “IQR giúp tìm điểm khác biệt trong phân bố; nó không chứng minh bản ghi sai. Nhóm giữ bản gốc, gắn cờ và so sánh kết quả khi có/không hiển thị các điểm này. Quyết định loại hẳn chỉ dùng cho điều kiện chất lượng có lý do rõ.”

**Nhi chuyển sang Đạt:** “Quy tắc không chỉ được mô tả bằng lời: mã xử lý và nhật ký từng dòng cho phép chạy lại. Đạt sẽ trình bày cách tái lập và các mở rộng đã thực thi.”

**Đạt về K-means:** “Phân cụm giúp mô tả những nhóm tin có đặc điểm gần nhau trong không gian biến đã chọn. Nhóm dùng [biến/log/scaler thực], k là [k thực], seed là [seed thực]. Nhãn tên cụm do nhóm diễn giải từ thống kê sau chạy; đây không phải mô hình dự đoán giá và không có nhãn chuẩn để tính Accuracy.”

**Đạt về SQL:** “Nhóm tạo DB thật từ CSV và chạy cùng truy vấn trước/sau index. Bảng này cho số dòng, số lượt, trung vị thời gian và kế hoạch thực thi. Với tập dữ liệu nhỏ, chênh lệch tốc độ có thể ít hoặc index chưa nhanh hơn; kết quả đo là minh chứng cho trường hợp này, không chứng minh tối ưu ở mọi quy mô.”

**Đạt kết thúc:** “Đóng góp chính là dữ liệu có nguồn rõ, xử lý có thể truy nguyên và các kết luận gắn với số liệu. Giới hạn lớn nhất là đây là tin rao không có ngày đăng/ID ổn định và mẫu không đại diện thị trường. Nếu phát triển tiếp, nhóm sẽ ưu tiên chất lượng nguồn và xác minh nhãn trước khi tăng độ phức tạp của thuật toán.”

Không đọc nguyên văn tất cả các đoạn. Bỏ các phần chưa chạy hoặc chưa kiểm chứng; cập nhật lời nói để khớp sản phẩm cuối.

## 4. Câu hỏi bảo vệ và cách trả lời

| Câu hỏi của thầy | Cách trả lời trọng tâm | Người chính | Minh chứng mở khi cần |
|---|---|---|---|
| Đề tài của nhóm có bắt buộc dự đoán giá không? | STT 22/47 yêu cầu xây dựng, xử lý, trực quan hóa và rút ý nghĩa. Nhóm hoàn thành phần chính Chương 1–3; K-means/SQL là mở rộng. Nếu dùng thuật toán thì có code; nếu nói tối ưu SQL thì có DB và SQL thực. | Quỳnh/Đạt | `references/DOI_CHIEU_SLIDE.md`, danh sách đăng ký |
| Dữ liệu tự thu thập hay tải về? | Nhóm dùng dữ liệu công khai của ba tác giả trên Mendeley v2; giữ nguyên raw, ghi nguồn/giấy phép và tự kiểm chứng/cải tiến quy trình được bàn giao. Không nhận là nhóm tự crawl nếu chưa crawl. | Nhi | Metadata, DOI, `DATA_SOURCE.md` |
| Vì sao nguồn ghi 10.000 nhưng báo cáo ghi 9.004? | Đó là khác biệt giữa mô tả và nội dung file tải. File JSON có 9.004 đối tượng và checksum khớp nguồn. Nhóm không biết lý do của tác giả nên công khai, không suy đoán/bù dữ liệu. | Nhi | Lệnh đếm JSON, checksum, manifest |
| Đây có phải giá giao dịch không? | Là giá nêu trong tin quảng cáo, trong báo cáo gọi giá rao. Không có hồ sơ xác nhận giao dịch. Tên biến kỹ thuật `sale_price_vnd` không làm giá rao trở thành giá đã bán. | Nhi | Trường `price` raw và từ điển |
| Dữ liệu có phản ánh giá hiện nay không? | File công bố năm 2021 và thiếu ngày đăng từng tin. Nhóm chỉ mô tả file lịch sử đó, không coi là giá năm 2026. Ngày tải là ngày lấy dữ liệu, không phải ngày giao dịch. | Nhi | Metadata nguồn, giới hạn trong báo cáo |
| Vì sao không dùng đầy đủ 29 trường? | Nhiều trường chi tiết có dấu hiệu không ăn khớp nội dung và kéo dài qua nhiều tin. Nhóm chọn trường lõi dễ truy nguyên; bỏ biến đáng nghi để giảm kết luận sai, không vì nhiều cột tự động tốt hơn. | Nhi | Ví dụ kiểm tra thủ công, quy tắc chọn biến |
| Area là đất hay sàn? Giá/m² có chính xác không? | `area_m2` xuất phát từ diện tích trường lõi trong tin; ý nghĩa có thể khác giữa loại bất động sản. Giá/m² là tỷ số của hai trường này, là chỉ số mô tả trong mẫu. So sánh cùng nhóm khi có thể và nêu hạn chế; không gọi tất cả là giá đất/m². | Nhi/Quỳnh | Từ điển, ví dụ nguồn, tập lọc biểu đồ |
| Dấu `11.300` là 11,3 hay 11.300 m²? | Đọc quy tắc parse cụ thể trong mã và cờ mơ hồ; kiểm tra văn cảnh khi có thể. Không khẳng định quy tắc đoán luôn đúng. Trường hợp chưa xác minh được phải có trạng thái và phân tích độ nhạy. | Nhi | Hàm parse, ví dụ raw, lineage |
| Tại sao không sửa giá 900.000 đồng thành 900 triệu? | Đó là suy đoán thêm ba số 0, không có bằng chứng chắc chắn. Giữ raw và cách ly/đánh dấu theo chính sách, để báo cáo không tạo dữ liệu hợp lý giả. | Nhi | Ví dụ giá `đ`, dòng bị cách ly |
| Có bao nhiêu căn nhà khác nhau? | Nhóm đếm tin theo khóa nội dung, không xác định chắc số bất động sản vì không có ID chuẩn. Cùng nhà có thể nhiều tin; tin giống nhau có thể khác trường chi tiết. | Nhi | Định nghĩa dedupe, số đếm từng phương án |
| Vì sao khóa trùng gồm các trường đó? | Mã dùng năm trường lõi chuẩn hóa, gồm cả description, để gộp bản ghi có cùng nội dung kiểm tra được. Là quy ước của nhóm, có nguy cơ bỏ sót/gộp nhầm; nhóm báo số liệu theo khóa này và so sánh phương án khác. | Nhi/Đạt | Mã khóa trùng, bảng độ nhạy |
| `sale_assumed` có chắc là tin bán? | Chưa chắc. Đó là suy luận từ ngữ cảnh nguồn khi tiêu đề không nói rõ bán/thuê, luôn có cờ chất lượng. Nhóm nêu tỷ lệ nhóm này và kiểm tra độ nhạy chỉ dùng tiêu đề bán rõ; không đồng nhất tập giữ với giao dịch đã xác minh. | Nhi/Quỳnh | `transaction_status`, bảng độ nhạy |
| Outlier có phải lỗi? Vì sao giữ lại? | Không. Bất động sản lớn/đắt có thể hợp lệ. IQR là cờ thống kê, khác ràng buộc miền giá trị sai. Nhóm giữ điểm hợp lệ, công bố chính sách và xem độ nhạy. | Nhi | Cờ IQR, histogram/scatter, bảng độ nhạy |
| Công thức IQR là gì, slide có dạy không? | IQR = Q3−Q1; hàng rào thường dùng Q1−1,5IQR và Q3+1,5IQR, theo biến/nhóm mà mã thực sự tính. Slide Chương 2 dạy khái niệm outlier; quy tắc IQR là phần bổ sung có nguồn riêng. | Nhi | Mã ngưỡng, phần phương pháp và nguồn IQR |
| Chuẩn hóa dữ liệu có phải mọi biến về 0–1? | Chuẩn cách viết/đơn vị và co giãn số là hai việc khác. EDA giữ đơn vị gốc; K-means dùng scaler thực tế trong mã để biến lớn không chi phối khoảng cách. Min–Max và Z-score có trong Chương 2. | Đạt/Nhi | Hàm chuẩn hóa và bước scaler |
| Tại sao dùng trung vị? | Giá thường lệch và có điểm cao; trung vị ít bị kéo bởi cực trị hơn trung bình. Nhóm vẫn báo cả hai cùng n/IQR để không che giấu phân bố. Kết luận cụ thể phải dựa số đo thực. | Quỳnh | Bảng summary, histogram |
| Vì sao tỉnh A có giá cao nhất? | Chỉ có thể nói trong tập lọc và nhóm đủ n ở biểu đồ. Khác biệt có thể do loại tin, diện tích, cách lấy mẫu và vị trí; chưa kiểm soát yếu tố nhiễu nên không kết luận tỉnh đó đắt nhất toàn thị trường. | Quỳnh | Bảng n/tỉnh, bộ lọc, đơn vị giá/m² |
| Diện tích lớn làm giá tăng đúng không? | Scatter/tương quan mô tả mối liên hệ, không chứng minh nhân quả. Vị trí, loại hình và biến thiếu có thể cùng ảnh hưởng. Nếu có tỷ số giá/m², còn phải lưu ý liên hệ toán học do mẫu số. | Quỳnh | Scatter, loại hệ số, giới hạn |
| Tại sao không vẽ đường giá theo năm hoặc bản đồ? | File không có ngày đăng/tọa độ căn nhà. Không dựng thời gian hay tọa độ giả. Bar theo tên tỉnh trả lời được câu hỏi địa phương trong phạm vi dữ liệu. | Quỳnh | Schema raw và báo cáo |
| Dashboard chính xác đến đâu? | KPI được đối chiếu CSV/Excel cùng tập lọc. Làm tròn để hiển thị nhưng giữ số gốc để tính. Bộ lọc thay đổi n và quần thể đang xem; không so sánh KPI giữa hai bộ lọc mà quên mẫu số. | Quỳnh/Đạt | Biên bản đối chiếu, một demo lọc |
| K-means giải quyết điều gì? | Phân nhóm tin theo đặc trưng số đã chọn, hỗ trợ mô tả. Không phân loại chất lượng pháp lý, không định giá chuyên nghiệp, không dự đoán giá tương lai. | Đạt | Biến vào, bảng tâm và kích thước cụm |
| Vì sao chọn k? Cụm có đúng không? | Trình bày phương án k đã chạy và tiêu chí thật: kích thước, khả năng diễn giải, inertia/silhouette nếu có, độ ổn định seed. Không có nhãn chuẩn nên không nói đúng/sai theo Accuracy. | Đạt | Bảng thí nghiệm k/seed |
| K-means có cần log/scaler không? | Khoảng cách chịu ảnh hưởng độ lớn và phân phối. Log giúp giảm lệch theo lựa chọn của nhóm; scaler cân bằng biến. Phải chỉ ra đúng thứ tự và biến đã dùng, không nói đó là yêu cầu cho mọi dữ liệu. | Đạt | Đoạn mã transform, thông số scaler |
| Các cụm có đại diện phân khúc thị trường không? | Cụm là kết quả thuật toán trên mẫu và đặc trưng này; tên mô tả do nhóm đặt. Cần dữ liệu/kiểm chứng chuyên môn thêm để gọi là phân khúc thị trường. | Đạt | Bảng phân cụm, phạm vi và giới hạn |
| Tại sao SQLite mà không SQL Server/MySQL? | SQLite phù hợp minh họa trên laptop, lưu DB thật một file và chạy SQL kiểm chứng. Nếu giảng viên yêu cầu hệ quản trị cụ thể thì phải chuyển theo yêu cầu đó; chưa có quy định ấy trong thông tin nhóm nhận. | Đạt | DB, schema và truy vấn |
| Index có luôn nhanh hơn không? | Không. Lợi ích phụ thuộc kích thước, độ chọn lọc, truy vấn và chi phí. Nhóm đo trên cùng dữ liệu, kết quả bằng nhau, nhiều lượt; nêu cả kế hoạch và đánh đổi ghi/dung lượng. | Đạt | SQL benchmark/plan thực |
| Tập vài nghìn tin có gọi dữ liệu lớn không? | Không. Đây là minh họa cơ chế truy vấn/index trên dữ liệu nhỏ. Không suy ra hiệu năng production; nếu thử tải bằng nhân bản phải gắn nhãn dữ liệu tổng hợp và tách khỏi EDA. | Đạt | Số dòng DB, mô tả benchmark |
| Nhóm đóng góp gì khi đã có bộ mã nền? | Nói đúng việc từng người tự chạy/kiểm chứng/cải tiến: quy tắc được sửa, mẫu được rà, thí nghiệm đã đo, kết luận đã viết và kiểm tra chéo. Nêu hỗ trợ công cụ/AI trung thực theo quy định của môn. | Cả ba | Nhật ký thay đổi, output thực nghiệm, biên bản |
| Nếu làm tiếp thì ưu tiên gì? | Nguồn có quyền sử dụng, ngày và ID rõ; xác minh diện tích/loại hình; tách bán/thuê; đánh giá chất lượng trước thuật toán phức tạp. Dự đoán sau này cần mục tiêu, train/test và đánh giá riêng. | Cả ba | Hướng cải tiến trong Chương 6 |

## 5. Bài tập tự kiểm tra trước bảo vệ

Mỗi người phải làm được phần của mình mà không đọc lời gợi ý:

- **Đạt:** giải thích một hàm pipeline; tự tính một vòng K-means với ví dụ nhỏ; mở DB và chạy một truy vấn; giải thích vì sao kết quả trước/sau index phải bằng nhau.
- **Nhi:** parse ba chuỗi giá/diện tích thật; chỉ một dòng cách ly và lý do; giải thích khóa trùng; viết công thức IQR và phân biệt cờ outlier với lỗi dữ liệu; trích đúng DOI/giấy phép.
- **Quỳnh:** đọc một histogram và một scatter bằng n/đơn vị; tính một KPI bằng cách độc lập; thay bộ lọc dashboard và giải thích mẫu đang xem; viết một kết luận không chứa khẳng định nhân quả.
- **Cả ba:** nêu được một kết quả chính, một giới hạn, một cải tiến do mình thực sự làm và một việc kiểm tra chéo đã phát hiện hoặc xác nhận.

Tập thử một lượt 10 phút có bấm giờ và một lượt hỏi chéo không nhìn tài liệu. Nếu chưa giải thích được số liệu hoặc phương pháp, giảm phạm vi kết luận và quay lại kiểm chứng, không học thuộc câu trả lời để che khoảng trống.

## 6. Cách xử lý khi không chắc câu trả lời

Nói cụ thể phần đã biết và chỉ ra minh chứng có thể mở: “Trong file này nhóm chưa có trường xác nhận đó; nhóm chưa thể kết luận. Phần đã kiểm tra là …, thể hiện ở …”. Nếu thầy chỉ ra lỗi, ghi nhận đúng vấn đề, kiểm tra lại raw/quy tắc và nói rõ kết quả nào có thể bị ảnh hưởng. Không tự tạo lời giải thích cho nguồn dữ liệu hoặc số đo chưa thực hiện.

Nguồn định hướng nội dung: [đối chiếu slide môn học](../references/DOI_CHIEU_SLIDE.md) và [nguồn dữ liệu Mendeley v2](../references/DATA_SOURCE.md).
