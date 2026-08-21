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

## Ghi chú

Project `ai-evaluation` do `braintrust.init_logger()` tự tạo ở lần log đầu tiên
(`eval/tracing.py`, `DEFAULT_PROJECT`). Nếu trong sidebar Braintrust còn thấy project
`My Project` thì đó là project mặc định của org, không phải nơi chứa trace của bài này.
