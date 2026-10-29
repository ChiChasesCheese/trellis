---
id: uth-compose-k8s-workqueue-3-code
node: compose.k8s-workqueue
type: qa
step: 3
---
## Q
**不变量与核心代码**｜Kubernetes · client-go v0.37

三个结构之间必须保持哪些关系？用 Python 写出最小版本。

## A
**不变量。**

- `queue` 里的每个 key 都在 `dirty` 里，且不在 `processing` 里
- 同一个 key 在 `queue` 里至多一份
- key 在 `dirty` 里，就表示它还欠一次处理

**细节。**

- `add`：先记 `dirty`，再决定入不入队，顺序不能反
- `get`：弹出后立刻从 `dirty` 删除，因为这次处理会读到最新状态，旧账清零
- `done`：先离开 `processing`，再看 `dirty` 有没有新账
- 真实实现里三个方法在同一把锁里执行，别的线程看不到中间状态

```python
from collections import deque


class WorkQueue:
    def __init__(self) -> None:
        self.queue: deque[str] = deque()    # 只管顺序：放着等待处理的 key
        self.dirty: set[str] = set()        # 还欠一次处理的 key
        self.processing: set[str] = set()   # 正被 worker 处理的 key

    def add(self, key: str) -> None:
        if key in self.dirty:               # 已经欠着一次：合并，不重复排队
            return
        self.dirty.add(key)
        if key in self.processing:          # 正在处理：先记账，done 时再入队
            return
        self.queue.append(key)

    def get(self) -> str | None:            # 真实版在队列空时阻塞等待
        if not self.queue:
            return None
        key = self.queue.popleft()
        self.processing.add(key)
        self.dirty.discard(key)             # 这次处理会读最新状态，旧账清零
        return key

    def done(self, key: str) -> None:
        self.processing.discard(key)
        if key in self.dirty:               # 处理期间又来了新事件：补一轮
            self.queue.append(key)
```

例：`add("a")` 两次，队列里只有一份 `a`；`get()` 取走 `a` 后再 `add("a")`，只记在 `dirty`、不入队；`done("a")` 才把它补回队列。

**例题：** 卖家任务调度器（轮转 + VIP + 优先级）

任务属于不同卖家：`receive_task(task_id, seller_id, priority, timestamp)` 接收任务，`process_next_task()` 取下一个任务，没有则返回 `None`。卖家之间轮转，VIP 卖家每轮处理两个；同一卖家内部按 `priority`、`timestamp`、到达顺序；卖家的任务处理完就退出轮转，再收到它的任务时排到队尾。例：VIP 为 `{"V"}`，依次接收 `(t1,A,2,1)`、`(t2,A,1,2)`、`(t3,V,1,3)`、`(t4,V,2,4)`、`(t5,V,3,5)`、`(t6,B,1,6)`，连续处理七次 → `t2, t3, t4, t6, t1, t5, None`。

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
