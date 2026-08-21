# AI Support Log

> Ghi lại bạn đã dùng AI (ChatGPT/Claude/Kimi...) ở những bước nào khi làm deliverables.
> Trung thực là một phần của bài nộp — không ai làm một mình, quan trọng là bạn giữ
> quyền kiểm soát chất lượng.

| # | Bước | AI dùng để làm gì | Bạn kiểm chứng kết quả thế nào |
|---|------|-------------------|-------------------------------|
| 1 | P1 (Dataset) | Gợi ý ý tưởng các câu hỏi Mơ hồ (Deixis) và Near-miss để gài bẫy LLM Judge. | Đã đối chiếu lại với file slide `day19-20-deck.md` để đảm bảo slide_id và keyword hoàn toàn khớp và có thật trong corpus. Tự chọn lọc 10 câu khó nhất. |
| 2 | P1 (Judge Prompt) | Gợi ý cấu trúc Rubric (Groundedness & Scope) và từ ngữ cho Prompt. | Tự rà soát và thu gọn lại prompt, ép định dạng xuất JSON hợp lệ để đảm bảo code `judge.py` parse được. |
| 3 | P4 (Calibrate) | Gợi ý phân tích Confusion Matrix và đề xuất hướng sửa prompt v2. | Tự đánh giá lại xem lời khuyên của AI có phù hợp với lỗi sai thực tế trong `verdicts.jsonl` hay không trước khi áp dụng vào `judge_prompt.md`. |

- Phần nào AI gợi ý mà bạn **bác bỏ**? Vì sao?
  - Bác bỏ việc dùng LLM Judge để kiểm tra định dạng citation (`doc_id`, `section_id`). Vì phần này có thể dùng Python code check chính xác 100% với chi phí 0$, thay vì tốn tiền gọi API.
- Phần nào bạn **hoàn toàn tự làm**?
  - Chấm tay 100% độc lập để tạo baseline (Labels). Việc đánh giá chất lượng sư phạm và sắc thái câu trả lời của AI Tutor hoàn toàn do con người tự cảm nhận và quyết định.
