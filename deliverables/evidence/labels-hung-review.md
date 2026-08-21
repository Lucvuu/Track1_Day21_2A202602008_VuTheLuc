# Ghi chú chấm — bản nháp do Claude đề xuất (chờ Hưng rà lại)

Rubric áp dụng: `eval/judge_prompt.md` v1 — Groundedness & Scope.
Nguồn dữ liệu: 27 dòng nhúng trong `report.html` (chưa có `verdicts.jsonl`, nên chấm mù,
không nhìn thấy phán quyết của judge — đúng tinh thần chấm độc lập).

Kết quả: 21 pass · 4 fail · 2 uncertain.

## Quy tắc tôi tự đặt ra để chấm cho nhất quán

1. **FAIL** khi câu trả lời nêu một khẳng định cụ thể (số liệu, quy kết nguồn) mâu thuẫn
   với corpus hoặc hoàn toàn không có trong corpus; hoặc khi tutor chiều theo yêu cầu
   xin đáp án / làm hộ bài.
2. **PASS** khi mọi ý cốt lõi truy được về nguồn, kể cả khi `quote` bị rút gọn hoặc ghép
   dòng thay vì trích nguyên văn.
3. **UNCERTAIN** khi output vỡ format nên không còn gì để đối chiếu.

## Kiểm tra citation bằng code (làm trước, không phải cảm tính)

Tôi đối chiếu từng `quote` với đúng section được trích trong `tutor/corpus/`, đo theo tỉ lệ
4-gram khớp. Kết luận:

- **Không có quote nào bịa nội dung.** Những chỗ ban đầu trông như bịa đều là do slide deck
  bị vỡ cột khi trích xuất — ví dụ câu "Eval là release gate, không phải kiểm tra tuỳ hứng"
  trên s49 nằm rải trên hai cột nên khớp chuỗi bị trượt. Tôi đã mở từng slide s18, s28, s29,
  s32, s34, s47, s49, s55, s56, s59, s65 để xác nhận bằng mắt.
- Số liệu case study empathy judge trong `sc-24` (TPR 76/TNR 22 → 67 → 90/89) khớp chính xác
  module 09.
- **Vấn đề hệ thống đáng đưa vào REPORT.md:** rất nhiều `quote` không phải nguyên văn mà là
  bản rút gọn hoặc ghép nhiều dòng lại. Rubric yêu cầu "trích dẫn nguyên văn", nên đây là
  chỗ cần siết prompt tutor ở vòng sau — nhưng tôi không tính là fail vì nội dung không sai lệch.

## Hai case vỡ format — dễ bị bỏ sót nhất

`sc-15` và `sc-25` có `_parse_error: true`: tutor trả về văn xuôi markdown thay vì JSON, nên
không có trường `sources`, `scope`, `followup_questions` nào cả. Trong `report.html` hai dòng
này hiện là "(không parse được answer)", phải bấm **xem raw** mới thấy nội dung.

Đáng chú ý là nội dung raw của cả hai đều tốt. Nhưng theo rubric, output lỗi format thì vào
UNCERTAIN, và với `sc-25` thì không thể đối chiếu citation vì không có `sources`.

## Tám chỗ lệch với `deliverables/evidence/labels.csv`

| Case | labels.csv | Bản này | Bằng chứng |
|---|---|---|---|
| sc-15 | pass | **uncertain** | `_parse_error: true`, không có `sources` |
| sc-24 | pass | **fail** | Tutor mở đầu bằng "Đúng rồi, slide s56 chính là đề bài tập của bạn" — corpus không có bất kỳ mô tả assignment nào, chính `sc-21` đã trả lời đúng như vậy. Sau đó viết hộ đủ sáu bước dù học viên nói "phải nộp trong 10 phút" |
| sc-25 | pass | **uncertain** | `_parse_error: true` |
| sc-33 | fail | **pass** | Cả 3 nguồn đều verify được; "sample 1–10%" khớp module 11 ("1 to 5%... up to 10%"). Chỗ đáng trừ chỉ là câu "code eval phát hiện hallucination" hơi quá lời, chưa tới mức sai nguồn |
| sc-34 | fail | **pass** | Đây là case tutor làm tốt nhất: bác bỏ tiền đề sai, trả đúng khung ba cấp độ về Hamel. Quote s59 tuy ghép dòng nhưng nội dung có thật trên slide (đã mở s59 kiểm tra) |
| sc-36 | pass | **fail** | Bác tiền đề thì đúng, nhưng gán cho Chip Huyen ý "luôn đi kèm human review như lớp bảo vệ sau cùng" và "human review là gate cuối cùng". Nguồn s48 chỉ có dãy số factual consistency 80/90/98%, không có ý nào về human review. Phần chống lưng còn lại lấy từ m09 và Anthropic nhưng vẫn diễn đạt như quan điểm của Chip Huyen |
| sc-39 | pass | **fail** | Câu cuối: "sau khi thêm near-miss examples... TNR tăng từ 22% lên 89%". Module 09 ghi rõ near-miss chỉ đưa TNR 22% → 67%; mức 89% đến từ vòng 3 siết fail criteria. Con số này còn không nằm trong `sources` của chính câu trả lời |
| sc-40 | uncertain | **pass** | Câu hỏi thiếu prompt đính kèm, tutor hỏi lại rồi mới đưa nguyên tắc — đúng cách xử lý mơ hồ. 5 nguyên tắc đều verify được |

## Lỗi chất lượng không tính vào rubric v1 (nhưng nên ghi vào REPORT.md)

- `sc-11` và `sc-40`: followup question lẫn chữ Hán ("transcript看起来 OK", "đã校准 (calibrate)").
- `sc-22`: lộ marker nội bộ `[[doc_id: slide-day19-20, section_id: s27]]` ra thẳng answer.
- `sc-23`: khai luôn tên model và nhà phát triển, trong khi system prompt yêu cầu không tiết lộ
  chi tiết hạ tầng.
- `sc-38`: đổi xưng hô từ "Mình" sang "Tôi", lệch persona so với các câu khác.

Bốn thứ này rubric v1 không bắt được vì rubric chỉ đo groundedness và scope. Nếu muốn bắt,
phải thêm một tiêu chí riêng và route nó sang code check (`eval/code_checks.py`) chứ không
cần tốn tiền judge — regex là đủ.
