---
id: leetcode-c-range-query
node: advanced-ds-heap.range-query
type: cloze
anki: 1787102263612
tags: [concept-cloze, leetcode, recall]
---
Sparse Table 用两个可能重叠的区间在 {{c1::O(1)}} 时间内完成静态区间查询，这依赖于聚合操作满足 {{c2::幂等性（idempotence，如 op(x,x)==x）}}，例如 min/max/gcd；区间和不满足此性质，静态区间和应改用前缀和而非 Sparse Table 的重叠技巧。

min(x,x)=x, max(x,x)=x, gcd(x,x)=x 都成立，但 x+x != x，所以重叠区间查询对 sum 会重复计算，得到错误结果。

**Evidence**

经典 Sparse Table 用两个可能重叠的区间完成 O(1) 查询，所以只适用于 min/max/gcd 这类幂等操作。静态区间和应该使用前缀和。

[原文 ↗](obsidian://open?vault=lc&file=concepts%2F%E5%8C%BA%E9%97%B4%E6%9F%A5%E8%AF%A2%E6%95%B0%E6%8D%AE%E7%BB%93%E6%9E%84)
