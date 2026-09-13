---
id: leetcode-q-time-based-key-value-store-pattern
node: design-simulation.design
type: qa
anki: 1787102263282
tags: [lc::981, leetcode, pattern, recall]
---
## Q
如何设计支持“按时间戳查询最近版本”的 Time Based Key-Value Store（TimeMap）？

## A
用 dict[key] -> list[(timestamp, value)]，set 时按 key 分组 append（题目保证 timestamp 严格递增，天然有序，无需排序）。get 时对该 key 的列表用 bisect_right(timestamps, target) - 1 做二分查找，取小于等于 target 的最大 timestamp 对应的 value；索引 < 0 说明没有符合条件的记录，返回 ""。核心不变量：每个 key 对应的时间戳序列单调递增，可直接二分；set 均摊 O(1)，get 为 O(log n)。

**Evidence**

self.dic[key].append((timestamp, value)) 结合 bisect_right(self.dic[key], timestamp, key=lambda x: x[0]) - 1，并对 idx < 0 返回空字符串。

[原文 ↗](obsidian://open?vault=lc&file=questions%2F981%20-%20Time%20Based%20Key-Value%20Store)
