---
id: tlc-snapshot-array-0-whole
node: b.snapshot-array
type: qa
---
## Q
**LC 1146 快照数组**｜Medium · TikTok 高频

实现支持快照的数组 `SnapshotArray`：`SnapshotArray(length)` 初始化长度为 `length` 的数组，所有元素初始为 `0`；`set(index, val)` 把下标 `index` 处设为 `val`；`snap()` 给当前数组拍快照，返回快照号 `snap_id`（等于 `snap()` 的总调用次数减一）；`get(index, snap_id)` 返回拍下编号为 `snap_id` 的那次快照时，下标 `index` 处的值。

约束：`1 <= length <= 50000`，`set` / `snap` / `get` 总共最多 `50000` 次调用，`0 <= index < length`，`0 <= snap_id <` `snap()` 的调用次数，`0 <= val <= 10^9`。

例：`SnapshotArray(3)`；`set(0,5)`；`snap()` → `0`；`set(0,6)`；`get(0,0)` → `5`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 不复制数组，而是给每个下标记一份「(快照号, 值)」的历史；`set` 只往该下标的历史追加（同一快照期覆盖），`snap` 只把快照号加一，`get` 在该下标的历史里二分查找最后一个快照号不超过 `snap_id` 的记录。

**识别。** 「快照 / 版本 / 回看历史」的设计题：天真的做法是每次 `snap` 复制整个数组，空间 `O(snaps × length)`，在 `50000 × 50000` 的规模下是 `2.5·10^9` 个整数，立刻爆内存。信号：操作次数 `50000`、数组长度 `50000`、只有少数下标会被修改 → 记录**变化**而不是整体副本；读取按「时间」查找 → 历史按快照号有序 → **二分**。

**推导。** 朴素：`snap` 时复制数组，`get` 直接取，`snap` 是 `O(length)`、空间 `O(snaps·length)`，最坏 `2.5·10^9`。浪费在于：两次快照之间只有少数下标变了，却整份复制。改进：只记录变化。每个下标维护一份有序历史 `[(snap_id, val), ...]`，快照号单调递增（`snap_id` 只增不减）；`set` 在当前快照期内追加或覆盖，`snap` 只自增计数；`get` 要的是「在 `snap_id` 那一刻（含）之前最后一次写入的值」，也就是按快照号二分，找最后一个 `<= snap_id` 的记录。初始值 `0` 作为 `(0, 0)` 放在每个下标的历史开头，保证二分一定有结果。

```python
class SnapshotArray:
    def __init__(self, length: int) -> None:
        self.snap_id = 0
        # 每个下标一条历史：(写入时的快照号, 值)，快照号递增；初始值 0 记在快照 0
        self.history: list[list[tuple[int, int]]] = [[(0, 0)] for _ in range(length)]

    def set(self, index: int, val: int) -> None:
        hist = self.history[index]
        if hist[-1][0] == self.snap_id:        # 同一个快照期内多次写：覆盖即可
            hist[-1] = (self.snap_id, val)
        else:
            hist.append((self.snap_id, val))

    def snap(self) -> int:
        self.snap_id += 1                      # 不复制数组，只推进快照号
        return self.snap_id - 1

    def get(self, index: int, snap_id: int) -> int:
        hist = self.history[index]
        # 找最后一个 “快照号 <= snap_id” 的记录
        pos = bisect_right(hist, snap_id, key=lambda rec: rec[0]) - 1
        return hist[pos][1]
```

运行：`["SnapshotArray","set","snap","set","get"], [[3],[0,5],[],[0,6],[0,0]]` → `[None, None, 0, None, 5]`，`没写过的下标` → `[None, 0, 0]`，`同一快照期内写两次、再跨快照读` → `[None, None, None, 0, None, 1, 2, 3]`，`length=50000 连续 50000 次 snap，最后一次的返回值` → `49999`。

**复杂度。** `set` 与 `snap` 均 `O(1)`；`get` 是 `O(log k)`，`k` 为该下标被写入过的快照期个数（二分）；空间 `O(length + 写入次数)`，不随快照次数增长。

**易错点。**
- `snap` 复制整个数组：`50000 × 50000` 个整数，内存爆炸；`snap` 本身也变成 `O(length)`。
- 二分用了 `bisect_left`：找不到恰好等于 `snap_id` 的那条记录。`set(0,5)`、`snap()`、`set(0,6)`、`snap()`，`get(0,1)` 应得 `6`，用 `bisect_left` 得 `5`。必须用 `bisect_right` 再减 1。
- 没有初始记录：从未写过的下标，历史为空，二分结果 `-1`，对 `[]` 取下标出错；给每个下标放 `(0, 0)` 就不会。
- 同一个快照期内多次 `set` 都追加，历史会变长：结果仍然对（`bisect_right` 取最后一条），但浪费空间；覆盖最后一条更省。

**追问。**
- 再加 `rollback(snap_id)`（回到某个快照）：把每个历史里快照号 `> snap_id` 的记录截掉，并把 `snap_id` 设回去；摊还可以接受，但要遍历被改过的下标，需额外记录哪些下标被写过。
- 下标范围很大（稀疏数组）：`history` 改成 `defaultdict(list)` 或 `dict`，只为被写过的下标建历史，`get` 找不到就返回默认值 `0`。
- 同一模式的「时间版 KV 存储」（LC 981）：键换成字符串、快照号换成时间戳，同样「每键一份有序历史 + 二分」。

**同模式。** LC 981 基于时间的键值存储、LC 1244 力扣排行榜、LC 2034 股票价格波动、LC 146 LRU 缓存（设计题对比）、LC 432 全 O(1) 的数据结构。
