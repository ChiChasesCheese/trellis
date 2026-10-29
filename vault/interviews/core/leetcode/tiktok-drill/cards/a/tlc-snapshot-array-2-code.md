---
id: tlc-snapshot-array-2-code
node: a.snapshot-array
type: qa
step: 2
---
## Q
**LC 1146 快照数组**｜写出 Python 实现

实现 `SnapshotArray` 类：`set(index: int, val: int)`、`snap() -> int`、`get(index: int, snap_id: int) -> int`。数组长度 `1..50000`，三种操作合计最多 `50000` 次，初值为 `0`。`snap` 不能复制整个数组。

## A
**思路。** 每个下标一条历史，元素是 `(快照号, 值)`，开头放 `(0, 0)` 代表初值。`set` 往该下标的历史末尾追加；如果最后一条的快照号等于当前快照号，直接覆盖。`snap` 只把快照号加一并返回旧值。`get` 在该下标的历史上用 `bisect_right` 按快照号二分，取最后一个快照号不超过 `snap_id` 的记录的值。

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

**写法要点。** `bisect_right(hist, snap_id, key=lambda rec: rec[0])` 用 Python 3.10+ 的 `key` 参数，按元组的第一项二分，不用额外构造一个只含快照号的列表，也不用 `(snap_id, inf)` 这种哨兵技巧；减 `1` 得到「最后一个 `<=`」；初值 `(0, 0)` 保证 `pos >= 0`；`[[(0, 0)] for _ in range(length)]` 用推导式，避免 `[[(0, 0)]] * length` 让所有下标共享同一个列表；元组是不可变的，覆盖要整体替换 `hist[-1] = (...)`。
