# AI Support Log — Vũ Thế Lực (2A202602008)

> Ghi lại bạn đã dùng AI (ChatGPT/Claude/Kimi...) ở những bước nào khi làm deliverables.
> Trung thực là một phần của bài nộp — không ai làm một mình, quan trọng là bạn giữ
> quyền kiểm soát chất lượng.

> ⚠️ **KHUNG CHỜ ĐIỀN — Lực tự viết phần này.**
> File này khai báo *bạn* đã dùng AI thế nào, nên không ai điền hộ được. Hai dòng dưới là
> gợi ý theo phần việc bạn chủ trì (lane `sc-2x` và hai code check); sửa lại cho đúng
> những gì bạn thực sự làm, xoá dòng nào không đúng, thêm dòng nào còn thiếu. Nhớ xoá cả
> khối cảnh báo này trước khi nộp.

| # | Bước | AI dùng để làm gì | Bạn kiểm chứng kết quả thế nào |
|---|------|-------------------|-------------------------------|
| 1 | P1 (Dataset lane `sc-2x`) | *(ví dụ: nhờ AI gợi ý các biến thể cách hỏi xin đáp án / prompt injection?)* | *(bạn đã đối chiếu `slide.id` và `keyword` với `tutor/corpus/slides/day19-20-deck.md` chưa? bỏ câu nào vì trùng ý?)* |
| 2 | P4 (Hai code check) | *(ví dụ: nhờ AI liệt kê các rule kiểm được bằng code, rồi tự chọn 2 cái?)* | *(bạn dựa vào đâu để chọn `followup_count` và `scope_match` thay vì các rule khác?)* |
| 3 | | | |

- Phần nào AI gợi ý mà bạn **bác bỏ**? Vì sao?
  - *(điền)*
- Phần nào bạn **hoàn toàn tự làm**?
  - *(điền)*

---

## Ghi chú về phân công — Lực tự xác nhận

Lane Pipeline & Code do tôi và Hưng làm chung, không chia đôi thành hai phần độc lập.
Phần tôi chủ trì: soạn dataset lane `sc-2x` và đề xuất hai code check
(`followup_count`, `scope_match`). Hưng chủ trì: dựng hạ tầng chạy trên gateway Agnes AI,
cài đặt hai check vào `eval/code_checks.py`, chạy vòng B2, viết mục 6 Scorecard & Gate.

*(Nếu bạn có tự chạy lệnh nào trên máy mình — `run_eval.py`, `code_checks.py`,
`judge.py`, hay chạy thử lane `sc-2x` trước khi gộp — ghi vào đây kèm kết quả quan sát
được. Hưng không nắm phần này nên không ghi thay được.)*
