---
id: flatten-outer-keeps-empty-arrays
node: semistructured.flatten-lateral-joins
type: qa
tags: [grown]
---
## Q
用 `LATERAL FLATTEN(input => o.v:items)` 统计每个订单的商品后，发现没有商品（`items` 为空或缺失）的订单从结果里消失了。为什么？怎么修？

## A
FLATTEN 对空数组或缺失路径不产生任何行，而 LATERAL 连接的语义类似内连接：右侧没有行时，左侧这一行也被丢弃。加上 `OUTER => TRUE` 后，对于无法展开的输入，FLATTEN 会输出一行，展开相关列为 NULL，于是这些订单得以保留，效果类似左外连接。
