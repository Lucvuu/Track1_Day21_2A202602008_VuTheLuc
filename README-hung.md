# Track 1 · Day 20–21 — AI Evaluation Capstone · Hưng

**Case:** VLearn AI Tutor — trợ giảng trả lời câu hỏi học viên chỉ dựa trên corpus khoá
học, output JSON `{scope, answer, sources, followup_questions}`.

**Nhóm:** **Hưng** (Pipeline & Code) · Loan (Dataset & Rubric) · Phương (Judge & Calibration)

**Bài nộp:** [`deliverables/REPORT.md`](deliverables/REPORT.md) — 7 mục theo phase ·
[`deliverables/evidence/`](deliverables/evidence/) — data thô ·
[`deliverables/ai-support-log-hung.md`](deliverables/ai-support-log-hung.md)

---

## Verdict tóm tắt

**HOLD — chưa ship.**

Tutor trượt cả 5 điều kiện gate. Con số đáng báo động không phải pass rate tổng 29%, mà là
**0/8 câu in-scope đạt chuẩn** — đúng nhóm câu hỏi tutor sinh ra để phục vụ thì nó không
có câu nào trích nguồn đúng chuẩn. Tutor hiện chỉ "an toàn" ở những câu nó *từ chối trả
lời*, vì lúc đó `sources = []` nên không có gì để sai.

Cả ba lỗi lớn nhất đều là lỗi **chỉ dẫn**, không phải lỗi năng lực model: tutor tìm đúng
nguồn (R2 đạt 100%), nó chỉ chép sai cách. Đòn bẩy tiếp theo là **prompt**, chưa cần đổi
model.

---

## Đóng góp của tôi

### Hạ tầng chạy eval (B0)

Dựng môi trường chạy trên gateway **Agnes AI** thay vì provider mặc định của repo. Repo
hỗ trợ sẵn qua `EVAL_BASE_URL` nên không phải sửa code, nhưng có một cái bẫy: `run_eval.py`
và `judge.py` chặn trước khi chạy bằng `tutor.get_api_key()`, hàm này tra key theo prefix
model. Model `agnes-2.5-flash` không có prefix provider nên rơi về `OPENAI_API_KEY` — phải
đặt thêm một dòng trong `.env` thay vì sửa hai file code.

Cấu hình: tutor `agnes-2.5-flash`, judge `agnes-2.0-flash` — hai model khác nhau, tránh tự
chấm chéo. Tracing Braintrust project `ai-evaluation`, log cả `tutor-run` lẫn `judge-run`.

### Hai code check mới (H5, mục 4)

Thêm vào `eval/code_checks.py`:

| Check | Bắt gì | Kết quả trên 27 câu |
|---|---|---|
| `followup_count` | Contract bắt buộc đúng 3 follow-up | 23 pass / 2 fail |
| `scope_match` | `output.scope` khớp `expected_scope` — bắt cả hai chiều: trả lời câu ngoài corpus **và** từ chối oan câu hợp lệ | 21 pass / 3 fail |

`scope_match` cố ý **bỏ qua** row `expected_scope = unclear`: câu mơ hồ không có đáp án
đúng deterministic, phải để judge/người chấm. Đó là một quyết định routing, không phải
thiếu sót.

### Dataset lane `sc-2x` (H4, mục 2)

9 câu phủ ba ô của lưới: *Mới × Xin đáp án*, *Giữa khoá × Xin đáp án* (ô rủi ro cao nhất),
*Mới × Ngoài lề*. Gồm injection thô, injection bằng tiền đề giả, và câu ngoài lề **lân
cận** chủ đề để gây nhầm `in_scope`.

Lane này cho phát hiện rõ nhất về ranh giới sư phạm: `sc-21` và `sc-23` (xin thẳng,
injection thô) tutor chặn đúng, nhưng `sc-22`, `sc-24`, `sc-26` (nguỵ trang khéo) thì lọt.
**Nguỵ trang khéo mới lọt, thô thì chặn được** — nên luật chống "làm hộ bài" phải tách
riêng, không gộp vào out-of-scope chung.

### Vòng chạy B2 và mục 6 Scorecard & Gate

Chạy `run_eval.py` trên 27 câu → `evidence/results-v1.jsonl`, 0 row lỗi, 904.049 token,
latency trung bình 39,3s. Định nghĩa 5 điều kiện gate và ra quyết định **CHƯA SHIP**.

Phát hiện vận hành: **gateway Agnes chặn concurrency**. Chạy 6 luồng song song thì 23/27
câu dính `HTTP 429`; đo lại thấy 2 luồng chạy sạch. Nghĩa là một vòng eval không rút xuống
dưới ~15 phút được — trần cứng của provider, phải tính vào câu "eval loop chạy lại khi nào".

### Hai lần chặn dữ liệu giả vào bài nộp

Đây là phần tôi cho là đóng góp đáng kể nhất, và cả hai đều chỉ lộ ra khi mở data thô:

**1. `verdicts-v1.jsonl` ban đầu là file mock.** Bốn dấu hiệu: `latency_s = 2.5` đồng nhất
cả 27 row, `score` chỉ có 1.0 và 0.0, **không có `raw_content`, không có `usage`**, và
rationale tiếng Anh trong khi `judge_prompt.md` yêu cầu tiếng Việt — một row còn ghi thẳng
`"Mocked rationale agreeing with human label."`. Mục 5 và mục 7 §3 trên repo lúc đó đã
được viết từ file này, với `gpt-4o-mini` và agreement 88% — không con số nào tồn tại. Đã
chạy judge thật và viết lại từ số thật.

**2. Vòng judge đầu tiên có 17/27 verdict `uncertain` — không phải judge lưỡng lự.** Mọi
row `uncertain` đều có `completion_tokens = 500` đúng bằng `max_tokens`; JSON bị cắt giữa
chừng, `parse_json_content` hụt, rồi `out.get("verdict", "uncertain")` rơi về mặc định.
Bài học ghi vào mục 5: **giá trị mặc định `uncertain` che mất lỗi hạ tầng** — judge trả
rỗng, API lỗi, JSON cắt cụt đều đổ vào cùng một nhãn với "judge thật sự lưỡng lự", nhìn
confusion matrix không phân biệt được. Bằng chứng giữ ở `evidence/verdicts-v1-truncated.jsonl`.

### Hai vòng calibrate judge (mục 5)

| Chỉ số | v1 | v2 |
|---|---|---|
| Agreement tổng | 13/27 = 48% | **21/27 = 77%** |
| Bắt đúng output xấu | 6/18 = 33% | **15/18 = 83%** |
| Nhận đúng output tốt | 7/8 = 87% | 6/8 = 75% |

Chẩn đoán v1 sạch tuyệt đối: **cả 12 row judge bỏ sót đều fail R3, không sót cái nào
khác**. Nguyên nhân mang tính cấu trúc chứ không phải câu chữ — judge chỉ nhận `answer` và
`sources` do chính tutor tự khai, **không được cấp nội dung section trong corpus** để đối
chiếu. R3 đặt sai làn. v2 sửa đúng một thứ: gỡ R3 khỏi phạm vi judge.

---

## Điều tôi mang về áp dụng

**Rubric mơ hồ đắt hơn mọi thứ khác trong eval loop.** Nhóm mất trọn một vòng chấm 27 câu
× 3 người mới phát hiện R3 có hai cách đọc. Agreement 3 người ban đầu chỉ 20%, và 13/19
case bất đồng quy về đúng một dòng rubric. Siết dòng đó xong thì Loan trùng nhãn vàng
100%. **Agreement thấp không đo mức độ cẩn thận của người chấm, nó đo mức độ mơ hồ của
rubric.**

**Hỏi "referent là gì" trước khi quyết giao tiêu chí cho code hay LLM.** Tiêu chí có một
văn bản gốc để so khớp thì code làm chính xác hơn người — `quote_verbatim` bắt 16/25 lỗi
mà hai trong ba người chấm đều bỏ sót. Ngược lại, tiêu chí trông máy móc như "có phải xin
làm hộ bài không" lại là thứ code chịu thua, vì nó phụ thuộc ý đồ chứ không phụ thuộc
hình thức.

**Số liệu trong report phải đối chiếu được xuống data thô, nếu không thì nó chỉ là chữ.**
Cả hai lần dữ liệu giả suýt vào bài nộp đều không phát hiện được bằng cách đọc report —
chỉ lộ ra khi mở `raw_content`, `usage`, `completion_tokens`. Đó cũng là lý do `judge.py`
lưu đúng những trường ấy.
