---
id: craft-heapq-tuple-ordering-6-scales-delay-queue
node: craft.idioms.heapq-tuple-ordering
type: qa
step: 6
---
## Q
**heapq 的元组序 · 从单线程 CPU 到延迟队列与 Redis ZSET**｜写法

LeetCode 的单线程 CPU、LLD 的任务调度器、分布式系统里的延迟队列，都在做「按到期时间取最早的」。同一个堆在三个尺度上有什么相同和不同？

## A
**要点。** 三层都是「按分数排序，每次取最小」的结构：LeetCode 的分数是 `(处理时长, 下标)`；调度器是 `(到期时间, 优先级, 序号, id)`；Redis 有序集合（ZSET）里是 score = 到期时间、成员 = 任务 id，取出用 `ZRANGEBYSCORE ... <= now`。tie-break 的位置从来没变：分数后面必须有一个能唯一确定顺序的字段。

```python
# LeetCode 1834 单线程 CPU: 任务 (入队时间, 处理时长)。
# 空闲时从「已到达」的任务里取处理时长最短的，时长相同取下标小的
def get_order(tasks: list[list[int]]) -> list[int]:
    by_arrival = sorted(range(len(tasks)), key=lambda i: tasks[i][0])
    ready: list[tuple[int, int]] = []        # (处理时长, 下标): 下标就是 tie-break
    order, t, k = [], 0, 0
    while len(order) < len(tasks):
        if not ready and k < len(by_arrival):
            t = max(t, tasks[by_arrival[k]][0])          # CPU 空转到下一个任务到达
        while k < len(by_arrival) and tasks[by_arrival[k]][0] <= t:
            i = by_arrival[k]; k += 1
            heapq.heappush(ready, (tasks[i][1], i))
        dur, i = heapq.heappop(ready)
        t += dur
        order.append(i)
    return order

# 分布式的延迟队列：Redis ZSET 的 score 就是到期时间，成员是任务 id。
# 这里用堆模拟同样的两个操作：加入 (ZADD) 和取出所有到期的 (ZRANGEBYSCORE ... <= now)
class DelayQueue:
    def __init__(self) -> None:
        self._h: list[tuple[float, int, str]] = []
        self._seq = 0
    def add(self, due: float, job: str) -> None:
        self._seq += 1
        heapq.heappush(self._h, (due, self._seq, job))
    def poll_due(self, now: float) -> list[str]:
        out = []
        while self._h and self._h[0][0] <= now:     # 只看堆顶，O(log n) 每个
            out.append(heapq.heappop(self._h)[2])
        return out

print(get_order([[1, 2], [2, 4], [3, 2], [4, 1]]))
q = DelayQueue()
q.add(5.0, "retry-1"); q.add(2.0, "email"); q.add(5.0, "retry-2")
print(q.poll_due(3.0), q.poll_due(5.0))
```

实际输出：

```
[0, 2, 3, 1]
['email'] ['retry-1', 'retry-2']
```

**变化。** 单进程的堆在内存里，进程重启任务就丢，定时靠本进程的时钟。分布式里要换成持久的有序存储，多个消费者要防止同一个任务被取两次（取出和标记要原子），时钟也成了问题：不同机器的时间不一致，到期判断以存储端的时间为准。

**代价。** 堆里的任务不能高效取消：删除任意元素是 O(n)，所以通常用「懒删除」（标记作废，弹出时再丢弃，见 lazy-deletion-heap）。ZSET 则是按成员删除。

**信号。** 需求里有「某个时间之后才能执行」「按优先级、同级先来先服务」。
