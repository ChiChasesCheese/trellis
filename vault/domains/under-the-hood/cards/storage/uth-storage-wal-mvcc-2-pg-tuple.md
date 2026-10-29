---
id: uth-storage-wal-mvcc-2-pg-tuple
node: storage.wal-mvcc
type: qa
step: 3
---
## Q
**PostgreSQL：旧版本就留在表里**｜PostgreSQL · 18

PostgreSQL 里 `UPDATE` 一行，旧数据去哪了？读事务为什么不用等写事务？

## A
**背景。** MVCC 要保留旧版本。PostgreSQL 的做法最直白：旧版本就留在原来的表里。

**结构。** 堆表里每个元组（tuple，一行记录的一个版本）带 23 字节的头：`t_xmin`（创建它的事务号）、`t_xmax`（删除或锁定它的事务号）、`t_ctid`（指向新版本的指针）。`UPDATE` = 写一个新元组，并把旧元组的 `xmax` 设成当前事务。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 146">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">旧元组</text>
<rect x="12" y="20" width="102" height="26" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="63" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">xmin=100</text>
<rect x="118" y="20" width="102" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="169" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">xmax=105</text>
<rect x="224" y="20" width="102" height="26" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="275" y="37.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">ctid</text>
<text x="8" y="76" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">新元组</text>
<rect x="12" y="84" width="102" height="26" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="63" y="101.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">xmin=105</text>
<rect x="118" y="84" width="102" height="26" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="169" y="101.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">xmax=0</text>
<rect x="224" y="84" width="102" height="26" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="275" y="101.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">新数据</text>
<line x1="275" y1="46" x2="275" y2="76" stroke="currentColor" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="275,82 272.0,76.0 278.0,76.0" stroke="currentColor" stroke-width="0.5" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)"/>
<text x="170" y="140" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">UPDATE: 写新元组, 旧的 xmax 设为 105</text>
</svg>
```

**细节。**

- 读事务拿一个快照，逐个元组判断：`xmin` 已提交且在快照之前、`xmax` 未提交或在快照之后，这个版本才可见。
- 没有任何快照还需要的旧版本叫死元组，由 `VACUUM`（后台清理任务）回收。

**为什么。** 读不加锁、不阻塞写；代价是表会膨胀，必须靠 VACUUM 清理。

**例题：** LC 1146 快照数组

实现 `SnapshotArray(length)`：`set(index, val)` 改值；`snap()` 拍快照并返回快照号；`get(index, snap_id)` 返回拍下该快照时 `index` 处的值。初始元素都是 `0`。

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
