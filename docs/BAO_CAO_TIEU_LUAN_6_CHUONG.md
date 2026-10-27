# Báo cáo sáu chương hiện hành

Bản trích nội dung từ Word; hình và định dạng nằm trong DOCX/PDF.

HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG

BÁO CÁO TIỂU LUẬN

Học phần Nhập Môn Khoa Học Dữ Liệu

Phân tích giá rao bất động sản Việt Nam

Giảng viên hướng dẫn: Nguyễn Ngọc Duy

Nhóm thực hiện

Võ Văn Đạt  —  N23DCCN078

Nguyễn Thị Yến Nhi  —  N23DCCN112

Hứa Như Quỳnh  —  N23DCCN118

Tháng 10 năm 2026

LỜI CẢM ƠN

Nhóm chúng em xin chân thành cảm ơn Thầy Nguyễn Ngọc Duy, giảng viên học phần Nhập môn Khoa học Dữ liệu tại Học viện Công nghệ Bưu chính Viễn thông, đã truyền đạt những kiến thức nền tảng và hướng dẫn chúng em trong quá trình học tập. Những kiến thức đó đã giúp nhóm có cơ sở để thực hiện đề tài Phân tích giá rao bất động sản Việt Nam.

Trong quá trình nghiên cứu và thực hiện đề tài, nhóm có cơ hội vận dụng kiến thức về thu thập, làm sạch, phân tích và trực quan hóa dữ liệu vào một bộ dữ liệu thực tế. Qua đó, chúng em cũng tích lũy thêm kinh nghiệm trong việc xử lý dữ liệu, sử dụng các phương pháp thống kê và phân cụm, xây dựng sản phẩm phân tích, cũng như phối hợp làm việc nhóm.

Mặc dù đã cố gắng hoàn thành đề tài, báo cáo khó tránh khỏi những thiếu sót do giới hạn về thời gian, kiến thức và kinh nghiệm. Nhóm chúng em mong nhận được những ý kiến nhận xét, góp ý từ Thầy để có thể tiếp tục hoàn thiện kiến thức và kỹ năng chuyên môn.

Nhóm chúng em xin chân thành cảm ơn!

TÓM TẮT

Tiểu luận xây dựng một quy trình có thể chạy lại để khám phá và so sánh giá rao trong mẫu tin bất động sản lịch sử từ Vietnam Real Estate Data v2, công bố trên Mendeley Data năm 2021. Từ 9.004 bản ghi, quy trình gộp 1.884 dòng trùng theo năm trường lõi, cách ly 209 dòng chưa đáp ứng chính sách và giữ 6.911 tin. Bản nguồn được kiểm checksum; dữ liệu sạch đi kèm cờ chất lượng và nhật ký truy nguyên để giải thích các quyết định xử lý.

Trung vị tổng giá là 2,25 tỷ VND, diện tích 70 m² và đơn giá 32,50 triệu VND/m². Tương quan diện tích–tổng giá thay đổi theo nhóm: 0,610 ở căn hộ và 0,643 ở nhà tại Hà Nội. K-means tạo hai nhóm từ 6.652 tin; 65 phép fit bổ sung cho thấy cụm ổn định với mẫu con nhưng nhạy với cách biểu diễn đặc trưng. SQLite minh họa truy vấn và chỉ mục trên cùng dữ liệu.

Sản phẩm gồm bảng/hình, dashboard HTML và workbook Excel. Mẫu 180 tin được tách thành 120 phát triển và 60 đánh giá. Một thành viên gán nhãn ban đầu; AI hỗ trợ rà soát và trực tiếp chỉnh 17 tin. Kết quả đối chiếu được báo theo trường và tầng lấy mẫu, chưa phải kiểm định nhãn người độc lập. Phân tích mở rộng theo tỉnh × loại × khoảng diện tích và độ nhạy phân cụm giúp giới hạn kết luận trong mẫu tin lịch sử.

Từ khóa: giá rao bất động sản; chuẩn bị dữ liệu; trực quan hóa; truy nguyên; K-means; SQLite.

Mốc phân tích và sản phẩm hiện hành: 20261027T065401Z-5c8df2cc. Các bảng mở rộng cùng mốc được lưu tại outputs/extended. Nguồn công bố 12/01/2021; ngày xử lý không phải thời điểm giá thị trường.

Mục lục

Chương 1 Giới thiệu đề tài	1

Chương 2 Cơ sở lý thuyết và nền tảng kỹ thuật	3

Chương 3 Phân tích và thiết kế ứng dụng	8

Chương 4 Hiện thực hệ thống	13

Chương 5 Vận hành và kết quả thực nghiệm	17

Chương 6 Kết luận và đánh giá khả năng ứng dụng	29

Tài liệu tham khảo	33

Phụ lục tái lập và nguồn minh chứng	34

Danh mục hình và bảng

Hình 1: Sơ đồ luồng xử lý và các sản phẩm dữ liệu	9

Hình 2: Sơ đồ quan hệ ba bảng trong SQLite	11

Hình 3: Phân bố tổng giá rao ở thang gốc và thang log	19

Hình 4: Mối liên hệ giữa diện tích và tổng giá rao	20

Hình 5: Ma trận tương quan Spearman của ba biến phân tích	21

Hình 6: Trung vị đơn giá của mười địa phương có nhiều tin nhất	22

Hình 7: Đối soát làm sạch và độ nhạy theo lựa chọn xử lý	23

Hình 8: Phân nhóm K-means và khảo sát số cụm	24

Hình 9: Vùng chỉ tiêu trong bản render trang Dashboard của Excel	27

Bảng 1: Phạm vi ứng dụng và giới hạn suy luận	2

Bảng 2: Dữ liệu minh họa hai nhánh giữ và cách ly	9

Bảng 3: Từ điển 18 biến của dữ liệu sạch	9

Bảng 4: Bản ghi minh họa liên kết ba bảng	11

Bảng 5: Liên kết mô-đun với đầu vào và đầu ra	13

Bảng 6: Lệnh vận hành và phạm vi tạo kết quả	17

Bảng 7: Đối soát quy mô dữ liệu trước và sau xử lý	18

Bảng 8: Thống kê minh họa phân bố giá và diện tích	18

Bảng 9: Một số tin minh họa cho biểu đồ diện tích và giá	20

Bảng 10: Hệ số Spearman giữa các biến phân tích	21

Bảng 11: Dữ liệu mười địa phương có nhiều tin nhất trong hình	22

Bảng 12: Thống kê theo loại hình suy luận từ tiêu đề	23

Bảng 13: Độ nhạy của trung vị đơn giá theo lựa chọn xử lý	24

Bảng 14: Khảo sát số cụm trên cùng tập fit	25

Bảng 15: Đặc điểm hai cụm ở đơn vị gốc	25

Bảng 16: Năm dòng đầu của truy vấn khoảng đơn giá	26

Bảng 17: Thời gian truy vấn trước và sau chỉ mục	26

Bảng 18: Kết quả kiểm logic các trạng thái dashboard	27

Bảng 19: Phạm vi và kết quả các lớp kiểm chứng	28

Bảng 20: Mức đáp ứng mục tiêu theo bằng chứng hiện có	29

Chương 1 Giới thiệu đề tài

Đề tài Phân tích giá rao bất động sản Việt Nam xây dựng một quy trình xử lý dữ liệu có thể chạy lại, từ bản ghi tin quảng cáo đến các bảng thống kê, biểu đồ và công cụ tra cứu. Mục tiêu duy nhất là giúp người phân tích khám phá và so sánh đặc điểm giá rao trong mẫu tin lịch sử sau khi áp dụng các quy tắc kiểm tra chất lượng công khai. Giá rao được hiểu là số tiền được nêu trong quảng cáo, chưa phải số tiền của giao dịch đã hoàn tất. Cách xác định này chi phối việc chọn nguồn, thiết kế dữ liệu và phạm vi diễn giải của toàn bộ tiểu luận.

Khó khăn của bài toán xuất hiện trước bước vẽ biểu đồ. Cùng một giá trị có thể được viết bằng tỷ, triệu hoặc đồng; một chuỗi giá có thể kèm diện tích, chứa giá trên mét vuông hoặc khoản thanh toán ban đầu. Diện tích có thể dùng dấu phẩy thập phân, dấu chấm hàng nghìn, đơn vị héc-ta hoặc các mô tả về đất và diện tích sử dụng khác nhau. Tin lặp làm tăng trọng số của nội dung được đăng nhiều lần. Nếu chuyển các chuỗi này thành số mà bỏ qua cơ sở giá và ý nghĩa diện tích, kết quả tổng hợp vẫn có thể tính được nhưng không còn trả lời đúng câu hỏi ban đầu.

Ý nghĩa thực tiễn của đề tài là cung cấp một cách tổ chức và đọc dữ liệu rao bán rõ nguồn gốc. Người dùng có thể quan sát phân bố giá, so sánh trung vị giữa các tập lọc và xem kết quả nhạy đến mức nào với lựa chọn xử lý. Khi gặp giá khác thường, hệ thống cho phép truy nguyên dòng nguồn và lý do cách ly, thay vì chỉ đưa ra một con số cuối cùng. Sản phẩm phù hợp với học tập, khảo sát dữ liệu và chuẩn bị giả thuyết phân tích; việc định giá để giao dịch cần những nguồn và quy trình xác minh bổ sung.

Đối với cộng đồng nghiên cứu, đóng góp nằm ở tình huống thực nghiệm có thể kiểm tra lại: giữ bản nguồn bất biến, công bố quy tắc biến đổi, phân biệt suy luận nhãn với thông tin đã xác minh và đánh giá độ nhạy của kết quả. Các bước này giúp nghiên cứu sau hiểu vì sao hai phép phân tích cùng một nguồn có thể cho số lượng tin hoặc trung vị khác nhau. Tiểu luận không đề xuất thuật toán mới; các kỹ thuật thống kê, K-means và chỉ mục quan hệ được sử dụng để xây dựng một quy trình có bằng chứng. Điều này phù hợp với vai trò trích xuất tri thức, tư duy phản biện và truyền đạt kết quả trong nội dung mở đầu học phần [2].

Nguồn thực nghiệm là Vietnam Real Estate Data phiên bản 2, do Duc Chung Tran, Huy Hoang Nguyen và Hong Son Ha công bố trên Mendeley Data ngày 12/01/2021 theo giấy phép CC BY 4.0 [1]. Mô tả nguồn ghi 10.000 bài đăng, trong khi tệp JSON được công bố thực tế chứa 9.004 bản ghi. Nghiên cứu sử dụng 9.004 làm mẫu số đầu vào, giữ nguyên sự khác biệt này trong hồ sơ nguồn và không bổ sung bản ghi để khớp mô tả. Ngày công bố dữ liệu không phải ngày đăng của từng tin; ngày thực hiện phân tích năm 2026 cũng không biến những giá rao lịch sử thành giá thị trường năm 2026.

Đơn vị quan sát là một bản ghi quảng cáo. Sau khi gộp trùng nội dung, một dòng giữ lại vẫn chưa chắc tương ứng với một bất động sản duy nhất: cùng tài sản có thể được nhiều môi giới đăng với tiêu đề khác nhau, và nguồn không có mã tin ổn định để xác nhận. Tương tự, loại hình và trạng thái bán là nhãn được suy luận bằng quy tắc từ tiêu đề, không phải nhãn chuyên gia cung cấp. Trong toàn văn, các thuật ngữ tin, giá rao và loại hình suy luận được dùng nhất quán để tránh chuyển từ đối tượng quan sát sang đối tượng chưa được đo.

Phạm vi ứng dụng được thu hẹp trong Bảng 1. Mọi chức năng đều phục vụ mục tiêu khám phá mẫu tin: làm sạch tạo điều kiện so sánh, trực quan giúp đọc phân bố, K-means gợi ý cấu trúc nhóm, còn SQLite minh họa truy vấn cùng tập dữ liệu. Các câu hỏi về phân bố giá, sự khác biệt địa phương và độ nhạy là những câu hỏi con của cùng mục tiêu, không hình thành các hệ thống độc lập về dự báo, môi giới hay đầu tư.

Bảng 1: Phạm vi ứng dụng và giới hạn suy luận

| Thành phần | Phạm vi được chọn | Giới hạn |
| --- | --- | --- |
| Đối tượng | Tin quảng cáo bất động sản trong tệp v2 | Không đồng nhất tin với tài sản hoặc giao dịch |
| Thời gian | Nguồn công bố 12/01/2021 | Không suy ra giá thị trường 2026 hoặc chuỗi thời gian |
| Địa phương | Nhãn địa chỉ lịch sử trong nguồn | Không suy tọa độ hay tự đổi địa giới hiện hành |
| Người sử dụng | Người phân tích và người xem kết quả | Hai cách sử dụng, chưa có phân quyền tài khoản |
| Đầu ra | Thống kê, hình, nhóm thăm dò, HTML/Excel/SQL | Chưa dùng định giá, môi giới hoặc khuyến nghị đầu tư |

Nguồn: thiết kế phạm vi nghiên cứu, đối chiếu metadata Mendeley v2 [1].

Đề tài đặt bốn câu hỏi phân tích. Câu hỏi 1: giá tổng và đơn giá phân bố ra sao, trung bình khác trung vị như thế nào? Câu hỏi 2: quan hệ diện tích–tổng giá thay đổi thế nào khi phân nhóm theo loại hình và địa phương? Câu hỏi 3: trung vị đơn giá khác nhau ra sao giữa các địa phương có nhiều tin, và thành phần mẫu giới hạn phép so sánh đó như thế nào? Câu hỏi 4: trung vị đơn giá nhạy đến đâu với chính sách ngoại lệ, cách ghi số và tiêu đề bán rõ? Chương 5 cung cấp bằng chứng định lượng, Chương 6 tổng hợp câu trả lời và những kiểm chứng còn cần thực hiện.

Sản phẩm của đề tài gồm dữ liệu đã chuẩn hóa, tập tin cách ly, nhật ký truy nguyên, các bảng tổng hợp, tám biểu đồ tĩnh, cơ sở dữ liệu SQLite, dashboard HTML ngoại tuyến và workbook Excel. Giải thuật phân cụm có mã thực thi bằng NumPy; phần minh họa SQL có database và câu lệnh thật. Dữ liệu có thể được xem qua HTML và Excel sau khi tạo, còn việc tái tạo phân tích được điều khiển bằng Python. Các lựa chọn này đáp ứng yêu cầu triển khai của học phần mà không buộc người xem phải cài hệ quản trị máy chủ hoặc sử dụng một dịch vụ dữ liệu trực tuyến.

Phương pháp triển khai gắn trực tiếp với bài học. Chương chuẩn bị dữ liệu của môn học cung cấp nền tảng về thiếu, nhiễu, không nhất quán, ngoại lệ, biến đổi và tổng hợp [3]. Chương trực quan hóa định hướng chọn biểu đồ, đơn vị và cách truyền đạt [4]. Phần K-means và SQL vận dụng nội dung mở rộng về phân cụm và dữ liệu quan hệ [5]–[7]. Các kỹ thuật bổ sung như bootstrap, silhouette và chỉ số Rand điều chỉnh được giải thích riêng, tránh coi mọi công cụ sử dụng đều đã được trình bày đầy đủ trong slide.

Chương 2 Cơ sở lý thuyết và nền tảng kỹ thuật

Quy trình khoa học dữ liệu trong đề tài gồm xác định đối tượng quan sát, kiểm tra nguồn, chuẩn hóa, mô tả, khảo sát cấu trúc và truyền đạt kết quả. Chất lượng ở mỗi bước ảnh hưởng đến bước sau: phép chia giá cho diện tích chỉ có nghĩa khi cả hai đại lượng được hiểu đúng, và khoảng cách phân cụm chỉ có nghĩa khi biến đã được biến đổi phù hợp. Vì vậy, cơ sở lý thuyết được trình bày theo các phép xử lý thực sự xuất hiện trong mã, đồng thời chỉ ra điều kiện áp dụng và sai lệch có thể còn lại.

Python điều phối việc đọc nguồn, xử lý, xuất kết quả và kiểm thử. Các thư viện pathlib, json, urllib.request và hashlib hỗ trợ đường dẫn, dữ liệu JSON, tải HTTPS và SHA-256 [12]. NumPy phục vụ tính toán số; pandas tổ chức bảng; Matplotlib tạo biểu đồ. Môi trường ảo và phiên bản thư viện giúp tái lập kỹ thuật. Lựa chọn công cụ không thay thế việc kiểm nội dung nguồn hoặc giải thích các quyết định phân tích.

Chuẩn hóa văn bản sử dụng Unicode NFKC, thu gọn khoảng trắng và casefold. NFKC làm đồng nhất một số biểu diễn ký tự tương thích; casefold hỗ trợ so sánh không phân biệt cách viết hoa. Biểu thức chính quy sau đó nhận diện số, đơn vị và từ khóa. Những thao tác này phục vụ so khớp và phân tích, không ghi đè bản nguồn. Chúng cũng có giới hạn: từ viết tắt, lỗi chính tả, dấu câu hoặc từ có nhiều nghĩa có thể làm quy tắc bỏ sót hay nhận nhầm. Do đó, kết quả nhận diện được giữ cùng cờ chất lượng, nhóm chưa xác định và ví dụ truy nguyên, thay vì xem chuẩn hóa là bước sửa mọi sai lệch ngôn ngữ.

Kiểm nguồn dùng SHA-256 trên toàn bộ byte của tệp. Hai tệp có cùng tên hoặc cùng số dòng chưa đủ chứng minh cùng phiên bản; dấu kiểm giúp phát hiện thay đổi nội dung hoặc byte xuống dòng. Trong đề tài, checksum được ghim theo bản công bố, rồi kiểm số lượng 9.004 đối tượng và kiểu cấu trúc trước khi xử lý. Mã định danh nội dung của từng tin có mục đích khác: băm năm trường lõi đã chuẩn hóa để phát hiện những bản ghi đồng nhất theo quy tắc. Hash nguồn kiểm phiên bản tệp; hash nội dung phục vụ gộp trùng. Cả hai đều không chứng minh hai tin là cùng bất động sản hoặc nội dung tin là sự thật.

Về kiểu dữ liệu, pandas biểu diễn bảng bằng DataFrame, mỗi dòng là một tin và mỗi cột là một thuộc tính. Các mặt nạ logic chọn những dòng đủ điều kiện, groupby chia theo khóa rồi áp dụng hàm tổng hợp. Phép chia giá cho diện tích được thực hiện trên từng dòng trước khi tính phân vị. Khi tính trung vị đơn giá, nhóm lấy trung vị của các tỷ số cá thể; đó không phải tỷ số của hai trung vị hay tổng giá chia tổng diện tích. Việc phân biệt thứ tự phép toán giúp tránh tạo một chỉ tiêu khác dưới cùng tên gọi. Kết quả xuất CSV và JSON để các sản phẩm sau cùng đọc một bộ biến đã được xác định [9].

Chuẩn hóa số phải xét cả ký hiệu lẫn đơn vị. Quy tắc quan sát của nguồn ưu tiên dấu phẩy thập phân và dấu chấm chia nhóm ba chữ số; một dấu chấm với ba chữ số cuối được gắn cờ do có thể mơ hồ. Diện tích héc-ta đổi sang mét vuông bằng hệ số 10.000; giá tỷ và triệu đổi sang VND bằng hệ số tương ứng. Một biểu thức giá trên mét vuông chỉ được quy thành tổng giá khi có diện tích phù hợp. Ngược lại, khi trường giá giống giá đơn vị trong mô tả nhưng thiếu cơ sở giải quyết, tin được cách ly. Đề tài không dùng trung bình hoặc mô hình để điền giá và diện tích thiếu, vì những giá trị đó quyết định trực tiếp biến phân tích.

(1)

Trong Công thức 1, Pᵢ là tổng giá rao sau chuẩn hóa, Aᵢ là diện tích được đọc từ tin, uᵢ là đơn giá; Pᵢ có đơn vị VND và Aᵢ có đơn vị m². Điều kiện Aᵢ dương ngăn phép chia không hợp lệ. Dòng nguồn số 1 có Pᵢ bằng 2.380.000.000 và Aᵢ bằng 100, nên uᵢ bằng 23.800.000 VND/m². Tính đúng số học của phép chia vẫn phụ thuộc cách người đăng hiểu diện tích là đất, sàn hoặc diện tích sử dụng.

Giá trị thiếu được phân biệt với giá trị không phân tích được. Một trường có văn bản như giá thỏa thuận không rỗng nhưng không cung cấp giá trị số; một chuỗi diện tích có nhiều khoảng lựa chọn cũng không tương đương với một diện tích đơn. Dữ liệu nguồn không có trường lõi trống trong lần đếm, nhưng có các chuỗi không đọc được theo bộ phân tích. Việc chỉ báo tỷ lệ ô không rỗng sẽ bỏ qua vấn đề này. Quy trình lưu lỗi phân tích, lý do cách ly và nguồn khôi phục diện tích để người đọc thấy quyết định được đưa ra từ bằng chứng nào [3].

Trung bình mô tả tổng giá trị chia số quan sát và nhạy với các giá rất lớn. Trung vị là vị trí giữa sau sắp thứ tự; với số quan sát chẵn, trung vị bằng trung bình của hai phần tử giữa. Phân vị Q1 và Q3 mô tả phần giữa của phân bố. Với giá rao lệch phải, việc báo trung vị cùng trung bình, tứ phân vị và số mẫu giúp thấy cả mức điển hình lẫn ảnh hưởng của phần đuôi. Không có một chỉ số đơn lẻ đủ thay thế toàn bộ phân bố, nhất là khi mẫu trộn nhiều loại bất động sản và địa phương.

(2)

IQR và hàng rào ở Công thức 2 được dùng như quy tắc gắn cờ thống kê. Giá trị nằm ngoài khoảng không mặc nhiên là lỗi: tài sản diện tích lớn hoặc vị trí đặc biệt có thể tạo quan sát khác biệt hợp lệ. Đề tài gắn cờ theo nhóm tỉnh và loại khi nhóm có ít nhất 30 tin; nếu không đủ, dùng nhóm loại hoặc toàn mẫu. Ngưỡng 30 là lựa chọn thiết kế để hạn chế nhóm tham chiếu quá ít quan sát, không phải bảo đảm độ chính xác thống kê. Bộ lọc IQR dùng các cờ đã tính trong pipeline, không ước lượng lại hàng rào sau mỗi tương tác dashboard.

Đánh giá độ nhạy đặt các phương án xử lý cạnh nhau trên cùng nguồn, gồm bỏ ngoại lệ, bỏ nhóm chuỗi số mơ hồ và chỉ giữ tiêu đề bán rõ. Sự thay đổi của n và trung vị cho biết tác động của từng chính sách. Loại một nhóm tin làm thay đổi thành phần mẫu, nên chưa đo riêng sai số do đọc nhầm dấu số. Muốn đánh giá sai số đó cần kiểm nguồn và thử các cách hiểu còn hợp lý của cùng tin. Trung vị ít thay đổi cũng không chứng minh từng nhãn hoặc giá trị đã đúng.

Tương quan Spearman được tính bằng tương quan Pearson trên thứ hạng, với thứ hạng trung bình cho các giá trị bằng nhau. Mã dùng rank rồi corr, nên không áp dụng công thức rút gọn giả định mọi thứ hạng phân biệt. Spearman phản ánh mối liên hệ đơn điệu, có thể hữu ích khi phân phối lệch; hệ số gần 0 không phủ nhận quan hệ phi tuyến hoặc các quan hệ tồn tại riêng trong từng nhóm. Đặc biệt, đơn giá u bằng P/A chứa diện tích ở mẫu số, nên tương quan A với u còn chịu ràng buộc toán học. Không diễn giải hệ số này thành tác động nhân quả của diện tích lên giá.

(3)

Khoảng bootstrap của trung vị địa phương được tạo bằng cách lấy lại mẫu có hoàn lại trong chính nhóm đang xét, tính trung vị cho mỗi mẫu rồi lấy các phân vị 2,5% và 97,5%. Mã sử dụng 500 lần lấy mẫu và seed cố định. Khoảng này mô tả biến động có điều kiện trên các tin đã thu được; nó không hiệu chỉnh thiên lệch chọn mẫu, không xác nhận mẫu đại diện và có thể đánh giá thấp bất định khi nhiều tin phụ thuộc cùng môi giới hoặc cùng tài sản. Vì thế, khoảng bootstrap đi kèm n và cảnh báo phạm vi khi biểu diễn chênh lệch địa phương [16].

(4)

NumPy cung cấp mảng số và phép toán vector cho phân cụm. Ma trận dữ liệu có n hàng và hai đặc trưng; broadcasting cho phép tạo khoảng cách giữa các điểm và tâm qua các trục mở rộng thay vì vòng lặp Python theo từng cặp. Mã bình phương hiệu, cộng theo chiều đặc trưng rồi chọn chỉ số khoảng cách nhỏ nhất. Cách tính này gắn trực tiếp với bài toán khoảng cách Euclid, nhưng bộ nhớ tăng theo số điểm, số tâm hoặc kích thước ma trận cặp. Silhouette vì vậy được tính trên tối đa 1.000 tin lấy mẫu, thay vì tạo ma trận khoảng cách cho toàn bộ mọi tin [8].

Hai đặc trưng phân cụm là log tự nhiên của diện tích và đơn giá. Log giảm chênh lệch quy mô; Z-score dùng trung bình và độ lệch chuẩn tổng thể của tập fit để co giãn hai biến. Tuy nhiên, log đơn giá bằng log tổng giá trừ log diện tích, nên diện tích tham gia cả hai đặc trưng. Cấu trúc cụm có thể chịu ảnh hưởng của quan hệ toán học này. So sánh với cặp log diện tích–log tổng giá là hướng kiểm tra độ nhạy; chưa phải thí nghiệm đã thực hiện trong lần chạy chính.

(5)

Trong Công thức 5, xᵢⱼ là giá trị dương của đặc trưng j ở tin i; μⱼ và σⱼ lần lượt là trung bình và độ lệch chuẩn tổng thể của ln(xᵢⱼ) trên tập fit. zᵢⱼ là giá trị đã co giãn, không còn đơn vị gốc. Nếu σⱼ bằng 0 thì đặc trưng không có biến thiên và phép chia không hợp lệ; mã từ chối trường hợp đó thay vì tạo vô hạn.

K-means tìm cách giảm tổng bình phương khoảng cách từ điểm đến tâm cụm theo Công thức 6. Thuật toán Lloyd luân phiên gán mỗi điểm vào tâm gần nhất và cập nhật tâm bằng trung bình các điểm của cụm. Quá trình hướng đến một nghiệm phụ thuộc khởi tạo, không bảo đảm cực tiểu toàn cục trong mọi trường hợp. Cụm phù hợp với cấu trúc gọn theo khoảng cách trong không gian biến đổi; chúng có thể không tương ứng với nhóm nghiệp vụ mà chuyên gia bất động sản quan tâm [5].

(6)

(7)

Trong Công thức 6 và 7, zᵢ là vector hai đặc trưng đã chuẩn hóa của tin i, Cⱼ là tập chỉ số thuộc cụm j, cⱼ là vector tâm cụm và k là số cụm. J là tổng bình phương khoảng cách, còn |Cⱼ| là số điểm của cụm. Ký hiệu cⱼ phân biệt tâm trong không gian phân cụm với μⱼ là trung bình log dùng để chuẩn hóa ở Công thức 5.

K-means++ chọn tâm đầu từ dữ liệu, sau đó ưu tiên điểm có bình phương khoảng cách lớn tới các tâm đã có [13]. Hiện thực trong đề tài dùng mười lần khởi tạo cho mỗi k và giữ mô hình có inertia thấp nhất, tối đa 150 vòng lặp. Điều kiện dừng dựa trên độ thay đổi tọa độ tâm nhỏ hơn 10⁻⁷; sau vòng lặp, nhãn và inertia được tính lại theo tâm cuối. Trường hợp cụm rỗng được xử lý bằng điểm xa nhất theo khoảng cách nhỏ nhất hiện tại. Những lựa chọn này là chi tiết hiện thực cần ghi rõ để người khác có thể chạy lại cùng quy trình.

Silhouette so sánh khoảng cách trung bình trong cụm aᵢ với khoảng cách trung bình tới cụm khác gần nhất bᵢ. Công thức 8 cho giá trị cao hơn khi điểm tương đối gần cụm của nó và xa cụm khác [14]. Các k từ 2 đến 5 được khảo sát với cùng quy trình; lựa chọn ưu tiên silhouette trung bình cao hơn, khi bằng nhau ưu tiên k nhỏ hơn. Đây là lựa chọn trong bốn phương án đã thử. Vì điểm số tính trên tập con, nó không được ghi thành đánh giá chính xác cho mọi điểm của toàn bộ tập fit.

(8)

Chỉ số Rand điều chỉnh, ARI, đo mức đồng thuận giữa hai phân hoạch của cùng các điểm và không phụ thuộc tên cụm [15]. Nhãn của seed chính được so với seed 7 và 42. ARI bằng 1 cho biết các phân hoạch trùng nhau trong phép thử này; chưa chứng minh ổn định khi đổi mẫu, đặc trưng hoặc chính sách ngoại lệ. Không có nhãn chuẩn bên ngoài nên ARI và silhouette không được gọi là độ chính xác nhận diện phân khúc thị trường.

SQLite là hệ quản trị nhúng lưu cơ sở dữ liệu trong một tệp và được gọi qua kết nối sqlite3 của Python. Bảng tỉnh và bảng loại giữ tên duy nhất, bảng listings tham chiếu chúng bằng khóa ngoại. PRIMARY KEY, UNIQUE, NOT NULL và CHECK biểu diễn các điều kiện có thể kiểm ngay khi ghi. Do SQLite dùng cơ chế kiểu linh hoạt trong các bảng hiện tại, khai báo REAL không thay cho toàn bộ kiểm dữ liệu đầu vào; quy trình còn chuyển kiểu và kiểm miền giá trị trước khi chèn. Hệ thống này phù hợp tra cứu cục bộ và minh họa quan hệ, chưa thiết kế cho nhiều người cùng cập nhật qua mạng [6], [11].

Khóa ngoại cần được bật trên từng kết nối có ghi bằng PRAGMA foreign_keys=ON; việc có câu khai báo REFERENCES trong lược đồ không nên bị hiểu thành mọi kết nối đều tự áp dụng cùng chế độ. Mã tạo database thực hiện bật kiểm tra, nạp dữ liệu bằng câu lệnh có tham số, commit và kiểm tra toàn vẹn. Giao dịch của SQLite giúp nhóm thao tác trong database có thể được xác nhận theo đơn vị ghi của nó; cơ chế đó khác với xuất bản nhiều tệp CSV, JSON, ảnh và Excel. Đối với các tệp này, hệ thống dùng vùng tạm và manifest chứ không có một giao dịch phân tán duy nhất.

Chỉ mục ghép được sắp theo thứ tự province_id, type_id, price_per_m2_vnd và row_id. Hai cột đầu phù hợp điều kiện bằng, cột đơn giá phù hợp truy vấn khoảng và thứ tự sắp, row_id phân giải trường hợp cùng đơn giá. EXPLAIN QUERY PLAN cho biết SQLite quét bảng hay tìm qua chỉ mục; ANALYZE cung cấp thống kê phục vụ lựa chọn kế hoạch. Chỉ mục hiện tại không chứa mọi cột trả về nên không được gọi là covering index cho truy vấn minh họa. Tác động đến thời gian còn phụ thuộc dữ liệu, cache và môi trường; cần kiểm cả kết quả bằng nhau lẫn phân bố thời gian, không suy ra tăng tốc chỉ từ việc thấy tên chỉ mục trong plan [7], [11].

Matplotlib tạo hình tĩnh từ các mảng và bảng đã xử lý. Histogram tổng giá được vẽ ở thang gốc và log để thấy phần đuôi; scatter dùng hai trục log vì giá và diện tích có khoảng biến thiên lớn. Biểu đồ cột địa phương kèm n và khoảng bootstrap, boxplot che các điểm ngoài râu trên hình nhưng không xóa chúng khỏi dữ liệu. Với khoảng giá không đều trong dashboard, chiều cao cột là số tin của từng khoảng, không được diễn giải như mật độ histogram có bề rộng bằng nhau. Đơn vị trục, tập lọc và số mẫu là một phần của ý nghĩa hình, không chỉ là trang trí [4], [10].

Dashboard sử dụng HTML cho cấu trúc, CSS cho bố cục và JavaScript cho trạng thái lựa chọn cùng tính toán. Dữ liệu công khai đã lược bỏ nội dung liên hệ được đóng vào HTML; các biểu đồ SVG và bảng được cập nhật từ tập lọc trong trình duyệt. Vì vậy, sau khi dựng, sản phẩm có thể mở ngoại tuyến mà không cần backend hoặc API bất động sản. Cách triển khai giảm phụ thuộc vận hành nhưng dữ liệu vẫn là snapshot và kích thước trang tăng theo số bản ghi; nó không phải một dịch vụ cập nhật thị trường trực tiếp.

Excel là kênh đọc và thao tác bảng bổ sung. Công thức đơn giá kiểm điều kiện đầu vào số dương trước phép chia; các cột phụ đổi đơn vị sang tỷ và triệu để tổng hợp. Công thức động có thể tính lại trong vùng workbook, còn cờ IQR, nhãn cụm và một số bảng là snapshot của pipeline. AutoFilter trong trang dữ liệu không mặc nhiên đổi KPI toàn workbook, vì các công thức tổng hợp không được xây dựng như mọi phép SUBTOTAL theo hàng hiển thị. Việc phân biệt này tránh kỳ vọng rằng chỉnh một ô hoặc ẩn một hàng đã làm toàn bộ quy trình phân tích chạy lại.

Cuối cùng, kiểm thử và truy nguyên là nền tảng để nối các công nghệ. Kiểm thử đơn vị kiểm quy tắc và tình huống biên; kiểm tích hợp so đầu ra giữa các định dạng; kiểm hash phát hiện sản phẩm khác phiên bản. Kiểm nội dung nguồn và kiểm bố cục giao diện có phạm vi riêng, không thể thay hoàn toàn bằng một mã thoát thành công. Chương 3 sử dụng các nguyên tắc trên để thiết kế các hợp đồng dữ liệu, còn Chương 5 báo cáo chính xác những lớp kiểm đã thực hiện và những lớp chưa được xác nhận.

Chương 3 Phân tích và thiết kế ứng dụng

Bài toán được phân tích từ chuỗi hoạt động của người sử dụng dữ liệu. Người vận hành cần tạo lại kết quả từ đúng nguồn và đọc được lý do loại một tin; người xem cần hiểu tập tin đang được phân tích, chọn địa phương hoặc loại hình và xuất bảng phục vụ diễn giải. Đây là hai cách sử dụng trong một quy trình cục bộ, không phải hai mức quyền được hiện thực bằng tài khoản. Thiết kế không bổ sung chức năng xác thực, duyệt giao dịch hay quản lý môi giới vì những chức năng đó không cần cho mục tiêu khám phá mẫu giá rao.

Yêu cầu chức năng đầu tiên là kiểm bản dữ liệu trước khi biến đổi, giữ raw bất biến và xác định được mỗi dòng đã đi đâu. Tiếp theo, hệ thống phải chuẩn hóa giá và diện tích, phát hiện trùng theo quy tắc, cách ly trường hợp chưa đủ cơ sở và tạo các biến số cần cho thống kê. Kết quả cần đọc được qua bảng, biểu đồ, SQLite, HTML và Excel. Khi dùng K-means hoặc minh họa truy vấn chỉ mục, mã thực thi và đầu ra phải tồn tại trong dự án, thay vì chỉ mô tả thuật toán ở phần lý thuyết.

Yêu cầu chất lượng tập trung vào tính nhất quán và khả năng giải thích. Các sản phẩm phải tham chiếu cùng run_id và nguồn; phép chia đơn giá phải khớp từng tin; số dòng trong lineage phải bảo toàn quy mô đầu vào. Khi thiếu nguồn hoặc hash không đúng, quy trình phải báo lỗi sớm. Khi một biểu đồ chỉ vẽ mẫu điểm cho nhẹ giao diện, chú thích phải phân biệt số điểm vẽ với số tin dùng tính KPI. Thông tin liên hệ và địa chỉ chi tiết không cần cho phân tích công khai nên không đưa vào các bảng xuất phục vụ xem kết quả.

Năm trường lõi được chọn gồm title, price, area, location và description. Title phục vụ nhận diện sơ bộ loại/giao dịch; price và area cung cấp đại lượng số; location cung cấp nhãn địa phương; description cung cấp ngữ cảnh kiểm nhất quán. Các trường chi tiết khác có dấu hiệu lặp không ăn khớp giữa bản ghi khác loại, nên không dùng số phòng, nội thất hoặc pháp lý để phân tích chính. Đây là quyết định giảm thuộc tính dựa trên chất lượng có thể quan sát, không phải kết luận đã xác minh phương pháp thu thập của tác giả nguồn.

Kiến trúc ở Hình 1 chia dữ liệu thành ba lớp logic: nguồn nguyên bản, dữ liệu đã chuẩn hóa có truy nguyên và sản phẩm phân tích. Các khối tương ứng với tệp/mô-đun cục bộ, không phải dịch vụ mạng độc lập. Ví dụ dòng nguồn 1 đi từ 100 m² và 2,38 tỷ sang 23,8 triệu VND/m² rồi xuất tới bảng sạch và database; dòng 638 đi vào tập cách ly do chưa giải quyết được cơ sở giá. Hai ví dụ ở Bảng 2 minh họa rằng đầu ra của chuẩn bị dữ liệu có nhiều nhánh, không phải mọi dòng đều bị ép thành số hợp lệ.

Hình 1: Sơ đồ luồng xử lý và các sản phẩm dữ liệu

Nguồn: thiết kế theo mã và dữ liệu dự án. Dữ liệu minh họa: 9.004 nguồn → 1.884 trùng + 209 cách ly + 6.911 giữ; dòng 1 tạo 23,8 triệu/m², dòng 638 cách ly.

Bảng 2: Dữ liệu minh họa hai nhánh giữ và cách ly

| Dòng nguồn | Dữ liệu quan sát | Đầu ra |
| --- | --- | --- |
| 1 | 100 m²; 2.380.000.000 VND | Giữ; 23.800.000 VND/m² |
| 638 | 143 m²; giá lõi 20 triệu; mô tả 20tr/m2 | Cách ly do cơ sở giá chưa rõ; không tự sửa |

Nguồn: raw, listings_clean.csv, listings_rejected.csv và row_lineage.csv; cùng run_id.

Từ điển biến được tóm tắt ở Bảng 3. CSV sạch có 18 cột, trong đó các biến dẫn xuất được xác định rõ nguồn và đơn vị. row_id giữ vị trí bản ghi trong mảng nguồn, bắt đầu từ 1. listing_id là tiền tố 20 ký tự của hash nội dung; toàn bộ hash được dùng trong bộ nhớ để phát hiện trùng, còn ID xuất ra được kiểm tính duy nhất trước khi nạp database. Các ID này không thay cho mã tài sản ngoài thực tế. Những cột cờ và bằng chứng cần được giữ ngay cả khi không hiển thị hết trên dashboard, vì chúng phục vụ giải thích quyết định xử lý.

Bảng 3: Từ điển 18 biến của dữ liệu sạch

| Biến | Kiểu và đơn vị | Ý nghĩa |
| --- | --- | --- |
| row_id | Số nguyên | Vị trí nguồn từ 1; khóa truy nguyên |
| listing_id | Chuỗi | Tiền tố hash nội dung; không phải ID tài sản |
| province | Chuỗi | Nhãn tỉnh xác định hoặc Chưa xác định |
| district | Chuỗi | Thành phần địa chỉ theo mẫu; không suy từ đường |
| property_type | Chuỗi | land / house / apartment / other_unknown |
| transaction_status | Chuỗi | sale / sale_assumed / sale_with_rental_income |
| area_m2 | Số, m² | Diện tích được đọc; không chứng thực đất hay sàn |
| sale_price_vnd | Số, VND | Giá rao tổng chuẩn hóa theo cơ sở giá |
| price_per_m2_vnd | Số, VND/m² | Giá tổng chia diện tích từng tin |
| price_basis | Chuỗi | total hoặc per_m2; giữ cơ sở quy đổi |
| area_source | Chuỗi | Trường diện tích hoặc phần ghi rõ trong chuỗi giá |
| source_review_evidence | JSON dạng chuỗi | Cụm số/chữ của quy tắc kiểm, không phải nhãn chuẩn |
| quality_flags | Chuỗi | Các cờ chất lượng, phân cách bằng dấu chấm phẩy |
| is_outlier_global | Boolean | Cờ IQR toàn mẫu |
| is_outlier_group | Boolean | Cờ IQR theo nhóm có dự phòng |
| iqr_group | Chuỗi | Nhóm tham chiếu dùng tính ngưỡng |
| cluster | Số nguyên | 1 hoặc 2; −1 cho tin ngoài tập fit |
| area_band | Chuỗi | Khoảng diện tích có biên xác định |

Nguồn: schema listings_clean.csv và src/pipeline.py. CSV giữ 6.911 tin.

Lineage được thiết kế là bảng có một dòng cho mỗi dòng nguồn. status nhận kept, rejected hoặc duplicate; canonical_row_id chỉ về dòng đại diện khi nội dung trùng; reasons mô tả lý do. Nhờ đó, phép đối soát số lượng được kiểm ở cấp dòng, không chỉ so tổng số tệp. Tập rejected giữ giá trị đã đọc cùng lý do cách ly để có thể xem lại mà không mất bằng chứng. Một tin có nhiều lý do không làm tăng số tin cách ly: số lượt lý do được thống kê riêng và có thể chồng nhau.

Hình 2 biểu diễn quan hệ ba bảng của SQLite. provinces có 48 hàng gồm 47 nhãn xác định và nhóm chưa rõ, property_types có bốn hàng, listings có 6.911 hàng. Quan hệ một–nhiều từ mỗi bảng danh mục tới listings giúp giữ một cách viết tên chuẩn cho mỗi khóa và hỗ trợ JOIN. Không cần tạo nhiều bảng nghiệp vụ chỉ để tăng kích thước lược đồ; số bảng phải xuất phát từ đối tượng mà ứng dụng thực sự lưu và truy vấn.

Hình 2: Sơ đồ quan hệ ba bảng trong SQLite

Nguồn: thiết kế theo mã và dữ liệu dự án. Dữ liệu minh họa: provinces 48 hàng, property_types 4 hàng, listings 6.911 hàng; ví dụ liên kết cụ thể tại Bảng 4.

Bảng 4: Bản ghi minh họa liên kết ba bảng

| Đối tượng | Khóa và tên | Dữ liệu minh họa |
| --- | --- | --- |
| provinces | province_id=44; Đà Nẵng | 48 hàng, gồm nhóm chưa rõ |
| property_types | type_id=3; land | 4 hàng nhãn suy luận |
| listings | row_id=1; tham chiếu hai khóa trên | 100 m²; 2,38 tỷ; 23,8 triệu/m² |

Nguồn: truy vấn chỉ đọc outputs/real_estate.sqlite; lược đồ sql/01_schema.sql.

Trong listings, row_id là INTEGER PRIMARY KEY; listing_id có NOT NULL và UNIQUE; province_id và type_id là khóa ngoại. Diện tích phải lớn hơn 0, tổng giá tối thiểu 10 triệu VND, đơn giá dương, cờ IQR chỉ nhận 0 hoặc 1. Ràng buộc kiểm tổng giá xấp xỉ diện tích nhân đơn giá dùng sai số số thực nhỏ. Các điều kiện này bảo vệ tính hợp lệ tính toán và chính sách chấp nhận, chưa kiểm được giá thật, pháp lý hoặc tính nhất quán đầy đủ của ngôn ngữ quảng cáo. Ví dụ, một tổng giá sai nhưng vẫn dương có thể vượt ràng buộc database nếu không được phát hiện trước đó.

Thiết kế phân tích giữ riêng ba quần thể sử dụng. Quần thể mặc định gồm 6.911 tin đã qua chính sách; quần thể không có cờ IQR nhóm gồm 6.652 tin và được dùng fit phân cụm; các quần thể độ nhạy được tạo theo từng điều kiện minh bạch. Nhóm phân cụm được lưu dưới nhãn 1 và 2, còn −1 chỉ những tin ngoài tập fit. Lọc dashboard chỉ chọn lại các bản ghi có sẵn và tính lại thống kê hiển thị, không fit lại K-means hoặc cập nhật scaler theo mỗi tổ hợp lựa chọn.

Thiết kế dashboard có ba bộ chọn chính: tỉnh, loại suy luận và phạm vi giao dịch, kèm tùy chọn bỏ cờ IQR nhóm và nút đặt lại. KPI cùng biểu đồ dùng tập lọc cấp trang. Ô tìm kiếm trong bảng áp dụng thêm điều kiện cho bảng và CSV, không thay KPI toàn trang; phân trang chỉ giới hạn dòng đang hiển thị, còn xuất CSV chứa toàn bộ bảng đã lọc/tìm. Trạng thái không có dữ liệu cần hiện n bằng 0 và thông báo phù hợp, tránh để KPI của lần chọn trước khiến người đọc nhầm có kết quả.

Thiết kế Excel có ba trang Dashboard, Du lieu và Chat luong; trang dữ liệu có 19 cột vì chứa các cột quy đổi và diện tích hợp lệ phục vụ công thức, đồng thời không đưa mọi cột CSV sang nguyên trạng. Các biểu đồ và công thức dựa trên vùng dữ liệu được tạo cho lần chạy đó. HTML và Excel là hai giao diện cho cùng nền dữ liệu nhưng không có mọi tương tác đồng nhất: HTML lọc và tính thống kê bằng JavaScript; Excel dùng bảng và công thức theo vùng đã thiết kế. Bởi vậy, nghiệm thu cần so ngữ nghĩa chỉ tiêu, không chỉ so hình thức hoặc tên nhãn.

Hợp đồng phiên bản gắn nguồn, mã lõi và đầu ra qua run_manifest.json. Dashboard và workbook có metadata dẫn xuất riêng, chứa core_run_id, hash sản phẩm và hash mã dựng. Khi một sản phẩm không khớp, verifier phải báo khác phiên bản; dashboard cũng không quảng bá workbook cũ như một bản cùng dữ liệu. Cách tổ chức này giảm nguy cơ dùng ảnh hoặc Excel của một lần chạy cũ để minh họa cho số liệu mới. Tuy nhiên, đây là hợp đồng kiểm tính nhất quán, không thay thế việc đánh giá nội dung tin và không biến toàn bộ quá trình xuất tệp thành một giao dịch nguyên tử.

Thiết kế trên dẫn tới tiêu chí nghiệm thu có thể đo: bảo toàn 9.004 dòng trong lineage; mọi tin sạch có giá/diện tích hợp lệ theo chính sách; CSV, JSON, database và workbook cùng giá trị; các bộ lọc trả n tương ứng; truy vấn trước/sau chỉ mục có cùng kết quả; tài liệu giải thích được giới hạn. Chương 4 mô tả cách chuyển các yêu cầu này thành hàm và tệp thực thi, còn Chương 5 dùng kết quả lưu của cùng lần chạy để đánh giá mức đáp ứng.

Chương 4 Hiện thực hệ thống

Hệ thống được hiện thực trong kho mã KHDL-BatDongSan với các thư mục scripts, src, data, sql, tools, tests và outputs [17]. scripts điều khiển tải và chạy; src chứa quy tắc lõi; tools dựng sản phẩm và đối soát; outputs lưu kết quả cùng phiên bản. Cách chia này tách mã xử lý khỏi sản phẩm sinh ra và cho phép kiểm một bước riêng khi cần chẩn đoán. Bảng 5 liên kết những mô-đun chính với đầu vào và đầu ra; các đoạn mã ngắn trong chương được trích từ hiện thực, còn toàn bộ mã được cung cấp trong kho dự án.

Bảng 5: Liên kết mô-đun với đầu vào và đầu ra

| Mô-đun | Đầu vào | Đầu ra |
| --- | --- | --- |
| download_data.py | URL pin và manifest nguồn | JSON nguyên bản, metadata |
| pipeline.py / source_checks.py | Năm trường lõi của raw | CSV/JSON sạch, rejected, lineage, bảng/hình/DB |
| artifact_contract.py | Nguồn, mã, manifest và sản phẩm | Xác nhận phiên bản hoặc lỗi |
| build_dashboard.py / template | CSV sạch và manifest | HTML có dữ liệu nhúng, metadata dựng |
| build_workbook.mjs | Dữ liệu sạch và analysis | Excel ba trang/bốn hình, metadata/kiểm tính lại |
| demo_sql.py | SQLite và bốn SQL | Kết quả truy vấn chỉ đọc |
| verify_delivery.py | Các sản phẩm cùng phiên bản | Kết quả đối soát hoặc lỗi |
| run_project.py | Cấu hình chạy và nguồn | Điều phối toàn bộ phần được chọn |

Nguồn: mã nguồn trong src, scripts và tools tại phiên bản phân tích [17].

Mô-đun tải scripts/download_data.py sử dụng URL của bản dữ liệu được ghim, lưu metadata và manifest để kiểm chứng. Khi nguồn cục bộ đã có checksum đúng, không cần tải lại để phân tích ngoại tuyến. Trước pipeline, read_verified_source trong src/artifact_contract.py kiểm SHA-256, cấu trúc mảng và số lượng 9.004 đối tượng. Nếu thiếu hoặc khác bản nguồn, chương trình dừng với thông báo. Bước này ngăn tình huống một tệp sửa riêng vẫn được gắn tên và DOI của bộ dữ liệu công bố; nó không xác thực nội dung kinh tế của từng quảng cáo.

Trong src/pipeline.py, normalize tạo chuỗi so khớp; parse_number đọc cấu trúc dấu số và từ chối biểu thức không rõ; parse_area tìm một diện tích có đơn vị và xử lý dấu gạch đầu chuỗi nguồn như ký tự phân cách. Những chuỗi là khoảng diện tích không bị ép thành một điểm. Khi trường area chưa đọc được nhưng chuỗi price có phần diện tích ghi rõ, clean_records có thể khôi phục từ phần đó và ghi area_source cùng cờ. Với 347 tin giữ được khôi phục theo cách này, giá trị không được nội suy từ tin khác hoặc từ mô hình dự đoán.

parse_price tách phần diện tích có nhãn khỏi chuỗi giá rồi đọc số tiền và đơn vị. Giá ghép như 1 tỷ 200 triệu chỉ được cộng khi các thành phần không âm và đơn vị giảm dần; đơn vị lặp hoặc phần dư chưa giải thích được làm chuỗi không hợp lệ. Với giá ghi rõ trên m², tổng được suy ra khi diện tích dương có sẵn và price_basis lưu cơ sở đó. Sau chuẩn hóa, dòng 1 tạo 2.380.000.000 VND và 100 m², nên đơn giá bằng 23.800.000 VND/m². Đây là ví dụ của phép biến đổi có thể kiểm lại bằng số gốc, không phải một giá được hệ thống định giá lại.

Gộp trùng thực hiện trên hash của danh sách năm trường đã normalize. Bộ nhớ fingerprints giữ dòng đầu gặp làm canonical_row_id; các dòng có cùng khóa được ghi duplicate trong lineage và không xử lý như quan sát độc lập mới. Quy tắc này khác việc so toàn bộ JSON: một số trường chi tiết có thể khác dù nội dung lõi giống nhau. Ngược lại, thay một phần mô tả có thể làm cùng tài sản không được gộp. Do thiếu mã tin ổn định và thông tin giao dịch, báo cáo chỉ kết luận về trùng nội dung theo khóa đã chọn.

classify_title nhận diện loại hình và giao dịch bằng các mẫu từ khóa có thứ tự ưu tiên. Một số cụm tên riêng hoặc ngữ cảnh như Nhà Bè, Nha Trang hay nhà đầu tư được loại khỏi những cách khớp dễ nhầm. Căn hộ, nhà và đất được nhận theo mẫu; phần còn lại thành other_unknown. Tin có tín hiệu thuê/bán lẫn nhau được xử lý khác với tin bán có nhắc thu nhập cho thuê. Khi không có tín hiệu bán rõ nhưng ngữ cảnh nguồn phù hợp, sale_assumed được giữ cùng cờ. Các điều kiện này giải thích được bằng mã nhưng vẫn phụ thuộc cách diễn đạt của người đăng, đặc biệt lỗi chính tả và viết tắt.

src/source_checks.py bổ sung đối chiếu chéo giá, đơn vị, diện tích và ngữ cảnh thanh toán. Hàm check_source_consistency trả về lý do, cờ và các cụm số/chữ tối thiểu; nó không trả một giá đúng để thay nguồn. Dòng 638 có tổng giá đọc được 20 triệu nhưng mô tả ghi 20tr/m2, nên nhận unresolved_price_basis_from_source_text. Dòng 335 có diện tích lõi 2 m² nhưng tiêu đề 2 ha, nên đi vào cách ly. Những từ như sào, công phụ thuộc quy ước địa phương được giữ là bất định khi không đủ cơ sở đổi đơn vị.

Các quy tắc kiểm chéo chỉ phát hiện một số mâu thuẫn số học và ngữ cảnh; ngưỡng chênh ít nhất năm lần không bắt mọi sai khác nhỏ. Dòng 5093 có 9,7 tỷ ở trường giá nhưng 9,9 tỷ trong mô tả. Dòng 8151 có 18.000 m² ở trường lõi và 180.000 m² trong mô tả; dòng 8535 có 6 m² ở trường lõi nhưng mô tả nêu 55/60 m². Những tin này vẫn ở tập EDA. Dòng 8535 được gắn cờ IQR và không tham gia fit cụm, nhưng cờ thống kê không giải quyết được diện tích nào đúng. Cần bổ sung trạng thái cần rà soát cho mâu thuẫn chưa giải quyết, giữ bằng chứng và tránh tự sửa số theo cảm giác.

Sau clean_records, hệ thống xuất ba bảng về tin giữ, tin cách ly và lineage. add_outlier_flags tính Q1/Q3 và hàng rào theo nhóm có cơ chế dự phòng như thiết kế. summarize_groups tính n, trung vị, tứ phân vị và tỷ lệ cờ; bootstrap chỉ được dùng ở những bảng thực sự cần khoảng biến động của trung vị. sensitivity_table tạo các phương án trên cùng dữ liệu đã qua chính sách. Các bảng CSV được ghi với UTF-8 có BOM để thuận tiện mở trong Excel; JSON giữ Unicode và biểu diễn số phục vụ ứng dụng. Sai khác làm tròn khi xuất bảng được tách khỏi phép tính nội bộ.

cluster_records chọn các tin không có cờ IQR nhóm, log hai biến và chuẩn hóa bằng trung bình/độ lệch chuẩn của chính tập đó. Hàm kmeans triển khai K-means++ và Lloyd bằng NumPy; dòng tính khoảng cách, gán nhãn và cập nhật tâm thể hiện trực tiếp việc dùng giải thuật để tạo kết quả. Đoạn mã ở dưới minh họa phần gán và cập nhật tâm, không thay thế toàn bộ các kiểm đầu vào, khởi tạo và chọn mô hình trong tệp nguồn.

distances = ((x[:, None, :] - centers[None, :, :]) ** 2).sum(axis=2)

labels = distances.argmin(axis=1)

updated = np.array([

x[labels == j].mean(axis=0) if np.any(labels == j)

else x[np.argmax(distances.min(axis=1))]

for j in range(k)

])

Nguồn: mã thực thi trong src/pipeline.py; chỉ ngắt dòng để trình bày. SQL đầy đủ ở sql/02_queries.sql.

Các mô hình k từ 2 đến 5 được đánh giá bằng sampled_silhouette. Kết quả ưu tiên điểm silhouette cao nhất; nếu bằng nhau ưu tiên k nhỏ. Nhãn được sắp lại theo tâm đơn giá rồi diện tích để cách trình bày ổn định, không làm thay đổi phân hoạch. Hai seed bổ sung được so bằng adjusted_rand_index. Cuối cùng, cụm chỉ được gán cho các tin thuộc tập fit, những tin còn lại mang giá trị −1. Cấu trúc này cho phép dashboard giữ thông tin cụm của pipeline trong khi lựa chọn lọc có thể thay đổi.

build_database tạo lược đồ bằng SQL, ánh xạ tên tỉnh và loại sang khóa danh mục rồi nạp listings bằng executemany với tham số. Bảng listings lưu 11 cột cần cho truy vấn, khác 18 cột của CSV sạch. Hàm thực hiện ANALYZE, chọn một cặp tỉnh–loại nhiều tin và dùng khoảng phân vị 35%–65% của đơn giá để tạo tham số benchmark. Trước và sau khi tạo index, cùng câu SELECT được chạy, lấy plan, hash kết quả và đo nhiều lần. Nếu hash hai kết quả khác nhau, chương trình từ chối công bố kết quả của lần dựng đó.

SELECT row_id, area_m2, sale_price_vnd, price_per_m2_vnd

FROM listings

WHERE province_id = ? AND type_id = ?

AND price_per_m2_vnd BETWEEN ? AND ?

ORDER BY price_per_m2_vnd, row_id LIMIT 100;

Nguồn: mã thực thi trong src/pipeline.py; chỉ ngắt dòng để trình bày. SQL đầy đủ ở sql/02_queries.sql.

Đối với truy vấn này, idx_listings_search hỗ trợ phần lọc tỉnh/loại và khoảng đơn giá, đồng thời thứ tự đơn giá–row_id cho kết quả xác định khi có giá bằng nhau. Giá trị diện tích và tổng giá vẫn cần đọc từ bảng. SQL minh họa khác tổng hợp theo tỉnh, theo loại trong TP.HCM và liệt kê các tin có cờ ngoại lệ. AVG trong các truy vấn đó được gọi là trung bình, không gắn nhãn trung vị. scripts/demo_sql.py mở database ở chế độ chỉ đọc, thực thi bốn câu lệnh rồi in kết quả và PRAGMA integrity_check.

tools/build_dashboard.py kiểm manifest trước khi đọc CSV, chọn mười trường cần cho giao diện rồi chuyển các cột số và boolean về đúng kiểu. JSON nhúng được thay ký tự mở thẻ thành biểu diễn Unicode escape để không tạo chuỗi kết thúc thẻ ngoài ý muốn. src/dashboard_template.html cung cấp hàm lọc, tính median, dựng SVG, phân trang và xuất CSV. Mẫu scatter được giảm điểm để giữ trang nhẹ, còn thống kê dùng toàn bộ tập lọc. Liên kết mở Excel chỉ được cung cấp như bản cùng dữ liệu khi metadata workbook đã vượt kiểm phiên bản.

tools/build_workbook.mjs dùng runtime Node và Artifact Tool để tạo ba trang cùng bốn biểu đồ. Tại dòng dữ liệu đầu tiên, công thức đơn giá yêu cầu H và G là số dương rồi mới lấy H/G; cột Q đổi tổng giá sang tỷ, R đổi đơn giá sang triệu và S giữ diện tích hợp lệ. Các trường hợp giá/diện tích trống, 0 hoặc văn bản được thử riêng trên bản kiểm. Cờ IQR và cụm là kết quả phân tích có sẵn, không phải công thức huấn luyện lại trong Excel. Việc tạo chính xác workbook này phụ thuộc gói ngoài requirements Python, nên khả năng mở file có sẵn được phân biệt với khả năng dựng lại file trên một môi trường mới.

Quy trình xuất bản sản phẩm trong main dựng phần lõi ở một thư mục staging dưới tmp. Khi tạo thành công, từng tệp được chuyển sang vị trí đích, sau đó run_manifest.json được thay cuối cùng. Thiết kế này tránh công bố một bộ phân tích chưa dựng xong, nhưng bước chuyển nhiều tệp không phải nguyên tử toàn bộ: lỗi giữa chừng có thể để lại hỗn hợp tệp. Manifest và verifier phát hiện trạng thái không đồng nhất đó trước khi dùng để khẳng định một phiên bản hoàn tất. Dashboard và workbook được dựng/kiểm như sản phẩm dẫn xuất có metadata riêng.

scripts/run_project.py điều phối tải/kiểm nguồn, pipeline, dựng HTML, kiểm thử, SQL và verifier. Tùy chọn --workbook yêu cầu dựng thêm Excel; --skip-download dùng nguồn cục bộ đã đúng checksum, không bỏ kiểm nguồn; --skip-tests không được diễn giải thành đã kiểm thử đạt. Bộ test Python bao quát các quy tắc phân tích và hợp đồng đầu ra, trong khi test JavaScript chạy mã thật trên DOM tối giản để kiểm các trạng thái và CSV. Cách tách lớp kiểm này cho phép ghi chính xác phần đã chạy bằng máy và phần bố cục trình duyệt hoặc Excel thật còn cần xác nhận.

tools/verify_delivery.py kiểm lại nguồn và manifest, đối soát từng bản ghi giữa CSV/JSON/database, kiểm phép chia và lineage, rồi kiểm sản phẩm dẫn xuất. Chế độ --require-workbook còn đọc đủ các dòng và KPI Excel, đối chiếu metadata cùng bằng chứng tính lại. tools/prepare_handover_evidence.py bổ sung phép tính trung vị bằng csv/statistics và SQLite ORDER BY, chạy lại bốn truy vấn chỉ đọc và tạo hồ sơ rà soát. Bộ bổ sung được ghim theo mốc dữ liệu, tránh chuyển một nhận xét nội dung cũ thành kết quả kiểm cho lần chạy khác.

Chương 5 Vận hành và kết quả thực nghiệm

Các kết quả chính dùng lần chạy 20261027T065401Z-5c8df2cc: Python 3.12.3, NumPy 2.3.3, pandas 2.3.3, Matplotlib 3.10.6, SQLite 3.45.1. Dữ liệu sạch gồm 6.911 tin. Script complete_analysis.py đối chiếu nhãn và chạy phân tích mở rộng mà không thay quy tắc đã khóa. Ngày nguồn công bố vẫn là 12/01/2021; không diễn giải thành thị trường hiện tại.

Để vận hành phần cốt lõi từ bản clone, người dùng tạo môi trường Python phù hợp, cài requirements và chạy scripts/run_project.py. Lệnh mặc định tải hoặc kiểm nguồn trước pipeline; sau đó tạo dữ liệu, database, hình và HTML rồi thực thi các bước kiểm. Nếu chỉ cần xem kết quả đã tạo, có thể mở outputs/DASHBOARD_BAT_DONG_SAN.html bằng trình duyệt hoặc workbook bằng Excel mà không chạy lại thuật toán. Bảng 6 ghi lệnh cùng phạm vi của từng thao tác, tránh nhầm việc xem một file có sẵn với tái tạo thành công cả hệ thống.

Bảng 6: Lệnh vận hành và phạm vi tạo kết quả

| Lệnh từ thư mục repo | Phạm vi |
| --- | --- |
| python scripts/run_project.py | Tải/kiểm nguồn, chạy lõi, dựng HTML, test/SQL/verifier; Excel không tự dựng mặc định |
| python scripts/run_project.py --skip-download | Dùng raw có sẵn, vẫn kiểm checksum |
| python scripts/run_project.py --workbook | Thêm bước dựng Excel; cần Node và Artifact Tool |
| python tools/verify_delivery.py --require-workbook | Đối soát sản phẩm lưu gồm Excel, không chạy lại phân tích |
| python scripts/demo_sql.py | Bốn truy vấn đọc và kiểm toàn vẹn |
| MO_DASHBOARD.cmd | Mở HTML có sẵn trong trình duyệt |

Nguồn: scripts/run_project.py và README. Dùng Python trong môi trường đã cài requirements.

Đối soát bảo toàn 9.004 dòng: 1.884 dòng trùng, 209 dòng cách ly và 6.911 tin giữ. Có 459 chuỗi diện tích nguồn chưa đọc được ban đầu; 347 tin giữ được khôi phục từ chuỗi giá. Trong tập giữ có 3.864 tin sale_assumed (55,91%), 3.032 tin bán rõ và 15 tin có thu nhập thuê. Các lý do cách ly có thể trùng trên một dòng nên không cộng lượt lý do thành số tin.

Bảng 7: Đối soát quy mô dữ liệu trước và sau xử lý

| Trạng thái | Số dòng | Ý nghĩa |
| --- | --- | --- |
| Nguồn | 9.004 | Mảng JSON công bố v2 |
| Trùng | 1.884 | Trùng theo năm trường lõi |
| Cách ly | 209 | Chưa đáp ứng chính sách |
| Giữ | 6.911 | Tập EDA mặc định |
| Ngoại lệ IQR nhóm | 259 | Vẫn thuộc tập giữ |
| Fit K-means | 6.652 | Tập giữ sau loại cờ IQR nhóm |

Nguồn: outputs/analysis.json, counts và clustering; đơn vị dòng/tin.

Khả năng truy nguyên được minh họa bằng hai dòng đã sử dụng trong thiết kế. Dòng 1 được giữ với 100 m², tổng giá 2,38 tỷ và đơn giá 23,8 triệu/m². Dòng 638 có 143 m², giá lõi 20 triệu và mô tả 20tr/m2, nên chuyển vào rejected thay vì tự sửa thành một tổng giá suy đoán. Các ví dụ bổ sung như 7811 có 860 tỷ so với 860 triệu, hoặc 335 có 2 m² so với 2 ha, cho thấy kiểm chéo nguồn có vai trò trước thống kê. Đồng thời, các khác biệt nhỏ, mô tả nhiều lô hoặc viết tắt vẫn có thể vượt qua bộ quy tắc, nên tập giữ chỉ được coi là hợp lệ theo chính sách đã nêu.

Tổng hợp chính cho thấy trung vị diện tích là 70 m², trung vị tổng giá 2,25 tỷ VND và trung vị đơn giá khoảng 32,5000 triệu VND/m². Trung bình tổng giá khoảng 3,7042 tỷ, cao hơn trung vị, phù hợp với phần đuôi giá cao. Bảng 8 cung cấp các phân vị để việc đọc hình không chỉ dựa vào cảm giác. Hình 3 đặt histogram tổng giá ở thang gốc cạnh thang log, giúp quan sát cả phần đuôi và khu vực tập trung. Hai histogram dùng cùng 6.911 tin, không phải hai mẫu trước và sau loại ngoại lệ.

Bảng 8: Thống kê minh họa phân bố giá và diện tích

| Chỉ tiêu | Diện tích m² | Giá tổng tỷ VND | Đơn giá triệu VND/m² |
| --- | --- | --- | --- |
| Số tin | 6.911 | 6.911 | 6.911 |
| Trung bình | 796,54 | 3,7042 | 49,6666 |
| Q1 | 48,00 | 1,1500 | 12,5409 |
| Trung vị | 70,00 | 2,2500 | 32,5000 |
| Q3 | 108,00 | 4,3000 | 73,3333 |
| Lớn nhất | 767.000,00 | 100,0000 | 833,3333 |

Nguồn: descriptive_statistics.csv; hàng số tin ở ba cột đều 6.911, không áp dụng quy đổi đơn vị.

Hình 3: Phân bố tổng giá rao ở thang gốc và thang log

Nguồn: xử lý từ Mendeley v2 [1], cùng run_id. n=6.911; tổng giá theo tỷ VND, log10(giá/tỷ VND); lần lượt 50 và 35 khoảng. Số liệu minh họa tại Bảng 8.

Hình 4 biểu diễn diện tích và tổng giá trên hai trục log, với màu theo loại suy luận. Các dòng minh họa tại Bảng 9 có thể kiểm lại trong CSV sạch. Dải giá và diện tích rộng làm các quan sát chồng lên nhau; vì vậy mật độ nhìn thấy trong một vùng không được hiểu như tỷ trọng thị trường. Scatter tĩnh vẽ toàn bộ tập giữ, trong khi dashboard có thể lấy mẫu điểm để hiển thị nhẹ và ghi riêng số điểm được vẽ.

Hình 4: Mối liên hệ giữa diện tích và tổng giá rao

Nguồn: xử lý từ Mendeley v2 [1], cùng run_id. n=6.911, hai trục log; diện tích m² và tổng giá tỷ VND, màu theo loại suy luận. Ví dụ tại Bảng 9.

Bảng 9: Một số tin minh họa cho biểu đồ diện tích và giá

| Dòng | Loại suy luận | Diện tích m² | Giá tổng tỷ VND |
| --- | --- | --- | --- |
| 1 | land | 100,00 | 2,3800 |
| 2 | house | 79,00 | 18,0000 |
| 3 | land | 500,00 | 1,0000 |
| 4 | house | 60,00 | 0,5250 |
| 5 | land | 150,00 | 0,4400 |

Nguồn: listings_clean.csv; các dòng minh họa thuộc hình scatter toàn bộ 6.911 tin.

Spearman diện tích–tổng giá toàn mẫu là -0,037440, nhưng đạt 0,609864 ở căn hộ, 0,232733 ở nhà và 0,021633 ở đất. Nhà tại Hà Nội đạt 0,6427, nhà tại TP.HCM đạt 0,3334. Các quan hệ thay đổi theo thành phần nhóm, hỗ trợ phân tích có điều kiện; chưa chứng minh tác động nhân quả.

Hình 5: Ma trận tương quan Spearman của ba biến phân tích

Nguồn: xử lý từ Mendeley v2 [1], cùng run_id. n=6.911; hệ số không có đơn vị, tính từ thứ hạng. Bảng 10 nêu các cặp biến, không diễn giải nhân quả.

Bảng 10: Hệ số Spearman giữa các biến phân tích

| Cặp biến | Hệ số | Phạm vi diễn giải |
| --- | --- | --- |
| Diện tích – tổng giá | -0,037440 | Mối liên hệ đơn điệu tổng thể trong mẫu |
| Diện tích – đơn giá | -0,588740 | Có liên hệ toán học qua mẫu số diện tích |
| Tổng giá – đơn giá | 0,768038 | Có biến giá chung trong tử số |
| Diện tích – tổng giá (căn hộ) | 0,609864 | n=366; tương quan trong nhóm suy luận |
| Diện tích – tổng giá (nhà) | 0,232733 | n=3.624; tương quan trong nhóm suy luận |
| Diện tích – tổng giá (đất) | 0,021633 | n=1.855; tương quan trong nhóm suy luận |
| Diện tích – tổng giá (nhà, Hà Nội) | 0,642744 | n=623; tương quan trong nhóm suy luận |
| Diện tích – tổng giá (nhà, TP.HCM) | 0,333439 | n=2.105; tương quan trong nhóm suy luận |

Nguồn: analysis.json cho ba cặp toàn mẫu; tính bổ sung từ listings_clean.csv cho các nhóm. Dùng thứ hạng trung bình khi bằng nhau, rồi tính tương quan Pearson; không diễn giải nhân quả. Hình 5 chỉ biểu diễn ba biến của toàn mẫu.

TP.HCM và Hà Nội chiếm 61,93% tập giữ. Hình 6 chọn mười địa phương nhiều tin nhất (n≥30), rồi sắp theo trung vị; Bảng 11 ghi số liệu.

Hình 6: Trung vị đơn giá của mười địa phương có nhiều tin nhất

Nguồn: xử lý từ Mendeley v2 [1], cùng run_id. Chọn theo n, chỉ nhóm n≥30; đơn vị triệu VND/m²; bootstrap 95% có điều kiện, 500 lần. Bảng 11 kèm toàn bộ số liệu hình.

Bảng 11: Dữ liệu mười địa phương có nhiều tin nhất trong hình

| Địa phương | n | Trung vị triệu VND/m² | Bootstrap 95% triệu VND/m² |
| --- | --- | --- | --- |
| Tp Hồ Chí Minh | 3.266 | 45,45 | 43,22 – 47,90 |
| Hà Nội | 1.014 | 77,12 | 74,08 – 80,26 |
| Bình Dương | 457 | 13,00 | 11,19 – 14,81 |
| Đà Nẵng | 455 | 42,86 | 38,52 – 47,00 |
| Đồng Nai | 249 | 7,13 | 4,51 – 8,33 |
| Long An | 238 | 8,68 | 7,92 – 9,88 |
| Cần Thơ | 225 | 26,88 | 23,32 – 30,00 |
| Đắk Lắk | 126 | 10,39 | 8,66 – 12,83 |
| Lâm Đồng | 106 | 3,00 | 2,54 – 3,65 |
| Bà Rịa - Vũng Tàu | 77 | 4,64 | 4,00 – 5,50 |

Nguồn: analysis.json, province_summary. Chọn theo số tin; khoảng bootstrap có điều kiện, 500 lần.

Hà Nội có trung vị đơn giá 77,12 triệu/m², TP.HCM 45,45 và Đà Nẵng 42,86. Phân tích bổ sung tạo 405 nhóm tỉnh × loại × khoảng diện tích; 41 nhóm biết tỉnh/loại có n≥30, bao phủ 4.594 tin. Bảng mở rộng báo trung vị, Q1–Q3 và độ nhạy khi bỏ IQR nhóm. Cách tách này giảm khác biệt cơ cấu nhưng chưa kiểm soát chất lượng nhà hay vị trí xác minh.

Số lượng và trung vị theo loại hình được trình bày ở Bảng 12, tính từ nhãn suy luận của lần chạy mới. Có 1.066 tin other_unknown, không được hiểu là đã nhận diện đúng một loại tài sản khác. Đối chiếu nhãn tham chiếu có 43/58 trường loại hình xác định khớp; kết quả chịu giới hạn mẫu phân tầng và nhãn đã hiệu chỉnh bằng AI, không suy thành accuracy toàn bộ nguồn.

Bảng 12: Thống kê theo loại hình suy luận từ tiêu đề

| Loại suy luận | n | Diện tích trung vị m² | Đơn giá trung vị triệu/m² |
| --- | --- | --- | --- |
| Nhà | 3.624 | 56,00 | 56,0000 |
| Đất | 1.855 | 117,00 | 8,5100 |
| Chưa xác định | 1.066 | 75,00 | 40,0000 |
| Căn hộ | 366 | 60,00 | 27,8312 |

Nguồn: analysis.json, type_summary; nhãn chưa có kiểm định bằng bộ nhãn chuẩn.

Bỏ IQR nhóm còn 6.652 tin, trung vị đơn giá thay đổi -4,62%; chỉ giữ bán rõ còn 3.032 tin, thay đổi 1,77%. Bỏ 326 tin có cờ dấu chấm hàng nghìn còn 6.585 tin, thay đổi 8,88%. Đây là độ nhạy theo thành phần mẫu, chưa tách riêng tác động lỗi đọc số.

Hình 7: Đối soát làm sạch và độ nhạy theo lựa chọn xử lý

Nguồn: xử lý từ Mendeley v2 [1], cùng run_id. Phần trái đơn vị dòng/tin; phần phải trung vị triệu VND/m². Số liệu tương ứng ở Bảng 7 và Bảng 13.

Bảng 13: Độ nhạy của trung vị đơn giá theo lựa chọn xử lý

| Phương án | n | Trung vị triệu/m² | Thay đổi % |
| --- | --- | --- | --- |
| Toàn bộ tin giữ | 6.911 | 32,5000 | 0,00 |
| Bỏ IQR toàn cục | 6.681 | 30,9091 | -4,90 |
| Bỏ IQR nhóm | 6.652 | 31,0000 | -4,62 |
| Bỏ dấu chấm nghìn | 6.585 | 35,3846 | 8,88 |
| Tiêu đề bán rõ | 3.032 | 33,0747 | 1,77 |

Nguồn: analysis.json, sensitivity; so với toàn bộ 6.911 tin giữ. Các phương án khác nhau về thành phần mẫu.

Đợt kiểm mới dùng 60 ID đánh giá đã khóa riêng với 120 tin phát triển. Một thành viên gán nhãn ban đầu; AI hiệu chỉnh 17 tin theo yêu cầu nhóm, chưa ghi nhận thành viên xác nhận lại toàn bộ sửa đổi. Có 7 usable, 1 exclude và 52 review; 8/8 quyết định đã xác định khớp chương trình nhưng chỉ bao phủ 13,33% mẫu. Không gọi đây là độ chính xác 100%. Các trường unknown hoặc số trống được tách khỏi mẫu số từng chỉ tiêu; kết quả theo ba tầng nằm ở outputs/extended/evaluation_metrics.csv.

K-means fit 6.652 tin không có cờ IQR nhóm. Với k=2–5, k=2 đạt silhouette 0,5934 trên mẫu tối đa 1.000 tin, cao nhất trong lần thử chính. Seed 7 và 42 cho ARI=1 so với lần chạy chính. Kiểm bổ sung dùng 5 cấu hình × 4 giá trị k × 3 seed và 5 mẫu con 80%, tổng cộng 65 lần fit. Silhouette của phần bổ sung dùng mẫu tối đa 500 tin, nên không đồng nhất trực tiếp với điểm ở Bảng 14.

Hình 8: Phân nhóm K-means và khảo sát số cụm

Nguồn: xử lý từ Mendeley v2 [1], cùng run_id. Fit 6.652 tin; diện tích m², đơn giá triệu VND/m² trên trục log; silhouette lấy mẫu tối đa 1.000 tin. Dữ liệu tại Bảng 14 và Bảng 15.

Bảng 14: Khảo sát số cụm trên cùng tập fit

| k | Silhouette mẫu | Inertia | Cụm nhỏ nhất |
| --- | --- | --- | --- |
| 2 | 0,5934 | 6.247,9643 | 989 |
| 3 | 0,4629 | 3.842,1813 | 455 |
| 4 | 0,3977 | 2.975,5686 | 304 |
| 5 | 0,3740 | 2.461,2340 | 120 |

Nguồn: cluster_trials.csv và analysis.json; fit 6.652, silhouette lấy tối đa 1.000 tin, seed 20261015.

Bảng 15: Đặc điểm hai cụm ở đơn vị gốc

| Cụm | n | Diện tích trung vị m² | Đơn giá trung vị triệu/m² |
| --- | --- | --- | --- |
| 1 | 989 | 450 | 2,3500 |
| 2 | 5.663 | 63 | 39,7059 |

Nguồn: cluster_summary.csv và analysis.json; nhãn cụm phục vụ thăm dò, chưa xác nhận phân khúc nghiệp vụ.

Cụm 1 có 989 tin, trung vị diện tích 450 m² và đơn giá 2,35 triệu/m²; cụm 2 có 5.663 tin, diện tích 63 m² và đơn giá 39,71 triệu/m². Cụm 1 có 732 tin đất; cụm 2 có 3406 tin nhà. Đối chiếu nhãn loại hình hỗ trợ diễn giải, không xác nhận cụm là phân khúc thị trường.

Ở k=2, so với log diện tích–log đơn giá, z-score và seed 42, ARI đạt 0,9764 khi giữ ngoại lệ; 0,0071 khi dùng thang gốc; 0,7221 với chuẩn hóa trung vị/IQR; 0,1833 khi đổi sang log diện tích–log tổng giá. Năm mẫu con 80% đạt ARI 0,9792–0,9980 trên các ID chung. Kết luận: cụm bền với lấy mẫu và khởi tạo đã thử, nhưng nhạy với đặc trưng và chuẩn hóa; chỉ dùng thăm dò. Điểm silhouette không tính được nếu mẫu ngẫu nhiên chỉ có một cụm được để trống, không thay bằng 0.

Cơ sở dữ liệu SQLite chứa 6.911 listings và vượt kiểm tra toàn vẹn, không ghi nhận lỗi khóa ngoại trong PRAGMA foreign_key_check. Bốn truy vấn đọc trả lần lượt 20, 4, 20 và 100 dòng; truy vấn cuối dùng cùng tỉnh/loại và khoảng đơn giá đã lưu trong benchmark. Bảng 16 trình bày một phần kết quả thật của truy vấn cuối. Việc có database, câu SQL, tham số và bản ghi trả về làm minh họa có thể kiểm chứng được, thay vì chỉ dùng ảnh cú pháp chưa thực thi.

Bảng 16: Năm dòng đầu của truy vấn khoảng đơn giá

| row_id | Diện tích m² | Giá tỷ VND | Đơn giá triệu/m² |
| --- | --- | --- | --- |
| 6561 | 40,00 | 1,3500 | 33,7500 |
| 7070 | 40,00 | 1,3500 | 33,7500 |
| 7878 | 40,00 | 1,3500 | 33,7500 |
| 5677 | 59,00 | 2,0000 | 33,8983 |
| 3666 | 56,00 | 1,9000 | 33,9286 |

Nguồn: SELECT thật từ SQLite; TP.HCM, house, đơn giá từ 33,7500 đến 77,9504 triệu/m²; LIMIT 100.

Trước index, kế hoạch quét listings và sắp xếp tạm; sau index, dùng idx_listings_search. Hai kết quả 100 dòng cùng hash. Trung vị trước 3,5297 ms, sau 0,6029 ms; tỷ số trước/sau 5,854. Đây là một lượt đo tuần tự warm-cache trên máy hiện tại, chưa chứng minh tăng tốc ổn định hay hiệu năng production. Kết quả cũ được giữ trong lịch sử thay vì lựa chọn lần đo có lợi.

Bảng 17: Thời gian truy vấn trước và sau chỉ mục

| Giai đoạn | Trung vị ms | P10 ms | P90 ms |
| --- | --- | --- | --- |
| Trước index | 3,5297 | 2,9149 | 4,3122 |
| Sau index | 0,6029 | 0,3297 | 0,9001 |

Nguồn: sql_benchmark.json; cùng truy vấn/tham số, mỗi pha 10 warmup + 51 lần đo; thứ tự tuần tự warm-cache.

Phép đo dùng cùng kết nối, câu lệnh và tham số; mỗi pha có 10 warmup và 51 lần đo, với ANALYZE trước pha tương ứng. Thiết kế trước–sau là tuần tự warm-cache, chưa ngẫu nhiên hóa hoặc lặp các khối độc lập, cũng chưa đo chi phí ghi và dung lượng chỉ mục. Vì vậy, bằng chứng phù hợp để giải thích kế hoạch truy vấn, đối soát kết quả và thảo luận giới hạn, chưa cho phép khẳng định cải thiện hiệu năng production hoặc mọi truy vấn. Bản chạy khác có thể cho tỷ số khác và phải được ghi như một lần đo riêng.

Đối với sản phẩm sử dụng, test JavaScript thực trong DOM tối giản kiểm các trạng thái ở Bảng 18. Bộ lọc toàn trang, tìm kiếm bảng, phân trang và CSV đã có kiểm logic; tìm Hà Nội ở ô bảng cho 1.014 dòng trong bảng/CSV trong khi KPI toàn trang giữ 6.911 nếu chưa đổi bộ lọc cấp trang. Những kết quả này giúp xác định hành vi mong đợi, nhưng không được ghi thành đã quan sát mọi bố cục trong một trình duyệt thật. Công cụ kiểm trình duyệt không truy cập được URL file cục bộ của bản mới; các xác nhận người dùng trước đây thuộc bản 7.001 tin không được chuyển sang xác nhận bản hiện tại.

Bảng 18: Kết quả kiểm logic các trạng thái dashboard

| Trạng thái | Số tin | Phạm vi kiểm |
| --- | --- | --- |
| Mặc định | 6.911 | JS thật trên DOM tối giản |
| TP.HCM | 3.266 | Như trên |
| TP.HCM + căn hộ | 235 | Như trên |
| Bỏ IQR nhóm | 6.652 | Như trên |
| Chỉ tiêu đề bán rõ | 3.032 | Như trên |
| Điều kiện không có dữ liệu | 0 | Ca kiểm lập trình |
| Tìm Hà Nội trong bảng | 1.014 | Bảng/CSV; KPI toàn trang 6.911 |

Nguồn: dashboard_test_results.json và AUDIT_RESULTS.json; chưa thay thế kiểm bố cục trình duyệt bản mới.

Workbook có ba trang và bốn biểu đồ, được đối soát đủ 6.911 dòng cùng các KPI lưu. Bằng chứng Artifact Tool ghi tính lại sau thay giá/diện tích, tám kiểm đầu vào không hợp lệ và quét lỗi công thức. Ví dụ trên bản thử, dòng Excel 10 ban đầu H=2.380.000.000, G=100 cho I=23.800.000; đổi H thành 3.380.000.000 thì I=33.800.000. Thao tác tính lại trực tiếp trong Microsoft Excel thật chưa được xác nhận trong lượt kiểm này. Tài liệu phân biệt rõ phép kiểm bằng engine/cached values với nghiệm thu giao diện ứng dụng cuối.

Hình 9 trích vùng chỉ tiêu của trang Dashboard từ ảnh render workbook cùng phiên bản, không phải ảnh chụp thao tác Microsoft Excel. Các giá trị 6.911 tin, giá trung vị 2,25 tỷ, giá trung bình hiển thị 3,70 tỷ, diện tích 70,00 m² và đơn giá 32,50 triệu/m² phù hợp số chưa làm tròn ở Bảng 8. Việc đưa vùng số liệu cùng đơn vị vào minh họa giúp đánh giá kết quả thực tế của sản phẩm mà không biến ảnh render thành bằng chứng của một loại thao tác chưa kiểm.

Hình 9: Vùng chỉ tiêu trong bản render trang Dashboard của Excel

Nguồn: xử lý từ Mendeley v2 [1], cùng run_id. Ảnh render bằng Artifact Tool, không phải thao tác Microsoft Excel. Dữ liệu: 6.911 tin; trung vị 2,25 tỷ, trung bình hiển thị 3,70 tỷ; diện tích 70 m²; đơn giá 32,50 triệu/m². Đối chiếu Bảng 8.

Bảng 19 tổng hợp lần chạy 27/10/2026: dữ liệu sạch 6.911 dòng, các bảng cách ly và lineage đã đối soát; HTML và Excel được dựng cho cùng run_id. Kiểm Python gồm 42 ca lõi và 3 ca mới cho xử lý giá trị thiếu, nhãn chưa quyết định và ID thiếu trong phép đối chiếu. Kiểm logic JavaScript dùng DOM mô phỏng; chưa thay nghiệm thu tương tác bằng Microsoft Excel thật.

Bảng 19: Phạm vi và kết quả các lớp kiểm chứng

| Lớp kiểm | Bằng chứng | Kết quả và giới hạn |
| --- | --- | --- |
| Mã Python | 45 test; 0 lỗi | 42 ca lõi và 3 ca phân tích bổ sung |
| Dữ liệu/phiên bản | Hash, lineage, từng bản ghi | CSV/JSON/DB/workbook cùng lần chạy |
| Trung vị | Đối chiếu CSV/database/Excel | Khớp analysis.json |
| SQL | 4 truy vấn; integrity/FK; hash | Thời gian là một lượt đo trên máy này |
| HTML | JS thật với DOM mô phỏng | Chưa nghiệm thu toàn bộ bố cục trình duyệt |
| Excel | 6.911 dòng; 4 biểu đồ | Artifact Tool; chưa kiểm Excel thật |
| Tái chạy | Nguồn đúng checksum, Linux | Bộ đầu ra mới cùng run_id |
| Nội dung nguồn | 60 tin, một người và AI hiệu chỉnh | 52 review; không phải gold độc lập |

Nguồn: outputs/python_test_results.json, dashboard_test_results.json, workbook_test_results.json và DELIVERY_CHECK.json của lần chạy hiện hành.

Chương 6 Kết luận và đánh giá khả năng ứng dụng

Đề tài đã xây dựng quy trình khám phá giá rao có thể tái lập và truy nguyên. Với câu hỏi 1, từ 9.004 dòng nguồn giữ 6.911 tin, trung vị tổng giá là 2,25 tỷ VND, trung bình khoảng 3,70 tỷ; chênh lệch phù hợp với phân phối lệch phải. Trung vị diện tích 70 m² và đơn giá 32,50 triệu/m² chỉ mô tả tập tin qua chính sách xử lý. Việc giữ nguồn nguyên bản, tin cách ly và lineage giúp giải thích kết quả thay vì chỉ công bố con số tổng hợp.

Độ tin cậy tính toán được hỗ trợ bởi checksum và đối soát sản phẩm. Độ tin cậy nội dung còn hạn chế: hơn nửa tin được giả định bán, vẫn có nhãn chưa rõ và mâu thuẫn chưa bị cách ly. Bộ 60 tin có một người gán ban đầu và AI hiệu chỉnh; phần lớn quyết định giữ/loại vẫn là review. Vì vậy, chỉ báo mức khớp và bao phủ từng trường trên mẫu, không coi dữ liệu đã xác minh hoặc ước lượng độ chính xác toàn thị trường.

Bộ kiểm Python có 45 ca và kiểm logic dashboard bằng JavaScript. Dữ liệu, hình, HTML, database và Excel được tái tạo cho cùng lần chạy. Workbook được kiểm công thức và đầu vào không hợp lệ bằng Artifact Tool. Tương tác trực tiếp trong Microsoft Excel thật và nghiệm thu toàn bộ bố cục trình duyệt vẫn cần xác nhận riêng; sản phẩm là phân tích ngoại tuyến của mẫu lịch sử.

Về tích hợp, các mô-đun chia sẻ bộ biến, run_id và metadata để giảm nhầm phiên bản. SQLite cung cấp truy vấn quan hệ, HTML cung cấp lựa chọn tương tác, Excel cung cấp bảng/công thức, còn các bảng và ảnh phục vụ phân tích. Đây là tích hợp qua tệp và lệnh cục bộ; chưa phải một dịch vụ nhiều người dùng có backend và đồng bộ trực tuyến. Excel có phụ thuộc dựng riêng và một số snapshot, còn bước xuất nhiều tệp chưa nguyên tử toàn bộ. Manifest cùng verifier là cơ chế phát hiện không nhất quán sau lỗi hoặc chỉnh sửa riêng, không nên được mô tả thành bảo đảm giao dịch cho mọi sản phẩm.

Ba phần cải thiện đã được thực hiện: đối chiếu bộ nhãn có hỗ trợ AI; phân tích tỉnh × loại × khoảng diện tích; kiểm độ nhạy K-means qua 65 lần fit. Quan hệ diện tích–giá cần đọc trong nhóm. Cụm ổn định với mẫu con nhưng thay đổi mạnh khi đổi đặc trưng; không gán nghĩa phân khúc thị trường. SQLite bảo toàn kết quả truy vấn; thời gian chỉ là minh họa trên một máy, không suy rộng.

Bảng 20: Mức đáp ứng mục tiêu theo bằng chứng hiện có

| Khía cạnh | Mức đã đạt | Giới hạn cần giữ |
| --- | --- | --- |
| Tin cậy | Đúng bản nguồn, tính toán/phiên bản đối soát | Chưa xác minh mọi tin hoặc độ chính xác nhãn |
| Vận hành | Lõi đã tái lập; SQL, HTML và workbook có kiểm | Thiếu nghiệm thu trình duyệt và Excel thật |
| Tích hợp | Dữ liệu chung, metadata, một lệnh điều phối | Tích hợp tệp cục bộ; workbook phụ thuộc runtime riêng |
| Ứng dụng | Khám phá mẫu lịch sử, học tập, truy nguyên | Chưa dùng định giá hiện tại, pháp lý hoặc đầu tư |

Nguồn: tổng hợp kết quả và giới hạn ở Chương 5; phạm vi mục tiêu Chương 1.

Phạm vi ứng dụng phù hợp là học tập, khám phá mẫu lịch sử và truy nguyên trường hợp cần rà soát. Bảng 20 tóm tắt mức đáp ứng cùng giới hạn. Vì thiếu ngày từng tin, vị trí xác minh và giá giao dịch, sản phẩm chưa cung cấp căn cứ mua bán, đánh giá pháp lý hoặc khuyến nghị đầu tư.

Mẫu đã có 120 tin phát triển và 60 tin đánh giá, thay cho kế hoạch chưa thực hiện trước đây. Việc còn lại thuộc chất lượng tham chiếu: thành viên nhóm cần đọc lại các sửa đổi có hỗ trợ AI và giải quyết trường review khi có đủ nguồn. Chưa có hai người đọc độc lập và không tính hệ số đồng thuận. Nếu dùng các lỗi evaluation để sửa quy tắc tiếp, cần một mẫu đánh giá mới trước khi công bố cải thiện.

Quy tắc đã được cải thiện bằng mẫu phát triển và kiểm hồi quy trước khi đối chiếu evaluation. Lượt này giữ nguyên hash mã phân loại, không chỉnh theo nhãn cuối. Hướng tiếp theo là kiểm tin gần trùng, chuẩn hóa ý nghĩa diện tích và thu thập mẫu độc lập từ nguồn khác; mọi bước phải giữ bằng chứng và không tự sửa số mơ hồ thành giá đúng.

Phần phân tích nhóm và độ ổn định cụm đã có bảng, hình và script chạy lại trong outputs/extended. Phát triển tiếp nên kiểm khả năng lặp lại trên nguồn khác, đánh giá chất lượng nhãn và tách định nghĩa diện tích trước khi thêm mô hình dự báo. Thí nghiệm SQL có thể bổ sung khối đo ngẫu nhiên, chi phí ghi và dung lượng index nếu phù hợp phạm vi môn học.

Về bàn giao, bổ sung hướng dẫn Windows/Linux, kiểm các bộ lọc trong trình duyệt và tính lại công thức bằng Excel thật; đồng bộ README, báo cáo và metadata trước mỗi lần nộp. Cần phân biệt báo cáo chưa được một verifier kiểm với báo cáo chưa hoàn thành, tránh trạng thái mặc định lỗi thời. Các thành viên phải giải thích được nguồn, lựa chọn xử lý và giới hạn của phần mình phụ trách; đóng góp được ghi theo công việc thực tế, không dùng hồ sơ phân công thay bằng chứng đã thực hiện.

Kết quả bổ sung về kiểm nhãn và phân tích nhóm

Bộ nhãn ban đầu do một thành viên thực hiện, sau đó AI sửa 17 tin. Chưa có xác nhận độc lập cho các sửa đổi. Bảng dưới báo số khớp trên số nhãn xác định; số còn lại không bị coi là sai hoặc đúng. Đây là thống kê trên mẫu phân tầng, không suy rộng cho toàn bộ nguồn.

| Trường | Khớp / xác định | Chưa xác định |
| --- | --- | --- |
| Loại tài sản | 43/58 | 2 |
| Giao dịch | 28/45 | 15 |
| Cơ sở giá | 46/54 | 6 |
| Tổng giá | 47/50 | 10 |
| Diện tích | 53/54 | 6 |
| Giữ / cách ly | 8/8 | 52 |

Quy tắc sale_assumed được xem là chưa khẳng định giao dịch, other_unknown là chưa khẳng định loại. Các dự đoán này không được tính khớp với nhãn cụ thể. So số chỉ đo giá trị parser, kể cả tin đã cách ly; không chứng minh quyết định giữ đúng. Các bảng theo tầng được lưu riêng trong evaluation_metrics.csv.

Phân tích 405 nhóm tỉnh × loại × khoảng diện tích có 41 nhóm biết tỉnh/loại và n≥30, tổng 4.594 tin. Các nhóm nhỏ vẫn được lưu nhưng không dùng để so sánh chính. Khoảng Q1–Q3 mô tả độ phân tán, không phải khoảng tin cậy. Loại tài sản và ý nghĩa diện tích vẫn chịu sai số nguồn.

Độ ổn định và độ nhạy của phân cụm

Thử 5 cấu hình, k=2–5, seed 7/42/2026 với 10 khởi tạo mỗi lần; thêm 5 mẫu con 80%. So ARI trên đúng các ID chung tại k=2, lấy cấu hình log diện tích–log đơn giá, z-score, bỏ IQR và seed 42 làm mốc. ARI không đo độ đúng nghiệp vụ.

| Thay đổi so với mốc | ARI trên ID chung |
| --- | --- |
| Không đổi | 1,0000 |
| Giữ ngoại lệ | 0,9764 |
| Thang gốc + z-score | 0,0071 |
| Log + trung vị/IQR | 0,7221 |
| Log diện tích + log tổng giá | 0,1833 |

Năm mẫu con 80% đạt ARI 0,9792–0,9980. Cụm ổn định với nhiễu lấy mẫu và khởi tạo đã thử nhưng thay đổi mạnh theo cách biểu diễn. Silhouette trên mẫu có thể không tính được khi mẫu chỉ chứa một cụm; kết quả được để trống và ghi lý do. Không so điểm giữa các hình học như một tiêu chuẩn chọn mô hình tuyệt đối.

Bảng chi tiết và hình ở outputs/extended gồm cluster_robustness_trials.csv, cluster_seed_stability.csv, cluster_feature_sensitivity.csv và cluster_subsample_stability.csv. Kết quả giữ vai trò thăm dò, chưa cho phép đặt tên cụm là phân khúc cao cấp/bình dân hoặc suy ra giá thị trường.

Tài liệu tham khảo

[1] Tran, D. C., Nguyen, H. H., và Ha, H. S. (2021). Vietnam Real Estate Data, Version 2. Mendeley Data. DOI: 10.17632/5477zhnmn2.2. https://data.mendeley.com/datasets/5477zhnmn2/2. CC BY 4.0.

[2] Tài liệu học phần Nhập môn khoa học dữ liệu. Chương 1 Mở đầu. Tệp Chuong 1 - Mo dau.pdf do người học cung cấp; đối chiếu trang PDF 3–5 và 12.

[3] Tài liệu học phần Nhập môn khoa học dữ liệu. Chương 2 Chuẩn bị dữ liệu. Tệp Chuong 2 - Chuan bi du lieu.pdf; các trang về chất lượng, ngoại lệ, Z-score, lấy mẫu và tổng hợp; xem references/DOI_CHIEU_SLIDE.md.

[4] Tài liệu học phần Nhập môn khoa học dữ liệu. Chương 3 Trực quan hóa dữ liệu. Tệp Chuong 3 - Truc quan hoa du lieu.pdf; các trang về mục đích và lựa chọn biểu đồ.

[5] Tài liệu học phần Nhập môn khoa học dữ liệu. Chương 4 Học máy phần 2. Tệp Chương 4 - Hoc may - 2.pdf; nội dung K-means và phân cụm.

[6] Tài liệu học phần Nhập môn khoa học dữ liệu. Chương 5 Cơ sở dữ liệu và SQL phần 1. Tệp Chuong 5 - Co so du lieu va SQL - 1.pdf; mô hình quan hệ, khóa và SQL.

[7] Tài liệu học phần Nhập môn khoa học dữ liệu. Chương 5 Cơ sở dữ liệu và SQL phần 2. Tệp Chuong 5 - Co so du lieu va SQL - 2.pdf; nội dung truy vấn và tổ chức truy cập dữ liệu.

[8] NumPy Developers. NumPy v2.3 Manual, Broadcasting. https://numpy.org/doc/2.3/user/basics.broadcasting.html. Truy cập 16/10/2026.

[9] pandas Developers. pandas 2.3.3 Documentation, Group by split apply combine. https://pandas.pydata.org/pandas-docs/version/2.3/user_guide/groupby.html. Truy cập 16/10/2026.

[10] Matplotlib Development Team. Matplotlib 3.10.6 Documentation, matplotlib.pyplot.hist. https://matplotlib.org/3.10.6/api/_as_gen/matplotlib.pyplot.hist.html. Truy cập 16/10/2026.

[11] SQLite. Query Planning; Foreign Key Support; CREATE TABLE; EXPLAIN QUERY PLAN. https://www.sqlite.org/queryplanner.html; https://www.sqlite.org/foreignkeys.html; https://www.sqlite.org/lang_createtable.html; https://www.sqlite.org/eqp.html. Truy cập 16/10/2026.

[12] Python Software Foundation. Python Standard Library, tài liệu về unicodedata, hashlib, pathlib và urllib.request. https://docs.python.org/3/library/. Truy cập 16/10/2026.

[13] Arthur, D., và Vassilvitskii, S. (2007). k-means++ The Advantages of Careful Seeding. Proceedings of SODA, tr. 1027–1035. https://theory.stanford.edu/~sergei/papers/kMeansPP-soda.pdf.

[14] Rousseeuw, P. J. (1987). Silhouettes A graphical aid to the interpretation and validation of cluster analysis. Journal of Computational and Applied Mathematics, 20, tr. 53–65. DOI: 10.1016/0377-0427(87)90125-7.

[15] Hubert, L., và Arabie, P. (1985). Comparing partitions. Journal of Classification, 2, tr. 193–218. DOI: 10.1007/BF01908075.

[16] Efron, B. (1979). Bootstrap Methods Another Look at the Jackknife. The Annals of Statistics, 7(1), tr. 1–26. DOI: 10.1214/aos/1176344552.

[17] Kho mã dự án KHDL-BatDongSan. https://github.com/vandat-snk/KHDL-BatDongSan. Bản làm việc cục bộ trên nhánh improve-data-validation; run_id 20261027T065401Z-5c8df2cc. Hash mã và sản phẩm được lưu trong manifest; chưa khẳng định đã đẩy các sửa đổi này lên GitHub.

Phụ lục tái lập và nguồn minh chứng

Bộ nguồn chotot_data.json được lưu nguyên bản tại data/raw trên máy thực hiện, không đưa lên Git do kích thước và nội dung chi tiết. SHA-256: ef39f153f48a55af07baa86883cd9036652f6d52232fed0be6e8991c7a5bf811. Script tải kiểm đúng bản này trước khi phân tích. Các bản CSV phục vụ công khai không giữ tiêu đề, mô tả, thông tin liên hệ hoặc địa chỉ đường chi tiết.

Nguồn số liệu là outputs/analysis.json, run_manifest.json, outputs/tables và outputs/extended/results.json của mốc 20261027T065401Z-5c8df2cc. Hình được thay bằng sản phẩm hiện hành. Các tương quan theo nhóm tính thứ hạng trong từng nhóm, không dùng thứ hạng toàn mẫu. Phần mở rộng có hash bộ nhãn và script; kết quả không tự cập nhật khi sửa Excel nhãn.

Mẫu đánh giá mới nằm trong docs/manual_validation/sample_manifest.json. Bộ nhãn đã sửa được giữ riêng trong private với lịch sử thay đổi, không đưa mô tả và liên hệ lên bảng kết quả công khai. Chạy python scripts/complete_analysis.py --labels <duong_dan_xlsx> sau pipeline để tạo các bảng đối chiếu, phân nhóm và độ nhạy. Không đồng nhất bộ 60 tin này với đợt rà soát trợ lý cũ.

Để tái lập lõi, cài Python 3.11 trở lên và requirements.txt trong môi trường ảo. Trên Linux: python3 -m venv .venv; sau đó .venv/bin/python -m pip install -r requirements.txt và .venv/bin/python scripts/run_project.py. Trên Windows dùng .venv\Scripts\python.exe cho hai lệnh sau. Thêm --skip-download khi raw đã có đúng checksum. Dựng workbook còn cần Node và Artifact Tool. Chạy lại đổi run_id và thời gian benchmark, nên phải đối soát các sản phẩm liên quan trước khi thay bộ số liệu chính.

Lượt cập nhật 27/10/2026 đã chạy lại trên Linux với raw đúng checksum; chương trình giữ 6.911 tin và cách ly 209 tin. Các kết quả cũ được lưu riêng để truy nguyên. Đánh giá nhãn, thống kê nhóm và kiểm phân cụm có đầu ra máy đọc được. Phần chưa xác nhận là chất lượng nhãn người độc lập, thao tác Microsoft Excel thật và tính đại diện của mẫu dữ liệu.

Việc xây dựng mã, rà soát và biên soạn có sử dụng trợ lý AI. Tài liệu không gán các thao tác kiểm bằng công cụ thành xác nhận độc lập của từng thành viên. Những nhận định được giữ theo kết quả lưu và giới hạn kiểm chứng; hồ sơ phân công dùng để tiếp quản nội dung, không thay thế bằng chứng đóng góp đã thực hiện.
