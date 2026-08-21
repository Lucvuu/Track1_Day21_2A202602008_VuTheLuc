# Minh chứng tracing — ảnh chụp Braintrust

Bổ sung cho [`braintrust-link.md`](braintrust-link.md). Project Braintrust thuộc org `FPT`
nên link chỉ mở được bởi thành viên org; phần này ghi lại nội dung quan sát trực tiếp trên
giao diện Braintrust để người chấm (kể cả hệ thống chấm tự động) đối chiếu được mà không
cần quyền truy cập.

- **Link project:** https://www.braintrust.dev/app/FPT/p/ai-evaluation
- **Org:** `FPT` · **Project:** `ai-evaluation` · **Plan:** Starter
- **Ảnh chụp:** `braintrust-01-overview.png`, `braintrust-02-logs.png` (cùng thư mục này)

---

## Ảnh 1 — `braintrust-01-overview.png` · màn hình Overview của project

Xác nhận project tồn tại đúng tên và đang nhận log.

| Trường hiển thị | Giá trị |
|---|---|
| Org / Project | `FPT` / `ai-evaluation` |
| Logs in the last 7 days | **128 Traces** |
| Biểu đồ log theo ngày | Cột dồn vào **Fri 21** (ngày chạy toàn bộ vòng eval) |
| Recent logs | 5 dòng `judge-run`, mốc "4h ago" |
| Starter plan usage | Model credits $0/$10 · Logs 0.0003 GB / 1 GB · Scores 0 / 10.000 |

Sidebar còn một project khác tên `My Project` — đó là project mặc định Braintrust tạo sẵn
cho org, **không chứa dữ liệu của bài này**.

## Ảnh 2 — `braintrust-02-logs.png` · màn hình Logs, chế độ Traces

Xác nhận nội dung từng trace.

| Trường hiển thị | Giá trị |
|---|---|
| Bộ lọc | `Traces` · `Past 3 days` |
| Tổng | **128 traces** |
| Cột `Name` | `judge-run` |
| Cột `Input` | `{"judge_model"...}` |
| Cột `Output` | `{"rationale":"...` |
| Cột `Created` | `Aug 21` — dải `12:42:35 PM` đến `12:46:16 PM` |

Mốc thời gian sát nhau vài giây đến vài chục giây, khớp với việc `judge.py` chạy tuần tự
từng row (và vòng v2 chạy 2 luồng song song).

---

## Vì sao cột Duration / Tokens / LLM cost hiển thị 0

Đây là điểm người chấm tự động dễ hiểu nhầm, nên ghi rõ.

Trong ảnh 2, các cột `Duration`, `LLM duration`, `Time to first token` và tokens đều hiện
`0s` / `-` / `0`, trong khi data thô có đầy đủ số liệu. Nguyên nhân nằm ở
[`eval/tracing.py`](../../eval/tracing.py):

```python
span = self._logger.start_span(name=name, type="task")
span.log(input=inputs, output=outputs, metrics=metrics, metadata=metadata)
```

Span được tạo với `type="task"`, và `metrics` là dict tự đặt (`total_tokens`, `latency_s`,
`cost_usd`). Các cột tổng hợp dựng sẵn của Braintrust chỉ tự động điền cho span
`type="llm"` với cặp `metrics.start` / `metrics.end` theo chuẩn của nó. Vì vậy:

- **Số liệu vẫn được log đầy đủ** — mở một trace ra sẽ thấy trong phần `metrics`.
- **Cột tổng hợp ở màn hình danh sách không đọc được chúng** nên hiện 0.

`0 Tokens` và `$0 LLM cost` trên màn hình Overview **không có nghĩa là không có lời gọi
model**. Con số thật, đã kiểm chứng được, nằm ở:

| Nguồn | Số liệu |
|---|---|
| `results-v1.jsonl` | 904.049 token · latency trung bình 39,3s · `tool_calls` từng câu |
| `verdicts-v1.jsonl` | 58.642 token · latency trung bình 17,9s · có `raw_content` |
| `verdicts-v2.jsonl` | có `raw_content` và `usage` từng row |
| [`trace-summary.md`](trace-summary.md) | bảng đầy đủ từng row, sinh bằng script từ ba file trên |

`$0` ở dòng Model credits cũng đúng: model chạy qua gateway **Agnes AI**
(`EVAL_BASE_URL=https://apihub.agnes-ai.com/v1`), không tiêu credit của Braintrust.
Braintrust ở đây chỉ đóng vai trò nơi nhận trace.

---

## Đối chiếu con số 128 trace

128 trace nhiều hơn 27 câu của dataset, vì **mỗi lần chạy lại đều log trace mới**. Phân rã:

| Nguồn trace | Số lượng |
|---|---|
| `tutor-run` — vòng B2 hoàn chỉnh trên 27 câu | 27 |
| `tutor-run` — vòng B2 đầu bị dừng giữa chừng (3–9 câu) và các lần chạy shard/probe | ~40 |
| `judge-run` — 1 lần verify hạ tầng ban đầu | 1 |
| `judge-run` — vòng 0, bị cắt cụt vì `max_tokens=500` | 27 |
| `judge-run` — vòng 1 (số thật, sau khi nâng lên 1500) | 27 |
| `judge-run` — vòng 2 (`judge-prompt-v2`) | 27 |
| `judge-run` — vá 4 row v2 chạm trần 1500 | 4 |

Đống trace dư chính là **dấu vết của quá trình calibrate**: nó cho thấy vòng eval được
chạy đi chạy lại thật, gồm cả những lần hỏng phải bỏ đi, chứ không phải một lần chạy đẹp
duy nhất.
