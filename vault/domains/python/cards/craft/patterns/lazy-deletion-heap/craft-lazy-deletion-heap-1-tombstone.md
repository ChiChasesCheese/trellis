---
id: craft-lazy-deletion-heap-1-tombstone
node: craft.patterns.lazy-deletion-heap
type: qa
step: 1
---
## Q
**惰性删除堆 · heapq 删不了中间元素，取消任务怎么办**｜写法

调度器用 `heapq` 存任务的到期时间。用户取消一个还没到期的任务，它在堆中间，`heapq` 只有 `heappush` 和 `heappop`。直接 `heap.remove(x)` 再 `heapify` 行吗？不删的话又怎么保证它不会被执行？

## A
**要点。** 不真正删，只标记它无效（墓碑，tombstone），等它浮到堆顶被弹出时再丢掉。取消变成 O(1)，丢弃的成本摊在弹出上。`remove` 是 O(n) 的查找，`heapify` 又是 O(n)，每次取消都付一遍。

```python
if mode == "remove+heapify":
    heap.remove((tid, tid))        # O(n) 查找 + 移动
    heapq.heapify(heap)            # 再 O(n) 重建
else:
    dead.add(tid)                  # O(1)：只做标记

# 取任务时
due, tid = heapq.heappop(heap)
if tid in dead:
    continue                       # 墓碑：弹出时丢弃
```

2 万个任务，取消 300 个，再取最早的 5000 个执行：

```
remove+heapify  取消耗时   150.1 ms，已执行 5000 个，其中被取消的 0 个
tombstone       取消耗时     0.0 ms，已执行 5000 个，其中被取消的 0 个
```

耗时数字随机器变化，两者相差的量级才是要点；两种做法都没执行被取消的任务。

**代价。** 墓碑占着内存，直到被弹出或被压实（见第 3 张卡）；堆的大小不再等于任务的数量。

**为什么。** 这是 `heapq` 文档里的配方：用标记代替删除，用弹出时的过滤代替查找。
