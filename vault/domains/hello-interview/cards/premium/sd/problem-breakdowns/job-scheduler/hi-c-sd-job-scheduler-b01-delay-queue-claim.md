---
id: hi-c-sd-job-scheduler-b01-delay-queue-claim
node: sd.problem-breakdowns.job-scheduler.beyond
type: qa
step: 1
---
## Q
**分布式任务调度器 · 拓展：自建延迟队列的三个必要部件**｜拓展 · 加分

不用 SQS，自己用有序集合造延迟队列，必须解决哪些问题？Python 里怎么写最小版本？

## A
- **三个部件：**
  - 按到期时间排序：最小堆（Redis 里的 ZSET）；
  - 原子领取：取出和登记为处理中必须一步完成，否则两个 worker 拿到同一个作业；
  - 可见性超时：领取后没在期限内确认（ack）就当崩溃，重新放回队列。
- **最小实现里的对应关系：** 锁对应 Redis 里的 Lua 脚本（脚本在 Redis 里原子执行）；`processing` 字典对应“处理中”有序集合；`_requeue_expired` 对应回收器。
- **实测：** 4 个线程并发领取 5 个到期作业，每个作业恰好被领取一次；一个领取后不确认的作业，在 30 秒可见性期限之前领不到，之后重新出现。
- **PriorityQueue 不能延迟可见：** Python 的 `queue.PriorityQueue` 只按优先级阻塞等待，不支持“还没到期就不可见”，也不支持可见性超时；要自己扩展。
- **取舍：** 自建掌握一切细节，代价是必须自己保证持久（Redis 持久化）和高可用（Sentinel/Cluster）；SQS 把这些都做了。
- **模式。** 租借领取：不把“取走”当作终点，而是借出一个带期限的所有权，确认了才算完成。

```python
def claim(self, now, visibility=30):
    with self.lock:                        # 取出 + 登记处理中：一步完成
        self._requeue_expired(now)         # 先把超时没 ack 的放回来
        if self.heap and self.heap[0][0] <= now:
            _, job = heapq.heappop(self.heap)
            self.processing[job] = now + visibility
            return job
    return None
```
