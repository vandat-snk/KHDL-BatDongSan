# Đối chiếu yêu cầu báo cáo với hệ thống thực tế

Ngày cập nhật: 16/10/2026. Đây là tài liệu chuẩn bị nội dung và tiêu chí nghiệm thu, không phải báo cáo hoàn chỉnh. Xem kết quả sửa code và các giới hạn còn lại trong [biên bản rà soát kỹ thuật](RA_SOAT_KY_THUAT.md).

## Quyết định phạm vi

Tên đề tài: **Phân tích giá rao bất động sản Việt Nam**.

Mục tiêu duy nhất: xây dựng một quy trình có thể chạy lại, giúp người phân tích khám phá và so sánh đặc điểm giá rao trong một mẫu tin bất động sản lịch sử sau khi kiểm tra chất lượng dữ liệu.

Phạm vi dữ liệu là Vietnam Real Estate Data phiên bản 2, công bố trên Mendeley Data ngày 12/01/2021. Đơn vị quan sát là một tin rao; không đồng nhất với một bất động sản hoặc giao dịch. Kết quả chỉ mô tả mẫu tin đủ điều kiện theo các quy tắc công khai. Địa phương được giữ theo nhãn lịch sử của nguồn. Dữ liệu không có ngày từng tin, tọa độ xác minh hoặc giá giao dịch để suy luận thị trường hiện tại.

Các chức năng làm sạch, thống kê, trực quan, phân cụm thăm dò và truy vấn SQL cùng phục vụ mục tiêu trên. Không mở rộng sang định giá để mua bán, dự báo giá, khuyến nghị đầu tư, môi giới, quản lý giao dịch hay hệ thống tài khoản. Ví dụ của giảng viên về hai mức người dùng hoặc 32 bảng không phải yêu cầu bắt buộc của đề tài này; mô hình thực tế có ba bảng SQLite.

## Trạng thái bản báo cáo cũ

`BAO_CAO_DO_AN.docx` và `BAO_CAO_DO_AN.md` là bản thảo trước khi nhận yêu cầu sáu chương. Giữ lại để đối chiếu số liệu và diễn giải cũ; chưa xem là bản báo cáo đáp ứng yêu cầu mới, chưa dùng để nộp.

Đợt rà soát hiện tại ưu tiên sửa và kiểm chứng code. Chưa viết lại báo cáo Word trong đợt này. Chỉ biên soạn bản hoàn chỉnh khi các sửa đổi kỹ thuật đã chạy qua kiểm tra và có bộ đầu ra nhất quán.

## Cấu trúc sáu chương cần dùng khi viết lại

| Chương báo cáo | Nội dung bắt buộc | Bằng chứng và mức chi tiết cần có |
|---|---|---|
| Chương 1. Giới thiệu đề tài | Tên đề tài; vấn đề; ý nghĩa thực tiễn; ý nghĩa đối với cộng đồng nghiên cứu; một mục tiêu; phạm vi ứng dụng và giới hạn | Giải thích khó khăn do chuỗi giá/diện tích không đồng nhất. Ý nghĩa thực tiễn là hỗ trợ khám phá mẫu tin có kiểm chứng. Ý nghĩa nghiên cứu là một tình huống thực hành tái lập về chất lượng dữ liệu và phân tích mô tả; không tự nhận thuật toán mới hay mẫu đại diện. Liệt kê các câu hỏi phân tích như các câu hỏi con của cùng một mục tiêu. |
| Chương 2. Cơ sở lý thuyết và nền tảng kỹ thuật | Những phương pháp và công nghệ thật sự dùng để hiện thực đề tài | Trình bày nguyên lý, đầu vào/đầu ra, tham số, cơ chế hoạt động, lý do chọn và giới hạn của từng kỹ thuật trong bảng bên dưới. Mỗi phần phải liên hệ với mã và thiết kế; không chèn giới thiệu công nghệ chung hai hoặc ba dòng. |
| Chương 3. Phân tích và thiết kế ứng dụng | Yêu cầu chức năng; yêu cầu chất lượng; kiến trúc; luồng xử lý; thiết kế dữ liệu và giao diện | Sơ đồ luồng nguồn → kiểm tra → xử lý → kết quả → dashboard/SQL/Excel. Từ điển biến và quy tắc chấp nhận/cách ly. Thiết kế ba bảng, khóa, quan hệ và chỉ mục bám đúng SQLite thực tế. Phân biệt người vận hành pipeline với người xem kết quả như hai cách sử dụng, không mô tả chúng thành phân quyền chưa được code. |
| Chương 4. Hiện thực hệ thống | Chuyển lý thuyết và thiết kế thành các mô-đun cụ thể | Với mỗi mô-đun: tên file/hàm, đầu vào, xử lý, đầu ra, kiểm tra lỗi và ví dụ dữ liệu. Bao gồm tải/kiểm nguồn; đọc giá và diện tích; truy xuất dòng; IQR; thống kê; K-means; tạo database/SQL; dựng dashboard; xác minh đầu ra. Giải thích tích hợp bằng file và lệnh thực thi. |
| Chương 5. Demo và vận hành hệ thống | Hướng dẫn cài/chạy; kịch bản thực tế; kết quả; kiểm thử; bằng chứng chạy được | Dùng kết quả của lần chạy cuối: dữ liệu đầu vào, bảng trước/sau, log test, màn hình mặc định, lọc, CSV xuất, truy vấn và benchmark. Mỗi hình phải có dữ liệu minh họa, bộ lọc, đơn vị, số mẫu và nguồn; không dùng ảnh giao diện trống để thay bằng chứng. Nêu rõ test tự động và xác nhận do người dùng thực hiện. |
| Chương 6. Kết luận | Kết quả đạt được theo mục tiêu; độ tin cậy có điều kiện; vận hành; tích hợp; khả năng ứng dụng; hạn chế và việc tiếp theo | Trả lời bằng chứng cụ thể: chạy lại được đến đâu, số liệu các sản phẩm có khớp không, nguồn được kiểm thế nào, phần nào mới minh họa, phần nào còn cần gán nhãn thủ công. Không kết luận tuyệt đối “chính xác”, “đáng tin cậy” hoặc “ứng dụng rộng rãi” chỉ vì code chạy xong. |

Đây là sáu chương của báo cáo, khác với số chương trong slide môn học. Có thể chia tiểu mục hợp lý trong mỗi chương, nhưng mỗi chương phải có lập luận và nội dung hoàn chỉnh.

## Độ sâu kỹ thuật cần trình bày ở Chương 2

| Nền tảng hoặc phương pháp | Nội dung cần giải thích và đối chiếu code |
|---|---|
| Python và môi trường | Phiên bản thực chạy, môi trường ảo, cài phụ thuộc, đường dẫn tương đối theo thư mục dự án, đầu vào/đầu ra file, lỗi và mã thoát. Phân biệt công cụ phát triển với thành phần cần khi người dùng chỉ mở dashboard. |
| Tải và kiểm chứng dữ liệu | HTTPS bằng `urllib.request`, timeout, SHA-256, manifest/metadata, kiểm đúng bản nguồn và giữ raw bất biến. Không mô tả là hệ thống thu thập tin thời gian thực hay API bất động sản nếu chưa có chức năng đó. |
| Chuẩn hóa và truy xuất | Unicode NFKC, khoảng trắng, regex, từ khóa giao dịch/loại hình, đọc đơn vị, quy ước dấu số, phát hiện xung đột. Khóa năm trường dùng băm chỉ xác định trùng nội dung theo quy tắc; không chứng minh cùng bất động sản. |
| pandas | DataFrame, kiểu cột, missing khác với chuỗi không phân tích được, lọc mặt nạ, `groupby`, phân vị, phép kết hợp nhóm, xuất CSV/JSON. Giải thích đơn giá được tính từng dòng trước khi tổng hợp. |
| NumPy và thống kê | Mảng số, khoảng cách, seed và phép toán vector. Trung bình/trung vị, IQR, tương quan Spearman và bootstrap phải có định nghĩa, công thức phù hợp, giả định và giới hạn. Những kỹ thuật ngoài slide cần tài liệu bổ sung. |
| K-means | Log tự nhiên và Z-score, hai đặc trưng, khoảng cách Euclid, hàm mục tiêu, khởi tạo K-means++, bước gán/cập nhật, số lần khởi tạo, điều kiện dừng, thử k và silhouette/ARI. Cụm không phải nhãn đúng hoặc mô hình dự đoán giá. |
| Matplotlib | Cách chọn histogram/bin, scatter hai trục log, cột, boxplot, nhãn trục/đơn vị/cỡ mẫu và khả năng che khuất điểm. Phân biệt dữ liệu để tính KPI với mẫu vẽ cho nhẹ giao diện. |
| SQLite | CSDL nhúng lưu file, kết nối, giao dịch, bật khóa ngoại theo kết nối, kiểu dữ liệu và ràng buộc, khóa chính/ngoại/UNIQUE/CHECK, JOIN và GROUP BY. Chỉ mục ghép có thứ tự cột; giải thích kế hoạch thực thi, chi phí lưu/ghi và giới hạn benchmark bộ dữ liệu nhỏ. |
| HTML/CSS/JavaScript | HTML cho cấu trúc, CSS cho bố cục, JavaScript cho trạng thái lọc và tính thống kê; DOM/SVG; dữ liệu đóng gói vào HTML; xử lý mẫu rỗng; phân trang và CSV. Không gọi dashboard file tĩnh là dịch vụ backend hoặc ứng dụng có xác thực. |
| Excel | Tập dữ liệu trong workbook, công thức đổi đơn vị/tổng hợp và nguồn biểu đồ. Nêu rõ bảng nào là snapshot, công thức nào tự tính lại, phần nào cần tạo lại bằng công cụ ngoài môi trường Python. Không khẳng định mọi chỉ số đổi đúng nếu tự sửa một cột đầu vào mà bỏ qua biến dẫn xuất. |
| Tích hợp và kiểm thử | Lệnh chạy từ nguồn đến sản phẩm, phiên bản schema, dấu vết nguồn và hash đầu ra, đối soát dòng, kiểm thử đơn vị/tích hợp, test UI thực tế và điều kiện để xác nhận một phiên bản sẵn sàng báo cáo. |

## Quy định hình, bảng, công thức và định dạng

1. Văn bản thân bài căn đều hai bên. Dùng thống nhất font, cỡ chữ, giãn dòng, lề, cấp tiêu đề và đánh số chương; in đậm theo vai trò cấu trúc, không bôi đậm cả đoạn tùy ý.
2. Mỗi hình có tên theo mẫu `Hình 1: Sơ đồ luồng xử lý dữ liệu`; mỗi bảng có tên theo mẫu `Bảng 1: Quy mô dữ liệu trước và sau xử lý`. Dùng cùng một quy tắc đánh số liên tục hoặc theo chương cho toàn văn, có danh mục hình và danh mục bảng.
3. Dưới hình/bảng ghi nguồn, phiên bản dữ liệu, đơn vị, số quan sát, bộ lọc và quy tắc đặc biệt. Trong thân bài phải dẫn chiếu hình/bảng và giải thích kết quả, không chỉ chèn ảnh.
4. Với ảnh dashboard, ghi trạng thái lọc và bảng số liệu đi kèm. Với ảnh SQL, ghi câu truy vấn/tham số và bảng kết quả. Với sơ đồ, ghi nguồn là thiết kế của nhóm và kèm ví dụ các giá trị đi qua các bước; không dùng số liệu giả làm kết quả thực nghiệm.
5. Công thức phải ở dạng toán học đọc được trong Word, ưu tiên Equation/OMML có phân số, chỉ số và dấu tổng phù hợp. Không đưa chuỗi lệnh LaTeX thô vào thân bài. Giải thích ký hiệu, đơn vị và ví dụ số thật sau công thức.
6. Mọi số liệu ở Chương 5 và 6 lấy từ lần chạy đã kiểm chứng sau cùng. Không sao chép tốc độ SQL cũ khi đã chạy lại; thời gian đo có thể thay đổi theo máy.
7. Phân biệt bằng chứng đã có với công việc còn chờ. Xác nhận thao tác của người dùng phải ghi đúng nguồn xác nhận; không biến nó thành việc công cụ đã tự quan sát mọi trạng thái màn hình.

## Điều kiện trước khi bắt đầu bản báo cáo mới

- Quy trình trên bản clone đã hướng dẫn đủ bước tải nguồn và cài phụ thuộc; các file kiểm tra không phụ thuộc ảnh/PDF tạm của một máy duy nhất.
- Kiểm thử phù hợp chạy đạt; thay đổi quy tắc dữ liệu có kiểm thử hồi quy và nhật ký lý do.
- Nguồn và các đầu ra được đối soát; kết quả phân tích, dashboard, database, các bảng và workbook được kiểm tra hoặc nêu rõ trạng thái snapshot.
- Có bảng đánh giá nhãn thủ công cho các quy tắc suy luận nếu muốn kết luận về độ chính xác nhãn. Chưa có nhãn kiểm chứng thì nêu giới hạn rõ; không tự tạo tỷ lệ chính xác.
- Đã tách dữ liệu/source khỏi tệp đầu ra tạm; mỗi tuyên bố kiểm thử gắn với một lần chạy và bằng chứng kiểm tra thật.
- Nhóm bổ sung thông tin trường, lớp học phần, giảng viên và STT đăng ký. Thiếu các thông tin hành chính này không phải lý do tự đổi đề tài hoặc dựng thông tin.

Sau khi các điều kiện kỹ thuật được hoàn tất, viết báo cáo mới theo sáu chương trên. [Phân công đã cập nhật](PHAN_CONG_VA_NOI_DUNG_BAO_CAO.md): Nhi chủ trì Chương 1–2, Đạt Chương 3–4, Quỳnh Chương 5–6; mỗi người cung cấp nội dung kỹ thuật cho các chương liên quan và đọc chéo. Công việc chưa được nghiệm thu phải giữ trạng thái chờ, không chuyển kế hoạch thành kết quả.
