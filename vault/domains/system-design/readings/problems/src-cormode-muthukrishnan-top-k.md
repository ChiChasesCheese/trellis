---
nodes: [problems.search.top-k]
url: https://dsf.berkeley.edu/cs286/papers/countmin-latin2004.pdf
tags: []
---
# An Improved Data Stream Summary: The Count-Min Sketch and its Applications

值得读：Count-Min Sketch 的原始论文，给出宽度/深度的精确公式（`w=⌈e/ε⌉`,
`d=⌈ln(1/δ)⌉`）和误差界的完整证明（定理 1：`a_i ≤ â_i`，且以概率 `1-δ` 有
`â_i ≤ a_i + ε‖a‖₁`），以及它作为线性摘要天然可跨节点相加的性质。本题「深入探讨」第 2、5
节的误差计算和跨分片合并论证直接引用这篇论文；论文本身还覆盖了区间查询和内积查询，
本题没有用到。
