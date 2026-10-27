# Hướng dẫn gán nhãn và phạm vi kiểm dữ liệu

Phiên bản hướng dẫn 2 — 27/10/2026. Phương án một người gán nhãn; mẫu và code phân tích vẫn giữ bản chốt ngày 26/10/2026. Đơn vị quan sát là tin rao lịch sử, không phải giao dịch đã xác minh. Người đọc chỉ kết luận từ tiêu đề, mô tả và hai trường giá/diện tích gốc. Không gọi điện, xác minh pháp lý hoặc dùng giá hiện nay để sửa tin.

## 1. Các nhãn

| Cột | Giá trị hợp lệ và cách hiểu |
|---|---|
| transaction_label | `sale`: bán rõ trong nguồn; `rental`: cho thuê; `mixed`: cả bán và thuê hoặc hai trường mâu thuẫn chưa giải quyết; `transfer`: sang hoạt động kinh doanh/hợp đồng thuê; `unknown`: không đủ căn cứ. |
| property_label | `house`: nhà, biệt thự, dãy trọ bán cả công trình; `land`: đất là tài sản chính, kể cả ghi bán đất tặng nhà; `apartment`: một căn hộ, gồm căn hộ chung cư mini; `other`: officetel, tòa căn hộ dịch vụ hoặc tài sản khác; `unknown`: thiếu thông tin hoặc mâu thuẫn. Không gán house chỉ vì có chữ nhà trong địa danh. |
| price_basis | `total`, `per_m2`, `per_block` (100/1000m2, sào/công...), `partial_payment`, `rental`, `transfer`, `foreign`, `unknown`. Giá USD ghi foreign, không đổi tỷ giá. |
| verified_price_vnd | Chỉ ghi tổng giá rao VND khi xác định được một tài sản và cơ sở giá rõ; trường này không xác nhận giá giao dịch. Không tự nhân 1000, không lấy khoản trả trước suy ra tổng giá nếu còn mơ hồ. Ghi phép đổi đơn vị rõ trong evidence. Không xác định thì để trống. |
| area_basis | `land`, `usable`, `recognized`, `gross_floor`, `apartment_unspecified`, `unknown`. Không trộn đất, sàn, công nhận, thông thủy/tim tường. Có thể ghi chi tiết hơn trong evidence. |
| verified_area_m2 | Diện tích của tài sản/đại lượng được nêu rõ. Thiếu hoặc mâu thuẫn thì để trống. Không dùng tích ngang×dài để tự thay diện tích pháp lý. |
| conflict_status | `yes`: có thông tin bất nhất rõ; `no`: chưa thấy bất nhất rõ trong nguồn; `uncertain`: khác đại lượng, nhiều tài sản, số gần đúng hoặc thiếu căn cứ. `no` không có nghĩa tin đã xác thực. |
| usability | `usable`: có thể giữ theo phạm vi phân tích, chưa thấy lý do loại rõ; `review`: cần rà soát thêm; `exclude`: ngoài phạm vi hoặc có mâu thuẫn/chưa xác định cơ sở giá khiến chưa thể dùng. Đây là nhận xét của người đọc, không tự sửa pipeline. |
| evidence | Ghi đoạn trích ngắn và giải thích quyết định. Không chép số điện thoại, tên người liên hệ, địa chỉ chi tiết. |
| reviewer, reviewed_on | Tên/mã người thực sự đọc và ngày đọc. Không ghi tên người khác, không ghi AI thành người. |

`unknown` về giao dịch không mặc nhiên là `exclude`: người đọc ghi thiếu bằng chứng, còn chính sách sale_assumed của dự án được đánh giá riêng. Nhãn unknown theo tiêu đề của chương trình cũng không nhất thiết là lỗi: người đọc có thêm mô tả. Báo riêng mức bao phủ và nhầm nhãn, không đánh đồng hai nhiệm vụ.

## 2. Quy tắc đọc

1. Đọc tiêu đề, mô tả, giá, diện tích. Bỏ qua phần giới thiệu môi giới không liên quan tới tài sản chính.
2. Xác định tài sản đang rao, khác với công viên/chung cư/nhà thờ ở gần hoặc công trình có thể xây trong tương lai.
3. Xác định bán, thuê, sang kinh doanh hoặc thiếu căn cứ. “Tiện cho thuê” chỉ nói công năng. “Đang cho thuê” có thể là thu nhập của nhà đang bán. Nếu tiêu đề và mô tả trái nhau, ghi review/mixed, không tự đoán.
4. Kiểm tổng giá khác giá/m2, giá theo lô diện tích, trả trước, giá thuê, hoa hồng, bảo hiểm và giá cũ. Không chọn một giá trong danh sách nhiều căn mà chưa nối được diện tích tương ứng.
5. Phân biệt diện tích đất, công nhận, xây dựng, sàn, thông thủy/tim tường. Hai đại lượng khác nhau không tự động là mâu thuẫn.
6. Giá thấp/cao bất thường là lý do kiểm, không phải bằng chứng sai. Không dùng kiến thức thị trường để tự sửa đơn vị.
7. Điền nhãn, bằng chứng và người đọc. Các con số xác nhận không rõ phải để trống, không điền 0.

## 3. Thiết kế mẫu đã cố định

- Nguồn SHA-256: `ef39f153f48a55af07baa86883cd9036652f6d52232fed0be6e8991c7a5bf811`.
- Mốc dữ liệu cũ: `20261016T015620Z-f2e661a6`.
- Ba nhóm: kept_assumed, kept_other, rejected. Mỗi nhóm 40 development + 20 evaluation.
- Tổng 180 tin: 120 phát triển, 60 đánh giá. Seed 42; danh sách và số lượng từng tầng ở sample_manifest.json.
- Loại 67 ID đã rà soát/biết trước khỏi cả mẫu mới. Không bao gồm các dòng trùng chính xác đã loại bởi pipeline.
- Trong mỗi nhóm, chia theo loại dự đoán × cờ rủi ro. Chọn cân bằng luân phiên giữa các tầng còn tin, xáo ID bằng seed cố định. Phân bổ 20 evaluation bằng phần nguyên và phần dư lớn nhất theo số mẫu từng tầng.
- Cờ rủi ro dùng trạng thái IQR của bản sạch nếu có và một số cờ parse/nguồn. Tin rejected không có IQR nên dùng cờ parse/nguồn. Cờ lấy mẫu không phải nhãn đúng/sai.
- Mẫu không tự trọng số. Báo theo nhóm/tầng; không dùng tỷ lệ thô 180 tin để suy ra tỷ lệ toàn bộ 9004 tin. Mẫu này cũng loại những ID đã biết và không đại diện tin trùng.
- Chưa bảo đảm đã loại hết quảng cáo gần trùng/cùng tài sản. Kiểm trùng ngữ nghĩa cần làm riêng. Đây là mẫu giữ lại cho đánh giá quy tắc, không phải kiểm định trên một nguồn dữ liệu mới độc lập.

## 4. Cách dùng các file

- `private/development_blank.csv` hoặc workbook phát triển: bảng trống để nhóm đọc 120 tin nếu muốn.
- `AI_REVIEW_DEVELOPMENT_120.csv`: 120 nhận xét do Codex AI thực hiện, là tài liệu phát triển, không phải gold labels hoặc đánh giá độc lập. Các cột human vẫn trống ở bảng người đọc.
- `private/evaluation_reader_A.csv` và `private/DANH_GIA_60_NGUOI_A.xlsx`: chỉ một người đọc 60 tin. Không cần file B. Giữ bản gán nhãn ban đầu và bản sửa riêng; ghi người đọc/ngày áp dụng cho toàn bộ bảng nếu cùng một người thực hiện.
- Bảng người đọc không có nhãn/cờ của chương trình hoặc nhóm lấy mẫu. `sample_manifest.json`, `private/baseline_predictions.json` và bảng so sánh dành cho người điều phối, không gửi cho người đánh giá trước khi họ chốt nhãn.
- CSV là dữ liệu máy đọc; khi mở bằng Excel dùng nhập UTF-8 và định dạng các cột nguồn là Text. Workbook đã định dạng văn bản nguồn và có danh sách chọn nhãn.
- Tab Nguon trong workbook giữ mô tả đầy đủ theo các đoạn có row_id/part; đọc đủ tất cả đoạn của tin. CSV giữ nguyên mô tả trong một ô.

## 5. Ranh giới của phiên bản này

Bước 1.1–1.3 đã chuẩn bị. Bước 1.4 là đọc bằng AI, không thay nhãn tham chiếu của người thật. Bước 1.5 có sửa code/test dựa trên development và ca hồi quy cũ. Bước 1.6 chốt bằng hash mã nguồn và danh sách mẫu. Ngày 27/10 đã nhận một bảng người đọc và phát hiện các ô cần rà lại. Chưa chốt nhãn hoặc tính accuracy. Không sửa code phân loại theo bảng đánh giá này. Nếu sửa tiếp sau khi xem nhãn evaluation, phải đổi trạng thái mẫu đó thành dữ liệu phát triển và chuẩn bị mẫu đánh giá khác.

Các số cũ 6936 tin, biểu đồ, dashboard và báo cáo đang là baseline cũ. Chưa chạy lại toàn dự án ở bước 1.6. Trước khi nộp bản mới phải hoàn thành đánh giá, chạy lại và đồng bộ các sản phẩm.

## 6. Phương án một người và trạng thái hiện tại

Một thành viên đọc đủ nguồn của 60 tin. Chưa xem dự đoán chương trình trước khi chốt bản nhãn đầu; nếu điều kiện này không được đáp ứng, ghi rõ giới hạn. Không tính hệ số đồng thuận nhiều người và không tính AI là người thứ hai.

Bảng đã gửi ngày 27/10 đang được rà lỗi nhập số và tính nhất quán, chưa phải nhãn cuối. Người đọc xác nhận lại các ô được đánh dấu; trợ lý không tự thay đáp án. Báo cáo sau này nêu một người gán nhãn, có AI hỗ trợ kiểm chất lượng nếu đã dùng phản hồi này, và nguy cơ sai sót chủ quan.

Tên file A được giữ để không làm nhầm bảng đang dùng. Tab HuongDan trong workbook mẫu phát hành ngày 26/10 có câu về hai người; phần đó đã được thay bằng hướng dẫn một người tại tài liệu này. Không yêu cầu đọc file B hoặc thống nhất giữa hai người nữa.

Bản chốt cũ giữ ở history/FREEZE_MANIFEST_20261026.json. Bản chốt hiện tại chỉ cập nhật hồ sơ/quy trình một người và danh sách file trống; hash mã phân tích, test, mẫu và nhận xét phát triển không đổi. Không dùng cập nhật hồ sơ để coi code đã được tái đánh giá.
