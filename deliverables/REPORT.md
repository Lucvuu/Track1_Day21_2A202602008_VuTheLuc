# REPORT — Eval loop A→Z: VLearn AI Tutor

Report A→Z của eval loop — mỗi mục ứng một phase của bài lab. Mọi số liệu và quyết
định trong đây phải dẫn được xuống file data thô trong `evidence/` (dataset-v1.jsonl,
results-vN.jsonl, labels.csv, judge-prompt-vN.md, verdicts-vN.jsonl, braintrust-link.md).


---

## 1. Input Grid

> Lưới input = trục "ai hỏi" × "hỏi kiểu gì". LLM giúp sinh input, con người kiểm soát
> coverage. Trả lời các câu hỏi sau rồi vẽ lưới của bạn.

- AI Tutor của bạn phục vụ những **nhóm người dùng** nào? (học viên mới, học viên đang
  làm bài, học viên ôn lại, PM khác team...?)
- Mỗi nhóm có những **ý định (intent)** hỏi nào? (hỏi khái niệm, xin ví dụ, hỏi ngoài
  lề, xin đáp án, hỏi mơ hồ...?)
- Ô nào trong lưới là **rủi ro cao** nhất (trả lời sai thì hại người học)? Ô nào **tần
  suất cao** nhất?

**Trả lời nhanh:**

- **Nhóm người dùng:** Học viên mới (chưa học qua bài nào) · Học viên giữa khoá (đang làm bài tập) · Học viên ôn thi/ôn lại (đã học xong, cần tổng hợp).
- **Intent:** hỏi khái niệm · bám slide đang xem (deixis) · xin tổng hợp/lộ trình ôn nhiều bài · hỏi mơ hồ/thiếu ngữ cảnh · xin đáp án bài tập (adversarial) · hỏi ngoài lề (out-of-scope).
- **Ô rủi ro cao nhất:** "Học viên giữa khoá × Xin đáp án" (đang làm bài, cám dỗ xin đáp án cao nhất — tutor bịa/đưa đáp án là hại việc học nặng nhất) và "Ôn thi × Tổng hợp nhiều bài" (retrieval dễ trích sai nguồn khi phải gộp nhiều module).
- **Ô tần suất cao nhất:** "Học viên giữa khoá × Bám slide" (deixis "giải thích đoạn này" — hành vi thật khi đang học theo bài giảng).

### Lưới của bạn

Dựng theo đúng khung slide **s27–s29** (`tutor/corpus/slides/day19-20-deck.md`) — dùng ví dụ chuẩn của bài (AI Tutor hỏi đáp tài liệu, có trích nguồn). Ký hiệu: ■ chọn test — có ý nghĩa sản phẩm · □ cân nhắc sau · ▨ tổ hợp phi lý — loại.

| Persona \ Intent | Hỏi khái niệm | Bám slide (deixis) | Tổng hợp nhiều bài | Mơ hồ / thiếu ngữ cảnh | Xin đáp án (adversarial) | Ngoài lề |
|---|---|---|---|---|---|---|
| **Học viên mới** | ■ test | ■ test | □ cân nhắc sau | ■ test **(risk cao)** | ■ test | ■ test |
| **Học viên giữa khoá** | ■ test | ■ test **(×2 — tần suất cao nhất)** | ■ test | ■ test **(risk cao)** | ■ test **(risk cao nhất)** | □ cân nhắc sau |
| **Học viên ôn thi** | ■ test | □ cân nhắc sau | ■ test **(risk cao)** | ■ test | □ cân nhắc sau | ▨ phi lý — loại |

**Vì sao loại/cân nhắc sau:**
- *Mới × Tổng hợp nhiều bài* — học viên mới chưa học đủ nội dung để hỏi câu cần gộp nhiều module, tần suất thấp.
- *Giữa khoá × Ngoài lề* — đang tập trung làm bài, ít khi lạc đề hơn nhóm Mới.
- *Ôn thi × Bám slide* — giai đoạn ôn thường hỏi tổng hợp xuyên suốt hơn là bám đúng 1 slide.
- *Ôn thi × Xin đáp án* — ít "bài tập mới" ở giai đoạn ôn, để dành nếu thiếu quota.
- *Ôn thi × Ngoài lề* — tổ hợp vô nghĩa, học viên ôn thi nghiêm túc hiếm khi tán gẫu với tutor.

**Kiểm dimension (test s26):** đổi persona hoặc intent có làm hành vi *đúng* của tutor đổi theo không? Có — "Mới × khái niệm" cần giải thích từ nền, còn "Ôn thi × tổng hợp" cần cite nhiều nguồn + không lặp follow-up đã hỏi trước đó → cả hai trục đều là dimension thật, không chỉ là paraphrase.

### Quota theo lane (khớp `sc-1x/2x/3x` trong TEAM-PLAN.md)

| Lane | Người | Cột trong lưới | Số ô ■ | Câu (mỗi ô 2–3 cách diễn đạt) |
|---|---|---|---|---|
| `sc-1x` | Loan | Hỏi khái niệm + Bám slide + Tổng hợp nhiều bài | 8 ô | 8–10 câu |
| `sc-2x` | Hưng | Xin đáp án + Ngoài lề | 3 ô | 8–9 câu |
| `sc-3x` | Phương | Mơ hồ / thiếu ngữ cảnh (+ near-miss trên ô Tổng hợp) | 3 ô | 8–9 câu |

---

## 2. Dataset v1

> Dataset là "bộ đề thi" của tutor. Nêu rõ nó phủ những ô nào trong input-grid.

- `dataset.jsonl` của bạn có **bao nhiêu câu**? Mỗi câu thuộc ô nào trong lưới input?
- Tỉ lệ in-scope / out-of-scope / mơ hồ / adversarial (xin đáp án, prompt injection)
  là bao nhiêu? Vì sao chọn tỉ lệ đó?
- Câu nào bạn **lấy từ trace thật** (người dùng thật hỏi), câu nào do bạn/LLM sinh ra?
- Ai đã **review** dataset? Phát hiện gì khi review (câu trùng ý, câu quá dễ, thiếu ô
  rủi ro cao)?
- Nếu chỉ được giữ 10 câu, bạn giữ 10 câu nào? Vì sao?

**Phát hiện khi review (Loan, khi soạn lane `sc-1x`):** `tutor/corpus/manifest.json`
**bị lệch số slide so với file thật** `tutor/corpus/slides/day19-20-deck.md` — ví dụ
manifest ghi `s51` = "Vì sao calibration là bước cốt lõi" nhưng mở file thật thì `s51`
lại là một slide tiêu đề phần khác ("PA R T 06"); nội dung calibration thật nằm ở `s56`.
Kể cả ví dụ mẫu trong README (`s51`, `s29`) cũng bị lệch theo cách này. Nguyên nhân:
`tutor.py` (`load_corpus()`) parse **trực tiếp header `## sNN —` trong file `.md`** để
tạo `section_id` dùng cho retrieval và validate citation (`check_citation_exists` trong
`code_checks.py`) — không đọc qua `manifest.json`. Vậy manifest chỉ là tài liệu tham
khảo cũ, **không phải nguồn thật cho `metadata.slide`**. Đã báo Hưng + Phương tránh copy
id/title theo manifest khi viết lane `sc-2x`/`sc-3x` — phải grep trực tiếp
`^## sNN —` trong file slide để lấy đúng `id` + `title`.

### Danh sách scenario (bảng tóm tắt)

| scenario_id | ô trong lưới | expected | nguồn câu hỏi |
|---|---|---|---|
| sc-11-in-concept-trace | Học viên mới × Hỏi khái niệm | in_scope | Loan viết, bám s32 |
| sc-12-in-deixis-vibecheck | Học viên mới × Bám slide | in_scope | Loan viết, bám s15 |
| sc-13-in-concept-codebased | Giữa khoá × Hỏi khái niệm | in_scope | Loan viết, bám s40 |
| sc-14-in-deixis-tracecode | Giữa khoá × Bám slide (variant 1) | in_scope | Loan viết, bám s35 |
| sc-15-in-deixis-goldenoutput | Giữa khoá × Bám slide (variant 2) | in_scope | Loan viết, bám s16 |
| sc-16-in-synth-pipeline-concepts | Giữa khoá × Tổng hợp nhiều bài | in_scope | Loan viết, không gắn slide (cố ý) |
| sc-17-in-concept-passrate | Ôn thi × Hỏi khái niệm | in_scope | Loan viết, bám s48 |
| sc-18-in-synth-fullpipeline | Ôn thi × Tổng hợp nhiều bài | in_scope | Loan viết, không gắn slide (cố ý) |
| *(chờ lane `sc-2x` của Hưng — out-of-scope + adversarial)* | | | |
| *(chờ lane `sc-3x` của Phương — mơ hồ + near-miss)* | | | |

---

## 3. Rubric v1

> Rubric = định nghĩa "đủ tốt" mà cả team chấm giống nhau. Thu hẹp scope trước khi
> viết tiêu chí.

- Tutor trả lời một câu in-scope **"đủ tốt"** khi nào? Viết bằng 1–2 câu ai cũng hiểu.
- Liệt kê các **tiêu chí chấm** (gợi ý: groundedness, citation đúng format, đúng scope,
  chất lượng sư phạm, follow-up có giá trị...). Mỗi tiêu chí: pass/fail thế nào, ví dụ
  pass, ví dụ fail.
- Tiêu chí nào là **blocker** (fail là cả lượt fail)? Tiêu chí nào chỉ là "điểm cộng"?
- Với câu out-of-scope, hành vi nào được coi là pass? (từ chối + gợi ý chủ đề liên quan?)
- Bạn đã thử chấm chéo với ai chưa? Hai người chấm lệch nhau ở tiêu chí nào, sửa rubric
  ra sao sau đó?

### Rubric của bạn

| Tiêu chí | Pass khi | Fail khi | Blocker? |
|---|---|---|---|
| | | | |

---

## 4. Routing Map

> Cái gì kiểm bằng code, cái gì cần LLM judge, cái gì phải đến tay expert. Không phải
> tiêu chí nào cũng cần LLM.

- Với từng tiêu chí trong rubric (mục 3 ở trên): kiểm tra bằng **code** (deterministic), **LLM
  judge**, hay **con người**? Vì sao?
- Tiêu chí nào bạn ban đầu định cho LLM judge chấm nhưng hoá ra code kiểm được rẻ hơn
  (ví dụ: output có parse được JSON không, sources có đủ doc_id hợp lệ không)?
- Tiêu chí nào LLM judge **không tin được** và phải giữ cho con người?
- Judge prompt của bạn (`eval/judge_prompt.md`) chấm tiêu chí nào? Nhiệt độ, model judge là
  gì, vì sao chọn khác model của tutor?

### Bảng routing

| Tiêu chí | Code | LLM judge | Con người | Lý do |
|---|---|---|---|---|
| | | | | |

---

## 5. Calibration Report

> Judge chỉ đáng tin khi đã calibrate với chuẩn vàng của con người. Đây là minh chứng
> cho việc đó.

- Bạn đã **gán nhãn tay** bao nhiêu row? (labels.csv, export từ report.html)
- Chạy `python3 eval/judge.py`: **agreement** giữa judge và nhãn người là bao nhiêu %? Dán
  confusion matrix vào đây.
- Judge **sai ở đâu**? (chặt quá / lỏng quá / lệch ở nhóm câu nào — in-scope hay
  out-of-scope?)
- Bạn đã sửa `eval/judge_prompt.md` thế nào sau vòng calibrate đầu? Agreement sau sửa?
- Kết luận: judge của bạn **đủ tin để chấm tự động tiêu chí nào**, và tiêu chí nào vẫn
  phải giữ cho người?

### Confusion matrix (dán output judge.py)

```
(dán ở đây)
```

---

## 6. Scorecard & Gate

> Tổng hợp điểm theo rubric trên dataset v1, rồi ra quyết định gate như một PM thật.

- Kết quả chạy `eval/run_eval.py` + `eval/judge.py` trên dataset v1: **pass rate** theo từng tiêu
  chí là bao nhiêu? (kèm link/chỉ đường tới results.jsonl, verdicts.jsonl, report.html)
- Chi phí 1 vòng eval là bao nhiêu ($, token)? Latency trung bình 1 câu?
- **Gate**: ngưỡng nào thì ship? Ví dụ: groundedness pass ≥ 90%, không có fail nào ở
  nhóm blocker... — định nghĩa ngưỡng của bạn và giải thích vì sao.
- Kết quả hiện tại: **SHIP hay CHƯA SHIP**? Căn cứ vào gate ở trên.
- Nếu chưa ship: 3 lỗi lớn nhất cần fix ở tutor (prompt, retrieval, corpus)?

### Scorecard

| Tiêu chí | Pass | Fail | Uncertain | Pass rate |
|---|---|---|---|---|
| | | | | |

### Quyết định gate

**SHIP / CHƯA SHIP** — vì: ...

---

## 7. Verdict + Report cuối

> Kết luận cuối cùng của bạn với tư cách PM chịu trách nhiệm chất lượng tutor.
> Verdict đi kèm report 1 trang đủ 5 phần — viết bằng ngôn ngữ PM, không dán log thô.

### Report

#### 1. Dataset đã đánh giá

(tập nào, bao nhiêu traces, coverage chính là gì, blind spot nào còn lại)

#### 2. Quá trình đồng thuận của con người

- Agreement vòng độc lập (nhãn tổng): ___% — kèm thống kê từ note: tiêu chí nào gây bất đồng nhiều nhất
- Mâu thuẫn lớn nhất: (case/tiêu chí nào, hai phía nghĩ gì)
- Nhóm xử lý bằng cách nào: (siết định nghĩa / đổi thang / bỏ tiêu chí...)

#### 3. LLM judge

- Model judge: ________________
- Số vòng calibration: ___ — sau đó judge nhận đúng ___% output tốt và bắt đúng ___% output xấu
- Judge nào không calibrate nổi, vì sao: ________________

#### 4. Bảng quyết định routing (kèm lý giải)

| Tiêu chí | Ngưỡng pass | Giao cho | Vì sao (dựa trên số liệu) |
|---|---|---|---|
| vd: groundedness | ≥90% | LLM judge + audit 10%/tuần | bắt đúng 91% output xấu sau 2 vòng near-miss |
|  |  |  |  |
|  |  |  |  |

#### 5. Verdict + bước tiếp theo

**Ship / Ship with conditions / Hold** — vì: ________________

- Nếu Ship: monitoring tuần đầu xem gì, sample bao nhiêu %, alert ở ngưỡng nào?
- Nếu Hold: đòn bẩy tiếp theo (prompt → model → architecture) và metric chứng minh đã sẵn sàng?

### Câu hỏi tự soi

- Tin cậy nhất ở đâu, đáng lo nhất ở đâu? (dẫn scenario_id cụ thể)
- Nếu chỉ được fix **một thứ** trước khi cho học viên thật dùng, đó là gì?
- Eval loop này sẽ chạy lại **khi nào** (mỗi lần đổi prompt? mỗi tuần? khi corpus đổi?) và ai nhìn kết quả?
- Điều gì trong bài này bạn sẽ **mang về áp dụng** vào sản phẩm thật của mình?
