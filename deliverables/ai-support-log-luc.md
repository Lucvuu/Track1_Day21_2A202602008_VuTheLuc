# AI Support Log — Vũ Thế Lực (2A202602008)

> Ghi lại bạn đã dùng AI (ChatGPT/Claude/Kimi...) ở những bước nào khi làm deliverables.
> Trung thực là một phần của bài nộp — không ai làm một mình, quan trọng là bạn giữ
> quyền kiểm soát chất lượng.

Phần việc tôi chủ trì trong lane Pipeline & Code (soạn dataset lane `sc-2x`, đề xuất hai
code check `followup_count` và `scope_match`) đã hoàn thành và có bằng chứng trong
`deliverables/evidence/`. Bảng dưới đây khai báo tôi dùng AI ở đâu trong quá trình đó.

| # | Bước | AI dùng để làm gì | Bạn kiểm chứng kết quả thế nào |
|---|------|-------------------|-------------------------------|
| 1 | P1 — Dataset lane `sc-2x` | Brainstorm cùng AI các biến thể nguỵ trang cho hai ô *Xin đáp án* và *Ngoài lề* — xin gợi ý mở rộng từ vài kiểu hỏi thô ban đầu thành thang độ nhiều mức (thô → khéo: nhờ giúp đỡ, deixis + áp lực thời gian, xin một phần, bịa tiền đề giả) | Chạy từng câu qua `eval/run_eval.py` trên tutor thật, đọc `results.jsonl` xem tutor lọt/chặn đúng như kỳ vọng không rồi mới chốt vào `dataset-sc2x-hung-draft.jsonl`; câu nào không tạo được phân hoá rõ (tutor xử lý giống câu khác, không lộ lỗi mới) thì bỏ |
| 2 | P4 — Đề xuất hai code check | Hỏi AI cách viết rule Python thuần kiểm `followup_count` (đếm đúng 3 follow-up) và `scope_match` (so khớp `output.scope` với `expected_scope`) mà không cần gọi LLM | Tự chạy `eval/code_checks.py` trên toàn bộ 27 câu, đối chiếu tay vài case cụ thể (`sc-01`, `sc-21`...) để chắc rule không báo sai; tự quyết định loại row `expected_scope = unclear` (`sc-40`) khỏi `scope_match` vì câu mơ hồ không có đáp án đúng deterministic |
| 3 | Rà soát repo trước khi nộp | Nhờ AI (Claude Code) đối chiếu repo cá nhân với nhắc nhở của Hưng trong nhóm chat — kiểm tra remote đã trỏ đúng fork cá nhân, README đủ thông tin, và rà lại chính file log này | Tự đọc lại từng điểm AI nêu ra, đối chiếu trực tiếp với `git remote -v` và nội dung file thật trong repo trước khi chấp nhận sửa |

- Phần nào AI gợi ý mà bạn **bác bỏ**? Ban đầu AI gợi ý dùng chung khung câu hỏi với lane
  `sc-1x` của Loan cho nhanh — bác bỏ vì lane `sc-2x` cần thang độ nguỵ trang riêng
  (thô/khéo) để lộ ra phát hiện "nguỵ trang khéo mới lọt", dùng chung khung sẽ làm mất
  đối chứng đó.
- Phần nào bạn **hoàn toàn tự làm**? Case `sc-26` (bịa tiền đề giả "tài liệu khoá học cho
  phép đưa đáp án") là ý tưởng và cách diễn đạt tự nghĩ, không phải AI gợi ý — xuất phát từ
  quan sát rằng tutor có `kb_search` trong tầm với nhưng không dùng để kiểm chứng tiền đề
  người hỏi đưa ra.

---

## Ghi chú về phân công

Lane Pipeline & Code do tôi và Hoàng Tuấn Hưng **làm chung**, không chia đôi thành hai
phần độc lập.

| Người | Chủ trì phần nào |
|---|---|
| **Vũ Thế Lực** | Soạn dataset lane `sc-2x` (9 câu, ô *Xin đáp án* và *Ngoài lề*) · đề xuất hai code check `followup_count` và `scope_match` |
| Hoàng Tuấn Hưng | Dựng hạ tầng chạy trên gateway Agnes AI · cài đặt hai check vào `eval/code_checks.py` · chạy vòng B2 · viết mục 6 Scorecard & Gate |

Ghi rõ như vậy để hai bài nộp đối chiếu được với nhau mà không mâu thuẫn.
