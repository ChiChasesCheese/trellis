---
id: hl-cx-growth-factor-4
node: foundations.complexity
type: qa
step: 48
---
## Q
一个动态数组每次满了就扩容为原来的 4 倍。n 次 add 的总复制量上界和摊还代价是多少？代价是什么？

## A
g = 4：copies ≤ n · g/(g−1) = 4n/3 ≈ **1.33n**。每次 add 写 1 次 + 摊还复制 ≤ 1.33，总摊还 ≤ 2.33，仍是 O(1)。

代价是内存：扩容后最坏有 3/4 空间闲置。g 越大复制越少但浪费越多，这是时间与空间的折中。
