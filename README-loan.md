# Track 1 · Day 20–21 — AI Evaluation Capstone · Loan

**Case:** VLearn AI Tutor — trợ giảng trả lời câu hỏi học viên chỉ dựa trên corpus khoá
học, output JSON `{scope, answer, sources, followup_questions}`.

**Nhóm:** Hưng (Pipeline & Code) · **Loan** (Dataset & Rubric) · Phương (Judge & Calibration)

**Bài nộp:** [`deliverables/REPORT.md`](deliverables/REPORT.md) — 7 mục theo phase ·
[`deliverables/evidence/`](deliverables/evidence/) — data thô ·
[`deliverables/ai-support-log-loan.md`](deliverables/ai-support-log-loan.md)

---

## Verdict tóm tắt

**HOLD — chưa ship.**

Tutor trượt cả 5 điều kiện gate. Nhưng con số đáng báo động không phải pass rate tổng 29%,
mà là **0/8 câu in-scope đạt chuẩn**: đúng nhóm câu hỏi tutor sinh ra để phục vụ thì nó
không có câu nào trích nguồn đúng chuẩn. Tutor hiện chỉ "an toàn" ở những câu nó *từ chối
trả lời* — vì lúc đó `sources = []` nên không có gì để sai.

Nguyên nhân gốc: **quote không nguyên văn**. Chỉ 17/79 nguồn (22%) khớp nguyên văn với
section được trích; tutor ghép 2–3 dòng rời của cùng một slide, nối bằng dấu hai chấm, rồi
đóng gói thành `quote`. Nội dung không sai, nhưng học viên bấm vào nguồn sẽ không tìm thấy
câu đó.

Cả ba lỗi lớn nhất đều là lỗi **chỉ dẫn**, không phải lỗi năng lực model — tutor tìm đúng
nguồn (R2 đạt 100%), nó chỉ chép sai cách. Nên đòn bẩy tiếp theo là **prompt**, chưa cần
đổi model.

---

## Đóng góp của tôi

Tôi cầm lane **Dataset & Rubric**: thiết kế coverage, chốt dataset, viết rubric, chia làn
chấm, và chủ trì phiên đồng thuận nhãn người.

### Sản phẩm tôi chịu trách nhiệm chính

| Deliverable | Nội dung |
|---|---|
| **REPORT mục 1** — Input Grid | Lưới Persona × Intent 3×6 theo khung slide `s26`–`s29`, chọn có chủ đích 14 ô, loại 5 ô kèm lý do. Chia quota 3 lane |
| **REPORT mục 2** — Dataset v1 | Gộp 3 lane → `dataset-v1.jsonl` (27 câu), review chéo, bảng 27 scenario |
| **REPORT mục 3** — Rubric v1 | 8 tiêu chí R1–R8, 6 blocker, định nghĩa pass cho out-of-scope / adversarial / unclear |
| **REPORT mục 4** — Routing Map | Map R1–R8 sang code / judge / người theo quy tắc referent của `s41` |
| `evidence/dataset-sc1x-loan-draft.jsonl` | 8 câu lane in-scope |
| `evidence/labels-loan.csv` | 27 nhãn người, **tự chấm tay**, sau thành nhãn vàng của nhóm |
| `evidence/b4-disagreement-analysis.md` | Phân tích bất đồng, 3 phương án kèm hệ quả pass rate |
| `evidence/verify-report-numbers.py` | Script đối chiếu mọi số trong REPORT với data thô |

### Ba việc tôi cho là đáng kể nhất

**1. Bắt lỗi `manifest.json` lệch corpus — cứu cả nhóm khỏi dataset hỏng.**
`tutor/corpus/manifest.json` ghi `section_id` lệch so với header thật trong file `.md`, mà
`tutor.py` lại parse thẳng file `.md`. Ai tra manifest để điền `metadata.slide` đều gán
sai. Phát hiện khi soạn lane `sc-1x`, báo cả nhóm, và bắt được thật 3 câu lane `sc-3x` khi
gộp — sửa trước khi chốt dataset. Slide sai nạp thẳng vào prompt của **cả tutor lẫn judge**,
để nguyên là tutor bị chấm fail oan còn judge chấm theo bối cảnh sai.

**2. Truy nguyên nhân bất đồng nhãn người về đúng một dòng rubric.**
Đồng thuận 3 người chỉ 20%, loan-vs-hung 37% — con số xấu. Nhưng khi truy note thì
**13/13 ca bất đồng đều quy về R3**, không một ngoại lệ. Không phải ba người "cảm nhận
khác nhau" mà là hai bên **làm hai việc khác nhau**: tôi mở `sources` đối chiếu ngược vào
corpus, hai bạn đọc `answer` thấy đúng rồi suy ra quote hợp lệ. Mơ hồ nằm ở *thao tác
chấm*, không nằm ở câu chữ tiêu chí — nên bản sửa rubric không đụng định nghĩa R3 mà thêm
một dòng thao tác bắt buộc.

**3. Chọn giữ R3 chặt dù nó ăn mất 22 điểm pass rate.**
Tôi tính trước hệ quả 3 phương án: giữ R3 blocker → 30%, hạ xuống điểm cộng → 52%, tách
hai mức → phải chấm lại. AI hỗ trợ khuyến nghị phương án tách. Tôi chọn giữ nguyên khối,
vì đây là vòng eval **đầu tiên** — một tiêu chí chặt mà ba người chấm ra cùng kết quả có
giá trị hơn một tiêu chí tinh vi mà mỗi người hiểu một kiểu (bài học `s23`). Bằng chứng
độc lập đứng về phía siết chặt: `check_quote_verbatim` thuần Python, không biết gì về nhãn
người, cho cùng kết luận.

### Việc tôi từ chối làm

- **Không chấm nhãn hộ Phương** khi phát hiện 3 row chấm lệch dữ liệu thật. Chỉ đổi tên
  file và báo lại — sửa nhãn hộ là phá tính độc lập của phép đo đồng thuận.
- **Không dùng AI chấm 27 nhãn.** Đó là chuẩn vàng để đo judge; nhờ AI chấm là làm hỏng
  luôn ý nghĩa phép đo.
- **Không dựng số judge khi hết quota API.** Vòng đầu `verdicts-v1.jsonl` là file mock —
  27 row chỉ có 3 `rationale`, một chuỗi ghi thẳng `"Mocked rationale agreeing with human
  label."`, `latency_s` = 2.5 đồng loạt, thiếu `raw_content`/`usage` mà `judge.py` luôn
  ghi. Dữ liệu được dựng để *trùng nhãn người*, nên con số 89% agreement không phải phép
  đo. Tôi báo nhóm thay vì để nó vào bài. Hưng chạy lại thật: **48%**, và bắt thêm được
  một lỗi hạ tầng đáng giá (`max_tokens=500` cắt JSON, `judge.py` rơi về mặc định
  `uncertain`).

---

## Điều tôi mang về

**Agreement thấp không đo mức cẩn thận của người chấm, nó đo mức mơ hồ của rubric.** 20%
đồng thuận mà truy được nguyên nhân về một dòng còn dùng được hơn 90% mà không ai biết vì
sao trùng nhau.

**Hỏi "referent là gì" trước khi quyết giao tiêu chí cho code hay LLM.** Routing map tôi
viết *trước* khi chạy judge đã dự đoán R3 phải giao code vì judge không được cấp văn bản
gốc để đối chiếu. Kết quả thực nghiệm: judge chấm **pass cho 14/19 row có quote sai**. Quy
tắc một câu ở slide `s41` tiết kiệm được cả một vòng judge tốn tiền.

**Pass rate phải đọc theo slice.** Con số 29% không nói lên gì. Chỉ khi tách theo lane mới
thấy tutor pass vì nó *từ chối*, và fail sạch ở đúng nhóm câu nó sinh ra để phục vụ.
