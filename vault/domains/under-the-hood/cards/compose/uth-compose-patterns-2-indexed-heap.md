---
id: uth-compose-patterns-2-indexed-heap
node: compose.patterns
type: qa
step: 2
---
## Q
**哈希表 + 带下标的堆：能取消，也能改优先级**｜Kubernetes 调度队列 · 1.37

堆取最小只要 O(log n)，但要取消其中某个任务、或改它的优先级，得先在堆里找到它。怎样让这两件事也是 O(log n)？

## A
**背景。** 堆（heap）是存进数组的完全二叉树，只保证“父不大于子”：最小的在下标 0，取出和插入是 O(log n)。别处无序，找指定元素只能扫，O(n)。

**结构。** 加一张哈希表：key → 数组下标，堆里每次交换都同步改它。取消 = 与末尾换位，再上浮或下沉；改优先级 = 原地改值，再上浮或下沉。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 206">
<text x="14" y="14" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">堆数组 (key 优先级) 与下标</text>
<text x="48.0" y="33" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">0</text>
<rect x="22" y="38" width="52" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="48.0" y="56.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a 1</text>
<text x="104.0" y="33" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">1</text>
<rect x="78" y="38" width="52" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="104.0" y="56.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b 3</text>
<text x="160.0" y="33" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">2</text>
<rect x="134" y="38" width="52" height="28" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="160.0" y="56.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c 2</text>
<text x="216.0" y="33" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">3</text>
<rect x="190" y="38" width="52" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="216.0" y="56.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">d 7</text>
<text x="272.0" y="33" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">4</text>
<rect x="246" y="38" width="52" height="28" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="272.0" y="56.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">e 5</text>
<rect x="22" y="100" width="52" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="48.0" y="117.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">c: 2</text>
<rect x="78" y="100" width="52" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="104.0" y="117.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">a: 0</text>
<rect x="134" y="100" width="52" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="160.0" y="117.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">e: 4</text>
<rect x="190" y="100" width="52" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="216.0" y="117.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">b: 1</text>
<rect x="246" y="100" width="52" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="272.0" y="117.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">d: 3</text>
<polyline points="48.0,100 48.0,84 160.0,84 160.0,68" fill="none" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="160.0,68.0 162.5,73.0 157.5,73.0" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="14" y="144" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">哈希表: key 到下标</text>
<text x="170" y="166" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">取消 c: 查表得下标 2</text>
<text x="170" y="182" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">换到末尾 再上浮或下沉 O(log n)</text>
<text x="170" y="198" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">每次交换 都要同步改表里的下标</text>
</svg>
```

| 操作 | 做法 | 复杂度 |
|---|---|---|
| 插入 | 放末尾上浮，登记下标 | O(log n) |
| 取消 / 改优先级 | 查表得下标再调整 | O(log n) |

**细节。**

- Kubernetes 调度器的待调度队列（`heap.Heap`）：`keyIndex map[string]int`，在 `Swap` 里同步
- Java `DelayedWorkQueue`（OpenJDK 25）：任务对象自带 `heapIndex`，没有哈希表
- Go 1.24 的 `container/heap` 示例：元素带 `index` 字段，改完调用 `heap.Fix`

**为什么。** 另一种做法是懒删除（lazy deletion）：只标记“已取消”，浮到堆顶再丢（Python `heapq` 文档的写法）。简单，但废项占着堆，取消多时堆会膨胀。

**坑。** 交换时漏改一个下标，之后就会取消错元素。

**例题：** 可删除任务的时间戳调度器（popTask）（同类：带 TTL 的 LRU 缓存）

实现任务调度器：`addTask(taskId, timestamp)` 加入任务（已存在则更新时间戳）；`removeTask(taskId)` 删除尚未取走的任务；`popTask(num)` 返回时间戳最早的 `num` 个任务并移除，时间戳相同按 `taskId` 字典序。操作总数不超过 `10^5`。例：加入 `(a,5)`、`(b,3)`、`(c,3)`，`popTask(2)` 得 `['b','c']`。下面是同一道题的懒删除写法，对比卡片里“带下标”的做法。

```python
import heapq


class TaskScheduler:
    def __init__(self) -> None:
        self._heap: list[tuple[int, str]] = []      # (timestamp, task_id)：时间戳小者在前，相同时按 task_id 字典序
        self._alive: dict[str, int] = {}            # 仍在调度器里的任务 -> 它当前的时间戳

    def addTask(self, task_id: str, timestamp: int) -> None:
        self._alive[task_id] = timestamp            # 同一个 id 重复加入视为改时间戳
        heapq.heappush(self._heap, (timestamp, task_id))

    def removeTask(self, task_id: str) -> bool:
        return self._alive.pop(task_id, None) is not None   # 只改字典，堆里的旧条目等弹出时再丢（懒删除）

    def popTask(self, num: int) -> list[str]:
        out: list[str] = []
        while self._heap and len(out) < num:
            timestamp, task_id = heapq.heappop(self._heap)
            if self._alive.get(task_id) != timestamp:   # 已被删除或已被改过时间戳的旧条目：跳过
                continue
            del self._alive[task_id]                    # popTask 取走即移除
            out.append(task_id)
        return out
```
