# Phân công hoàn thiện đồ án cho ba thành viên

Cập nhật 16/10/2026 theo yêu cầu rút ngắn thời gian: trợ lý thực hiện các kiểm tra và chuẩn bị tài liệu kỹ thuật có thể tự làm. Bảng này thay toàn bộ task D01–Q06 và I01–I10 trước đây; không còn yêu cầu mỗi người kiểm 20 tin rồi kiểm chéo thêm 20 tin.

Đề tài: **Phân tích giá rao bất động sản Việt Nam**. Mục tiêu duy nhất: xây dựng quy trình có thể chạy lại để khám phá và so sánh giá rao trong mẫu tin lịch sử sau kiểm tra chất lượng. Làm sạch, trực quan, phân cụm và SQL phục vụ cùng mục tiêu.

## 1. Những việc đã làm, nhóm không cần làm lại

Mốc dữ liệu `20261016T015620Z-f2e661a6`: 9.004 raw = 1.884 trùng + 184 cách ly + 6.936 giữ; 29 test Python đạt. Báo cáo bằng chứng mới ở `outputs/ASSISTANT_CHECKS.json`, kèm hash đầu vào. Các kết quả chỉ áp dụng cho phiên bản được ghi, không dùng làm hằng số ép lần chạy sau.

| Công việc trợ lý đã thực hiện/chuẩn bị | Bằng chứng để sử dụng ngay | Người tiếp quản để hiểu và viết |
| --- | --- | --- |
| Nguồn, DOI/v2, metadata, quyền sử dụng, SHA và khác biệt 10.000/9.004 | `references/DATA_SOURCE.md`, metadata/manifest raw; `docs/NGUON_QUY_TAC_VA_THIET_KE.md` | Nhi |
| Đọc slide, đối chiếu phương pháp với môn học và phạm vi đăng ký | `references/DOI_CHIEU_SLIDE.md`, `registration.json` | Nhi; cả ba nắm phạm vi |
| Code parse/đơn vị, trùng, cách ly, lineage, IQR/độ nhạy và kiểm thử | `src/pipeline.py`, `source_checks.py`, `tests/`; hồ sơ nguồn/quy tắc/thiết kế | Nhi hiểu dữ liệu; Đạt hiểu hiện thực |
| Đọc 60 tin mẫu và bảy tin trọng điểm, ghi rõ bất định/bỏ sót và độ nhạy bổ sung | `docs/DOI_CHIEU_60_TIN_TRO_LY.csv`, `KET_QUA_KIEM_TRA_NHAN.md` | Nhi dùng để giải thích giới hạn; không giao gán nhãn lại |
| Lập từ điển 18 cột, bảng quy tắc/ví dụ, kiến trúc/ERD và mô-đun I/O | `docs/NGUON_QUY_TAC_VA_THIET_KE.md` | Đạt dùng viết Chương 3–4; Nhi viết Chương 2 |
| Code K-means, bảng thử k/seed, giải thích tham số và một vòng lặp minh họa | `docs/THUC_NGHIEM_KMEANS_VA_SQL.md`, bảng `cluster_*` | Đạt |
| Tạo DB ba bảng; chạy lại bốn SQL đọc; đối chiếu kết quả, plan và benchmark thật | Tài liệu K-means/SQL; `outputs/ASSISTANT_CHECKS.json`, `sql_benchmark.json` | Đạt |
| Tính riêng ba trung vị từ CSV bằng thư viện chuẩn và bằng SQLite ORDER BY | `docs/DOI_CHIEU_SO_LIEU_TRUC_QUAN.md`, `ASSISTANT_CHECKS.json` | Quỳnh dùng phân tích và viết |
| Đối soát tất cả dòng CSV/JSON/DB/workbook, hash và lineage | `outputs/AUDIT_RESULTS.json`, `DELIVERY_CHECK.json` | Đạt nắm cách kiểm, không bắt chạy lại để chứng minh đã đọc |
| Kiểm JavaScript thật: lọc/KPI/rỗng/phân trang/tìm/CSV/lấy mẫu | `outputs/dashboard_test_results.json`, `tests/test_dashboard.mjs` | Quỳnh |
| Kiểm ba trang/bốn biểu đồ và công thức Excel bằng công cụ tính lại; thử giá/diện tích và tám đầu vào lỗi | `outputs/workbook_test_results.json`; giới hạn ở `NGHIEM_THU_EXCEL.md` | Quỳnh |
| Kiểm chạy bản sao chỉ có nguồn, cùng Python đã cài; giữ nguyên khả năng đối soát qua Git | `outputs/portability_check.json`, `.gitattributes` | Đạt; không gọi là cài mới trên máy khác |
| Chuẩn bị kịch bản demo, bảng dữ liệu kèm tám hình, nội dung sáu chương và tiêu chí định dạng | `DOI_CHIEU_SO_LIEU_TRUC_QUAN.md`, `DOI_CHIEU_YEU_CAU_BAO_CAO.md` | Quỳnh; cả nhóm dùng |

Các việc này do trợ lý làm, không ghi thành đóng góp đã hoàn thành của sinh viên. “Tiếp quản” nghĩa là đọc, hiểu, chọn bằng chứng, viết và chịu trách nhiệm nội dung. Đóng góp nhóm được ghi theo việc thực làm, không tự chia 33,33% hay ký thay người khác.

## 2. Những điểm vẫn chưa thể xác nhận

- Chưa quan sát đầy đủ bố cục/thao tác dashboard 6.936 tin trong trình duyệt: công cụ chặn URL file cục bộ. Xác nhận cũ 7.001 tin không áp dụng cho bản mới. Kiểm logic JavaScript và dữ liệu đã đạt.
- Đã thử mở bản sao Excel bằng giao diện nhưng công cụ không nhập được đường dẫn vào hộp mở tệp; chưa xác nhận tính lại trong Microsoft Excel thật. Công thức, cache, thử thay giá/diện tích bằng Artifact Tool đã đạt.
- Chưa cài pip mới trên máy khác. Bản sao nguồn chạy bằng cùng Python đã kiểm; không bắt nhóm làm thêm một cuộc thử môi trường mới nếu không có nhu cầu chạy trên máy khác.
- Rà soát nội dung vẫn phát hiện tin mơ hồ/mâu thuẫn lọt qua quy tắc. Bộ “sạch” là đủ điều kiện theo chính sách, không phải mọi tin đã xác minh. Chưa có nhãn người thật để công bố accuracy; không cần gán nhãn nếu không đưa ra tuyên bố đó.
- Bản thảo Word/Markdown cũ chưa đáp ứng đầy đủ sáu chương mới. Chưa tự viết lại bản hoàn chỉnh trong đợt phân công này.

Phần giao diện còn lại được gộp vào một buổi tổng duyệt ngắn và chụp ảnh báo cáo, không chia thành nhiều đợt kiểm trùng nhau. Nếu phát hiện lỗi cụ thể, nhóm gửi lại bước tái hiện; trợ lý có thể xử lý mã và chạy kiểm phù hợp.

## 3. Bảng phân công còn lại — Võ Văn Đạt

**Võ Văn Đạt — N23DCCN078.** Chủ trì Chương 3–4, giải thích luồng code và tích hợp. Không phải tự làm lại DB, K-means hay các kiểm tra đã có.

| Mã | Việc cụ thể cần làm | File/tài liệu đầu vào | Sản phẩm và tiêu chí hoàn thành | Ước lượng chủ động |
| --- | --- | --- | --- | --- |
| DAT-01 | Đọc luồng tải → sạch → thống kê/cụm → DB → HTML/Excel; đọc một ví dụ row_id=1 và một tin cách ly 638 | `NGUON_QUY_TAC_VA_THIET_KE.md`, README, mã tương ứng | Giải thích được bước xử lý, I/O, lý do cách ly, run_id/hash; đánh dấu điều chưa hiểu để hỏi | 45–60 phút |
| DAT-02 | Viết Chương 3: yêu cầu, kiến trúc, luồng, từ điển, ERD ba bảng, khóa/ràng buộc/index, trạng thái giao diện | Hồ sơ thiết kế đã chuẩn bị; `sql/01_schema.sql`; yêu cầu báo cáo | Chương hoàn chỉnh có sơ đồ + dòng dữ liệu minh họa, mô tả đúng ba bảng; không bịa backend/phân quyền | 1 buổi |
| DAT-03 | Viết Chương 4 theo mô-đun thật, giải thích K-means và SQL; cung cấp cho Nhi phần kỹ thuật Chương 2 | `THUC_NGHIEM_KMEANS_VA_SQL.md`, hồ sơ mô-đun, code | Mỗi mô-đun có file/hàm, I/O, xử lý, lỗi, ví dụ. Nêu đúng benchmark không tăng tốc trong lần ghi nhận | 1 buổi |
| DAT-04 | Tổng duyệt phần kỹ thuật và đọc chéo Chương 1–2 | Kịch bản demo có sẵn; phần viết của Nhi | Trình bày được vì sao cần log/Z-score, cách chọn k, index và hash; góp ý kỹ thuật có căn cứ | 30–45 phút |

Nếu thuyết trình trên máy khác, Đạt chạy thử trên đúng máy đó trước buổi bảo vệ; đây là chuẩn bị buổi demo theo nhu cầu, không biến thành yêu cầu nghiên cứu môi trường riêng. Không cần dựng lại Excel chỉ để học, vì bước dựng phụ thuộc runtime riêng.

## 4. Bảng phân công còn lại — Nguyễn Thị Yến Nhi

**Nguyễn Thị Yến Nhi — N23DCCN112.** Chủ trì Chương 1–2, nguồn tham khảo, phạm vi và diễn giải chất lượng. Không giao lại rà soát 60 tin, tính checksum hay lập từ điển từ đầu.

| Mã | Việc cụ thể cần làm | File/tài liệu đầu vào | Sản phẩm và tiêu chí hoàn thành | Ước lượng chủ động |
| --- | --- | --- | --- | --- |
| NHI-01 | Đọc hồ sơ nguồn, rà soát tin và bảng độ nhạy; chọn ba ví dụ dễ giải thích | `DATA_SOURCE.md`, `NGUON_QUY_TAC_VA_THIET_KE.md`, `KET_QUA_KIEM_TRA_NHAN.md` | Giải thích được giá rao khác giao dịch; cách ly khác tin giả; IQR khác lỗi; nhãn suy luận khác nhãn chuẩn | 45–60 phút |
| NHI-02 | Viết Chương 1: tên, thực tiễn, ý nghĩa nghiên cứu, một mục tiêu, đối tượng và phạm vi ứng dụng | `DOI_CHIEU_YEU_CAU_BAO_CAO.md`, hồ sơ nguồn | Nêu rõ mẫu lịch sử 2021, người dùng phân tích/học tập, những câu hỏi phục vụ một mục tiêu; không suy rộng thị trường 2026 | Nửa buổi |
| NHI-03 | Viết Chương 2 đủ chiều sâu; phối hợp Đạt phần thuật toán/SQLite và Quỳnh phần trực quan/Excel | Ma trận slide, tài liệu kỹ thuật và mã | Mỗi kỹ thuật có cơ chế, tham số, ví dụ, lý do và giới hạn; công thức đọc được bằng Equation trong Word; trích dẫn nhất quán | 1 buổi |
| NHI-04 | Xác nhận trường/lớp/học phần/giảng viên/STT đề tài/hạn nộp từ thông tin thật của nhóm; đọc chéo Chương 5–6 | Thông báo của lớp/thầy và phần viết của Quỳnh | Bổ sung thông tin bìa đúng; gỡ kết luận quá mức, nhầm trung bình/trung vị hoặc giá rao/giá bán | 30–45 phút, chưa tính chờ thông tin |

Không gọi lượt đọc bằng trợ lý là nhãn do Nhi/cả nhóm cung cấp. Nếu báo cáo không đánh giá độ chính xác nhãn, trình bày giới hạn thay vì phát sinh nhiệm vụ gán nhãn bắt buộc.

## 5. Bảng phân công còn lại — Hứa Như Quỳnh

**Hứa Như Quỳnh — N23DCCN118.** Chủ trì Chương 5–6, tổng hợp định dạng và minh chứng sử dụng. Không phải tính lại thống kê, vẽ lại tám hình hay kiểm lại từng dòng Excel.

| Mã | Việc cụ thể cần làm | File/tài liệu đầu vào | Sản phẩm và tiêu chí hoàn thành | Ước lượng chủ động |
| --- | --- | --- | --- | --- |
| QUYNH-01 | Trong một buổi tổng duyệt, mở dashboard bản cuối, tải lại, xem mặc định và vài bộ lọc; mở Excel trên máy sẽ demo | `DOI_CHIEU_SO_LIEU_TRUC_QUAN.md`, `KIEM_THU_THUC_TE.md`, `NGHIEM_THU_EXCEL.md` | Ghi người/ngày/run_id và kết quả thực. Kiểm mặc định 6.936; TP.HCM + căn hộ 239; bỏ IQR 6.676; một lần CSV. Mở ba trang/bốn biểu đồ Excel; chỉ thử sửa ô trên bản sao nếu cần minh họa tính lại | 20–30 phút |
| QUYNH-02 | Chụp ba trạng thái hữu ích trong cùng buổi: mặc định, bộ lọc có dữ liệu, SQL hoặc Excel | Kịch bản và bảng số liệu có sẵn | Ảnh ở `docs/minh_chung/`, có bộ lọc, n, đơn vị, nguồn, caption và bảng dữ liệu đi kèm; ảnh phải từ bản cuối | Gộp vào buổi trên |
| QUYNH-03 | Viết Chương 5: cài/chạy, demo, kết quả, kiểm thử; Chương 6: trả lời mục tiêu, vận hành/tích hợp/ứng dụng có điều kiện, hạn chế | Toàn bộ hồ sơ minh chứng; nhận bổ sung kỹ thuật từ Đạt, nguồn từ Nhi | Dẫn đúng run_id/số liệu; tách kiểm tự động, xác nhận UI và phần chưa kiểm; kết luận có bằng chứng | 1 buổi |
| QUYNH-04 | Ghép sáu chương, thống nhất bìa/mục lục/danh mục/hình/bảng/nguồn/công thức, đọc chéo Chương 3–4 | Bản viết của cả ba; ma trận yêu cầu | Căn đều thân bài, in đậm có mục đích, Equation đọc được, mọi hình/bảng có tên/dữ liệu và được phân tích trong thân bài; Word/PDF không vỡ bố cục | Nửa–một buổi |

Nếu giao diện có lỗi, ghi bước tái hiện/ảnh rồi chuyển trợ lý sửa; không yêu cầu Quỳnh tự nghiên cứu sửa JavaScript. Nếu không có thời gian thử sửa Excel, ghi đúng “chưa kiểm tính lại trong Excel thật”, vẫn dùng bằng chứng công thức/công cụ đã có với giới hạn rõ.

## 6. Phát triển chuyên nghiệp — những gì đã có và phần tùy chọn

Đã triển khai: raw bất biến/checksum, lineage và quarantine, quy trình chạy một lệnh, kiểm hash phiên bản, kiểm thử, đối soát đa sản phẩm, benchmark giữ số thật, dashboard lọc/tìm/CSV/phân trang, phân cụm có khảo sát k/seed, công thức Excel có kiểm đầu vào. Đợt này bổ sung hồ sơ kỹ thuật, đối soát trung vị độc lập và bộ rà soát định tính có dẫn chứng. Không cần thêm công nghệ để làm báo cáo trông lớn hơn.

Các cải tiến dưới là **tùy chọn sau khi bản báo cáo và demo đã ổn**, chưa coi là đã làm và không buộc mỗi người code một tính năng:

| Hướng | Người đề xuất/đặt câu hỏi | Giá trị cần chứng minh nếu thực hiện | Phần trợ lý có thể làm |
| --- | --- | --- | --- |
| Hiển thị cảnh báo chất lượng hoặc nhóm cần xem lại | Nhi chọn tình huống từ rà soát; Quỳnh góp ý cách đọc | Người dùng hiểu bản ghi chưa xác minh; không biến cờ nghi vấn thành kết luận tin sai | Code quy tắc/giao diện, test hồi quy và dựng lại các sản phẩm liên quan |
| Xuất kèm tóm tắt bộ lọc/run_id/n/đơn vị | Quỳnh chọn cách dùng trong báo cáo; Đạt kiểm tích hợp | File xuất tự giải thích được bối cảnh, khớp KPI/bảng đang lọc | Code xuất dữ liệu, test lọc kết hợp/rỗng, cập nhật hướng dẫn |
| CI và thử môi trường cài mới | Đạt xác định môi trường nhóm cần hỗ trợ | Kiểm từ nguồn pin trên môi trường được ghi rõ; phân biệt workbook runtime riêng | Chuẩn bị cấu hình, chạy kiểm ở môi trường có quyền truy cập; không giả đã chạy GitHub Actions |

Nếu không thực hiện, đưa vào “hướng phát triển” Chương 6. Không cần thêm dự đoán giá, chatbot, tài khoản, bản đồ hay nguồn thời gian thực vì chúng làm lệch phạm vi và phát sinh bằng chứng mới.

## 7. Sáu chương phải có gì

| Chương/chủ trì | Nội dung cần có | Bằng chứng chuẩn bị sẵn |
| --- | --- | --- |
| 1 — Nhi | Tên, vấn đề, ý nghĩa thực tiễn/nghiên cứu, mục tiêu duy nhất, phạm vi ứng dụng | Hồ sơ nguồn, ma trận yêu cầu |
| 2 — Nhi, Đạt/Quỳnh cung cấp kỹ thuật | Chuẩn hóa/làm sạch, thống kê/IQR, log/Z-score/K-means, Python/pandas/NumPy/Matplotlib, SQLite/index, HTML/JS, Excel và kiểm phiên bản | Ma trận slide, hồ sơ thiết kế, thí nghiệm K-means/SQL; giải thích sâu, ví dụ số, công thức và giới hạn |
| 3 — Đạt | Phân tích yêu cầu, kiến trúc/luồng, từ điển, ERD ba bảng, ràng buộc, thiết kế giao diện | Sơ đồ và mô-đun có dữ liệu minh họa trong hồ sơ kỹ thuật |
| 4 — Đạt | Hiện thực từng mô-đun từ lý thuyết/thiết kế: code, I/O, xử lý, lỗi, ví dụ và tích hợp | Mã nguồn, bảng mô-đun, manifest và log kiểm |
| 5 — Quỳnh | Vận hành/cài/chạy, demo dữ liệu thật, kết quả, kiểm thử, benchmark, minh chứng hình/bảng | Kịch bản và danh mục tám hình, audit/assistant checks, UI do nhóm bổ sung |
| 6 — Quỳnh, cả ba duyệt | Đạt mục tiêu đến đâu; độ tin cậy có điều kiện; chạy/tích hợp/ứng dụng được phần nào; giới hạn, hướng phát triển | Kết quả kiểm + rà soát tin; không dùng khẳng định tuyệt đối |

Thân bài viết theo chương có lập luận; tiểu mục chỉ hỗ trợ tổ chức. Mỗi hình/bảng có tên thống nhất, ví dụ `Hình 1: Sơ đồ luồng xử lý dữ liệu`, `Bảng 1: Quy mô dữ liệu trước và sau xử lý`. Căn đều hai bên; công thức ở dạng toán đọc được, không để mã LaTeX thô. Xem yêu cầu chi tiết ở [ma trận báo cáo](DOI_CHIEU_YEU_CAU_BAO_CAO.md).

## 8. Thứ tự hoàn thành và điều kiện chốt

1. Cả ba đọc đúng tài liệu phần mình; chốt cùng phạm vi và mốc dữ liệu. Hỏi những điểm chưa hiểu; không chạy lại toàn quy trình chỉ để đánh dấu nhiệm vụ.
2. Viết song song: Nhi Chương 1–2, Đạt Chương 3–4, Quỳnh Chương 5–6 từ bằng chứng sẵn có. Nếu đổi quy tắc/code thì dừng chốt số, nhờ trợ lý sửa và dựng/kiểm lại trước khi dùng.
3. Một buổi tổng duyệt/chụp ảnh; đọc chéo theo vòng Đạt → Chương 1–2, Nhi → Chương 5–6, Quỳnh → Chương 3–4; sau đó cả ba đọc toàn văn.
4. Quỳnh ghép định dạng; Nhi kiểm nguồn/phạm vi/thông tin bìa; Đạt kiểm phiên bản/SQL/mã. Ghi việc thực làm trong [nhật ký](NHAT_KY_KIEM_TRA_CHEO.md).
5. Mỗi người giải thích được toàn luồng và phần mình viết; không ký hoàn thành thay thành viên. Chưa xác nhận thời hạn nộp nên các ước lượng trên chỉ để xếp lịch.

Đợt cập nhật trợ lý được push lên `main` theo yêu cầu. Công việc nhóm sau đó nên dùng nhánh cá nhân/PR đọc chéo, không force-push. Raw, `.venv`, `node_modules`, `tmp` và file khóa Office không commit. Mời thành viên GitHub cần tài khoản và quyền do chủ repo quản lý; phân công này không đồng nghĩa đã gửi lời mời.
