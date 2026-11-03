---
id: craft-condition-wait-predicate-loop-5-scales-backpressure
node: craft.patterns.condition-wait-predicate-loop
type: qa
step: 5
---
## Q
**条件变量等待循环 · 有界队列的意义：从线程到背压**｜模式

为什么阻塞队列要有容量上限，而不是无限长？放大到服务之间，同样的想法怎么落地？

## A
**要点。** 有界队列让快的一方被迫和慢的一方同速，这就是背压（backpressure）：队列满了生产者阻塞（或被拒绝），内存和延迟都有上界。无界队列只是把问题推迟：消费者慢，积压无限增长，直到内存耗尽。

```python
q = queue.Queue(maxsize=maxsize)       # maxsize=0 表示无界
for i in range(300):
    q.put(i)                           # 满了就阻塞：背压
    peak = max(peak, q.qsize())
```

生产者连续放 300 个，消费者每个处理 1 毫秒：

```
无界队列 峰值积压 300
有界队列(10) 峰值积压 10 -> 生产者被迫和消费者同速
```

**尺度对照。** 线程间：有界队列的 `put` 阻塞；进程间：管道或套接字缓冲区写满后 `write` 阻塞；服务间：信号量或令牌限制并发、HTTP 429 让调用方退避；消息系统：消费者调用 `poll(timeout)` 拉取，慢了生产者不会被消息系统阻塞，但积压（lag）会增长，要靠监控和扩容。

**代价。** 阻塞会向上游传播：被阻塞的线程占着资源，整条链路的延迟变成最慢一环的延迟。需要时改成丢弃（`drop_when_full`）并计数，用可观测的丢失换业务线程不被拖慢。

**信号。** 生产者和消费者速度不匹配，或需要限制「在途工作量」。
