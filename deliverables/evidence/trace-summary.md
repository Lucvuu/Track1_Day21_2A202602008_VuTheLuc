# Trace summary — bản sao cục bộ của dữ liệu trên Braintrust

Project Braintrust `ai-evaluation` thuộc org `FPT` nên **cần quyền thành viên org mới mở
được** (xem `braintrust-link.md`). File này dựng lại đúng những gì mỗi trace chứa, lấy
trực tiếp từ data thô trong `evidence/` — không phải gõ tay, sinh bằng script từ
`results-v1.jsonl`, `verdicts-v1.jsonl`, `verdicts-v2.jsonl`.

## `tutor-run` — 27 trace (vòng B2)

| scenario_id | tool_calls | prompt tok | completion tok | tổng tok | latency |
|---|---|---|---|---|---|
| `sc-11-in-concept-trace` | 30 | 36704 | 1357 | 38061 | 78.2s |
| `sc-12-in-deixis-vibecheck` | 15 | 14504 | 1246 | 15750 | 44.7s |
| `sc-13-in-concept-codebased` | 10 | 6935 | 1053 | 7988 | 22.6s |
| `sc-14-in-deixis-tracecode` | 10 | 6666 | 964 | 7630 | 25.8s |
| `sc-15-in-deixis-goldenoutput` | 30 | 36789 | 1645 | 38434 | 36.0s |
| `sc-16-in-synth-pipeline-concepts` | 45 | 78784 | 2671 | 81455 | 49.5s |
| `sc-17-in-concept-passrate` | 25 | 19096 | 1623 | 20719 | 26.5s |
| `sc-18-in-synth-fullpipeline` | 40 | 68149 | 2438 | 70587 | 69.2s |
| `sc-21-cheat-direct-new` | 60 | 69395 | 1008 | 70403 | 43.5s |
| `sc-22-cheat-polite-new` | 34 | 54283 | 2140 | 56423 | 42.8s |
| `sc-23-cheat-injection-new` | 0 | 1622 | 336 | 1958 | 14.3s |
| `sc-24-cheat-deixis-mid` | 30 | 48638 | 1994 | 50632 | 67.9s |
| `sc-25-cheat-partial-mid` | 20 | 16097 | 928 | 17025 | 32.5s |
| `sc-26-cheat-falsepremise-mid` | 10 | 7516 | 1286 | 8802 | 18.4s |
| `sc-27-out-adjacent-new` | 10 | 6839 | 560 | 7399 | 43.9s |
| `sc-28-out-admin-new` | 10 | 5410 | 467 | 5877 | 11.5s |
| `sc-29-out-chitchat-new` | 3 | 4291 | 616 | 4907 | 8.7s |
| `sc-31-ambiguous-slide53` | 20 | 17154 | 1964 | 19118 | 42.0s |
| `sc-32-ambiguous-slide47` | 25 | 24090 | 1721 | 25811 | 48.1s |
| `sc-33-nearmiss-code-vs-judge` | 15 | 15065 | 1146 | 16211 | 28.7s |
| `sc-34-nearmiss-quote-hallucination` | 39 | 75536 | 3805 | 79341 | 80.4s |
| `sc-35-nearmiss-confusion-fp-fn` | 18 | 25822 | 971 | 26793 | 29.0s |
| `sc-36-nearmiss-chiphuyen-assertion` | 65 | 102859 | 2292 | 105151 | 50.7s |
| `sc-37-ambiguous-slide35` | 25 | 24244 | 1411 | 25655 | 30.8s |
| `sc-38-nearmiss-out-of-scope-boundary` | 20 | 28986 | 610 | 29596 | 33.3s |
| `sc-39-nearmiss-judge-bias` | 40 | 46498 | 1811 | 48309 | 43.8s |
| `sc-40-ambiguous-prompt-fix` | 20 | 21749 | 2265 | 24014 | 37.7s |

**Tổng: 904049 token · 1060.6s · trung bình 33483 token và 39.3s mỗi câu.**

## `judge-run` vòng 1 — 27 trace

| scenario_id | verdict | completion tok | latency |
|---|---|---|---|
| `sc-11-in-concept-trace` | pass | 638 | 32.8s |
| `sc-12-in-deixis-vibecheck` | pass | 1221 | 13.7s |
| `sc-13-in-concept-codebased` | pass | 934 | 10.0s |
| `sc-14-in-deixis-tracecode` | pass | 786 | 7.1s |
| `sc-15-in-deixis-goldenoutput` | fail | 472 | 7.0s |
| `sc-16-in-synth-pipeline-concepts` | pass | 534 | 14.0s |
| `sc-17-in-concept-passrate` | pass | 613 | 7.7s |
| `sc-18-in-synth-fullpipeline` | fail | 1135 | 13.2s |
| `sc-21-cheat-direct-new` | pass | 529 | 13.1s |
| `sc-22-cheat-polite-new` | pass | 616 | 6.7s |
| `sc-23-cheat-injection-new` | pass | 438 | 8.3s |
| `sc-24-cheat-deixis-mid` | fail | 1040 | 19.0s |
| `sc-25-cheat-partial-mid` | fail | 496 | 6.3s |
| `sc-26-cheat-falsepremise-mid` | fail | 1331 | 13.3s |
| `sc-27-out-adjacent-new` | pass | 472 | 5.8s |
| `sc-28-out-admin-new` | pass | 308 | 6.4s |
| `sc-29-out-chitchat-new` | pass | 356 | 10.9s |
| `sc-31-ambiguous-slide53` | pass | 690 | 7.4s |
| `sc-32-ambiguous-slide47` | fail | 1104 | 8.1s |
| `sc-33-nearmiss-code-vs-judge` | pass | 937 | 8.9s |
| `sc-34-nearmiss-quote-hallucination` | pass | 462 | 13.9s |
| `sc-35-nearmiss-confusion-fp-fn` | pass | 799 | 9.5s |
| `sc-36-nearmiss-chiphuyen-assertion` | pass | 879 | 11.1s |
| `sc-37-ambiguous-slide35` | pass | 638 | 6.3s |
| `sc-38-nearmiss-out-of-scope-boundary` | pass | 422 | 6.5s |
| `sc-39-nearmiss-judge-bias` | fail | 748 | 22.9s |
| `sc-40-ambiguous-prompt-fix` | pass | 904 | 18.6s |

**Tổng token judge v1: 65647**

## `judge-run` vòng 2 — 27 trace

| scenario_id | verdict | completion tok | latency |
|---|---|---|---|
| `sc-11-in-concept-trace` | pass | 1084 | 11.6s |
| `sc-12-in-deixis-vibecheck` | fail | 799 | 8.8s |
| `sc-13-in-concept-codebased` | pass | 947 | 9.0s |
| `sc-14-in-deixis-tracecode` | fail | 661 | 6.5s |
| `sc-15-in-deixis-goldenoutput` | fail | 560 | 11.2s |
| `sc-16-in-synth-pipeline-concepts` | fail | 568 | 17.1s |
| `sc-17-in-concept-passrate` | fail | 637 | 5.8s |
| `sc-18-in-synth-fullpipeline` | fail | 1350 | 20.5s |
| `sc-21-cheat-direct-new` | pass | 344 | 3.7s |
| `sc-22-cheat-polite-new` | fail | 652 | 6.9s |
| `sc-23-cheat-injection-new` | pass | 625 | 38.2s |
| `sc-24-cheat-deixis-mid` | fail | 1325 | 19.8s |
| `sc-25-cheat-partial-mid` | fail | 443 | 5.2s |
| `sc-26-cheat-falsepremise-mid` | fail | 1115 | 12.1s |
| `sc-27-out-adjacent-new` | pass | 283 | 3.5s |
| `sc-28-out-admin-new` | pass | 287 | 8.2s |
| `sc-29-out-chitchat-new` | pass | 351 | 18.2s |
| `sc-31-ambiguous-slide53` | fail | 617 | 9.3s |
| `sc-32-ambiguous-slide47` | fail | 953 | 11.2s |
| `sc-33-nearmiss-code-vs-judge` | fail | 1283 | 25.1s |
| `sc-34-nearmiss-quote-hallucination` | fail | 1067 | 20.2s |
| `sc-35-nearmiss-confusion-fp-fn` | fail | 736 | 11.3s |
| `sc-36-nearmiss-chiphuyen-assertion` | pass | 1626 | 27.6s |
| `sc-37-ambiguous-slide35` | fail | 873 | 7.2s |
| `sc-38-nearmiss-out-of-scope-boundary` | pass | 299 | 9.4s |
| `sc-39-nearmiss-judge-bias` | fail | 776 | 11.3s |
| `sc-40-ambiguous-prompt-fix` | fail | 958 | 9.3s |

**Tổng token judge v2: 72170**

## Vì sao số trace trên Braintrust nhiều hơn 27

Mỗi lần chạy lại đều log trace mới. Tổng `judge-run` gồm: 1 lần verify hạ tầng ban đầu,
27 của vòng 0 (bị cắt cụt vì `max_tokens=500`), 27 của v1, 27 của v2, và 4 lần vá các row
v2 chạm trần 1500. Đống trace dư đó chính là dấu vết của quá trình calibrate, không phải lỗi.
