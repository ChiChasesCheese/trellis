---
id: cc-rules-fee-split-sums-back
node: rules.fees
type: cloze
---
Splitting 100 cents three ways with `total // n` loses a cent, because {{c1::33 + 33 + 33 = 99}}. Give the first `total % n` parts one extra unit — {{c2::34, 33, 33}} — so the parts sum back to the total exactly. For a weighted split, floor each share and then hand the {{c3::leftover units to the shares with the largest remainders}} (largest-remainder method); either way, assert `sum(parts) == total` before returning.

## zh
把 100 分三等分时用 `total // n` 会丢掉一分，因为 {{c1::33 + 33 + 33 = 99}}。让前 `total % n` 份各多分一个单位 —— {{c2::34、33、33}} —— 各份之和就精确等于总额。若是加权拆分，先对每份向下取整，再把 {{c3::余下的单位分给余数最大的那几份}}（最大余数法）；无论哪种，返回前都断言 `sum(parts) == total`。
