---
id: tlc-tt-removable-timestamp-task-scheduler-4-followup
node: b.tt-removable-timestamp-task-scheduler
type: qa
step: 4
---
## Q
**可删除任务的时间戳调度器（popTask）**｜追问

面试官接着问：（1）大量 `removeTask` 之后堆里积压了很多失效条目，内存怎么办？（2）能不能让 `removeTask` 严格 `O(log n)`、不留任何残余？（3）再加一个 `peekTask()`。

## A
1. **清理积压**：当堆长度超过存活任务数的两倍时，用 `alive` 重建堆。重建是 `O(存活数)`，摊到之前的删除上仍是常数摊还。

```python
import heapq


def compact(heap: list[tuple[int, str]], alive: dict[str, int]) -> list[tuple[int, str]]:
    if len(heap) <= 2 * len(alive) + 16:
        return heap                                   # 积压不多，不必重建
    fresh = [(ts, tid) for tid, ts in alive.items()]
    heapq.heapify(fresh)                              # 线性时间建堆
    return fresh
```

先加 `100` 个任务再删 `90` 个，堆长度 `100`；重建后只剩 `10` 项，`popTask(3)` 得到最早的三个存活任务。
2. **严格删除**：用有序集合（平衡二叉搜索树、跳表），按 `(timestamp, taskId)` 排序，插入、删除、取最小都是 `O(log n)` 且没有残余。Python 标准库没有，面试里说明思路，需要时用第三方 `sortedcontainers.SortedList`。
3. **`peekTask()`**：先弹掉堆顶所有失效的条目（循环 `while heap and alive.get(id) != ts: heappop`），再读 `heap[0]`，不取走。这个清理不改变语义，只是提前做掉了本来也会做的丢弃。

**Python 提醒**：`heapq` 的堆顶是 `heap[0]`，其余位置不保证有序，所以不能用 `heap` 的遍历顺序或下标当排序结果；需要前 `k` 个而又不想移除时，用 `heapq.nsmallest(k, heap)`，它只读，不修改堆。
