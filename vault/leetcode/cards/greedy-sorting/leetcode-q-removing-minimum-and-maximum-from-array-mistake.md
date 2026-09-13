---
id: leetcode-q-removing-minimum-and-maximum-from-array-mistake
node: greedy-sorting.greedy
type: qa
anki: 1788391211398
tags: [lc::2091, leetcode, mistake, recall]
---
## Q
为什么最初写的 4 分支公式（被注释掉的代码）比最终解法多了一项？

## A
最初没有先对 p, q 排序，直接写了两个对称的双端删除公式 p+n-q+1 和 q+n-p+1，以为都要保留。实际上一旦令 p<q（排序后），p+n-q+1 恒小于等于 q+n-p+1，后者永远不会是最优解，是冗余分支。先排序 p, q 再列策略可以少一个分支、逻辑更清晰。

**Evidence**

注释代码：return min(max(p, q) + 1, n - min(p, q), p + n - q + 1, q + n - p + 1) → 简化为：p, q = min(p, q), max(p, q); return min(q + 1, n - p, p + 1 + n - q)

[原文 ↗](obsidian://open?vault=lc&file=questions%2F2091%20-%20Removing%20Minimum%20and%20Maximum%20From%20Array)
