---
id: leetcode-q-count-commas-in-range-ii-pattern
node: math-number-theory.math
type: qa
anki: 1789002117120
tags: [lc::3871, leetcode, pattern, recall]
---
## Q
如何用贡献法快速求 sum_{x=1}^{n} f(x)，其中 f(x) 只依赖 x 的位数（如逗号数、进制分组数）？

## A
把 f(x) 拆成若干个 0/1 指示项之和：f(x) = Σ_k [x 达到第 k 个阈值]。例如每 3 位加一个逗号，第 k 个逗号在 x ≥ 1000^k 时出现，所以 f(x) = Σ_{k≥1} [x ≥ 1000^k]。交换求和顺序后，Σ_{x=1}^n f(x) = Σ_k (满足 x≥1000^k 的 x 的个数) = Σ_k max(0, n - 1000^k + 1)。这样把逐个数字统计问题转化为对固定阈值集合求和，复杂度从 O(n) 降到 O(log n)。

**Evidence**

countCommas 最终解法：`return sum(max(0, n - 1000 ** i + 1) for i in range(1, 6))`，对应把每个逗号位置的贡献单独求和，而不是像 countCommas0 那样逐个数字统计 cnt(x)。

[原文 ↗](obsidian://open?vault=lc&file=questions%2F3871%20-%20Count%20Commas%20in%20Range%20II)
