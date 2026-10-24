---
id: tlc-tt-seller-task-scheduler-2-code
node: a.tt-seller-task-scheduler
type: qa
step: 2
---
## Q
**卖家任务调度器（轮转 + VIP + 优先级）**｜写出 Python 实现

用类实现任务调度器：构造时给出 VIP 卖家集合；`receive_task(task_id, seller_id, priority, timestamp)` 接收任务；`process_next_task()` 返回下一个任务的 `task_id`，没有任务返回 `None`。卖家之间轮转，VIP 每轮处理两个，其余一个；卖家内部先 `priority`（小者先）、再 `timestamp`、再接收顺序；卖家任务处理完后退出轮转，再收到任务时排到队尾。操作总数不超过 `10^5`。

## A
**思路。** `deque` 保存有任务的卖家，队首是当前卖家；`dict` 保存每个卖家的最小堆。`_served` 记录队首卖家本轮已处理几个，到达配额就 `rotate(-1)`，堆空就弹出队首。

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

运行：VIP 为 `{"V"}`，依次接收 `(t1,A,2,1)`、`(t2,A,1,2)`、`(t3,V,1,3)`、`(t4,V,2,4)`、`(t5,V,3,5)`、`(t6,B,1,6)`，调用七次 → `['t2', 't3', 't4', 't6', 't1', 't5', None]`；空调度器 → `None`；`x`（V）、`y`（A）后调用三次 → `x, y, None`，再收 `z`、`w`（V）、`u`（A）后调用四次 → `z, w, u, None`。

**复杂度。** 两个操作都是 `O(log k)`，`k` 为该卖家的待处理任务数；空间 `O(N)`。

**写法要点。** 元组 `(priority, timestamp, seq, task_id)` 利用元组的字典序一次表达三级排序；`itertools.count()` 生成单调递增的序号，保证元组不会比较到 `task_id`（`task_id` 可能不可比较）；`deque.rotate(-1)` 是 `O(1)` 地把队首移到队尾；`dict.get` 返回 `None` 当作「卖家不在轮转中」，同时避免两个数据结构各存一份状态；`heapq.heappop(heap)[-1]` 取元组最后一项即 `task_id`。
