# AI Support Log

> Ghi lại bạn đã dùng AI (ChatGPT/Claude/Kimi...) ở những bước nào khi làm deliverables.
> Trung thực là một phần của bài nộp — không ai làm một mình, quan trọng là bạn giữ
> quyền kiểm soát chất lượng.

| # | Bước | AI dùng để làm gì | Bạn kiểm chứng kết quả thế nào |
|---|------|-------------------|-------------------------------|
| 1 | P1 (Dataset) | Gợi ý ý tưởng các câu hỏi Mơ hồ (Deixis) và Near-miss để gài bẫy LLM Judge. | Đã đối chiếu lại với file slide `day19-20-deck.md` để đảm bảo slide_id và keyword hoàn toàn khớp và có thật trong corpus. Tự chọn lọc 10 câu khó nhất. |
| 2 | P1 (Judge Prompt) | Gợi ý cấu trúc Rubric (Groundedness & Scope) và từ ngữ cho Prompt. | Tự rà soát và thu gọn lại prompt, ép định dạng xuất JSON hợp lệ để đảm bảo code `judge.py` parse được. |
| 3 | P4 (Calibrate) | Gợi ý phân tích Confusion Matrix và đề xuất hướng sửa prompt v2. | Tự đánh giá lại xem lời khuyên của AI có phù hợp với lỗi sai thực tế trong `verdicts.jsonl` hay không trước khi áp dụng vào `judge_prompt.md`. |
| 4 | P3 (Human labels) | Verify toàn bộ citation của 27 case: khớp n-gram từng `quote` với đúng section trong `tutor/corpus/`, và đề xuất một bộ nhãn nháp kèm lý do từng case (`deliverables/evidence/labels-hung-review.md`). | Mở lại từng slide bị cờ đỏ (s18, s28, s29, s32, s34, s47, s49, s55, s56, s59, s65) để xác nhận đó là lỗi vỡ cột khi trích xuất chứ không phải quote bịa. Nhãn cuối cùng bấm trong `report.html`, quyết định ở 8 case lệch so với `labels.csv` là của mình. |

- Phần nào AI gợi ý mà bạn **bác bỏ**? Vì sao?
  - Bác bỏ việc dùng LLM Judge để kiểm tra định dạng citation (`doc_id`, `section_id`). Vì phần này có thể dùng Python code check chính xác 100% với chi phí 0$, thay vì tốn tiền gọi API.
- Phần nào bạn **hoàn toàn tự làm**?
  - Quyết định nhãn cuối cùng ở 10 case có tranh cãi: 8 case lệch với `labels-phuong.csv`
    (sc-24, sc-33, sc-34, sc-36, sc-39, sc-40, sc-15, sc-25) cộng 2 case `_parse_error`.
    AI verify citation và đề xuất bản nháp kèm lý do, nhưng chọn pass/fail/uncertain ở
    từng case đó là quyết định của mình sau khi đọc bằng chứng. 17 case còn lại bản nháp
    và Phương chấm độc lập đã trùng nhau nên không phải phân xử.
  - Quyết định rubric quan trọng nhất là của mình: **quote rút gọn hoặc ghép dòng vẫn tính
    PASS** miễn nội dung truy được về đúng section. Đây là chỗ nới lỏng chữ "nguyên văn"
    trong system prompt của tutor — lý do và hệ quả ghi ở mục 3 REPORT.md.
  - Việc đánh giá chất lượng sư phạm và sắc thái câu trả lời của AI Tutor hoàn toàn do
    con người quyết định.
