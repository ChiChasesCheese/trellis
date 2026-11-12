---
slug: tt-seller-task-scheduler
---
## Q
**卖家任务调度器（轮转 + VIP + 优先级）**｜Medium

`receive_task(task_id, seller_id, priority, timestamp)` 接收任务，`process_next_task()` 取出下一个任务（没有返回 `None`）。规则：有任务的卖家之间轮转，轮到一个卖家处理它一个任务，VIP 卖家（构造时给出）每轮处理两个；卖家内部按 `priority` 小者先，再按 `timestamp`，再按接收顺序；任务处理完的卖家退出轮转，再收到任务重新排队尾。

## A
**一句话。** `deque` 做卖家轮转队列，每个卖家一个最小堆，记队首本轮已处理个数，达到配额（VIP 为 2，否则 1）就转到队尾，堆空就退出。

```python
class SellerScheduler:
    def __init__(self, vip_sellers=None):
        self.vip = set(vip_sellers or ())
        self.heaps = {}       # 卖家 -> 堆
        self.ring = deque()   # 轮转队列，队首是当前卖家
        self.served = 0       # 队首卖家本轮已处理数
        self.seq = count()    # 到达序号，兜底先到先出

    def receive_task(self, tid, seller_id, prio, ts):
        heap = self.heaps.get(seller_id)
        if heap is None:      # 新卖家：排到队尾
            heap = self.heaps[seller_id] = []
            self.ring.append(seller_id)
        item = (prio, ts, next(self.seq), tid)
        heapq.heappush(heap, item)

    def process_next_task(self):
        if not self.ring:
            return None
        seller = self.ring[0]
        heap = self.heaps[seller]
        task_id = heapq.heappop(heap)[-1]
        self.served += 1
        if not heap:          # 处理完：退出，本轮作废
            self.ring.popleft()
            del self.heaps[seller]
            self.served = 0
        elif self.served == (2 if seller in self.vip
                             else 1):
            self.ring.rotate(-1)    # 配额用完，转下一个
            self.served = 0
        return task_id
```

**复杂度。** 时间 `O(log k)`（每次操作），空间 `O(N)`。

**易错点。**
- 卖家重复入队：收任务时不判断是否已在队列，`A` 收两个、`B` 收一个会变成 `A, A, B`，得 `t1, t2, t3`，应为 `t1, t3, t2`。
- 卖家退出时 `served` 没清零：残留计数让下一位卖家少处理，VIP 的 `y, z` 只出一个就被转走。

**追问。**
- 加权轮转？：配额换成每个卖家的权重，其余不变。
- 防饥饿？：加老化，等待越久有效优先级越高。

**同模式。** LC 621 任务调度器、LC 1834 单线程 CPU、LC 355 设计推特、LC 253 会议室 II
