"""Đối chiếu mọi con số trong REPORT.md với data thô trong evidence/.

Checklist nộp bài yêu cầu "số liệu trong REPORT.md khớp với data trong
deliverables/evidence/ (kiểm chứng được)". Script này là cách kiểm chứng đó —
chạy lại bất cứ lúc nào, không gọi API, không tốn tiền.

    python deliverables/evidence/verify-report-numbers.py

In ra từng con số đã khẳng định trong REPORT.md kèm giá trị tính lại từ file
thô, và OK/LỆCH cho từng dòng.
"""
import collections
import csv
import json
import sys
from pathlib import Path

E = Path(__file__).resolve().parent
ROOT = E.parent.parent
sys.path.insert(0, str(ROOT / "tutor"))
import tutor  # noqa: E402

fails = []


def check(label, actual, claimed):
    ok = str(actual) == str(claimed)
    if not ok:
        fails.append(label)
    print("  %-46s %-22s %s" % (label, actual, "OK" if ok else "LỆCH (REPORT ghi %s)" % claimed))


def labels(name):
    with open(E / name, encoding="utf-8") as f:
        return {r["scenario_id"]: r["label"] for r in csv.DictReader(f) if r["label"].strip()}


def jsonl(name):
    with open(E / name, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


ds, rs = jsonl("dataset-v1.jsonl"), jsonl("results-v1.jsonl")
G, L, H, P = (labels(n) for n in ("labels.csv", "labels-loan.csv",
                                  "labels-hung.csv", "labels-phuong.csv"))

print("\n--- Mục 2: Dataset ---")
check("số câu dataset", len(ds), 27)
sc = collections.Counter(r["expected_scope"] for r in ds)
check("in_scope / out_of_scope / unclear",
      "%d / %d / %d" % (sc["in_scope"], sc["out_of_scope"], sc["unclear"]), "16 / 10 / 1")
check("scenario_id không trùng", len({r["scenario_id"] for r in ds}) == len(ds), True)

print("\n--- Mục 3 + 7§2: Nhãn người và đồng thuận ---")
for name, d, claimed in [("Loan", L, "8/18/1"), ("Hưng", H, "21/4/2"), ("Phương", P, "7/2/1")]:
    c = collections.Counter(d.values())
    check("nhãn %s (pass/fail/uncertain)" % name,
          "%d/%d/%d" % (c["pass"], c["fail"], c["uncertain"]), claimed)
check("nhãn vàng (pass/fail/uncertain)",
      "%d/%d/%d" % tuple(collections.Counter(G.values())[k] for k in ("pass", "fail", "uncertain")),
      "8/18/1")

common = set(L) & set(H)
agree = sum(1 for s in common if L[s] == H[s])
check("agreement loan vs hung", "%d/%d = %d%%" % (agree, len(common), 100 * agree // len(common)),
      "10/27 = 37%")
tri = set(L) & set(H) & set(P)
agree3 = sum(1 for s in tri if L[s] == H[s] == P[s])
check("agreement 3 người (phần giao)",
      "%d/%d = %d%%" % (agree3, len(tri), 100 * agree3 // len(tri)), "2/10 = 20%")

for name, d, claimed in [("Loan", L, "27/27"), ("Hưng", H, "10/27"), ("Phương", P, "6/10")]:
    c = [s for s in d if s in G]
    check("%s trùng nhãn vàng" % name, "%d/%d" % (sum(1 for s in c if d[s] == G[s]), len(c)), claimed)

print("\n--- Mục 4 + 6: Làn code ---")
sec = {(s["doc_id"], s["section_id"]): s["text"] for s in tutor.load_corpus()}
tot = ok = 0
for r in rs:
    o = r.get("output") or {}
    if o.get("_parse_error"):
        continue
    for s in o.get("sources") or []:
        tot += 1
        ok += (s.get("quote") or "") in sec.get((s.get("doc_id"), s.get("section_id")), "")
check("quote nguyên văn (đếm theo source)", "%d/%d" % (ok, tot), "17/79")

print("\n--- Mục 6: Chi phí một vòng ---")
lat = [r["latency_s"] for r in rs]
check("tổng token", sum((r.get("usage") or {}).get("total_tokens", 0) for r in rs), 904049)
check("latency trung bình", "%.1f" % (sum(lat) / len(lat)), "39.3")
check("latency max", "%.1f" % max(lat), "80.4")

print("\n--- Mục 6: Pass rate theo lane (nhãn vàng) ---")
ln = collections.defaultdict(collections.Counter)
for sid, v in G.items():
    n = int(sid.split("-")[1])
    ln["sc-1x" if n < 20 else "sc-2x" if n < 30 else "sc-3x"][v] += 1
for k, claimed in [("sc-1x", "0/8/0"), ("sc-2x", "5/4/0"), ("sc-3x", "3/6/1")]:
    check("lane %s (pass/fail/uncertain)" % k,
          "%d/%d/%d" % (ln[k]["pass"], ln[k]["fail"], ln[k]["uncertain"]), claimed)

print("\n--- Mục 5: Judge ---")
try:
    V = jsonl("verdicts-v1.jsonl")
    rat = len({r.get("rationale", "") for r in V})
    real = rat > len(V) // 3 and "raw_content" in V[0] and len({r.get("latency_s") for r in V}) > 1
    print("  verdicts-v1.jsonl: %d row · %d rationale khác nhau · raw_content: %s · latency khác nhau: %d"
          % (len(V), rat, "raw_content" in V[0], len({r.get("latency_s") for r in V})))
    if not real:
        fails.append("verdicts-v1.jsonl KHÔNG phải judge chạy thật")
        print("  ⚠ KHÔNG phải output của eval/judge.py — judge.py luôn ghi raw_content + usage,")
        print("    và latency mỗi row phải khác nhau. Mục 5 đang tựa trên dữ liệu này.")
    else:
        cm = collections.Counter((r["verdict"], G[r["scenario_id"]])
                                 for r in V if r["scenario_id"] in G)
        n = sum(cm.values())
        a = sum(cm[(x, x)] for x in ("pass", "fail", "uncertain"))
        print("  agreement judge vs nhãn vàng: %d/%d = %d%%" % (a, n, 100 * a // n))
except FileNotFoundError:
    print("  chưa có verdicts-v1.jsonl")

print("\n" + ("TẤT CẢ KHỚP." if not fails else "CÓ %d CHỖ CẦN SỬA:" % len(fails)))
for f in fails:
    print("  -", f)
sys.exit(1 if fails else 0)
