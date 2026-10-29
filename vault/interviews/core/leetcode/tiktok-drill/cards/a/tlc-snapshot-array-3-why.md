---
id: tlc-snapshot-array-3-why
node: a.snapshot-array
type: qa
step: 3
---
## Q
**LC 1146 快照数组**｜正确性

为什么 `get` 要用 `bisect_right(...) - 1`？用 `bisect_left` 会错在哪里？为什么历史里的快照号一定是有序的？

## A
**不变量。** 对每个下标，`history[index]` 的快照号严格递增（同一快照期只留一条），且第一条是 `(0, 0)`。`set` 总是用当前 `snap_id` 写入，而 `snap_id` 只增不减，所以追加的记录一定在末尾，保持有序。

**`get` 要什么。** 在 `snap_id` 那次快照时（含）的值 = 该下标在「快照期 `<= snap_id`」内最后一次写入的值。快照期 `snap_id` 内的写入发生在第 `snap_id` 次 `snap()` 之前，所以应包含在快照里。

**为什么 `bisect_right`。** 它返回第一个「快照号 `> snap_id`」的位置，减 `1` 就是最后一个「快照号 `<= snap_id`」的记录。`bisect_left` 返回第一个「`>= snap_id`」的位置，减 `1` 就会错过恰好等于 `snap_id` 的那条。

**反例。** `SnapshotArray(1)`，`set(0,5)`，`snap()` → `0`，`set(0,6)`，`snap()` → `1`。历史为 `[(0,5), (1,6)]`。`get(0,1)`：`bisect_right` 找到位置 `2`，减 `1` 得下标 `1`，值 `6`；`bisect_left` 找到位置 `1`，减 `1` 得下标 `0`，值 `5`，错。
