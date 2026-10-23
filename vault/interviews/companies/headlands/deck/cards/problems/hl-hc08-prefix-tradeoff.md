---
id: hl-hc08-prefix-tradeoff
node: problems.hc08-order-sequence-api
type: qa
step: 2
---
## Q
前缀和（prefix sum）的两个极端做法各是什么复杂度？朴素版订单序列慢到什么程度，为什么树状数组是折中？

## A
`P(i) = a[1] + … + a[i]`。`qtyUpTo` 是前缀和，`countUpTo` 是「每张订单值为 1」的前缀和。
| 做法 | 查询 `P(i)` | 修改 `a[j]` |
|---|---|---|
| 每次现算（从头加到 i） | O(n) | O(1) |
| 提前存所有 P | O(1) | O(n)（后面所有 P 都要加变化量） |

订单不断进出、查询也多，两者都不行；树状数组（Fenwick tree / BIT）折中：两者都 **O(log n)**。

朴素版：`ArrayList<long[]>` 存 `{id, qty}`，`find(id)` 是 O(n)，`delete` 扫描 + 往前挪 O(n)，`qtyUpTo` 扫到该 id O(n)，`idAt` O(1)。正确又短，先写它（还可当对拍参照）。5 万张订单、5 万次随机 `qtyUpTo` 约 **1.9 秒**；规模 ×10 时间约 ×100 ≈ **190 秒**；同样 50 万 + 50 万树状数组约 **60–130 毫秒**。100 万张订单每次从头加几十万次，问 100 万次就是 10¹¹~10¹² 次加法。

面试策略：先写对朴素版，再优化，再谈内存，比一上来背 Fenwick 更稳。

「亚线性」（sublinear）：时间增长比 n 慢，如 O(log n)。
