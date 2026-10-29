---
id: uth-compose-patterns-4-queue-set
node: compose.patterns
type: qa
step: 4
---
## Q
**队列 + 去重集合：同一个 key 不重复排队**｜Kubernetes workqueue · 1.37

事件不断到来，同一个对象一秒内被改了 100 次，只想让它在队里排一次；它正在被处理时又变了，处理完还得再来一次。怎么拼？

## A
**背景。** 先进先出的队列不管重复：同一个 key 来 100 次就排 100 次。去重要能 O(1) 问“它已经在队里吗”，这是哈希集合的活。

**结构。** 队列 `queue` 管先后；`dirty` 记还没处理的 key；`processing` 记正在处理的 key。

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 206">
<text x="14" y="28" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">队列 queue</text>
<text x="14" y="74" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">dirty 待处理</text>
<text x="14" y="120" text-anchor="start" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">processing 处理中</text>
<rect x="136" y="14" width="42" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="157.0" y="31.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k1</text>
<rect x="182" y="14" width="42" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="203.0" y="31.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k2</text>
<rect x="228" y="14" width="42" height="26" rx="3" stroke="currentColor" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12))"/>
<text x="249.0" y="31.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k3</text>
<rect x="136" y="60" width="42" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="157.0" y="77.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k1</text>
<rect x="182" y="60" width="42" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="203.0" y="77.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k2</text>
<rect x="228" y="60" width="42" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="249.0" y="77.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k3</text>
<rect x="274" y="60" width="42" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="295.0" y="77.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k5</text>
<rect x="136" y="106" width="42" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="157.0" y="123.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k4</text>
<rect x="182" y="106" width="42" height="26" rx="3" stroke-width="1.2" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)"/>
<text x="203.0" y="123.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">k5</text>
<text x="170" y="156" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">Add: 已在 dirty 就丢弃</text>
<text x="170" y="174" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--dim,#6b7280)">正在处理的 key 只进 dirty 不入队</text>
<text x="170" y="192" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">Done: dirty 里又有它 再入队 (k5)</text>
</svg>
```

| 动作 | 规则 |
|---|---|
| Add | `dirty` 里已有就丢弃；否则加入 `dirty`，不在处理中才入队 |
| Get | 出队，放进 `processing`，从 `dirty` 删掉 |
| Done | 从 `processing` 删掉；`dirty` 里又有它就再入队 |

**细节。**

- Kubernetes 的 `workqueue`：队里每个元素都在 `dirty` 里、不在 `processing` 里
- Linux 6.12 工作队列的 `queue_work` 靠一个 PENDING 标志位去重，已在队里就返回 `false`
- 广度优先搜索的“已访问集合”是最小的一种

**为什么。** 100 次变化合并成 1 次处理；处理中的 key 不入队，不会被两个工人同时处理，处理期间的变化也不会丢。

**坑。** 集合和队列要同进同出，少改一边，key 就会卡住。

**例题：** 卖家任务调度器（轮转 + VIP + 优先级）

实现多卖家任务调度器：`receive_task(task_id, seller_id, priority, timestamp)` 接收任务；`process_next_task()` 在有任务的卖家之间轮转，轮到的卖家处理一个任务（VIP 卖家处理两个），卖家内部按 `priority` 小者先；卖家的任务处理完就退出轮转，再收到任务时重新排到队尾。操作总数不超过 `10^5`。

```python
import heapq
from collections import deque
from itertools import count


class SellerScheduler:
    def __init__(self, vip_sellers: set[str] | None = None) -> None:
        self._vip = set(vip_sellers or ())
        self._heaps: dict[str, list[tuple[int, int, int, str]]] = {}   # 卖家 -> 最小堆 (priority, timestamp, 到达序号, task_id)
        self._ring: deque[str] = deque()        # 轮转队列：队首是当前轮到的卖家；有任务的卖家恰好出现一次
        self._served = 0                        # 队首卖家本轮已处理的个数
        self._seq = count()                     # 到达序号：priority 和 timestamp 都相同时保证先到先出

    def receive_task(self, task_id: str, seller_id: str, priority: int, timestamp: int) -> None:
        heap = self._heaps.get(seller_id)
        if heap is None:                        # 卖家此前没有待处理任务：加入轮转队尾
            heap = self._heaps[seller_id] = []
            self._ring.append(seller_id)
        heapq.heappush(heap, (priority, timestamp, next(self._seq), task_id))

    def process_next_task(self) -> str | None:
        if not self._ring:
            return None
        seller = self._ring[0]
        heap = self._heaps[seller]
        task_id = heapq.heappop(heap)[-1]
        self._served += 1
        if not heap:                            # 任务处理完：退出轮转，本轮作废
            self._ring.popleft()
            del self._heaps[seller]
            self._served = 0
        elif self._served == (2 if seller in self._vip else 1):   # 本轮配额用完：转给下一个卖家
            self._ring.rotate(-1)
            self._served = 0
        return task_id
```
