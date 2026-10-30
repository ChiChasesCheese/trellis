---
id: tlc-tt-seller-task-scheduler-0-whole
node: p4.tt-seller-task-scheduler
type: qa
---
## Q
**卖家任务调度器（轮转 + VIP + 优先级）**｜Medium · 近一年被问：美国 1 次、国内 0 次 · 最近 2026-09-02（面试记录）

实现一个任务调度器，任务属于不同卖家（seller）。接口：`receive_task(task_id, seller_id, priority, timestamp)` 接收一个任务；`process_next_task() -> task_id | None` 取出下一个要处理的任务，没有任务时返回 `None`。规则：（1）在有任务的卖家之间轮转（round-robin）：轮到一个卖家就处理它的一个任务，再轮到下一个卖家；（2）VIP 卖家（构造时给出）每轮可以处理两个任务，只剩一个时处理一个就轮到下一位；（3）同一卖家内部先按 `priority`（数值小的先），`priority` 相同按 `timestamp`，再相同按接收顺序；（4）卖家的任务全部处理完后退出轮转，之后再收到它的任务时，重新排到轮转队尾。操作总数不超过 `10^5`。例：VIP 卖家为 `{"V"}`，依次接收 `(t1,A,2,1)`、`(t2,A,1,2)`、`(t3,V,1,3)`、`(t4,V,2,4)`、`(t5,V,3,5)`、`(t6,B,1,6)`，连续调用 `process_next_task()` 七次 → `t2, t3, t4, t6, t1, t5, None`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 两层结构：外层用 `deque` 做卖家的轮转队列，队首就是当前轮到的卖家；每个卖家一个最小堆，堆元素是 `(priority, timestamp, 到达序号, task_id)`。再记下队首卖家本轮已处理的个数，达到配额（VIP 为 `2`，其他为 `1`）就把它转到队尾；堆空了就退出队列。接收和处理都是 `O(log k)`，`k` 是该卖家的待处理任务数。

**识别。** 「在组之间轮转 + 组内按优先级」就是外层循环队列加内层优先队列；「处理完退出、再来重新加入」说明队列里只放有任务的卖家，用「该卖家在字典里有没有堆」就能判断是否已在队列中。

**推导。** 暴力：每次 `process_next_task` 扫描所有任务，先按轮转算出该谁，再在他的任务里找最小，`O(N)` 一次 → 浪费：「该谁」和「该处理他的哪个」被混在一起重复扫描 → 洞察：把它们拆开。「该谁」永远是队首，`O(1)`；「处理哪个」是该卖家堆顶，`O(log k)`。队列里同一时刻只有队首的卖家可能处在「进行中的一轮」，所以只需要一个计数器 `_served`，配额用完或退出时清零。

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

运行：上面的例子 → `['t2', 't3', 't4', 't6', 't1', 't5', None]`；`{"V"}` 下先收 `x`（V）、`y`（A），调用三次 → `x, y, None`，之后再收 `z`、`w`（V）、`u`（A），调用四次 → `z, w, u, None`（V 退出后重新加入，又拿满两个）；没有任务时调用 → `None`。

**复杂度。** `receive_task` 和 `process_next_task` 都是 `O(log k)`；空间 `O(N)`。

**易错点。**
- 卖家重复入队：收到任务时不判断「是否已在队列」就 `append`。`A` 收两个任务、`B` 收一个，队列变成 `A, A, B`，会得到 `t1, t2, t3`，正确是 `t1, t3, t2`。
- 卖家退出时没把 `_served` 清零：`{"V","W"}` 为 VIP，`V` 有 `x`，`W` 有 `y, z`，`A` 有 `a`。`V` 处理 `x` 后退出，计数残留为 `1`，`W` 只处理了 `y` 就被转走，得到 `x, y, a, z`，正确是 `x, y, z, a`。
- 用 `heapq` 当最大堆：`heapq` 只有最小堆，约定是数值小的优先；要大的优先就存 `-priority`。

**追问。**
- 加权轮转：配额从固定的 `2 / 1` 换成每个卖家的权重 `weight[seller]`，其余不变。
- 防饥饿：卖家内部持续来高优先级任务，低优先级会一直等；可以加老化，等待越久有效优先级越高。
- 取消任务或删除卖家：堆里用懒删除，记录已取消的 `task_id`，弹出时跳过；卖家被删时从队列中摘掉。

**同模式。** LC 621 任务调度器、LC 1834 单线程 CPU、LC 355 设计推特、LC 253 会议室 II。
