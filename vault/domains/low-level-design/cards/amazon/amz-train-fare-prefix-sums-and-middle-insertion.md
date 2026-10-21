---
id: amz-train-fare-prefix-sums-and-middle-insertion
node: amazon.amz-train-fare
type: qa
step: 4
tags: [grown]
---
## Q
在 Amazon 火车票价设计里，要让区间价格可以不同，票价怎么算才能 O(1)？追加一站与在中间插入一站的代价为什么不同？

## A
存每个区间的价格，再存前缀和 prefix（prefix[i] 是首站到第 i 站的累计价格），票价 = |prefix[a] − prefix[b]|，查询 O(1)。追加一站：只在 prefix 末尾加一项，O(1)，已有两站间票价不变。在中间插入：其后所有站的位置和前缀和都要重排，O(n)，且被切开的区间会改变跨越它的票价。例：G→U→H→K→I 在 U 后插 N，G 到 I 由 4 变 5。
