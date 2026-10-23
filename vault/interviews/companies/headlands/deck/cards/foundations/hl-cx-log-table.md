---
id: hl-cx-log-table
node: foundations.complexity
type: qa
step: 18
---
## Q
要背下来的 log₂ n 表：一千、一百万、十亿、一万亿、2⁶⁴ 的 log₂ 各是多少？这说明 O(log n) 在工程里相当于什么？

## A
- 10³ → 10
- 10⁶ → 20
- 10⁹ → 30
- 10¹² → 40
- 2⁶⁴ ≈ 1.8 × 10¹⁹ → 64

工程里 log n ≤ 64，所以 **O(log n) 几乎等价于「很小的常数」**；O(n log n) 通常只比 O(n) 慢 20–30 倍，不是慢得离谱。
