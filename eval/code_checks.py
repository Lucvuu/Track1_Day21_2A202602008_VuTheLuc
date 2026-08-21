"""Code checks — kiểm tra results.jsonl bằng rule thuần Python (không tốn API).

Đây là làn "Code check" của bài lab: những tiêu chí viết được thành rule thì kiểm
bằng code — nhanh, rẻ, khách quan, chạy lại bao nhiêu lần cũng được.

Chạy:  python3 eval/code_checks.py            # in bảng pass/fail từng check từng row
Mở rộng: thêm hàm check_* mới của riêng nhóm (xem 3 hàm mẫu dưới).
"""
import json
import os
import re
import sys
from functools import lru_cache
from pathlib import Path

# tutor.py nằm ở tutor/ (khu vực sản phẩm) — thêm vào sys.path để import được
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tutor"))

import tutor  # dùng lại load_corpus

EXPECTED_FIELDS = {"scope", "answer", "sources", "followup_questions"}


def check_schema(rec):
    """Output parse được và đủ 4 field đúng contract."""
    out = rec.get("output") or {}
    if out.get("_parse_error"):
        return False, "JSON không parse được (xem raw_content)"
    missing = EXPECTED_FIELDS - set(out)
    if missing:
        return False, "thiếu field: " + ", ".join(sorted(missing))
    return True, None


def check_citation_exists(rec, valid_ids):
    """Mọi doc_id/section_id trong sources phải tồn tại thật trong corpus."""
    out = rec.get("output") or {}
    if out.get("_parse_error"):
        return None, "bỏ qua (JSON vỡ)"
    for s in out.get("sources") or []:
        key = (s.get("doc_id"), s.get("section_id"))
        if key not in valid_ids:
            return False, f'nguồn không tồn tại: {key[0]}#{key[1]}'
    return True, None


def _token_subsequence(needle, haystack):
    """True nếu chuỗi token của needle xuất hiện liên tiếp trong haystack."""
    if not needle:
        return True
    n = len(needle)
    return any(haystack[i:i + n] == needle for i in range(len(haystack) - n + 1))


def check_quote_verbatim(rec, section_tokens):
    """Quote phải nằm trong section đã cite — so theo chuỗi token (bỏ dấu, lowercase,
    bỏ mọi dấu câu/khoảng trắng) nên khác biệt gạch ngang/ngoặc kép không tính là sai."""
    out = rec.get("output") or {}
    if out.get("_parse_error"):
        return None, "bỏ qua (JSON vỡ)"
    for s in out.get("sources") or []:
        tokens = section_tokens.get((s.get("doc_id"), s.get("section_id")), [])
        quote_tokens = tutor.tokens(s.get("quote") or "")
        if quote_tokens and not _token_subsequence(quote_tokens, tokens):
            return False, f'quote không khớp section {s.get("section_id")}: "{(s.get("quote") or "")[:40]}..."'
    return True, None


@lru_cache(maxsize=1)
def _expected_scopes(path="dataset.jsonl"):
    """{scenario_id: expected_scope} đọc từ dataset — results.jsonl không mang field này.
    ponytail: khoá cứng dataset.jsonl ở root; chấm results của dataset khác thì sửa path."""
    if not os.path.exists(path):
        return {}
    out = {}
    for line in open(path, encoding="utf-8"):
        if not line.strip():
            continue
        row = json.loads(line)
        sid = row.get("scenario_id") or row.get("id")
        if sid and row.get("expected_scope"):
            out[sid] = row["expected_scope"]
    return out


def check_followup_count(rec):
    """Contract bắt buộc đúng 3 câu follow-up — không hơn, không kém."""
    out = rec.get("output") or {}
    if out.get("_parse_error"):
        return None, "bỏ qua (JSON vỡ)"
    n = len(out.get("followup_questions") or [])
    if n != 3:
        return False, f"có {n} follow-up, contract yêu cầu đúng 3"
    return True, None


def check_scope_matches_expected(rec):
    """scope tutor tự nhận có khớp expected_scope nhóm gán trong dataset không.

    Bắt hai lỗi ngược nhau bằng cùng một rule: trả lời câu ngoài corpus
    (out_of_scope -> in_scope) và từ chối oan câu trong corpus (ngược lại).

    expected_scope = "unclear" thì bỏ qua có chủ đích: câu mơ hồ không có đáp án
    đúng deterministic, phải để judge/người chấm (xem mục 4 Routing)."""
    out = rec.get("output") or {}
    if out.get("_parse_error"):
        return None, "bỏ qua (JSON vỡ)"
    expected = _expected_scopes().get(rec.get("scenario_id"))
    if expected not in ("in_scope", "out_of_scope"):
        return None, "bỏ qua (unclear hoặc thiếu expected_scope)"
    actual = out.get("scope")
    if actual != expected:
        return False, f"scope={actual}, dataset kỳ vọng {expected}"
    return True, None


CHECKS = [  # thêm check của nhóm vào đây
    ("schema_valid", check_schema),
    ("citation_exists", check_citation_exists),
    ("quote_verbatim", check_quote_verbatim),
    ("followup_count", check_followup_count),
    ("scope_match", check_scope_matches_expected),
]


def main(path="results.jsonl"):
    if not os.path.exists(path):
        raise SystemExit("Không thấy %s — chạy python3 eval/run_eval.py trước." % path)
    rows = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]

    sections = tutor.load_corpus()
    valid_ids = {(s["doc_id"], s["section_id"]) for s in sections}
    section_tokens = {(s["doc_id"], s["section_id"]): tutor.tokens(s["text"]) for s in sections}

    totals = {name: [0, 0] for name, _ in CHECKS}  # [pass, fail] (skip không đếm)
    for rec in rows:
        sid = rec.get("scenario_id", "?")
        line = [sid]
        for name, fn in CHECKS:
            if fn in (check_schema, check_followup_count, check_scope_matches_expected):
                ok, reason = fn(rec)
            elif fn is check_citation_exists:
                ok, reason = fn(rec, valid_ids)
            else:
                ok, reason = fn(rec, section_tokens)
            if ok is None:
                line.append(f"{name}: skip")
                continue
            totals[name][0 if ok else 1] += 1
            line.append(f"{name}: {'pass' if ok else 'FAIL — ' + str(reason)}")
        print(" | ".join(line))

    print("\nTổng kết:")
    for name, (p, f) in totals.items():
        print(f"  {name}: {p} pass / {f} fail")


if __name__ == "__main__":
    import sys
    main(sys.argv[1] if len(sys.argv) > 1 else "results.jsonl")
