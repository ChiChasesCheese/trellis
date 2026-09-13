---
id: leetcode-q-snapshot-array-pattern
node: advanced-ds-heap.persistent-data-structure
type: qa
anki: 1787102261281
tags: [lc::1146, leetcode, pattern, recall]
---
## Q
Snapshot Array 如何做到 set/snap O(1)、get O(log n)？

## A
每个 index 维护一个按 snap_id 递增的 [snap_id, val] 列表；set 时只追加新记录，不覆盖旧值；snap 只是自增一个全局计数器；get 时二分查找“≤ snap_id 的最后一条记录”——用 bisect_left(records, snap_id+1, key=lambda x: x[0]) - 1 定位。这是持久化数据结构（persistent data structure）的核心思路：只增量追加新版本，不修改/复制旧版本，用二分把“查某个历史时刻的值”转成“查有序序列里最后一个 ≤x 的位置”。

**Evidence**

self.history_records = [[[0, 0]] for _ in range(length)] ... self.history_records[index].append([self.id, val]) ... snap_index = bisect.bisect_left(self.history_records[index], snap_id + 1, key=lambda x: x[0]); return self.history_records[index][snap_index - 1][1]

[原文 ↗](obsidian://open?vault=lc&file=questions%2F1146%20-%20Snapshot%20Array)
