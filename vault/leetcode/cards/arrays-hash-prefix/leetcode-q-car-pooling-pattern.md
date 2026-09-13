---
id: leetcode-q-car-pooling-pattern
node: arrays-hash-prefix.prefix-sum
type: qa
anki: 1787175409884
tags: [lc::1094, leetcode, pattern, recall]
---
## Q
对于区间批量增减、求区间内最大/最小累积值的问题（如上下车人数、会议室占用），如何避免逐点更新导致的高复杂度？

## A
使用差分数组（Difference Array）：对每个区间 [from, to) 施加变化量 num 时，只需 deltas[from] += num; deltas[to] -= num；最后对 deltas 做前缀和（accumulate）即可得到每个位置的实际值，一次遍历判断是否超过容量。将逐点更新的 O(n·range) 降为 O(n + range)。等价写法是将 (from, +num) 和 (to, -num) 存入事件列表按位置排序后扫描（扫描线），本质相同。

**Evidence**

carPooling0 用完整数组逐点 `for loc in range(f, t): onboard[loc] += num` 更新，笔记中标注'这个是完整数组，但是改成差分数组就能降低复杂度'；carPooling 用 `deltas[f] += num; deltas[t] -= num` 加 `accumulate(deltas)` 实现，且笔记指出'很多差分的题也可以用扫描线做'，并关联了 Meeting Rooms II。

[原文 ↗](obsidian://open?vault=lc&file=questions%2F1094%20-%20Car%20Pooling)
