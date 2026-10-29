---
id: uth-redis-event-loop-persistence-2-rdb-fork
node: redis.event-loop-persistence
type: qa
step: 2
---
## Q
**RDB 快照时为什么不停服**｜Redis · 8.10

`BGSAVE` 要把几十 GB 内存写盘，主线程怎么还能处理写命令？

## A
**背景。** 要把内存里的数据存成文件，写的过程中数据还在被修改，前后就不一致。要么停服务写完，要么先拍一张“那一刻的照片”再慢慢写。操作系统的 `fork()` 几乎零成本就能拍出这张照片。

**结构。** `fork()` 出子进程：子进程看到 fork 那一刻的内存，慢慢写盘；父进程照常服务。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 210">
<text x="8" y="14" text-anchor="start" font-size="12" font-family="sans-serif" font-weight="bold" fill="currentColor">fork 之后: 父子两个进程共用同样的内存页</text>
<rect x="10" y="26" width="320" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<text x="170" y="42.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">父进程</text>
<line x1="65" y1="50" x2="65" y2="72" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="65,72 62.3,66.0 67.7,66.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="40" y="74" width="50" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="65" y="91.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">页 1</text>
<line x1="65" y1="134" x2="65" y2="102" stroke="currentColor" stroke-width="1"/>
<polygon points="65,102 67.7,108.0 62.3,108.0" fill="currentColor"/>
<line x1="165" y1="50" x2="165" y2="72" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="165,72 162.3,66.0 167.7,66.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="140" y="74" width="50" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="165" y="91.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">页 2</text>
<line x1="165" y1="134" x2="165" y2="102" stroke="currentColor" stroke-width="1"/>
<polygon points="165,102 167.7,108.0 162.3,108.0" fill="currentColor"/>
<line x1="265" y1="50" x2="265" y2="72" style="stroke:var(--accent,#3b6fd4)" stroke-width="1"/>
<polygon points="265,72 262.3,66.0 267.7,66.0" style="fill:var(--accent,#3b6fd4)"/>
<rect x="240" y="74" width="50" height="26" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="265" y="91.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">页 3</text>
<line x1="265" y1="134" x2="265" y2="102" stroke="currentColor" stroke-width="1"/>
<polygon points="265,102 267.7,108.0 262.3,108.0" fill="currentColor"/>
<rect x="10" y="134" width="320" height="24" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke="currentColor" stroke-width="1"/>
<text x="170" y="150.2" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">子进程 (看到 fork 那一刻的内存, 慢慢写盘)</text>
<text x="8" y="182" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">父进程要改页 2: 先复制一份给自己, 再改副本</text>
<text x="8" y="200" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">谁改哪一页才复制那一页; 子进程的页 2 不变</text>
</svg>
```

**细节。**

- 靠写时复制（copy-on-write）：父子共享内存页，谁改某一页才复制那一页
- 快照期间写得越多，复制的页越多，额外内存越多
- 默认触发：1 小时 1 次修改、5 分钟 100 次、1 分钟 10000 次，满足任一条

**为什么。** 不在主线程里遍历写盘，也不加锁就拿到一致快照。

**坑。** 数据集很大时，`fork()` 本身可能停服几毫秒到一秒。

**例题：** LC 1146 快照数组（同类：LC 981 基于时间的键值存储）

实现 `SnapshotArray(length)`：`set(index, val)` 改值，`snap()` 拍快照并返回快照号，`get(index, snap_id)` 读取拍那次快照时的值。例：`set(0,5)`、`snap()` → `0`、`set(0,6)`、`get(0,0)` → `5`。拍快照不复制整个数组，只记之后的改动，和 `fork` 的写时复制是同一个思路。

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
