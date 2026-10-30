---
id: tlc-snapshot-array-1-signal
node: b.snapshot-array
type: qa
step: 1
---
## Q
**LC 1146 快照数组**｜Medium · LC TikTok 热度 68/100

实现支持快照的数组 `SnapshotArray`：`SnapshotArray(length)` 初始化长度为 `length` 的数组，所有元素初始为 `0`；`set(index, val)` 把下标 `index` 处设为 `val`；`snap()` 给当前数组拍快照，返回快照号 `snap_id`（等于 `snap()` 的总调用次数减一）；`get(index, snap_id)` 返回拍下编号为 `snap_id` 的那次快照时，下标 `index` 处的值。

约束：`1 <= length <= 50000`，`set` / `snap` / `get` 总共最多 `50000` 次调用，`0 <= index < length`，`0 <= snap_id <` `snap()` 的调用次数，`0 <= val <= 10^9`。

例：`SnapshotArray(3)`；`set(0,5)`；`snap()` → `0`；`set(0,6)`；`get(0,0)` → `5`。

题面里哪些信号指向哪个模式？从暴力解怎样一步步推到最优解？

## A
**信号 → 模式。**
- 「快照 / 历史版本」+ 大量操作 → 不能整体复制，要**只记录变化**（持久化数据结构的朴素版本）。
- `get(index, snap_id)` 按「时间」读取：同一个下标的写入历史按快照号**有序** → 在每个下标的历史上用**二分**。
- `length`、操作数都是 `50000` → `snap × length` 的整体复制是 `2.5·10^9`，内存与时间都爆；每个操作需要 `O(1)` / `O(log n)`。

**推导链。**
1. 暴力：`snap` 复制整个数组，`get` 直接读副本；空间 `O(snaps · length)`，`snap` 是 `O(length)`。
2. 浪费：相邻快照之间只有少数下标变了，大部分是重复数据。
3. 洞察：每个下标一条历史 `[(snap_id, val)]`，按快照号递增；`set` 追加，`snap` 只自增计数。
4. 最优：`get` 时在历史里二分，找最后一个快照号 `<= snap_id` 的记录（`bisect_right - 1`）；`set` / `snap` `O(1)`，`get` `O(log k)`。

**同模式的题**：LC 981 基于时间的键值存储、LC 2034 股票价格波动、LC 1244 力扣排行榜、LC 635 设计日志存储系统。
