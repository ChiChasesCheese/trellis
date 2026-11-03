---
id: craft-backpressure-overflow-policy-1-three-answers-to-full
node: craft.patterns.backpressure-overflow-policy
type: qa
step: 1
---
## Q
**反压与溢出策略 · 队列满了，生产者该怎么办**｜写法

生产者每个时刻产生 3 条消息，消费者每个时刻只能处理 2 条。队列不设上限会怎样？设了上限（比如 10）以后，满的时候新来的消息有哪几种处理方式，各自把代价转嫁给谁？

## A
**要点。** 生产比消费快，差值一定会堆在某个地方。不设上限，堆在内存里，直到进程被杀。设上限就必须回答「满了怎么办」，只有三个答案：丢旧的（DROP_OLDEST，生产者永不阻塞，慢消费者丢消息）；让生产者等（BLOCK，一条不丢，生产者被拖慢）；立刻拒绝（REJECT，生产者收到错误，自己决定降级或重试）。三者没有对错，只是把代价转嫁给不同的人，所以代价必须在设计时写出来，不能留成「以后再说」。

```python
from collections import deque
from enum import Enum

class Overflow(Enum):
    DROP_OLDEST = "drop_oldest"     # 发布者永不阻塞，慢消费者丢旧消息
    BLOCK = "block"                 # 一条不丢，代价是生产者被拖慢
    REJECT = "reject"               # 立刻告诉生产者"满了"，由它决定
    UNBOUNDED = "unbounded"         # 对照：没有出口

def simulate(policy, ticks=100, produce=3, consume=2, cap=10):
    q = deque(); made = accepted = rejected = dropped = delayed = peak = 0
    for _ in range(ticks):
        for _ in range(produce):                      # 每个时刻想放 3 条
            made += 1
            if len(q) >= cap and policy is not Overflow.UNBOUNDED:
                if policy is Overflow.DROP_OLDEST: q.popleft(); dropped += 1   # 消费者吃亏：丢旧数据
                elif policy is Overflow.REJECT:    rejected += 1; continue     # 生产者吃亏：被告知失败
                else:                              delayed += 1; continue      # 生产者吃亏：被迫等待
            q.append(made); accepted += 1
        peak = max(peak, len(q))
        for _ in range(min(consume, len(q))): q.popleft()    # 每个时刻只处理 2 条
    return (f"{policy.value:12} 想放 {made}  进入 {accepted}  丢旧 {dropped}  "
            f"拒绝 {rejected}  被挡住 {delayed}  队列峰值 {peak}")

for p in Overflow: print(simulate(p))
```

100 个时刻，想放 300 条，容量 10：

```
drop_oldest  想放 300  进入 300  丢旧 92  拒绝 0  被挡住 0  队列峰值 10
block        想放 300  进入 208  丢旧 0  拒绝 0  被挡住 92  队列峰值 10
reject       想放 300  进入 208  丢旧 0  拒绝 92  被挡住 0  队列峰值 10
unbounded    想放 300  进入 300  丢旧 0  拒绝 0  被挡住 0  队列峰值 102
```

（模拟里 BLOCK 的 92 次是「这一时刻要等」，真实系统里它们稍后会进入。）

**为什么。** 无界队列看起来「什么都不丢」，实际上把压力延迟成一个更大的故障（OOM、延迟越来越高，队列里的消息在被处理时早已过期）。有界队列把故障提前、变小、可观测。

**怎么选。** 数据可以丢、新比旧重要（指标、日志）：丢旧。数据不能丢、生产者可以等（内部任务）：阻塞。生产者在处理用户请求、不能被卡住，且上游能重试：拒绝。
