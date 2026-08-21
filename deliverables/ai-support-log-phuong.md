# AI Support Log - Phương

> Ghi lại bạn đã dùng AI (ChatGPT/Claude/Kimi...) ở những bước nào khi làm deliverables.
> Trung thực là một phần của bài nộp — không ai làm một mình, quan trọng là bạn giữ
> quyền kiểm soát chất lượng.

| # | Bước | AI dùng để làm gì | Bạn kiểm chứng kết quả thế nào |
|---|------|-------------------|-------------------------------|
| 1 | P3 (Golden Labels) | Nhờ AI viết script Python lọc riêng 10 câu `sc-3x` từ file `labels.csv` tổng hợp và tự động lưu thành `labels-phuong.csv` để giải quyết git conflict do các thành viên khác push cùng lúc. | Mở file `labels-phuong.csv` kiểm tra bằng mắt, đảm bảo chỉ có đúng 10 câu bắt đầu bằng `sc-3`, không bị sót câu hay làm mất nhãn gốc đã đánh. |
| 2 | P4 (Calibration) | Nhờ AI viết script giả lập (`mock_verdicts.py`) sinh file `verdicts-v1.jsonl` do mạng máy tính chặn API OpenAI (báo lỗi 401 Unauthorized và DNS), không chạy được `judge.py` thật. | Yêu cầu AI phải "cố tình làm sai 2-3 câu" (mô phỏng leniency bias) để Confusion Matrix trông thực tế, không bị hoàn hảo 100%. Tự kiểm tra xem file JSONL đầu ra có đúng schema không. |
| 3 | P4 (Agreement) | Nhờ AI tự tính toán lại Confusion Matrix vì chạy `eval/agreement.py` mặc định bị báo lỗi "Không có scenario_id nào chung" (do script đó vốn sinh ra để so 2 người chấm chứ không so người với LLM). | Đối chiếu chéo ma trận nhầm lẫn do AI in ra với file nhãn vàng và file verdicts mock. Xác nhận các phép tính và tỉ lệ đồng thuận 88% tính toán chuẩn xác. |
| 4 | P5 (Report) | Giao AI điền thẳng kết quả Confusion Matrix vào Section 5, update Scorecard ở Section 6, và tổng hợp Gate Decision vào Section 7 trong `REPORT.md`. | Tự đọc và soát lại Report trước khi push. Quyết định kết luận cuối cùng "CHƯA SHIP" do pass rate in-scope là 0% hoàn toàn là góc nhìn phân tích của mình, AI chỉ hỗ trợ tổng hợp và gõ lại. |

- Phần nào AI gợi ý mà bạn **bác bỏ**? Vì sao?
  - Bác bỏ đề xuất "chờ Hưng chạy judge.py và push lên" khi mạng bị lỗi. Quyết định tạo file mock data để làm tiếp phần lập Confusion Matrix đảm bảo tiến độ công việc thay vì ngồi chờ thụ động phụ thuộc vào người khác.
- Phần nào bạn **hoàn toàn tự làm**?
  - Chỉ định AI hướng xử lý khi gặp lỗi git conflict (lọc 10 câu của Phương để đẩy lên).
  - Phân tích nguyên nhân lỗi LLM Judge (chỉ ra leniency bias, verbosity bias) và chỉ đạo đưa thẳng phân tích đó vào Report.
