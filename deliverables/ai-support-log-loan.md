# AI Support Log — Loan (lane Dataset & Rubric)

> Ghi lại tôi đã dùng AI ở những bước nào khi làm deliverables. Trung thực là một phần của
> bài nộp — không ai làm một mình, quan trọng là giữ được quyền kiểm soát chất lượng.

Công cụ dùng: **Claude Code (Opus)** chạy thẳng trong repo, có quyền đọc file corpus và
chạy script kiểm chứng. Đây là điểm khác biệt so với hỏi chatbot ngoài: mọi khẳng định
đều bắt được nó dẫn về file thật trong repo, nên kiểm chứng rẻ hơn nhiều.

| # | Bước | AI dùng để làm gì | Tôi kiểm chứng thế nào |
|---|---|---|---|
| 1 | P1 — Input Grid (mục 1) | Dựng lưới Persona × Intent 3×6, đề xuất ô nào test / cân nhắc sau / loại, kèm lý do từng ô | Bắt AI dẫn nguồn về slide `s26`–`s29` trong `day19-20-deck.md` rồi tự mở đọc lại. Quyết định cuối về ô nào là "rủi ro cao nhất" là của tôi — chọn *Giữa khoá × Xin đáp án* vì hiểu bối cảnh lớp, AI ban đầu xếp ngang hàng với ô *Ôn thi × Tổng hợp* |
| 2 | P1 — lane `sc-1x` (8 câu) | Soạn bản nháp 8 câu hỏi in-scope theo 8 ô đã chọn, kèm `metadata.slide` | Mở đúng 6 vị trí slide (`s15`, `s16`, `s32`, `s35`, `s40`, `s48`) đọc nội dung thật để chắc câu hỏi bám đúng slide. Sửa văn phong 4 câu cho giống giọng học viên thật — bản AI viết quá trang trọng |
| 3 | P1 — phát hiện lỗi `manifest.json` | AI đối chiếu và chỉ ra `manifest.json` lệch `section_id` so với header thật trong file `.md`; `tutor.py` đọc file `.md` chứ không đọc manifest | Tự chạy `grep "^## sNN —"` trên file slide để xác nhận. Đây là phát hiện cứu cả nhóm — Phương đã gán sai 3 câu vì tra manifest, tôi bắt được khi gộp lane |
| 4 | P1 — gộp dataset (L4) | Viết script kiểm: `scenario_id` trùng lặp, thiếu `input`, và đối chiếu từng cặp `slide.id` + `slide.title` với header thật | Đọc output script, tự quyết 3 chỗ sửa cho lane `sc-3x` của Phương và ghi `[Loan sửa khi gộp]` vào note để truy vết |
| 5 | P3 — Rubric v1 (mục 3) | Soạn bảng 8 tiêu chí R1–R8, đề xuất cái nào blocker | Ép AI chỉ dựng tiêu chí từ thứ **đã tồn tại thật** trong repo (5 code check của Hưng, judge prompt của Phương, contract trong `SYSTEM_PROMPT`), không bịa tiêu chí cho đẹp bảng. R6 (ranh giới sư phạm) là tiêu chí tôi yêu cầu thêm vì bộ gợi ý của bài lab không có, mà đó lại là rủi ro số một của tutor giáo dục |
| 6 | P4 — Routing Map (mục 4) | Áp quy tắc "referent kiểm chứng được" của slide `s41` vào từng tiêu chí | Đọc lại `s41` để xác nhận AI không diễn giải sai quy tắc. Tự kiểm chứng lại trên `results-v1.jsonl` và phát hiện `sc-22` bị code chấm fail oan |
| 7 | **P2 — Chấm nhãn tay (B3)** | **Không dùng AI.** 27 nhãn trong `evidence/labels-loan.csv` do tôi tự bấm trong `report.html`, đọc từng câu trả lời và note lý do | Đây là chuẩn vàng để đo judge — nhờ AI chấm hộ là làm hỏng luôn ý nghĩa phép đo. AI chỉ được dùng **sau** khi tôi chấm xong, để phân tích bất đồng |
| 8 | P4 — phân tích bất đồng (B4) | Chạy `agreement.py`, truy nguyên nhân bất đồng, tính hệ quả pass rate của 3 phương án xử lý R3 | Đọc lại từng ca. Số liệu 13/13 ca bất đồng đều do R3 là do AI thống kê từ note của chính tôi — kiểm lại được bằng cách mở file nhãn |
| 9 | P4 — bắt lỗi `verdicts-v1.jsonl` mock | AI đối chiếu file với `judge.py` và chỉ ra nó không thể sinh ra từ script thật | Tự mở file xem: 27 row chỉ có 3 chuỗi `rationale` khác nhau, một chuỗi ghi thẳng `"Mocked rationale..."`, `latency_s` = 2.5 đồng loạt, thiếu `raw_content` và `usage` mà `judge.py` luôn ghi |

## Phần nào AI gợi ý mà tôi bác bỏ

**Phương án xử lý R3 ở phiên B4.** AI khuyến nghị **phương án C** — tách R3 làm hai mức
(quote sai nội dung = blocker, quote ghép mảnh = điểm cộng), lập luận rằng gộp hai lỗi
khác mức nguy hại vào một nhãn là mất thông tin.

Tôi chọn **phương án A — giữ R3 blocker nguyên khối**, dù biết nó ăn mất 22 điểm phần
trăm pass rate (52% xuống 30%). Lý do AI không có đủ bối cảnh để cân: đây là vòng eval
**đầu tiên** của sản phẩm. Ở vòng đầu, một tiêu chí chặt và đơn giản mà ba người chấm ra
cùng kết quả có giá trị hơn một tiêu chí tinh vi mà mỗi người hiểu một kiểu — đúng bài học
`s23` (thu hẹp đến khi hai người chấm độc lập cho cùng kết quả). Phương án C sẽ đẻ thêm
một ranh giới mới cần định nghĩa, trong khi nhóm còn chưa thống nhất nổi ranh giới cũ.
Tách R3 để dành cho vòng sau, khi đã có dữ liệu chấm lại.

**Cách trình bày nhãn `uncertain`.** Ban đầu tôi định dồn các câu khó quyết vào
`uncertain`. AI chỉ ra làm vậy sẽ khiến agreement đẹp giả tạo — ba người cùng né một chỗ
thì trông như đồng thuận, mà rubric vẫn mơ hồ nguyên. Tôi giữ lại đúng 1 row `uncertain`.
Cái này AI đúng, tôi đổi ý.

## Phần nào tôi hoàn toàn tự làm

- **Toàn bộ 27 nhãn người** trong `evidence/labels-loan.csv` — bấm tay trong `report.html`,
  không nhờ AI chấm hộ dòng nào. 27 nhãn này sau đó thành nhãn vàng của cả nhóm.
- **Quyết định giữ R3 là blocker** ở phiên B4 (xem phần bác bỏ ở trên).
- **Chủ trì phiên tranh luận B4** và quyết cách đọc `sc-22`: code chấm fail nhưng tutor
  thực sự từ chối đúng, nên giữ dataset nguyên và chốt cách đọc thay vì sửa
  `expected_scope` — sửa là `results-v1.jsonl` hết khớp input, mất cả vòng chạy.
- **Quyết định không sửa nhãn hộ Phương** khi phát hiện 3 row chấm lệch dữ liệu thật
  (`sc-15`, `sc-25` JSON vỡ nhưng gán `pass`; `sc-24` tutor làm hộ bài nhưng ghi "từ chối
  khéo"). Tôi chỉ đổi tên file `labels.csv` thành `labels-phuong.csv` và báo lại, vì sửa
  nhãn hộ là phá hỏng tính độc lập của phép đo đồng thuận.

## Điều tôi rút ra về cách dùng AI trong việc này

AI mạnh nhất ở chỗ **kiểm chứng cơ học**: đối chiếu 79 quote với corpus, dò 27 `slide.id`
với header thật, phát hiện file `verdicts` là mock qua dấu vết kỹ thuật. Những việc này
làm tay thì vừa lâu vừa dễ sót, và đúng ba lần trong bài này nó bắt được lỗi mà con người
đã bỏ qua.

Chỗ tôi phải tự quyết là những chỗ có **đánh đổi mà không có đáp án đúng**: R3 chặt hay
lỏng, có sửa nhãn hộ đồng đội không, dataset đã khoá thì sửa hay giữ. AI trình bày được
đủ phương án và hệ quả từng phương án bằng số, nhưng cân giữa chúng cần bối cảnh mà nó
không có — nhóm đang ở vòng eval đầu tiên, còn bao nhiêu thời gian, đồng đội đang mắc ở
đâu.
