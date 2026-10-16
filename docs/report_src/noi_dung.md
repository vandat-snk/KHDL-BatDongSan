# Chương 1 Giới thiệu đề tài

Đề tài Phân tích giá rao bất động sản Việt Nam xây dựng một quy trình xử lý dữ liệu có thể chạy lại, từ bản ghi tin quảng cáo đến các bảng thống kê, biểu đồ và công cụ tra cứu. Mục tiêu duy nhất là giúp người phân tích khám phá và so sánh đặc điểm giá rao trong mẫu tin lịch sử sau khi áp dụng các quy tắc kiểm tra chất lượng công khai. Giá rao được hiểu là số tiền được nêu trong quảng cáo, chưa phải số tiền của giao dịch đã hoàn tất. Cách xác định này chi phối việc chọn nguồn, thiết kế dữ liệu và phạm vi diễn giải của toàn bộ tiểu luận.

Khó khăn của bài toán xuất hiện trước bước vẽ biểu đồ. Cùng một giá trị có thể được viết bằng tỷ, triệu hoặc đồng; một chuỗi giá có thể kèm diện tích, chứa giá trên mét vuông hoặc khoản thanh toán ban đầu. Diện tích có thể dùng dấu phẩy thập phân, dấu chấm hàng nghìn, đơn vị héc-ta hoặc các mô tả về đất và diện tích sử dụng khác nhau. Tin lặp làm tăng trọng số của nội dung được đăng nhiều lần. Nếu chuyển các chuỗi này thành số mà bỏ qua cơ sở giá và ý nghĩa diện tích, kết quả tổng hợp vẫn có thể tính được nhưng không còn trả lời đúng câu hỏi ban đầu.

Ý nghĩa thực tiễn của đề tài là cung cấp một cách tổ chức và đọc dữ liệu rao bán rõ nguồn gốc. Người dùng có thể quan sát phân bố giá, so sánh trung vị giữa các tập lọc và xem kết quả nhạy đến mức nào với lựa chọn xử lý. Khi gặp giá khác thường, hệ thống cho phép truy nguyên dòng nguồn và lý do cách ly, thay vì chỉ đưa ra một con số cuối cùng. Sản phẩm phù hợp với học tập, khảo sát dữ liệu và chuẩn bị giả thuyết phân tích; việc định giá để giao dịch cần những nguồn và quy trình xác minh bổ sung.

Đối với cộng đồng nghiên cứu, đóng góp nằm ở tình huống thực nghiệm có thể kiểm tra lại: giữ bản nguồn bất biến, công bố quy tắc biến đổi, phân biệt suy luận nhãn với thông tin đã xác minh và đánh giá độ nhạy của kết quả. Các bước này giúp nghiên cứu sau hiểu vì sao hai phép phân tích cùng một nguồn có thể cho số lượng tin hoặc trung vị khác nhau. Tiểu luận không đề xuất thuật toán mới; các kỹ thuật thống kê, K-means và chỉ mục quan hệ được sử dụng để xây dựng một quy trình có bằng chứng. Điều này phù hợp với vai trò trích xuất tri thức, tư duy phản biện và truyền đạt kết quả trong nội dung mở đầu học phần [2].

Nguồn thực nghiệm là Vietnam Real Estate Data phiên bản 2, do Duc Chung Tran, Huy Hoang Nguyen và Hong Son Ha công bố trên Mendeley Data ngày 12/01/2021 theo giấy phép CC BY 4.0 [1]. Mô tả nguồn ghi 10.000 bài đăng, trong khi tệp JSON được công bố thực tế chứa 9.004 bản ghi. Nghiên cứu sử dụng 9.004 làm mẫu số đầu vào, giữ nguyên sự khác biệt này trong hồ sơ nguồn và không bổ sung bản ghi để khớp mô tả. Ngày công bố dữ liệu không phải ngày đăng của từng tin; ngày thực hiện phân tích năm 2026 cũng không biến những giá rao lịch sử thành giá thị trường năm 2026.

Đơn vị quan sát là một bản ghi quảng cáo. Sau khi gộp trùng nội dung, một dòng giữ lại vẫn chưa chắc tương ứng với một bất động sản duy nhất: cùng tài sản có thể được nhiều môi giới đăng với tiêu đề khác nhau, và nguồn không có mã tin ổn định để xác nhận. Tương tự, loại hình và trạng thái bán là nhãn được suy luận bằng quy tắc từ tiêu đề, không phải nhãn chuyên gia cung cấp. Trong toàn văn, các thuật ngữ tin, giá rao và loại hình suy luận được dùng nhất quán để tránh chuyển từ đối tượng quan sát sang đối tượng chưa được đo.

Phạm vi ứng dụng được thu hẹp trong Bảng [[table:scope]]. Mọi chức năng đều phục vụ mục tiêu khám phá mẫu tin: làm sạch tạo điều kiện so sánh, trực quan giúp đọc phân bố, K-means gợi ý cấu trúc nhóm, còn SQLite minh họa truy vấn cùng tập dữ liệu. Các câu hỏi về phân bố giá, sự khác biệt địa phương và độ nhạy là những câu hỏi con của cùng mục tiêu, không hình thành các hệ thống độc lập về dự báo, môi giới hay đầu tư.

@table scope

Các câu hỏi phân tích được đặt theo dữ liệu có sẵn. Giá tổng và đơn giá phân bố ra sao, và trung bình khác trung vị bao nhiêu? Mối liên hệ giữa diện tích và giá có còn rõ khi mẫu trộn nhà, đất và căn hộ? Những địa phương có nhiều tin khác nhau thế nào về trung vị và độ phân tán? Kết quả thay đổi thế nào khi chỉ giữ tiêu đề bán rõ, bỏ ngoại lệ thống kê hoặc loại các chuỗi số có quy ước chưa chắc chắn? Cách đặt câu hỏi này cho phép dùng các kiểm tra định lượng cụ thể để đánh giá kết quả, thay vì kết luận chỉ từ hình dáng biểu đồ.

Sản phẩm của đề tài gồm dữ liệu đã chuẩn hóa, tập tin cách ly, nhật ký truy nguyên, các bảng tổng hợp, tám biểu đồ tĩnh, cơ sở dữ liệu SQLite, dashboard HTML ngoại tuyến và workbook Excel. Giải thuật phân cụm có mã thực thi bằng NumPy; phần minh họa SQL có database và câu lệnh thật. Dữ liệu có thể được xem qua HTML và Excel sau khi tạo, còn việc tái tạo phân tích được điều khiển bằng Python. Các lựa chọn này đáp ứng yêu cầu triển khai của học phần mà không buộc người xem phải cài hệ quản trị máy chủ hoặc sử dụng một dịch vụ dữ liệu trực tuyến.

Phương pháp triển khai gắn trực tiếp với bài học. Chương chuẩn bị dữ liệu của môn học cung cấp nền tảng về thiếu, nhiễu, không nhất quán, ngoại lệ, biến đổi và tổng hợp [3]. Chương trực quan hóa định hướng chọn biểu đồ, đơn vị và cách truyền đạt [4]. Phần K-means và SQL vận dụng nội dung mở rộng về phân cụm và dữ liệu quan hệ [5]–[7]. Các kỹ thuật bổ sung như bootstrap, silhouette và chỉ số Rand điều chỉnh được giải thích riêng, tránh coi mọi công cụ sử dụng đều đã được trình bày đầy đủ trong slide.

# Chương 2 Cơ sở lý thuyết và nền tảng kỹ thuật

Quy trình khoa học dữ liệu trong đề tài gồm xác định đối tượng quan sát, kiểm tra nguồn, chuẩn hóa, mô tả, khảo sát cấu trúc và truyền đạt kết quả. Chất lượng ở mỗi bước ảnh hưởng đến bước sau: phép chia giá cho diện tích chỉ có nghĩa khi cả hai đại lượng được hiểu đúng, và khoảng cách phân cụm chỉ có nghĩa khi biến đã được biến đổi phù hợp. Vì vậy, cơ sở lý thuyết được trình bày theo các phép xử lý thực sự xuất hiện trong mã, đồng thời chỉ ra điều kiện áp dụng và sai lệch có thể còn lại.

Python đảm nhiệm đọc JSON, thao tác đường dẫn, điều khiển các bước và báo lỗi. JSON chứa một mảng đối tượng với những trường văn bản không đồng nhất; quá trình xử lý chuyển các trường được chọn thành biến có kiểu và đơn vị rõ ràng. Thư viện chuẩn pathlib giúp xác định thư mục theo vị trí mã thay vì thư mục làm việc ngẫu nhiên; json đọc và ghi cấu trúc; urllib.request tải nguồn HTTPS; hashlib tạo dấu kiểm SHA-256. Môi trường ảo tách phụ thuộc của dự án, còn phiên bản thư viện được ghi trong kết quả chạy. Đây là cơ sở tái lập về kỹ thuật, không phải bảo đảm nội dung quảng cáo là đúng [12].

Chuẩn hóa văn bản sử dụng Unicode NFKC, thu gọn khoảng trắng và casefold. NFKC làm đồng nhất một số biểu diễn ký tự tương thích; casefold hỗ trợ so sánh không phân biệt cách viết hoa. Biểu thức chính quy sau đó nhận diện số, đơn vị và từ khóa. Những thao tác này phục vụ so khớp và phân tích, không ghi đè bản nguồn. Chúng cũng có giới hạn: từ viết tắt, lỗi chính tả, dấu câu hoặc từ có nhiều nghĩa có thể làm quy tắc bỏ sót hay nhận nhầm. Do đó, kết quả nhận diện được giữ cùng cờ chất lượng, nhóm chưa xác định và ví dụ truy nguyên, thay vì xem chuẩn hóa là bước sửa mọi sai lệch ngôn ngữ.

Kiểm nguồn dùng SHA-256 trên toàn bộ byte của tệp. Hai tệp có cùng tên hoặc cùng số dòng chưa đủ chứng minh cùng phiên bản; dấu kiểm giúp phát hiện thay đổi nội dung hoặc byte xuống dòng. Trong đề tài, checksum được ghim theo bản công bố, rồi kiểm số lượng 9.004 đối tượng và kiểu cấu trúc trước khi xử lý. Mã định danh nội dung của từng tin có mục đích khác: băm năm trường lõi đã chuẩn hóa để phát hiện những bản ghi đồng nhất theo quy tắc. Hash nguồn kiểm phiên bản tệp; hash nội dung phục vụ gộp trùng. Cả hai đều không chứng minh hai tin là cùng bất động sản hoặc nội dung tin là sự thật.

Về kiểu dữ liệu, pandas biểu diễn bảng bằng DataFrame, mỗi dòng là một tin và mỗi cột là một thuộc tính. Các mặt nạ logic chọn những dòng đủ điều kiện, groupby chia theo khóa rồi áp dụng hàm tổng hợp. Phép chia giá cho diện tích được thực hiện trên từng dòng trước khi tính phân vị. Khi tính trung vị đơn giá, nhóm lấy trung vị của các tỷ số cá thể; đó không phải tỷ số của hai trung vị hay tổng giá chia tổng diện tích. Việc phân biệt thứ tự phép toán giúp tránh tạo một chỉ tiêu khác dưới cùng tên gọi. Kết quả xuất CSV và JSON để các sản phẩm sau cùng đọc một bộ biến đã được xác định [9].

Chuẩn hóa số phải xét cả ký hiệu lẫn đơn vị. Quy tắc quan sát của nguồn ưu tiên dấu phẩy thập phân và dấu chấm chia nhóm ba chữ số; một dấu chấm với ba chữ số cuối được gắn cờ do có thể mơ hồ. Diện tích héc-ta đổi sang mét vuông bằng hệ số 10.000; giá tỷ và triệu đổi sang VND bằng hệ số tương ứng. Một biểu thức giá trên mét vuông chỉ được quy thành tổng giá khi có diện tích phù hợp. Ngược lại, khi trường giá giống giá đơn vị trong mô tả nhưng thiếu cơ sở giải quyết, tin được cách ly. Đề tài không dùng trung bình hoặc mô hình để điền giá và diện tích thiếu, vì những giá trị đó quyết định trực tiếp biến phân tích.

@equation unit_price

Trong Công thức [[equation:unit_price]], Pᵢ là tổng giá rao sau chuẩn hóa, Aᵢ là diện tích được đọc từ tin, uᵢ là đơn giá; Pᵢ có đơn vị VND và Aᵢ có đơn vị m². Điều kiện Aᵢ dương ngăn phép chia không hợp lệ. Dòng nguồn số 1 có Pᵢ bằng 2.380.000.000 và Aᵢ bằng 100, nên uᵢ bằng 23.800.000 VND/m². Tính đúng số học của phép chia vẫn phụ thuộc cách người đăng hiểu diện tích là đất, sàn hoặc diện tích sử dụng.

Giá trị thiếu được phân biệt với giá trị không phân tích được. Một trường có văn bản như giá thỏa thuận không rỗng nhưng không cung cấp giá trị số; một chuỗi diện tích có nhiều khoảng lựa chọn cũng không tương đương với một diện tích đơn. Dữ liệu nguồn không có trường lõi trống trong lần đếm, nhưng có các chuỗi không đọc được theo bộ phân tích. Việc chỉ báo tỷ lệ ô không rỗng sẽ bỏ qua vấn đề này. Quy trình lưu lỗi phân tích, lý do cách ly và nguồn khôi phục diện tích để người đọc thấy quyết định được đưa ra từ bằng chứng nào [3].

Trung bình mô tả tổng giá trị chia số quan sát và nhạy với các giá rất lớn. Trung vị là vị trí giữa sau sắp thứ tự; với số quan sát chẵn, trung vị bằng trung bình của hai phần tử giữa. Phân vị Q1 và Q3 mô tả phần giữa của phân bố. Với giá rao lệch phải, việc báo trung vị cùng trung bình, tứ phân vị và số mẫu giúp thấy cả mức điển hình lẫn ảnh hưởng của phần đuôi. Không có một chỉ số đơn lẻ đủ thay thế toàn bộ phân bố, nhất là khi mẫu trộn nhiều loại bất động sản và địa phương.

@equation iqr

IQR và hàng rào ở Công thức [[equation:iqr]] được dùng như quy tắc gắn cờ thống kê. Giá trị nằm ngoài khoảng không mặc nhiên là lỗi: tài sản diện tích lớn hoặc vị trí đặc biệt có thể tạo quan sát khác biệt hợp lệ. Đề tài gắn cờ theo nhóm tỉnh và loại khi nhóm có ít nhất 30 tin; nếu không đủ, dùng nhóm loại hoặc toàn mẫu. Ngưỡng 30 là lựa chọn thiết kế để hạn chế nhóm tham chiếu quá ít quan sát, không phải bảo đảm độ chính xác thống kê. Bộ lọc IQR dùng các cờ đã tính trong pipeline, không ước lượng lại hàng rào sau mỗi tương tác dashboard.

Đánh giá độ nhạy đặt các phương án xử lý cạnh nhau trên cùng nguồn. Các phương án gồm giữ toàn bộ tin đủ điều kiện, bỏ ngoại lệ toàn cục, bỏ ngoại lệ nhóm, bỏ chuỗi diện tích có quy ước dấu chấm và chỉ giữ tiêu đề bán rõ. Sự thay đổi của n và trung vị cho thấy kết luận phụ thuộc điều kiện nào. Đây là phép so sánh chính sách chấp nhận dữ liệu, không phải chọn phương án cho kết quả đẹp nhất. Một thay đổi nhỏ ở trung vị cũng không chứng minh từng nhãn hoặc từng giá trị đã đúng.

Tương quan Spearman được tính bằng tương quan Pearson trên thứ hạng, với thứ hạng trung bình cho các giá trị bằng nhau. Mã dùng rank rồi corr, nên không áp dụng công thức rút gọn giả định mọi thứ hạng phân biệt. Spearman phản ánh mối liên hệ đơn điệu, có thể hữu ích khi phân phối lệch; hệ số gần 0 không phủ nhận quan hệ phi tuyến hoặc các quan hệ tồn tại riêng trong từng nhóm. Đặc biệt, đơn giá u bằng P/A chứa diện tích ở mẫu số, nên tương quan A với u còn chịu ràng buộc toán học. Không diễn giải hệ số này thành tác động nhân quả của diện tích lên giá.

@equation spearman

Khoảng bootstrap của trung vị địa phương được tạo bằng cách lấy lại mẫu có hoàn lại trong chính nhóm đang xét, tính trung vị cho mỗi mẫu rồi lấy các phân vị 2,5% và 97,5%. Mã sử dụng 500 lần lấy mẫu và seed cố định. Khoảng này mô tả biến động có điều kiện trên các tin đã thu được; nó không hiệu chỉnh thiên lệch chọn mẫu, không xác nhận mẫu đại diện và có thể đánh giá thấp bất định khi nhiều tin phụ thuộc cùng môi giới hoặc cùng tài sản. Vì thế, khoảng bootstrap đi kèm n và cảnh báo phạm vi khi biểu diễn chênh lệch địa phương [16].

@equation bootstrap

NumPy cung cấp mảng số và phép toán vector cho phân cụm. Ma trận dữ liệu có n hàng và hai đặc trưng; broadcasting cho phép tạo khoảng cách giữa các điểm và tâm qua các trục mở rộng thay vì vòng lặp Python theo từng cặp. Mã bình phương hiệu, cộng theo chiều đặc trưng rồi chọn chỉ số khoảng cách nhỏ nhất. Cách tính này gắn trực tiếp với bài toán khoảng cách Euclid, nhưng bộ nhớ tăng theo số điểm, số tâm hoặc kích thước ma trận cặp. Silhouette vì vậy được tính trên tối đa 1.000 tin lấy mẫu, thay vì tạo ma trận khoảng cách cho toàn bộ mọi tin [8].

Hai đặc trưng phân cụm là log tự nhiên của diện tích và đơn giá. Log giảm chênh lệch theo quy mô trong phân phối lệch, sau đó Z-score đặt hai biến vào thang đo tương đương. Trung bình và độ lệch chuẩn tổng thể được tính trên chính tập fit, không dùng ddof bằng 1. Mã kiểm dữ liệu hữu hạn, số điểm phân biệt và độ lệch chuẩn khác 0 trước khi phân cụm. Cần giữ đúng thứ tự log rồi chuẩn hóa, đơn vị và scaler; nếu đổi VND thành triệu VND thì tham số trung bình log cũng thay đổi, không thể dùng nguyên scaler cũ.

@equation zscore

Trong Công thức [[equation:zscore]], xᵢⱼ là giá trị dương của đặc trưng j ở tin i; μⱼ và σⱼ lần lượt là trung bình và độ lệch chuẩn tổng thể của ln(xᵢⱼ) trên tập fit. zᵢⱼ là giá trị đã co giãn, không còn đơn vị gốc. Nếu σⱼ bằng 0 thì đặc trưng không có biến thiên và phép chia không hợp lệ; mã từ chối trường hợp đó thay vì tạo vô hạn.

K-means tìm cách giảm tổng bình phương khoảng cách từ điểm đến tâm cụm theo Công thức [[equation:kmeans]]. Thuật toán Lloyd luân phiên gán mỗi điểm vào tâm gần nhất và cập nhật tâm bằng trung bình các điểm của cụm. Quá trình hướng đến một nghiệm phụ thuộc khởi tạo, không bảo đảm cực tiểu toàn cục trong mọi trường hợp. Cụm phù hợp với cấu trúc gọn theo khoảng cách trong không gian biến đổi; chúng có thể không tương ứng với nhóm nghiệp vụ mà chuyên gia bất động sản quan tâm [5].

@equation kmeans

@equation centroid

Trong Công thức [[equation:kmeans]] và [[equation:centroid]], zᵢ là vector hai đặc trưng đã chuẩn hóa của tin i, Cⱼ là tập chỉ số thuộc cụm j, cⱼ là vector tâm cụm và k là số cụm. J là tổng bình phương khoảng cách, còn |Cⱼ| là số điểm của cụm. Ký hiệu cⱼ phân biệt tâm trong không gian phân cụm với μⱼ là trung bình log dùng để chuẩn hóa ở Công thức [[equation:zscore]].

K-means++ chọn tâm đầu từ dữ liệu, sau đó ưu tiên điểm có bình phương khoảng cách lớn tới các tâm đã có [13]. Hiện thực trong đề tài dùng mười lần khởi tạo cho mỗi k và giữ mô hình có inertia thấp nhất, tối đa 150 vòng lặp. Điều kiện dừng dựa trên độ thay đổi tọa độ tâm nhỏ hơn 10⁻⁷; sau vòng lặp, nhãn và inertia được tính lại theo tâm cuối. Trường hợp cụm rỗng được xử lý bằng điểm xa nhất theo khoảng cách nhỏ nhất hiện tại. Những lựa chọn này là chi tiết hiện thực cần ghi rõ để người khác có thể chạy lại cùng quy trình.

Silhouette so sánh khoảng cách trung bình trong cụm aᵢ với khoảng cách trung bình tới cụm khác gần nhất bᵢ. Công thức [[equation:silhouette]] cho giá trị cao hơn khi điểm tương đối gần cụm của nó và xa cụm khác [14]. Các k từ 2 đến 5 được khảo sát với cùng quy trình; lựa chọn ưu tiên silhouette trung bình cao hơn, khi bằng nhau ưu tiên k nhỏ hơn. Đây là lựa chọn trong bốn phương án đã thử. Vì điểm số tính trên tập con, nó không được ghi thành đánh giá chính xác cho mọi điểm của toàn bộ tập fit.

@equation silhouette

Chỉ số Rand điều chỉnh, ARI, được dùng để so mức đồng thuận của hai cách chia cùng các điểm, đã hiệu chỉnh theo một mô hình ngẫu nhiên và không phụ thuộc việc hoán đổi tên cụm [15]. Trong nghiên cứu này, nhãn của seed chính được so với seed 7 và 42. ARI bằng 1 cho biết hai phân hoạch trùng nhau trên dữ liệu đó; nó không đo tính đúng với phân khúc thị trường vì không có nhãn chuẩn bên ngoài. Như vậy, khảo sát k và seed cung cấp bằng chứng về lựa chọn/ổn định nội bộ, chưa cung cấp kiểm định nghiệp vụ.

SQLite là hệ quản trị nhúng lưu cơ sở dữ liệu trong một tệp và được gọi qua kết nối sqlite3 của Python. Bảng tỉnh và bảng loại giữ tên duy nhất, bảng listings tham chiếu chúng bằng khóa ngoại. PRIMARY KEY, UNIQUE, NOT NULL và CHECK biểu diễn các điều kiện có thể kiểm ngay khi ghi. Do SQLite dùng cơ chế kiểu linh hoạt trong các bảng hiện tại, khai báo REAL không thay cho toàn bộ kiểm dữ liệu đầu vào; quy trình còn chuyển kiểu và kiểm miền giá trị trước khi chèn. Hệ thống này phù hợp tra cứu cục bộ và minh họa quan hệ, chưa thiết kế cho nhiều người cùng cập nhật qua mạng [6], [11].

Khóa ngoại cần được bật trên từng kết nối có ghi bằng PRAGMA foreign_keys=ON; việc có câu khai báo REFERENCES trong lược đồ không nên bị hiểu thành mọi kết nối đều tự áp dụng cùng chế độ. Mã tạo database thực hiện bật kiểm tra, nạp dữ liệu bằng câu lệnh có tham số, commit và kiểm tra toàn vẹn. Giao dịch của SQLite giúp nhóm thao tác trong database có thể được xác nhận theo đơn vị ghi của nó; cơ chế đó khác với xuất bản nhiều tệp CSV, JSON, ảnh và Excel. Đối với các tệp này, hệ thống dùng vùng tạm và manifest chứ không có một giao dịch phân tán duy nhất.

Chỉ mục ghép được sắp theo thứ tự province_id, type_id, price_per_m2_vnd và row_id. Hai cột đầu phù hợp điều kiện bằng, cột đơn giá phù hợp truy vấn khoảng và thứ tự sắp, row_id phân giải trường hợp cùng đơn giá. EXPLAIN QUERY PLAN cho biết SQLite quét bảng hay tìm qua chỉ mục; ANALYZE cung cấp thống kê phục vụ lựa chọn kế hoạch. Chỉ mục hiện tại không chứa mọi cột trả về nên không được gọi là covering index cho truy vấn minh họa. Tác động đến thời gian còn phụ thuộc dữ liệu, cache và môi trường; cần kiểm cả kết quả bằng nhau lẫn phân bố thời gian, không suy ra tăng tốc chỉ từ việc thấy tên chỉ mục trong plan [7], [11].

Matplotlib tạo hình tĩnh từ các mảng và bảng đã xử lý. Histogram tổng giá được vẽ ở thang gốc và log để thấy phần đuôi; scatter dùng hai trục log vì giá và diện tích có khoảng biến thiên lớn. Biểu đồ cột địa phương kèm n và khoảng bootstrap, boxplot che các điểm ngoài râu trên hình nhưng không xóa chúng khỏi dữ liệu. Với khoảng giá không đều trong dashboard, chiều cao cột là số tin của từng khoảng, không được diễn giải như mật độ histogram có bề rộng bằng nhau. Đơn vị trục, tập lọc và số mẫu là một phần của ý nghĩa hình, không chỉ là trang trí [4], [10].

Dashboard sử dụng HTML cho cấu trúc, CSS cho bố cục và JavaScript cho trạng thái lựa chọn cùng tính toán. Dữ liệu công khai đã lược bỏ nội dung liên hệ được đóng vào HTML; các biểu đồ SVG và bảng được cập nhật từ tập lọc trong trình duyệt. Vì vậy, sau khi dựng, sản phẩm có thể mở ngoại tuyến mà không cần backend hoặc API bất động sản. Cách triển khai giảm phụ thuộc vận hành nhưng dữ liệu vẫn là snapshot và kích thước trang tăng theo số bản ghi; nó không phải một dịch vụ cập nhật thị trường trực tiếp.

Excel là kênh đọc và thao tác bảng bổ sung. Công thức đơn giá kiểm điều kiện đầu vào số dương trước phép chia; các cột phụ đổi đơn vị sang tỷ và triệu để tổng hợp. Công thức động có thể tính lại trong vùng workbook, còn cờ IQR, nhãn cụm và một số bảng là snapshot của pipeline. AutoFilter trong trang dữ liệu không mặc nhiên đổi KPI toàn workbook, vì các công thức tổng hợp không được xây dựng như mọi phép SUBTOTAL theo hàng hiển thị. Việc phân biệt này tránh kỳ vọng rằng chỉnh một ô hoặc ẩn một hàng đã làm toàn bộ quy trình phân tích chạy lại.

Cuối cùng, kiểm thử và truy nguyên là nền tảng để nối các công nghệ. Kiểm thử đơn vị kiểm quy tắc và tình huống biên; kiểm tích hợp so đầu ra giữa các định dạng; kiểm hash phát hiện sản phẩm khác phiên bản. Kiểm nội dung nguồn và kiểm bố cục giao diện có phạm vi riêng, không thể thay hoàn toàn bằng một mã thoát thành công. Chương 3 sử dụng các nguyên tắc trên để thiết kế các hợp đồng dữ liệu, còn Chương 5 báo cáo chính xác những lớp kiểm đã thực hiện và những lớp chưa được xác nhận.

# Chương 3 Phân tích và thiết kế ứng dụng

Bài toán được phân tích từ chuỗi hoạt động của người sử dụng dữ liệu. Người vận hành cần tạo lại kết quả từ đúng nguồn và đọc được lý do loại một tin; người xem cần hiểu tập tin đang được phân tích, chọn địa phương hoặc loại hình và xuất bảng phục vụ diễn giải. Đây là hai cách sử dụng trong một quy trình cục bộ, không phải hai mức quyền được hiện thực bằng tài khoản. Thiết kế không bổ sung chức năng xác thực, duyệt giao dịch hay quản lý môi giới vì những chức năng đó không cần cho mục tiêu khám phá mẫu giá rao.

Yêu cầu chức năng đầu tiên là kiểm bản dữ liệu trước khi biến đổi, giữ raw bất biến và xác định được mỗi dòng đã đi đâu. Tiếp theo, hệ thống phải chuẩn hóa giá và diện tích, phát hiện trùng theo quy tắc, cách ly trường hợp chưa đủ cơ sở và tạo các biến số cần cho thống kê. Kết quả cần đọc được qua bảng, biểu đồ, SQLite, HTML và Excel. Khi dùng K-means hoặc minh họa truy vấn chỉ mục, mã thực thi và đầu ra phải tồn tại trong dự án, thay vì chỉ mô tả thuật toán ở phần lý thuyết.

Yêu cầu chất lượng tập trung vào tính nhất quán và khả năng giải thích. Các sản phẩm phải tham chiếu cùng run_id và nguồn; phép chia đơn giá phải khớp từng tin; số dòng trong lineage phải bảo toàn quy mô đầu vào. Khi thiếu nguồn hoặc hash không đúng, quy trình phải báo lỗi sớm. Khi một biểu đồ chỉ vẽ mẫu điểm cho nhẹ giao diện, chú thích phải phân biệt số điểm vẽ với số tin dùng tính KPI. Thông tin liên hệ và địa chỉ chi tiết không cần cho phân tích công khai nên không đưa vào các bảng xuất phục vụ xem kết quả.

Năm trường lõi được chọn gồm title, price, area, location và description. Title phục vụ nhận diện sơ bộ loại/giao dịch; price và area cung cấp đại lượng số; location cung cấp nhãn địa phương; description cung cấp ngữ cảnh kiểm nhất quán. Các trường chi tiết khác có dấu hiệu lặp không ăn khớp giữa bản ghi khác loại, nên không dùng số phòng, nội thất hoặc pháp lý để phân tích chính. Đây là quyết định giảm thuộc tính dựa trên chất lượng có thể quan sát, không phải kết luận đã xác minh phương pháp thu thập của tác giả nguồn.

Kiến trúc ở Hình [[figure:architecture]] chia dữ liệu thành ba lớp logic: nguồn nguyên bản, dữ liệu đã chuẩn hóa có truy nguyên và sản phẩm phân tích. Các khối tương ứng với tệp/mô-đun cục bộ, không phải dịch vụ mạng độc lập. Ví dụ dòng nguồn 1 đi từ 100 m² và 2,38 tỷ sang 23,8 triệu VND/m² rồi xuất tới bảng sạch và database; dòng 638 đi vào tập cách ly do chưa giải quyết được cơ sở giá. Hai ví dụ ở Bảng [[table:trace_design]] minh họa rằng đầu ra của chuẩn bị dữ liệu có nhiều nhánh, không phải mọi dòng đều bị ép thành số hợp lệ.

@figure architecture

@table trace_design

Từ điển biến được tóm tắt ở Bảng [[table:dictionary]]. CSV sạch có 18 cột, trong đó các biến dẫn xuất được xác định rõ nguồn và đơn vị. row_id giữ vị trí bản ghi trong mảng nguồn, bắt đầu từ 1. listing_id là tiền tố 20 ký tự của hash nội dung; toàn bộ hash được dùng trong bộ nhớ để phát hiện trùng, còn ID xuất ra được kiểm tính duy nhất trước khi nạp database. Các ID này không thay cho mã tài sản ngoài thực tế. Những cột cờ và bằng chứng cần được giữ ngay cả khi không hiển thị hết trên dashboard, vì chúng phục vụ giải thích quyết định xử lý.

@table dictionary

Lineage được thiết kế là bảng có một dòng cho mỗi dòng nguồn. status nhận kept, rejected hoặc duplicate; canonical_row_id chỉ về dòng đại diện khi nội dung trùng; reasons mô tả lý do. Nhờ đó, phép đối soát số lượng được kiểm ở cấp dòng, không chỉ so tổng số tệp. Tập rejected giữ giá trị đã đọc cùng lý do cách ly để có thể xem lại mà không mất bằng chứng. Một tin có nhiều lý do không làm tăng số tin cách ly: số lượt lý do được thống kê riêng và có thể chồng nhau.

Hình [[figure:erd]] biểu diễn quan hệ ba bảng của SQLite. provinces có 48 hàng gồm 47 nhãn xác định và nhóm chưa rõ, property_types có bốn hàng, listings có 6.936 hàng. Quan hệ một–nhiều từ mỗi bảng danh mục tới listings giúp giữ một cách viết tên chuẩn cho mỗi khóa và hỗ trợ JOIN. Không cần tạo nhiều bảng nghiệp vụ chỉ để tăng kích thước lược đồ; số bảng phải xuất phát từ đối tượng mà ứng dụng thực sự lưu và truy vấn.

@figure erd

@table db_example

Trong listings, row_id là INTEGER PRIMARY KEY; listing_id có NOT NULL và UNIQUE; province_id và type_id là khóa ngoại. Diện tích phải lớn hơn 0, tổng giá tối thiểu 10 triệu VND, đơn giá dương, cờ IQR chỉ nhận 0 hoặc 1. Ràng buộc kiểm tổng giá xấp xỉ diện tích nhân đơn giá dùng sai số số thực nhỏ. Các điều kiện này bảo vệ tính hợp lệ tính toán và chính sách chấp nhận, chưa kiểm được giá thật, pháp lý hoặc tính nhất quán đầy đủ của ngôn ngữ quảng cáo. Ví dụ, một tổng giá sai nhưng vẫn dương có thể vượt ràng buộc database nếu không được phát hiện trước đó.

Thiết kế phân tích giữ riêng ba quần thể sử dụng. Quần thể mặc định gồm 6.936 tin đã qua chính sách; quần thể không có cờ IQR nhóm gồm 6.676 tin và được dùng fit phân cụm; các quần thể độ nhạy được tạo theo từng điều kiện minh bạch. Nhóm phân cụm được lưu dưới nhãn 1 và 2, còn −1 chỉ những tin ngoài tập fit. Lọc dashboard chỉ chọn lại các bản ghi có sẵn và tính lại thống kê hiển thị, không fit lại K-means hoặc cập nhật scaler theo mỗi tổ hợp lựa chọn.

Thiết kế dashboard có ba bộ chọn chính: tỉnh, loại suy luận và phạm vi giao dịch, kèm tùy chọn bỏ cờ IQR nhóm và nút đặt lại. KPI cùng biểu đồ dùng tập lọc cấp trang. Ô tìm kiếm trong bảng áp dụng thêm điều kiện cho bảng và CSV, không thay KPI toàn trang; phân trang chỉ giới hạn dòng đang hiển thị, còn xuất CSV chứa toàn bộ bảng đã lọc/tìm. Trạng thái không có dữ liệu cần hiện n bằng 0 và thông báo phù hợp, tránh để KPI của lần chọn trước khiến người đọc nhầm có kết quả.

Thiết kế Excel có ba trang Dashboard, Du lieu và Chat luong; trang dữ liệu có 19 cột vì chứa các cột quy đổi và diện tích hợp lệ phục vụ công thức, đồng thời không đưa mọi cột CSV sang nguyên trạng. Các biểu đồ và công thức dựa trên vùng dữ liệu được tạo cho lần chạy đó. HTML và Excel là hai giao diện cho cùng nền dữ liệu nhưng không có mọi tương tác đồng nhất: HTML lọc và tính thống kê bằng JavaScript; Excel dùng bảng và công thức theo vùng đã thiết kế. Bởi vậy, nghiệm thu cần so ngữ nghĩa chỉ tiêu, không chỉ so hình thức hoặc tên nhãn.

Hợp đồng phiên bản gắn nguồn, mã lõi và đầu ra qua run_manifest.json. Dashboard và workbook có metadata dẫn xuất riêng, chứa core_run_id, hash sản phẩm và hash mã dựng. Khi một sản phẩm không khớp, verifier phải báo khác phiên bản; dashboard cũng không quảng bá workbook cũ như một bản cùng dữ liệu. Cách tổ chức này giảm nguy cơ dùng ảnh hoặc Excel của một lần chạy cũ để minh họa cho số liệu mới. Tuy nhiên, đây là hợp đồng kiểm tính nhất quán, không thay thế việc đánh giá nội dung tin và không biến toàn bộ quá trình xuất tệp thành một giao dịch nguyên tử.

Thiết kế trên dẫn tới tiêu chí nghiệm thu có thể đo: bảo toàn 9.004 dòng trong lineage; mọi tin sạch có giá/diện tích hợp lệ theo chính sách; CSV, JSON, database và workbook cùng giá trị; các bộ lọc trả n tương ứng; truy vấn trước/sau chỉ mục có cùng kết quả; tài liệu giải thích được giới hạn. Chương 4 mô tả cách chuyển các yêu cầu này thành hàm và tệp thực thi, còn Chương 5 dùng kết quả lưu của cùng lần chạy để đánh giá mức đáp ứng.

# Chương 4 Hiện thực hệ thống

Hệ thống được hiện thực trong kho mã KHDL-BatDongSan với các thư mục scripts, src, data, sql, tools, tests và outputs [17]. scripts điều khiển tải và chạy; src chứa quy tắc lõi; tools dựng sản phẩm và đối soát; outputs lưu kết quả cùng phiên bản. Cách chia này tách mã xử lý khỏi sản phẩm sinh ra và cho phép kiểm một bước riêng khi cần chẩn đoán. Bảng [[table:modules]] liên kết những mô-đun chính với đầu vào và đầu ra; các đoạn mã ngắn trong chương được trích từ hiện thực, còn toàn bộ mã được cung cấp trong kho dự án.

@table modules

Mô-đun tải scripts/download_data.py sử dụng URL của bản dữ liệu được ghim, lưu metadata và manifest để kiểm chứng. Khi nguồn cục bộ đã có checksum đúng, không cần tải lại để phân tích ngoại tuyến. Trước pipeline, read_verified_source trong src/artifact_contract.py kiểm SHA-256, cấu trúc mảng và số lượng 9.004 đối tượng. Nếu thiếu hoặc khác bản nguồn, chương trình dừng với thông báo. Bước này ngăn tình huống một tệp sửa riêng vẫn được gắn tên và DOI của bộ dữ liệu công bố; nó không xác thực nội dung kinh tế của từng quảng cáo.

Trong src/pipeline.py, normalize tạo chuỗi so khớp; parse_number đọc cấu trúc dấu số và từ chối biểu thức không rõ; parse_area tìm một diện tích có đơn vị và xử lý dấu gạch đầu chuỗi nguồn như ký tự phân cách. Những chuỗi là khoảng diện tích không bị ép thành một điểm. Khi trường area chưa đọc được nhưng chuỗi price có phần diện tích ghi rõ, clean_records có thể khôi phục từ phần đó và ghi area_source cùng cờ. Với 349 tin giữ được khôi phục theo cách này, giá trị không được nội suy từ tin khác hoặc từ mô hình dự đoán.

parse_price tách phần diện tích có nhãn khỏi chuỗi giá rồi đọc số tiền và đơn vị. Giá ghép như 1 tỷ 200 triệu chỉ được cộng khi các thành phần không âm và đơn vị giảm dần; đơn vị lặp hoặc phần dư chưa giải thích được làm chuỗi không hợp lệ. Với giá ghi rõ trên m², tổng được suy ra khi diện tích dương có sẵn và price_basis lưu cơ sở đó. Sau chuẩn hóa, dòng 1 tạo 2.380.000.000 VND và 100 m², nên đơn giá bằng 23.800.000 VND/m². Đây là ví dụ của phép biến đổi có thể kiểm lại bằng số gốc, không phải một giá được hệ thống định giá lại.

Gộp trùng thực hiện trên hash của danh sách năm trường đã normalize. Bộ nhớ fingerprints giữ dòng đầu gặp làm canonical_row_id; các dòng có cùng khóa được ghi duplicate trong lineage và không xử lý như quan sát độc lập mới. Quy tắc này khác việc so toàn bộ JSON: một số trường chi tiết có thể khác dù nội dung lõi giống nhau. Ngược lại, thay một phần mô tả có thể làm cùng tài sản không được gộp. Do thiếu mã tin ổn định và thông tin giao dịch, báo cáo chỉ kết luận về trùng nội dung theo khóa đã chọn.

classify_title nhận diện loại hình và giao dịch bằng các mẫu từ khóa có thứ tự ưu tiên. Một số cụm tên riêng hoặc ngữ cảnh như Nhà Bè, Nha Trang hay nhà đầu tư được loại khỏi những cách khớp dễ nhầm. Căn hộ, nhà và đất được nhận theo mẫu; phần còn lại thành other_unknown. Tin có tín hiệu thuê/bán lẫn nhau được xử lý khác với tin bán có nhắc thu nhập cho thuê. Khi không có tín hiệu bán rõ nhưng ngữ cảnh nguồn phù hợp, sale_assumed được giữ cùng cờ. Các điều kiện này giải thích được bằng mã nhưng vẫn phụ thuộc cách diễn đạt của người đăng, đặc biệt lỗi chính tả và viết tắt.

src/source_checks.py bổ sung đối chiếu chéo giá, đơn vị, diện tích và ngữ cảnh thanh toán. Hàm check_source_consistency trả về lý do, cờ và các cụm số/chữ tối thiểu; nó không trả một giá đúng để thay nguồn. Dòng 638 có tổng giá đọc được 20 triệu nhưng mô tả ghi 20tr/m2, nên nhận unresolved_price_basis_from_source_text. Dòng 335 có diện tích lõi 2 m² nhưng tiêu đề 2 ha, nên đi vào cách ly. Những từ như sào, công phụ thuộc quy ước địa phương được giữ là bất định khi không đủ cơ sở đổi đơn vị.

Các quy tắc xung đột số học hiện tại thận trọng với mô tả nhiều sản phẩm, giá cũ, giảm giá, thu nhập hoặc nhiều loại diện tích. Một số phép so sử dụng ngưỡng chênh ít nhất năm lần, nên không bắt mọi sai khác nhỏ. Ví dụ rà soát bổ sung thấy dòng 5093 có 9,7 tỷ ở trường giá và 9,9 tỷ trong mô tả, trong khi dòng 8151 có diễn đạt diện tích khác trường lõi. Những phát hiện này được ghi trong hồ sơ rà soát riêng và giới hạn kết luận; không sửa thủ công một sản phẩm đầu ra để tạo ấn tượng tất cả dữ liệu đã được xác minh.

Sau clean_records, hệ thống xuất ba bảng về tin giữ, tin cách ly và lineage. add_outlier_flags tính Q1/Q3 và hàng rào theo nhóm có cơ chế dự phòng như thiết kế. summarize_groups tính n, trung vị, tứ phân vị và tỷ lệ cờ; bootstrap chỉ được dùng ở những bảng thực sự cần khoảng biến động của trung vị. sensitivity_table tạo các phương án trên cùng dữ liệu đã qua chính sách. Các bảng CSV được ghi với UTF-8 có BOM để thuận tiện mở trong Excel; JSON giữ Unicode và biểu diễn số phục vụ ứng dụng. Sai khác làm tròn khi xuất bảng được tách khỏi phép tính nội bộ.

cluster_records chọn các tin không có cờ IQR nhóm, log hai biến và chuẩn hóa bằng trung bình/độ lệch chuẩn của chính tập đó. Hàm kmeans triển khai K-means++ và Lloyd bằng NumPy; dòng tính khoảng cách, gán nhãn và cập nhật tâm thể hiện trực tiếp việc dùng giải thuật để tạo kết quả. Đoạn mã ở dưới minh họa phần gán và cập nhật tâm, không thay thế toàn bộ các kiểm đầu vào, khởi tạo và chọn mô hình trong tệp nguồn.

@code kmeans

Các mô hình k từ 2 đến 5 được đánh giá bằng sampled_silhouette. Kết quả ưu tiên điểm silhouette cao nhất; nếu bằng nhau ưu tiên k nhỏ. Nhãn được sắp lại theo tâm đơn giá rồi diện tích để cách trình bày ổn định, không làm thay đổi phân hoạch. Hai seed bổ sung được so bằng adjusted_rand_index. Cuối cùng, cụm chỉ được gán cho các tin thuộc tập fit, những tin còn lại mang giá trị −1. Cấu trúc này cho phép dashboard giữ thông tin cụm của pipeline trong khi lựa chọn lọc có thể thay đổi.

build_database tạo lược đồ bằng SQL, ánh xạ tên tỉnh và loại sang khóa danh mục rồi nạp listings bằng executemany với tham số. Bảng listings lưu 11 cột cần cho truy vấn, khác 18 cột của CSV sạch. Hàm thực hiện ANALYZE, chọn một cặp tỉnh–loại nhiều tin và dùng khoảng phân vị 35%–65% của đơn giá để tạo tham số benchmark. Trước và sau khi tạo index, cùng câu SELECT được chạy, lấy plan, hash kết quả và đo nhiều lần. Nếu hash hai kết quả khác nhau, chương trình từ chối công bố kết quả của lần dựng đó.

@code sql_search

Đối với truy vấn này, idx_listings_search hỗ trợ phần lọc tỉnh/loại và khoảng đơn giá, đồng thời thứ tự đơn giá–row_id cho kết quả xác định khi có giá bằng nhau. Giá trị diện tích và tổng giá vẫn cần đọc từ bảng. SQL minh họa khác tổng hợp theo tỉnh, theo loại trong TP.HCM và liệt kê các tin có cờ ngoại lệ. AVG trong các truy vấn đó được gọi là trung bình, không gắn nhãn trung vị. scripts/demo_sql.py mở database ở chế độ chỉ đọc, thực thi bốn câu lệnh rồi in kết quả và PRAGMA integrity_check.

tools/build_dashboard.py kiểm manifest trước khi đọc CSV, chọn mười trường cần cho giao diện rồi chuyển các cột số và boolean về đúng kiểu. JSON nhúng được thay ký tự mở thẻ thành biểu diễn Unicode escape để không tạo chuỗi kết thúc thẻ ngoài ý muốn. src/dashboard_template.html cung cấp hàm lọc, tính median, dựng SVG, phân trang và xuất CSV. Mẫu scatter được giảm điểm để giữ trang nhẹ, còn thống kê dùng toàn bộ tập lọc. Liên kết mở Excel chỉ được cung cấp như bản cùng dữ liệu khi metadata workbook đã vượt kiểm phiên bản.

tools/build_workbook.mjs dùng runtime Node và Artifact Tool để tạo ba trang cùng bốn biểu đồ. Tại dòng dữ liệu đầu tiên, công thức đơn giá yêu cầu H và G là số dương rồi mới lấy H/G; cột Q đổi tổng giá sang tỷ, R đổi đơn giá sang triệu và S giữ diện tích hợp lệ. Các trường hợp giá/diện tích trống, 0 hoặc văn bản được thử riêng trên bản kiểm. Cờ IQR và cụm là kết quả phân tích có sẵn, không phải công thức huấn luyện lại trong Excel. Việc tạo chính xác workbook này phụ thuộc gói ngoài requirements Python, nên khả năng mở file có sẵn được phân biệt với khả năng dựng lại file trên một môi trường mới.

Quy trình xuất bản sản phẩm trong main dựng phần lõi ở một thư mục staging dưới tmp. Khi tạo thành công, từng tệp được chuyển sang vị trí đích, sau đó run_manifest.json được thay cuối cùng. Thiết kế này tránh công bố một bộ phân tích chưa dựng xong, nhưng bước chuyển nhiều tệp không phải nguyên tử toàn bộ: lỗi giữa chừng có thể để lại hỗn hợp tệp. Manifest và verifier phát hiện trạng thái không đồng nhất đó trước khi dùng để khẳng định một phiên bản hoàn tất. Dashboard và workbook được dựng/kiểm như sản phẩm dẫn xuất có metadata riêng.

scripts/run_project.py điều phối tải/kiểm nguồn, pipeline, dựng HTML, kiểm thử, SQL và verifier. Tùy chọn --workbook yêu cầu dựng thêm Excel; --skip-download dùng nguồn cục bộ đã đúng checksum, không bỏ kiểm nguồn; --skip-tests không được diễn giải thành đã kiểm thử đạt. Bộ test Python bao quát các quy tắc phân tích và hợp đồng đầu ra, trong khi test JavaScript chạy mã thật trên DOM tối giản để kiểm các trạng thái và CSV. Cách tách lớp kiểm này cho phép ghi chính xác phần đã chạy bằng máy và phần bố cục trình duyệt hoặc Excel thật còn cần xác nhận.

tools/verify_delivery.py kiểm lại nguồn và manifest, đối soát từng bản ghi giữa CSV/JSON/database, kiểm phép chia và lineage, rồi kiểm sản phẩm dẫn xuất. Chế độ --require-workbook còn đọc đủ các dòng và KPI Excel, đối chiếu metadata cùng bằng chứng tính lại. tools/prepare_handover_evidence.py bổ sung phép tính trung vị bằng csv/statistics và SQLite ORDER BY, chạy lại bốn truy vấn chỉ đọc và tạo hồ sơ rà soát. Bộ bổ sung được ghim theo mốc dữ liệu, tránh chuyển một nhận xét nội dung cũ thành kết quả kiểm cho lần chạy khác.

# Chương 5 Vận hành và kết quả thực nghiệm

Các kết quả trong chương lấy từ lần chạy 20261016T015620Z-f2e661a6. Đây là mã định danh kỹ thuật của một bộ sản phẩm, không phải ngày dữ liệu thị trường. Môi trường được lưu trong analysis.json gồm Python 3.13.7, NumPy 2.3.3, pandas 2.3.3, Matplotlib 3.10.6 và SQLite 3.50.4. Nguồn, mã lõi và sản phẩm được nối bằng hash trong manifest; bảng, hình và kết luận bên dưới cùng tham chiếu bộ dữ liệu giữ 6.936 tin. Ngày công bố nguồn vẫn là 12/01/2021 [1].

Để vận hành phần cốt lõi từ bản clone, người dùng tạo môi trường Python phù hợp, cài requirements và chạy scripts/run_project.py. Lệnh mặc định tải hoặc kiểm nguồn trước pipeline; sau đó tạo dữ liệu, database, hình và HTML rồi thực thi các bước kiểm. Nếu chỉ cần xem kết quả đã tạo, có thể mở outputs/DASHBOARD_BAT_DONG_SAN.html bằng trình duyệt hoặc workbook bằng Excel mà không chạy lại thuật toán. Bảng [[table:operation]] ghi lệnh cùng phạm vi của từng thao tác, tránh nhầm việc xem một file có sẵn với tái tạo thành công cả hệ thống.

@table operation

Kết quả làm sạch được đối soát tại Bảng [[table:counts]]. Trong 9.004 bản ghi, có 1.884 tin trùng theo khóa năm trường, 184 tin cách ly và 6.936 tin giữ. Các trường lõi không trống không có nghĩa mọi giá trị đều phân tích được: 459 chuỗi diện tích nguồn chưa đọc được theo parser ban đầu; sau gộp trùng và khôi phục diện tích ghi rõ trong chuỗi giá, 349 tin giữ có diện tích khôi phục. Một tin bị cách ly có thể có nhiều lý do, do đó tổng số lượt lý do không được dùng thay số dòng cách ly.

@table counts

Khả năng truy nguyên được minh họa bằng hai dòng đã sử dụng trong thiết kế. Dòng 1 được giữ với 100 m², tổng giá 2,38 tỷ và đơn giá 23,8 triệu/m². Dòng 638 có 143 m², giá lõi 20 triệu và mô tả 20tr/m2, nên chuyển vào rejected thay vì tự sửa thành một tổng giá suy đoán. Các ví dụ bổ sung như 7811 có 860 tỷ so với 860 triệu, hoặc 335 có 2 m² so với 2 ha, cho thấy kiểm chéo nguồn có vai trò trước thống kê. Đồng thời, các khác biệt nhỏ, mô tả nhiều lô hoặc viết tắt vẫn có thể vượt qua bộ quy tắc, nên tập giữ chỉ được coi là hợp lệ theo chính sách đã nêu.

Tổng hợp chính cho thấy trung vị diện tích là 70 m², trung vị tổng giá 2,25 tỷ VND và trung vị đơn giá khoảng 32,3205 triệu VND/m². Trung bình tổng giá khoảng 3,6954 tỷ, cao hơn trung vị, phù hợp với phần đuôi giá cao. Bảng [[table:descriptive]] cung cấp các phân vị để việc đọc hình không chỉ dựa vào cảm giác. Hình [[figure:01_price_distribution]] đặt histogram tổng giá ở thang gốc cạnh thang log, giúp quan sát cả phần đuôi và khu vực tập trung. Hai histogram dùng cùng 6.936 tin, không phải hai mẫu trước và sau loại ngoại lệ.

@table descriptive

@figure 01_price_distribution

Hình [[figure:02_area_price_scatter]] biểu diễn diện tích và tổng giá trên hai trục log, với màu theo loại suy luận. Các dòng minh họa tại Bảng [[table:scatter_examples]] có thể kiểm lại trong CSV sạch. Dải giá và diện tích rộng làm các quan sát chồng lên nhau; vì vậy mật độ nhìn thấy trong một vùng không được hiểu như tỷ trọng thị trường. Scatter tĩnh vẽ toàn bộ tập giữ, trong khi dashboard có thể lấy mẫu điểm để hiển thị nhẹ và ghi riêng số điểm được vẽ.

@figure 02_area_price_scatter

@table scatter_examples

Tương quan Spearman diện tích–tổng giá bằng −0,037634, tức quan hệ đơn điệu tổng thể rất yếu trong mẫu đang trộn nhiều loại và địa phương. Kết quả không hỗ trợ câu kết luận đơn giản rằng diện tích lớn luôn đi kèm tổng giá cao trong toàn bộ tập này. Khi ghép đất diện tích lớn ở địa phương khác với nhà đô thị diện tích nhỏ, cấu trúc thành phần có thể che hoặc đảo các quan hệ bên trong nhóm. Hệ số diện tích–đơn giá bằng −0,588097 còn phải đọc cùng việc đơn giá chứa diện tích ở mẫu số, không thể xem là bằng chứng độc lập của tác động kinh tế.

@figure 08_spearman_correlation

@table correlations

Mẫu phân bố không đều theo địa phương. TP.HCM có 3.277 tin, Hà Nội 1.014, Bình Dương 465 và Đà Nẵng 455; riêng hai nhóm đầu chiếm khoảng 61,87% tập giữ. Hình [[figure:03_province_medians]] chọn mười địa phương nhiều tin nhất có n ít nhất 30 rồi sắp theo trung vị để trình bày. Tiêu chí chọn là độ phủ mẫu, không phải chọn mười địa phương đắt nhất. Bảng [[table:province_top]] kèm n và trung vị giúp xác định đúng tập đang được so sánh; khoảng bootstrap trên hình chỉ có ý nghĩa có điều kiện theo cách lấy lại mẫu đã mô tả.

@figure 03_province_medians

@table province_top

Trong các nhóm được trình bày, Hà Nội có trung vị đơn giá khoảng 77,1198 triệu/m², TP.HCM khoảng 45,2830 và Đà Nẵng khoảng 42,8571. Những khác biệt này có thể đồng thời phản ánh cơ cấu nhà/đất/căn hộ, diện tích, vị trí trong từng địa phương và cách thu thập tin. Không suy rộng chúng thành bảng xếp hạng giá thị trường hiện tại. Việc lọc cùng loại trong cùng địa phương là một bước mô tả hữu ích, nhưng vẫn chưa kiểm soát hết những biến không có trong nguồn như chất lượng nhà hoặc vị trí chính xác.

Loại nhà có 3.590 tin, đất 1.856, căn hộ 370 và chưa xác định 1.120. Bảng [[table:types]] cho thấy trung vị đơn giá nhà khoảng 56,4145 triệu/m², đất 8,5, căn hộ 27,6923 và nhóm chưa rõ 39,2857. Nhóm chưa rõ không được bỏ khỏi mẫu chỉ vì bất tiện khi diễn giải. Phần lớn nhãn do tiêu đề quyết định, trong khi lượt rà soát nhận thấy một số mô tả có thể xác định loại rõ hơn tiêu đề viết tắt. Vì vậy, sự khác biệt loại hình được báo cáo như kết quả theo nhãn suy luận hiện có.

@table types

Hình [[figure:06_cleaning_sensitivity]] và Bảng [[table:sensitivity]] thể hiện tác động của các lựa chọn xử lý. Bỏ IQR nhóm còn 6.676 tin và trung vị đơn giá giảm khoảng 4,52%; chỉ giữ tiêu đề bán rõ còn 3.030 tin và trung vị tăng khoảng 1,79%. Bỏ các tin có quy ước dấu chấm hàng nghìn còn 6.608 tin, trung vị tăng khoảng 8,84%, mức thay đổi lớn hơn hai trường hợp vừa nêu. Kết quả cho thấy bất định về chuỗi số và thay đổi thành phần mẫu đáng được nêu trong kết luận, không chỉ tập trung vào ngoại lệ thống kê.

@figure 06_cleaning_sensitivity

@table sensitivity

Rà soát bổ sung bằng trợ lý đọc 60 tin phân tầng và bảy tin trọng điểm, lưu diễn giải tách khỏi các cột nhãn người thật. Đây là một lượt kiểm nội dung hỗ trợ, không phải bộ nhãn chuẩn hoặc hai người đọc độc lập. Trong 40 tin giữ thuộc mẫu rà soát vẫn xuất hiện giá/diện tích hoặc ngữ cảnh giao dịch mơ hồ. Một phân tích tình huống riêng loại 16 tin giữ được chọn có chủ đích, gồm cả dòng 8535 ngoài mẫu; còn 6.920 tin, trung vị tổng giá và diện tích giữ ở 2,25 tỷ/70 m², đơn giá thành khoảng 32,3608 triệu/m². Sự ổn định này chỉ mô tả tình huống đã chọn; không ước lượng tỷ lệ lỗi toàn bộ tập và không làm mất nhu cầu xác minh nếu sử dụng cho mục đích quyết định thực tế.

Phân cụm được fit trên 6.676 tin sau loại cờ IQR nhóm khỏi tập fit. Hình [[figure:07_exploratory_clusters]] đặt kết quả nhóm bên cạnh điểm silhouette khi thử k=2–5; Bảng [[table:cluster_trials]] và Bảng [[table:cluster_summary]] cung cấp số liệu tương ứng. k=2 có silhouette mẫu khoảng 0,6231, cao nhất trong bốn phương án; inertia giảm khi tăng k nhưng không được dùng riêng để chọn k. Hai phép chạy seed 7 và 42 có ARI bằng 1 so với phân hoạch chính. Đây là độ ổn định nội bộ trên cùng đầu vào và cách biến đổi, không phải accuracy của việc nhận dạng phân khúc thị trường.

@figure 07_exploratory_clusters

@table cluster_trials

@table cluster_summary

Cụm 1 có 961 tin, trung vị diện tích 500 m² và đơn giá 2,3 triệu/m²; cụm 2 có 5.715 tin, diện tích 63 m² và đơn giá khoảng 39,1892 triệu/m². Có thể mô tả ngắn là nhóm diện tích lớn–đơn giá thấp và nhóm diện tích nhỏ hơn–đơn giá cao hơn trong không gian đã chọn. Những mô tả này không đồng nghĩa loại hình bất động sản hoặc mức chất lượng pháp lý. Việc chỉ dùng hai đặc trưng cùng dữ liệu nguồn còn bất định giới hạn khả năng diễn giải nghiệp vụ; phân cụm được dùng như công cụ thăm dò hỗ trợ các bảng mô tả.

Cơ sở dữ liệu SQLite chứa 6.936 listings và vượt kiểm tra toàn vẹn, không ghi nhận lỗi khóa ngoại trong PRAGMA foreign_key_check. Bốn truy vấn đọc trả lần lượt 20, 4, 20 và 100 dòng; truy vấn cuối dùng cùng tỉnh/loại và khoảng đơn giá đã lưu trong benchmark. Bảng [[table:sql_results]] trình bày một phần kết quả thật của truy vấn cuối. Việc có database, câu SQL, tham số và bản ghi trả về làm minh họa có thể kiểm chứng được, thay vì chỉ dùng ảnh cú pháp chưa thực thi.

@table sql_results

Trước chỉ mục, kế hoạch ghi SCAN listings và USE TEMP B-TREE FOR ORDER BY; sau chỉ mục, kế hoạch tìm qua idx_listings_search với các điều kiện tương ứng. Hai kết quả 100 dòng có cùng hash, nên minh họa bảo toàn câu trả lời khi thay cách truy cập. Tuy nhiên, Bảng [[table:sql_benchmark]] cho thấy trung vị thời gian trước là 0,6484 ms và sau 0,7788 ms; tỷ số trước/sau khoảng 0,833. Lần đo này không chứng minh tăng tốc. Chỉ mục thay đổi kế hoạch nhưng độ trễ còn chịu cache, dữ liệu nhỏ và tải máy; việc lựa chọn lại một lần chạy có số đẹp sẽ làm sai ý nghĩa thực nghiệm.

@table sql_benchmark

Phép đo dùng cùng kết nối, câu lệnh và tham số; mỗi pha có 10 warmup và 51 lần đo, với ANALYZE trước pha tương ứng. Thiết kế trước–sau là tuần tự warm-cache, chưa ngẫu nhiên hóa hoặc lặp các khối độc lập, cũng chưa đo chi phí ghi và dung lượng chỉ mục. Vì vậy, bằng chứng phù hợp để giải thích kế hoạch truy vấn, đối soát kết quả và thảo luận giới hạn, chưa cho phép khẳng định cải thiện hiệu năng production hoặc mọi truy vấn. Bản chạy khác có thể cho tỷ số khác và phải được ghi như một lần đo riêng.

Đối với sản phẩm sử dụng, test JavaScript thực trong DOM tối giản kiểm các trạng thái ở Bảng [[table:dashboard_states]]. Bộ lọc toàn trang, tìm kiếm bảng, phân trang và CSV đã có kiểm logic; tìm Hà Nội ở ô bảng cho 1.014 dòng trong bảng/CSV trong khi KPI toàn trang giữ 6.936 nếu chưa đổi bộ lọc cấp trang. Những kết quả này giúp xác định hành vi mong đợi, nhưng không được ghi thành đã quan sát mọi bố cục trong một trình duyệt thật. Công cụ kiểm trình duyệt không truy cập được URL file cục bộ của bản mới; các xác nhận người dùng trước đây thuộc bản 7.001 tin không được chuyển sang xác nhận bản hiện tại.

@table dashboard_states

Workbook có ba trang và bốn biểu đồ, được đối soát đủ 6.936 dòng cùng các KPI lưu. Bằng chứng Artifact Tool ghi tính lại sau thay giá/diện tích, tám kiểm đầu vào không hợp lệ và quét lỗi công thức. Ví dụ trên bản thử, dòng Excel 10 ban đầu H=2.380.000.000, G=100 cho I=23.800.000; đổi H thành 3.380.000.000 thì I=33.800.000. Thao tác tính lại trực tiếp trong Microsoft Excel thật chưa được xác nhận trong lượt kiểm này. Tài liệu phân biệt rõ phép kiểm bằng engine/cached values với nghiệm thu giao diện ứng dụng cuối.

Hình [[figure:workbook_kpi]] trích vùng chỉ tiêu của trang Dashboard từ ảnh render workbook cùng phiên bản, không phải ảnh chụp thao tác Microsoft Excel. Các giá trị 6.936 tin, giá trung vị 2,25 tỷ, giá trung bình hiển thị 3,70 tỷ, diện tích 70,00 m² và đơn giá 32,32 triệu/m² phù hợp số chưa làm tròn ở Bảng [[table:descriptive]]. Việc đưa vùng số liệu cùng đơn vị vào minh họa giúp đánh giá kết quả thực tế của sản phẩm mà không biến ảnh render thành bằng chứng của một loại thao tác chưa kiểm.

@figure workbook_kpi

Các lớp kiểm được tổng hợp tại Bảng [[table:verification]]. Bộ 29 test Python đạt, không có lỗi hoặc trường hợp bỏ qua. Verifier so từng bản ghi CSV/JSON/database, phép chia, lineage, hash và workbook; phép tính ba trung vị bằng thư viện csv/statistics và SQLite ORDER BY cũng khớp analysis.json. Một bản sao chỉ gồm nguồn/mã đã tạo lại 6.936 bản ghi giống nhau bằng cùng Python có thư viện sẵn. Kết quả đó chưa bao gồm cài pip mới trên máy khác, tải qua mạng khác hoặc dựng Excel ngoài runtime hiện có. Phân biệt các phạm vi này giúp đánh giá mức vận hành thực tế mà không mở rộng kết luận quá bằng chứng.

@table verification

# Chương 6 Kết luận và đánh giá khả năng ứng dụng

Mục tiêu khám phá và so sánh giá rao trong mẫu tin lịch sử đã được hiện thực thành một chuỗi xử lý có mã, dữ liệu dẫn xuất và sản phẩm tra cứu. Từ 9.004 dòng, hệ thống gộp 1.884 dòng trùng theo khóa nội dung, cách ly 184 dòng và giữ 6.936 tin; các phép đối soát bảo toàn quy mô và truy nguyên quyết định ở cấp dòng. Bảng thống kê và biểu đồ cho thấy trung vị tổng giá 2,25 tỷ, diện tích 70 m² và đơn giá khoảng 32,3205 triệu/m² trong tập giữ. Những con số này là kết quả của phạm vi và chính sách đã mô tả, không phải một mức giá chung cho thị trường Việt Nam.

Về độ tin cậy, bằng chứng mạnh nhất nằm ở đúng phiên bản nguồn, tính nhất quán tính toán và khả năng phát hiện sản phẩm khác lần chạy. SHA-256 khớp bản nguồn; dữ liệu giữa CSV, JSON, SQLite, HTML và workbook được đối soát; ba trung vị tính độc lập thống nhất. Tuy nhiên, độ tin cậy nội dung quảng cáo thấp hơn mức có thể kiểm bằng mã: vẫn có tin mơ hồ, nhãn suy luận từ tiêu đề và nhóm giả định bán. Rà soát bằng trợ lý đã phát hiện các trường hợp lọt quy tắc, chưa tạo bộ nhãn chuyên gia hoặc xác nhận giao dịch. Vì vậy, có thể sử dụng kết quả để mô tả mẫu có điều kiện, chưa đủ cơ sở dùng cho định giá hoặc khẳng định độ chính xác nhãn.

Về vận hành, phần cốt lõi đã chạy và có bộ 29 test Python đạt, kiểm logic JavaScript cùng các sản phẩm lưu thực tế. Quy trình một lệnh giúp nối bước tải/kiểm nguồn, xử lý, dựng HTML, truy vấn và xác minh. Dashboard có thể được phân phối như file chứa dữ liệu, Excel có thể mở từ workbook đã tạo. Mức xác nhận còn thiếu là bố cục/thao tác trình duyệt của bản 6.936 tin, tính lại trong Microsoft Excel thật và cài mới trên một máy độc lập. Các giới hạn này không phủ nhận phần xử lý đã thực thi, nhưng cần giữ rõ khi đánh giá sẵn sàng sử dụng trong những môi trường khác.

Về tích hợp, các mô-đun chia sẻ bộ biến, run_id và metadata để giảm nhầm phiên bản. SQLite cung cấp truy vấn quan hệ, HTML cung cấp lựa chọn tương tác, Excel cung cấp bảng/công thức, còn các bảng và ảnh phục vụ phân tích. Đây là tích hợp qua tệp và lệnh cục bộ; chưa phải một dịch vụ nhiều người dùng có backend và đồng bộ trực tuyến. Excel có phụ thuộc dựng riêng và một số snapshot, còn bước xuất nhiều tệp chưa nguyên tử toàn bộ. Manifest cùng verifier là cơ chế phát hiện không nhất quán sau lỗi hoặc chỉnh sửa riêng, không nên được mô tả thành bảo đảm giao dịch cho mọi sản phẩm.

Về kết quả phân tích, sự phân bố lệch, khác biệt thành phần địa phương và bất định cách ghi số ảnh hưởng trực tiếp đến diễn giải. Tương quan diện tích–tổng giá tổng thể yếu; các khác biệt tỉnh/loại chưa kiểm soát hết yếu tố nhiễu. Độ nhạy cho thấy bỏ nhóm dấu chấm hàng nghìn làm trung vị đơn giá thay đổi khoảng 8,84%, cần chú ý hơn một kết luận chỉ dựa vào ngoại lệ. K-means tạo hai nhóm ổn định theo các seed đã thử nhưng không có nhãn thị trường để kiểm định. SQL bảo toàn kết quả và thay plan, trong khi lần đo ghi nhận không tăng tốc. Việc giữ các kết quả không thuận kỳ vọng là điều kiện để kết luận thực nghiệm có thể được đánh giá nghiêm túc.

@table conclusion

Phạm vi ứng dụng phù hợp hiện tại là học tập, minh họa quy trình dữ liệu và khám phá có kiểm chứng một nguồn lịch sử. Người đọc có thể sử dụng các bảng/biểu đồ để đặt câu hỏi, so điều kiện lọc và truy nguyên trường hợp cần xem lại. Sản phẩm chưa cung cấp căn cứ mua bán, đánh giá pháp lý hoặc khuyến nghị tài chính; nguồn không có ngày từng tin, vị trí xác minh và giá giao dịch để phục vụ những mục đích đó. Bảng [[table:conclusion]] tóm tắt mức đạt theo từng khía cạnh thay vì đánh giá bằng một nhận xét chung rằng hệ thống hoàn toàn chính xác hoặc ứng dụng rộng rãi.

Hướng phát triển ưu tiên là tăng chất lượng bằng chứng trước khi tăng độ phức tạp mô hình. Trước hết, cần nguồn có quyền sử dụng, ngày đăng và mã tin rõ ràng, cùng một thiết kế gán nhãn người thật nếu muốn đánh giá bộ nhận diện. Tiếp theo, những cách ghi nhiều lô, tiền trả trước và nhiều định nghĩa diện tích cần chính sách phân biệt tốt hơn, đi kèm kiểm hồi quy cho cả trường hợp nên giữ. Nếu đo hiệu năng tiếp, cần lặp nhiều khối hoặc ngẫu nhiên thứ tự đo, báo chi phí lưu/ghi và tách dữ liệu thử tải khỏi EDA. Những hướng này đều phục vụ mục tiêu đọc giá rao đáng tin cậy hơn trong phạm vi đã xác định, thay vì mở rộng đề tài thành một hệ thống khác.
