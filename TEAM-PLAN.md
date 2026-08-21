# TEAM PLAN — Capstone AI Evaluation (K3 Track 1 · Day 20–21)

**Case:** VLearn AI Tutor · **Repo:** `K3-Track1-Day20-21-AI-Evaluation/`
**Team:** Hưng · Loan · Phương

---

## 0. Bối cảnh — bài này yêu cầu gì

Bạn đóng vai **PM chịu trách nhiệm chất lượng** cho "VLearn AI Tutor", chạy trọn một
eval loop trên tutor thật rồi ra quyết định **ship / hold**.

Sản phẩm bị đánh giá đã có sẵn: `tutor/tutor.py` — tutor thật, tool-calling `kb_search`,
BM25 trên corpus 18 tài liệu, output JSON `{scope, answer, sources, followup_questions}`.
**Không sửa tutor** — bạn xây bộ máy chấm nó.

### 6 phase → 7 mục trong `deliverables/REPORT.md`

| Phase | Làm gì | Lệnh | Sản phẩm |
|---|---|---|---|
| P1 Input Grid | lưới "ai hỏi × hỏi kiểu gì" | — | mục 1 |
| P2 Dataset + baseline người | viết `dataset.jsonl`, chạy tutor, 3 người chấm tay độc lập | `run_eval.py` → `report.py` → `agreement.py` | mục 2, `dataset-v1.jsonl`, `results-v1.jsonl`, `labels-*.csv` |
| P3 Rubric | tiêu chí pass/fail, cái nào là blocker | — | mục 3 |
| P4 Routing + calibrate judge | chia việc code / LLM judge / người; sửa judge prompt nhiều vòng | `code_checks.py`, `judge.py` | mục 4–5, `judge-prompt-vN.md`, `verdicts-vN.jsonl` |
| P5 Đọc kết quả | pass rate theo slice, cost, latency | `report.py` | mục 6 |
| P6 Verdict | SHIP / SHIP WITH CONDITIONS / HOLD | — | mục 7 |

### Ba thứ bắt buộc ở MỌI bước

> **đầu vào** + **data thô đầu ra** + **quyết định kèm vì sao**
> Thiếu một trong ba → bước đó coi như chưa làm.

### Hai điều dễ mất điểm nhất

- **Tracing bắt buộc** — phải có `BRAINTRUST_API_KEY` hoặc `LANGSMITH_API_KEY` trong
  `.env` **TRƯỚC khi chạy**. Chạy xong mới cắm key = không có trace = phải chạy lại.
- **Version hoá evidence** — mỗi lệnh **ghi đè** output của nó. Chạy xong 1 vòng phải
  `cp` ngay vào `deliverables/evidence/` với hậu tố `-v1`, `-v2`.

### Lưu ý về hình thức nộp

Cấu trúc nộp là `Track1_Day21_MHV_HoVaTen/` → **mỗi người nộp một bộ riêng**,
`ai-support-log.md` phải của chính người nộp.
→ **Evidence dùng chung, REPORT.md mỗi người tự viết.**

---

## 1. Chiến lược chia việc

Eval loop vốn **tuần tự** (dataset → run → nhãn người → judge → verdict), không chia
song song hoàn toàn được. Cách tối ưu:

1. **Chia theo lane sở hữu** — mỗi người làm chủ 1 tầng, không giẫm chân file của nhau.
2. **Ép mọi thứ không phụ thuộc results lên trước** — grid, rubric, judge prompt v1,
   `check_*` tuỳ biến đều viết được khi chưa có dữ liệu.
3. **Smoke run 5 câu ví dụ ngay phút thứ 10** — để 2 lane còn lại có `results.jsonl` thật
   mà phát triển, trong khi dataset lớn vẫn đang viết.
4. **Chỉ 1 người được chạy `run_eval.py`** — 3 người cùng chạy sẽ có 3 file
   `results.jsonl` khác nhau, nhãn người của A không so được với verdict judge chạy trên
   output của B → toàn bộ calibration vô nghĩa.

### Phân lane

| | **Hưng** — Pipeline & Code | **Loan** — Dataset & Rubric | **Phương** — Judge & Calibration |
|---|---|---|---|
| **Sở hữu file** | `.env`, `code_checks.py`, `results-vN.jsonl`, `braintrust-link.md` | `dataset-v1.jsonl` | `judge_prompt.md`, `verdicts-vN.jsonl` |
| **Mục REPORT chủ trì** | 6 (Scorecard & Gate) | 1, 2, 3 (Grid, Dataset, Rubric) | 4, 5 (Routing, Calibration) |
| **Việc chính** | setup env + tracing, chạy 44 test, chạy mọi vòng `run_eval`, viết 2 hàm `check_*` riêng, tổng hợp cost/latency/pass rate, quản version evidence | vẽ input grid, quota câu theo ô lưới, review chống trùng ý, rubric v1 + bảng blocker, routing map | soạn judge prompt v1 từ rubric, chạy `judge.py`, đọc confusion matrix, ≥2 vòng sửa prompt, viết diff v1→v2 |

**Vì sao chia thế này:** Hưng cầm phần duy nhất tốn tiền và cần key → tránh 3 người cùng
đốt quota. Loan cầm phần *không cần chạy code* → làm được ngay cả khi chưa cài xong môi
trường. Phương cầm phần cần vòng lặp nhiều nhất → không bị ai chặn sau khi có golden labels.

---

## 2. Master timeline (~8h)

| Block | Giờ | Phase | **Hưng** | **Loan** | **Phương** |
|---|---|---|---|---|---|
| **B0** | 0:00–0:30 | P0 Setup | `.env` + 2 API key + tracing key → `pip install -r requirements.txt` → `python tests/test_eval_kit.py` (44 test) → smoke run 5 câu example | Vẽ **Input Grid**: nhóm user × intent, đánh dấu ô rủi ro cao / tần suất cao | Đọc `judge_prompt.md` mẫu + module 07/09 trong corpus, phác 4–5 tiêu chí chấm |
| 🔒 | | | **SYNC 1** — `results.jsonl` (5 câu) có thật → Loan + Phương có dữ liệu mẫu | | |
| **B1** | 0:30–1:45 | P1 Dataset | Viết 8–10 câu lane `sc-2x` + code 2 hàm `check_*` mới | Viết 8–10 câu lane `sc-1x` + gộp/review chống trùng ý | Viết 8–10 câu lane `sc-3x` + soạn **judge prompt v1** |
| 🔒 | | | **SYNC 2** — Loan gộp 3 lane + review chéo 15' → `dataset.jsonl` **CHỐT** (24–30 câu) | | |
| **B2** | 1:45–2:15 | P2 Run | **Chỉ Hưng chạy**: `run_eval.py` full → `code_checks.py` → copy `results-v1.jsonl` vào evidence + phát tán | Chờ → viết trước bảng scenario (mục 2) | Chờ → hoàn thiện judge prompt v1 |
| **B3** | 2:15–3:15 | P2 Baseline | Chấm tay độc lập → `labels-hung.csv` | Chấm tay độc lập → `labels-loan.csv` | Chấm tay độc lập → `labels-phuong.csv` |
| | | | ⚠️ **Không nói chuyện, không nhìn bài nhau** — mỗi người browser riêng | | |
| **B4** | 3:15–4:00 | P2+P3 | Chạy `agreement.py labels-*.csv`, ghi % từng cặp | **Chủ trì** tranh luận case bất đồng → chốt **Rubric v1** + `labels.csv` golden | Ghi biên bản: tiêu chí nào gây bất đồng nhiều nhất |
| 🔒 | | | **SYNC 3** — `labels.csv` golden → Phương mở khoá vòng calibrate | | |
| **B5** | 4:00–5:30 | P4+P5 | Scorecard: pass rate/tiêu chí, cost/vòng, latency TB → định nghĩa **gate** | **Routing Map** (mục 4): code / judge / người + lý do | `judge.py` v1 → matrix → sửa prompt → v2 → v3. Copy evidence **mỗi vòng** |
| **B6** | 5:30–8:00 | P6 Verdict | Tự viết `REPORT.md` + `ai-support-log.md` + `README` cá nhân | Tự viết `REPORT.md` + `ai-support-log.md` + `README` cá nhân | Tự viết `REPORT.md` + `ai-support-log.md` + `README` cá nhân |
| | | | ⚠️ Evidence dùng chung — **verdict và lập luận phải của riêng từng người** | | |

### Chia lane dataset (chống trùng ý)

| Lane | Người | Loại câu | Số câu |
|---|---|---|---|
| `sc-1x` | Loan | in-scope khái niệm + in-scope bám slide (deixis "giải thích đoạn này") | 8–10 |
| `sc-2x` | Hưng | out-of-scope + adversarial (xin đáp án, prompt injection, hỏi ngoài corpus) | 8–10 |
| `sc-3x` | Phương | mơ hồ + **near-miss** (câu dễ khiến judge chấm sai) ← vàng để calibrate | 8–10 |

---

## 3. Task chi tiết theo từng người

### 👤 Hưng — lane Pipeline & Code

| # | Phase | Task | Input | Output | Mục REPORT |
|---|---|---|---|---|---|
| H1 | P0 | Setup env: 2 key khác họ (tutor ≠ judge) + `BRAINTRUST_API_KEY`/`LANGSMITH_API_KEY` | `.env.example` | `.env` (không commit) | — |
| H2 | P0 | Chạy 44 test offline + smoke run 5 câu | `data/dataset.example.jsonl` | `results.jsonl` (5 câu), link trace | — |
| H3 | P0 | Tạo project Braintrust/LangSmith, lấy link | — | `evidence/braintrust-link.md` | — |
| H4 | P1 | Viết 8–10 câu lane `sc-2x`: out-of-scope + adversarial | Input Grid của Loan | phần dataset của Hưng | 2 |
| H5 | P1 | Thêm 2 hàm `check_*` vào list `CHECKS` | `eval/code_checks.py` | `code_checks.py` đã sửa | 4 |
| H6 | P2 | **Chạy `run_eval.py` full** (độc quyền) | `dataset.jsonl` chốt | `evidence/results-v1.jsonl` | 6 |
| H7 | P2 | Chạy `code_checks.py`, ghi bảng pass/fail 5 rule | `results-v1.jsonl` | output làn code | 4, 6 |
| H8 | P2 | Chấm tay độc lập | `report.html` | `labels-hung.csv` | 5 |
| H9 | P2 | Chạy `agreement.py` 3 file, ghi % 3 người + từng cặp | 3 file `labels-*.csv` | số liệu agreement | 5, 7 |
| H10 | P5 | Scorecard: pass rate/tiêu chí, tổng cost $, latency TB/câu, pass rate theo slice | `results-v1.jsonl` + `verdicts-vN.jsonl` | bảng Scorecard | 6 |
| H11 | P5 | Định nghĩa **gate** (VD: groundedness ≥90%, 0 fail ở blocker) + kết luận SHIP/CHƯA | Scorecard | Quyết định gate | 6 |
| H12 | P6 | Bài nộp cá nhân | evidence chung | `REPORT.md`, `ai-support-log.md`, `README.md` | 1–7 |

**Gợi ý 2 hàm `check_*`** (chọn 2, thêm vào list `CHECKS` ở `eval/code_checks.py`):

| Hàm | Kiểm gì | Giá trị |
|---|---|---|
| `check_scope_matches_expected` | `output.scope` khớp `expected_scope` trong dataset | ⭐ đáng giá nhất — bắt lỗi từ chối oan / trả lời câu ngoài scope, và là lập luận mạnh cho mục 4 |
| `check_followup_count` | đúng 3 câu follow-up (contract ghi rõ) | rẻ, deterministic |
| `check_sources_when_in_scope` | in_scope mà `sources` rỗng là fail | bắt lỗi trích nguồn |
| `check_quote_length` | quote ≤ ~40 từ theo system prompt | bắt lỗi quote dài |
| `check_no_infra_leak` | answer không lộ tên file / đường dẫn nội bộ | bắt lỗi rò rỉ |

### 👤 Loan — lane Dataset & Rubric

| # | Phase | Task | Input | Output | Mục REPORT |
|---|---|---|---|---|---|
| L1 | P1 | **Input Grid**: nhóm user (HV mới / đang làm bài / ôn lại…) × intent (hỏi khái niệm / xin ví dụ / xin đáp án / mơ hồ / ngoài lề) | slide deck 66 slide | bảng lưới + đánh dấu ô rủi ro cao | 1 |
| L2 | P1 | Chia quota câu theo ô lưới, giao lane cho 3 người | Input Grid | bảng quota | 1, 2 |
| L3 | P1 | Viết 8–10 câu lane `sc-1x` — nhớ `metadata.slide` | corpus + deck | phần dataset của Loan | 2 |
| L4 | P1 | **Gộp 3 lane + review chéo**: bỏ câu trùng ý, câu quá dễ, bổ ô rủi ro cao còn thiếu | 3 phần dataset | `evidence/dataset-v1.jsonl` **CHỐT** | 2 |
| L5 | P1 | Bảng scenario: mỗi `scenario_id` thuộc ô nào, expected gì, nguồn câu từ đâu | `dataset-v1.jsonl` | bảng tóm tắt | 2 |
| L6 | P2 | Chấm tay độc lập | `report.html` | `labels-loan.csv` | 5 |
| L7 | P3 | **Chủ trì tranh luận case bất đồng** → mỗi bất đồng = một chỗ rubric mơ hồ → siết định nghĩa | output `agreement.py` | `labels.csv` golden | 3, 7 |
| L8 | P3 | **Rubric v1**: bảng tiêu chí / pass khi / fail khi / **blocker?** + định nghĩa pass cho câu out-of-scope | biên bản tranh luận | bảng Rubric | 3 |
| L9 | P4 | **Routing Map**: mỗi tiêu chí → code / LLM judge / người + lý do | Rubric v1 | bảng Routing | 4 |
| L10 | P6 | Bài nộp cá nhân | evidence chung | `REPORT.md`, `ai-support-log.md`, `README.md` | 1–7 |

### 👤 Phương — lane Judge & Calibration

| # | Phase | Task | Input | Output | Mục REPORT |
|---|---|---|---|---|---|
| F1 | P0 | Đọc `judge_prompt.md` mẫu + module 07 (LLM judge) & 09 (judge alignment) | corpus | ghi chú tiêu chí | 4 |
| F2 | P1 | Viết 8–10 câu lane `sc-3x`: **mơ hồ + near-miss** | Input Grid | phần dataset của Phương | 2 |
| F3 | P1 | **Judge prompt v1** từ rubric draft — chấm tiêu chí gì, thang gì | rubric draft của Loan | `evidence/judge-prompt-v1.md` | 4 |
| F4 | P2 | Chấm tay độc lập | `report.html` | `labels-phuong.csv` | 5 |
| F5 | P2 | Ghi biên bản bất đồng: tiêu chí nào gây lệch nhiều nhất, hai phía nghĩ gì | phiên tranh luận B4 | biên bản | 5, 7 |
| F6 | P4 | Chạy `judge.py` vòng 1 → đọc **confusion matrix + % agreement** | `results-v1.jsonl` + `labels.csv` | `evidence/verdicts-v1.jsonl` + matrix | 5 |
| F7 | P4 | Chẩn đoán: judge chặt quá / lỏng quá / lệch ở nhóm nào (in-scope hay out-of-scope) | matrix v1 | phân tích | 5 |
| F8 | P4 | **Copy prompt trước khi sửa** → sửa **một thứ** → chạy lại → so agreement. Lặp ≥2 vòng | v1 | `judge-prompt-v2.md`, `verdicts-v2.jsonl` (+v3) | 5 |
| F9 | P4 | Viết **diff v1→v2**: sửa gì, vì sao, agreement trước/sau | 2 bản prompt | giải thích diff | 5 |
| F10 | P4 | Kết luận: tiêu chí nào judge đủ tin để tự động, tiêu chí nào giữ cho người | các vòng calibrate | kết luận | 5, 7 |
| F11 | P6 | Bài nộp cá nhân | evidence chung | `REPORT.md`, `ai-support-log.md`, `README.md` | 1–7 |

---

## 4. Output/evidence — ai chịu trách nhiệm, xong lúc nào

| File trong `deliverables/evidence/` | Chủ sở hữu | Sinh ra từ | Xong ở block |
|---|---|---|---|
| `dataset-v1.jsonl` | **Loan** | gộp 3 lane `sc-1x/2x/3x` | B1 cuối |
| `results-v1.jsonl` | **Hưng** | `run_eval.py` (độc quyền chạy) | B2 |
| `labels-hung.csv` / `labels-loan.csv` / `labels-phuong.csv` | mỗi người | Export từ `report.html` | B3 |
| `labels.csv` (golden) | **Loan** chủ trì | tranh luận case bất đồng | B4 |
| `judge-prompt-v1.md` | **Phương** | copy trước khi sửa lần đầu | B1 |
| `verdicts-v1.jsonl` | **Phương** | `judge.py` vòng 1 | B5 |
| `judge-prompt-v2.md` + `verdicts-v2.jsonl` | **Phương** | vòng calibrate 2 | B5 |
| `braintrust-link.md` | **Hưng** | tạo project + dán link | B0 |
| `REPORT.md` × 3 | **mỗi người tự viết** | evidence chung | B6 |
| `ai-support-log.md` × 3 | **mỗi người tự viết** | — | B6 |

---

## 5. Sync point & rủi ro chặn

| Sync | Block | Điều kiện mở khoá | Ai chờ ai | Nếu trễ thì sao |
|---|---|---|---|---|
| **S1** | B0→B1 | `results.jsonl` 5 câu smoke chạy được | Loan + Phương chờ **Hưng** | Không có dữ liệu mẫu → judge prompt và `check_*` viết mù |
| **S2** | B1→B2 | `dataset.jsonl` chốt, đã review chéo | Hưng chờ **Loan** | Không chạy được vòng chính → cả nhóm đứng |
| **S3** | B2→B3 | `results-v1.jsonl` phát tán cho cả 3 | Cả 3 chờ **Hưng** | Không ai chấm tay được |
| **S4** | B4→B5 | `labels.csv` golden chốt | Phương chờ **cả nhóm** | Không đo được agreement → **mục 5 trống = mất điểm nặng nhất** |

**Quy tắc chống chết cứng:** ai xong sớm **không ngồi chờ** — nhảy vào viết mục REPORT
mình chủ trì.

---

## 6. Lỗi chí mạng cần tránh

| Lỗi | Hậu quả | Ai canh |
|---|---|---|
| Cắm tracing key **sau khi** đã chạy | Không có trace = thiếu minh chứng, phải chạy lại tốn tiền | Hưng — B0 |
| Cả 3 cùng chạy `run_eval.py` | 3 file `results.jsonl` khác nhau → nhãn người không so được với verdict judge → **toàn bộ calibration vô nghĩa** | Hưng độc quyền chạy |
| 3 người chấm cùng browser | `localStorage` key `evalkit-labels` cố định → **đè nhãn của nhau** | Mỗi người máy/profile riêng |
| Sửa `judge_prompt.md` mà quên copy bản cũ | Không có `judge-prompt-v1.md` để đối chiếu diff → mục 5 không dẫn chứng được | Phương — mỗi vòng |
| Sửa nhiều thứ trong 1 vòng calibrate | Không biết thay đổi nào làm agreement tăng | Phương |
| Xoá row `_parse_error` / `_truncated` | Mất một failure mode **thật** — đây là điểm cộng, không phải bug cần giấu | Hưng |
| Dataset toàn câu dễ | Judge nào cũng agreement cao → không chứng minh được đã calibrate | Phương — lane near-miss |
| 3 người copy chung 1 `REPORT.md` | Bài nộp là cá nhân (`Track1_Day21_MHV_HoVaTen`) — trùng nhau là rủi ro | B6, mỗi người |

---

## 7. Ghi chú kỹ thuật

- **Cần 2 API key khác họ.** Judge phải khác model tutor (mặc định tutor
  `deepseek/deepseek-v4-flash`, judge `openai/gpt-4o-mini`). Nếu cả nhóm chỉ có 1 key,
  dùng OpenRouter với 2 model khác nhau. Chi phí thật rất nhỏ — 30 câu × 2 vòng ≈ vài cent.
- **Chia sẻ file:** `.gitignore` đã ignore mọi scratch ở root (`dataset.jsonl`,
  `results.jsonl`, `labels*.csv`) nhưng **không** ignore `deliverables/evidence/`.
  Nên `git init` + repo private, quy ước: mọi file trao đổi giữa 3 người đều đi qua
  `deliverables/evidence/` — vừa là kênh chia sẻ, vừa tự động thành bài nộp.
- **Câu near-miss quyết định điểm mục 5.** Judge nào cũng đạt agreement cao trên câu dễ.
  Dataset phải có câu mà tutor trả lời *gần đúng* — nội dung đúng nhưng cite sai section,
  hoặc quote diễn giải lại thay vì nguyên văn. Đó mới là chỗ judge lệch khỏi người, và là
  chỗ chứng minh được mình đã calibrate thật.
- **Lệnh chạy nhanh:** chấm vài câu `python eval/judge.py sc-01 sc-03`; chạy dataset khác
  `python eval/run_eval.py ten-file.jsonl`; đổi model judge
  `EVAL_JUDGE_MODEL=... python eval/judge.py`.
