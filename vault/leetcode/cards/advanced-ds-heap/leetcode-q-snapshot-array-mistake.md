---
id: leetcode-q-snapshot-array-mistake
node: advanced-ds-heap.persistent-data-structure
type: qa
anki: 1787102794785
tags: [lc::1146, leetcode, mistake, recall]
---
## Q
为什么 Snapshot Array 不能在每次 snap() 时直接拷贝整个数组？

## A
会导致 MLE：如果用 self.history[snap_id] = self.cur[:] 做全量拷贝，空间开销是「数组长度 × snap 次数」，两者只要有一个大就爆内存。正确做法是每个 index 只记录变化点 (snap_id, val)，而不是把整个数组状态复制一份保存起来。

**Evidence**

class SnapshotArray_mle 中: self.history[snap_id] = self.cur[:] # 完整拷贝，非常慢；注释 'need to use temp arr as cur, not abuse prev snaps'

[原文 ↗](obsidian://open?vault=lc&file=questions%2F1146%20-%20Snapshot%20Array)
