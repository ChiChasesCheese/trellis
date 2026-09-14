---
id: leetcode-q-sum-game-pattern
node: dp-game-probability.game-theory
type: qa
anki: 1787613691600
tags: [lc::1927, leetcode, pattern, recall]
---
## Q
1927. Sum Game：字符串对半分，含 '?' 的博弈论求和问题，如何在 O(n) 内判断先手（Alice）是否必胜？

## A
核心不变量：设左半 '?' 数为 cntL、右半为 cntR，diff 为两半已知数字和之差（左-右）。
1) 若 cntL+cntR 为奇数，Alice（先手）必胜——因为总步数为奇数，最后一步永远由 Alice 走，她可以在终局前把差值调整为非零。
2) 若为偶数，双方交替填完所有 '?'，最优策略下同一侧的一对 '?' 无论谁先手，其两数之和会被双方拉扯稳定在 9（一个想最大一个想最小）。于是最终差值等价于把两侧多出的 '?' 两两配对后固定贡献 9，判断这个必然结果是否为 0：
 diff != (cntR - cntL) * 9 / 2 时 Alice 仍必胜，否则 Bob 必胜。
复杂度 O(n) 时间，O(1) 额外空间，只需一次遍历统计计数与和。

**Evidence**

代码：`left_blank, right_blank = num[:half].count('?'), num[half:].count('?')`；`diff = sum(...) - sum(...)`；`return (left_blank + right_blank) % 2 == 1 or diff != (right_blank - left_blank) * 9 // 2`

[原文 ↗](obsidian://open?vault=lc&file=questions%2F1927%20-%20Sum%20Game)
