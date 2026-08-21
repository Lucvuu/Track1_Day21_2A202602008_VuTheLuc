# B4 — Phân tích bất đồng nhãn người (chuẩn bị phiên tranh luận)

Loan soạn, chủ trì phiên B4. Nguồn: `labels-loan.csv`, `labels-hung.csv`,
`labels-phuong.csv` chấm độc lập trên `results-v1.jsonl`, đo bằng `eval/agreement.py`.

## 1. Ba phép đo

| Phép đo | Số row chung | Đồng thuận |
|---|---|---|
| 3 người (giao 3 file) | 10 | **2/10 = 20%** |
| loan vs hung | 27 | **10/27 = 37%** |
| loan vs phuong | 10 | 6/10 = 60% |
| hung vs phuong | 10 | 5/10 = 50% |

Phân bố nhãn: Loan pass 8 / fail 18 / uncertain 1 · Hưng pass 21 / fail 4 / uncertain 2 ·
Phương (10 row) pass 7 / fail 2 / uncertain 1.

Đọc thẳng: **Loan chấm chặt hơn hẳn hai người còn lại** — pass rate 30% so với 78% và 70%.

## 2. Nguyên nhân: gần như chỉ một tiêu chí

Trong **13 ca** `loan=fail / hung=pass` trên tập 27 row đầy đủ, **13/13 note của Loan đều
dẫn R3 (quote nguyên văn)**. Không một ngoại lệ.

Đây không phải bất đồng rải rác về "cảm nhận chất lượng" — hai bên đang **áp hai bộ tiêu
chí khác nhau**: Loan kiểm từng `quote` có nằm nguyên văn trong section đã cite không;
Hưng và Phương chấm theo nội dung câu trả lời và không mở quote ra đối chiếu.

Số liệu khách quan hậu thuẫn phía Loan: đếm trên toàn bộ `results-v1.jsonl`, chỉ
**17/79 quote (22%)** khớp nguyên văn với section được cite. `check_quote_verbatim` trong
làn code cũng báo 9 pass / 16 fail — độc lập với nhãn người và cho cùng kết luận.

Kiểu lỗi cụ thể của tutor: **ghép mảnh**. Nó lấy 2–3 dòng rời trong cùng slide, nối lại
bằng dấu hai chấm hoặc dấu `...`, thêm chữ nối cho trôi chảy, rồi đóng gói thành một
`quote`. Nội dung không sai, nhưng không còn là trích dẫn nguyên văn.

## 3. Câu hỏi phải chốt ở B4

> **R3 (quote nguyên văn) có thật sự là blocker không?**

Rubric v1 (mục 3) đang xếp R3 là blocker. Ba phương án, kèm hệ quả tính sẵn trên
27 row của `results-v1`:

| Phương án | Định nghĩa | Pass rate (nhãn Loan) |
|---|---|---|
| **A. Giữ R3 blocker** | Quote sai nguyên văn = fail cả lượt, như hiện tại | **8/27 = 30%** |
| **B. Hạ R3 xuống điểm cộng** | Quote ghép mảnh không chặn; chỉ fail khi quote **sai nội dung** | **14/27 = 52%** |
| **C. Tách R3 làm hai mức** | R3a *quote sai nội dung / gán nhầm section* = blocker · R3b *quote đúng nội dung nhưng ghép mảnh* = điểm cộng | cần chấm lại 16 row để biết |

Phân rã 18 ca fail của Loan để thấy phương án B đụng vào đâu:

- **6 ca fail CHỈ vì R3** → phương án B lật thành pass: `sc-11`, `sc-12`, `sc-16`,
  `sc-17`, `sc-34`, `sc-35`.
- **10 ca fail vì R3 **cộng** blocker khác** → vẫn fail dù chọn B: `sc-13` (+R1),
  `sc-14` (+R5), `sc-18` (+R5), `sc-22` (+R6), `sc-24` (+R6), `sc-26` (+R1,R6),
  `sc-31` (+R5), `sc-32` (+R5), `sc-33` (+R5), `sc-36` (+R5).
- **2 ca fail không liên quan R3** → không đổi: `sc-15`, `sc-25` (đều R1, JSON vỡ).

**Khuyến nghị của người chủ trì: phương án C.** Lý do: gộp "gán quote sang nhầm section"
với "ghép 2 dòng cùng một slide" vào chung một nhãn fail là làm mất thông tin — hai lỗi
này có mức nguy hại rất khác nhau với người học. Ví dụ `sc-11` gán một quote **tiếng Anh
của `ai-evals-m04`** vào section `s32` của slide tiếng Việt (lỗi nặng, dẫn học viên tới
nguồn sai), trong khi `sc-35` chỉ nối hai dòng liền nhau trong đúng `s55` (lỗi hình thức).
Phương án A đánh đồng cả hai, phương án B bỏ qua cả hai.

## 4. Các ca bất đồng KHÔNG do R3 — xử riêng

| Row | Nhãn | Việc cần làm |
|---|---|---|
| `sc-15`, `sc-25` | loan `fail` (R1) · hung `uncertain` · phương `pass` | Sự thật kiểm chứng được: output **JSON vỡ**, không parse được. Chốt quy ước: JSON vỡ là `fail` R1 hay `uncertain`? Phải thống nhất — không thể `pass`. |
| `sc-39` | loan `pass` · hung `fail` | Ca duy nhất Loan lỏng hơn Hưng. Tutor trả lời đúng verbosity bias nhưng thiếu self-preference + position bias. Thiếu ý có phải fail? |
| `sc-40` | loan `uncertain` · hung `pass` · phương `uncertain` | Row `unclear` duy nhất. Tutor có hỏi lại nhưng vẫn trả lời luôn. Hành vi đúng cho row `unclear` là gì? |
| `sc-36` | loan `fail` · hung `fail` · phương `pass` | Loan và Hưng cùng fail — kiểm lại đây có phải mẫu để siết định nghĩa R5 không. |

## 5. Vấn đề quy trình phải sửa trước khi chốt nhãn vàng

`labels-phuong.csv` hiện **chỉ có 10 row** (lane `sc-3x` của Phương), sau khi commit
`e41325e` cắt bỏ 17 row còn lại. Hai hệ quả:

1. `agreement.py` lấy **giao** của cả ba file, nên con số 3 người bị ép xuống còn 10 row —
   mất 17 row, trong đó có toàn bộ lane in-scope và adversarial.
2. Ba row bị cắt (`sc-15`, `sc-24`, `sc-25`) đúng là ba row Loan đã báo Phương chấm lệch
   so với dữ liệu thật (hai row JSON vỡ bị gán `pass`, và `sc-24` — ca tutor làm hộ trọn
   bài — bị gán "từ chối khéo"). Cắt bỏ không giải quyết bất đồng, chỉ giấu nó.

**Đề nghị:** Phương chấm lại đủ 27 row trên `report.html` rồi export lại. Chuẩn vàng phải
phủ cùng một tập với dataset thì mục 5 (calibration judge) mới dùng được — `judge.py` chấm
cả 27 row, nếu nhãn vàng chỉ có 10 thì confusion matrix chỉ dựng được trên 10.

## 6. Đầu ra cần có sau phiên B4

1. Chốt phương án cho R3, sửa lại bảng rubric ở REPORT mục 3 (đổi cột "Blocker?" của R3).
2. Chốt quy ước nhãn cho row JSON vỡ.
3. Chốt hành vi đúng cho row `unclear`.
4. Từ ba quyết định trên, cả nhóm chấm lại các ca bất đồng → ghi `labels.csv` **nhãn vàng**.
5. Ghi lại agreement trước/sau khi siết rubric — đây là số liệu cho mục 7 phần 2.
