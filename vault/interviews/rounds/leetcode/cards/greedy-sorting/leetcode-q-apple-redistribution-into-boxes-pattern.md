---
id: leetcode-q-apple-redistribution-into-boxes-pattern
node: greedy-sorting.sorting
type: qa
anki: 1787102262232
tags: [lc::3074, leetcode, pattern, recall]
---
## Q
LeetCode 3074（Apple Redistribution into Boxes）：如何用贪心求最少箱子数？

## A
把 capacity 降序排序，求 apple 总和 total；从容量最大的箱子开始累加，直到累加和 ≥ total，所用箱子数即为答案。等价写法：对 capacity 降序后做前缀和 acc，用 bisect_left(acc, total) + 1 直接定位。核心不变量：要用最少数量的箱子覆盖固定总容量，优先选容量最大的箱子必然最优（贪心的排序不等式直觉）。复杂度 O(m log m)（排序）。

**Evidence**

capacity.sort(reverse=True); apples = sum(apple); acc = list(accumulate(capacity)); return bisect_left(acc, apples) + 1

[原文 ↗](obsidian://open?vault=lc&file=questions%2F3074%20-%20Apple%20Redistribution%20into%20Boxes)
