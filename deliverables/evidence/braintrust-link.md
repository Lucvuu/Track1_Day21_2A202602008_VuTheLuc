# Trace link — Braintrust

Mọi run của tutor và judge trong bài này đều được log trace lên Braintrust.

- **Backend:** Braintrust (`braintrust` 0.34.0)
- **Org:** FPT
- **Project:** `ai-evaluation`
- **Link:** https://www.braintrust.dev/app/FPT/p/ai-evaluation

## Trong project có gì

| Trace name | Sinh ra từ | Nội dung mỗi trace |
|---|---|---|
| `tutor-run` | `eval/run_eval.py` | câu hỏi, slide context, output JSON, các bước tool-calling `kb_search`, tokens, latency |
| `judge-run` | `eval/judge.py` | scenario_id, model judge, verdict, rationale, tokens, latency |

## Cấu hình sinh ra trace

```
EVAL_BASE_URL     = https://apihub.agnes-ai.com/v1   (gateway Agnes AI, OpenAI-compatible)
EVAL_MODEL        = agnes-2.5-flash                  (tutor)
EVAL_JUDGE_MODEL  = agnes-2.0-flash                  (judge — khác model tutor)
BRAINTRUST_PROJECT= ai-evaluation
```

Key nằm trong `.env` ở root repo, đã gitignore, không commit.

## Số liệu quan sát trên giao diện (ngày 21/08/2026)

| Hạng mục | Giá trị |
|---|---|
| Tổng trace trong project | **128** |
| Tên span | `tutor-run`, `judge-run` |
| Plan | Starter — Logs 0.0003 GB / 1 GB |

Ảnh chụp và giải thích chi tiết: [`braintrust-screenshots.md`](braintrust-screenshots.md).

> **Lưu ý khi đối chiếu tự động:** cột `Duration`, `Tokens`, `LLM cost` trên Braintrust
> hiển thị `0` vì `eval/tracing.py` log span `type="task"` với `metrics` tự đặt, không
> phải span `type="llm"` theo chuẩn Braintrust. Số liệu thật nằm trong `results-v1.jsonl`
> (904.049 token) và `verdicts-v*.jsonl`, tổng hợp ở [`trace-summary.md`](trace-summary.md).

## Quyền truy cập

Project thuộc org `FPT` nên **cần là thành viên org mới mở được**. Người ngoài mở link sẽ
thấy *"This page is restricted or does not exist. Sign in to verify permissions."*

Để người chấm xem được trace, chọn một trong hai:

1. **Mời vào org** — Braintrust → Settings → Members → Invite, thêm email người chấm.
2. **Dùng bản sao cục bộ** — [`trace-summary.md`](trace-summary.md) dựng lại đúng nội dung
   từng trace (tool_calls, tokens, latency của cả `tutor-run` và `judge-run` hai vòng),
   sinh bằng script từ `results-v1.jsonl` và `verdicts-v*.jsonl`. Dữ liệu gốc nằm trong
   chính các file đó — Braintrust chỉ là bản trực quan hoá, không phải nguồn duy nhất.

## Ghi chú

Project `ai-evaluation` do `braintrust.init_logger()` tự tạo ở lần log đầu tiên
(`eval/tracing.py`, `DEFAULT_PROJECT`). Nếu trong sidebar Braintrust còn thấy project
`My Project` thì đó là project mặc định của org, không phải nơi chứa trace của bài này.
