---
id: cc-performance-budget-boundary-shifts-with-n
node: performance.budget
type: qa
tags: [grown]
---
## Q
An offline judge caps an array at n = 10^5, and you use sqrt-decomposition, giving O(n√n) ≈ 3×10^7 operations — comfortably inside a 2-second interpreted-language budget. You reuse the same sqrt-decomposition on a follow-up problem where the array is n = 10^6. Why does it now time out, even though 'O(n√n) is fine' held a moment ago?

## A
O(n√n) does not scale linearly with n: at n = 10^5 it is 10^5 × ~316 ≈ 3×10^7 operations, but at n = 10^6 it is 10^6 × 1000 ≈ 10^9 operations — over 30x more, not 10x more, because the √n factor itself grows with n. A complexity class that was boundary-safe at one order of magnitude can cross into too-slow at the next order of magnitude. Never carry over a verdict from a different input size — recompute the operation count for the new n before trusting the same technique.

## Q zh
一个离线判题器把数组上限定在 n = 10^5，你用 sqrt-decomposition（分块），复杂度 O(n√n) ≈ 3×10^7 次操作，在解释型语言 2 秒的预算里很宽裕。你把同一套分块原样搬到后续一题上，那题的数组是 n = 10^6。为什么现在会超时，明明刚才"O(n√n) 没问题"还成立？

## A zh
O(n√n) 并不随 n 线性增长：n = 10^5 时是 10^5 × ~316 ≈ 3×10^7 次操作，而 n = 10^6 时是 10^6 × 1000 ≈ 10^9 次——多了 30 倍以上而不是 10 倍，因为 √n 这个因子本身也随 n 增长。在某一个数量级上刚好安全的复杂度类，到下一个数量级就可能跨进"太慢"。永远不要把一个输入规模下的结论直接搬到另一个规模——在相信同一技巧之前，先按新的 n 重新算一遍操作次数。
