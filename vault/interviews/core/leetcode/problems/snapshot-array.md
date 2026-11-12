---
slug: snapshot-array
---
## Q
**LC 1146 快照数组**｜Medium

实现 `SnapshotArray(length)`，支持 `set(index, val)`、`snap()`（返回快照号）和 `get(index, snap_id)`（取该快照时的值）。初始全为 `0`。

## A
**一句话。** 不复制数组，每个下标存「(快照号, 值)」历史，`get` 在历史里二分。

```python
class SnapshotArray:
    def __init__(self, length):
        self.snap_id = 0
        # 每个下标一条历史，初值 0 记在快照 0
        self.history = [[(0, 0)] for _ in range(length)]

    def set(self, index, val):
        hist = self.history[index]
        if hist[-1][0] == self.snap_id:   # 同一快照期：覆盖
            hist[-1] = (self.snap_id, val)
        else:
            hist.append((self.snap_id, val))

    def snap(self):
        self.snap_id += 1
        return self.snap_id - 1

    def get(self, index, snap_id):
        hist = self.history[index]
        # 最后一个快照号 <= snap_id 的记录
        pos = bisect_right(hist, snap_id,
                           key=lambda r: r[0]) - 1
        return hist[pos][1]
```

**复杂度。** 时间 `set`、`snap` 为 `O(1)`，`get` 为 `O(log k)`，空间 `O(length+写入次数)`。

**易错点。**
- `snap` 复制整个数组：`50000×50000` 个整数，内存爆炸。
- 二分用 `bisect_left`：`set(0,5)`、`snap`、`set(0,6)`、`snap`，`get(0,1)` 应为 `6`，会得 `5`。
- 没有初始记录：从未写过的下标历史为空，取 `[-1]` 出错。

**追问。**
- 下标范围很大？：`history` 改成 `defaultdict`，只为写过的下标建历史，`get` 无记录返回 `0`。
- 同模式的键值版（LC 981）？：键换字符串、快照号换时间戳，同样「每键一份有序历史 + 二分」。

**同模式。** LC 981 基于时间的键值存储、LC 2034 股票价格波动、LC 146 LRU 缓存、LC 432 全 O(1) 的数据结构
