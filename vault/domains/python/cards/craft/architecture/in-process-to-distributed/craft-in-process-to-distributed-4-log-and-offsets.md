---
id: craft-in-process-to-distributed-4-log-and-offsets
node: craft.architecture.in-process-to-distributed
type: qa
step: 4
---
## Q
**从单进程到分布式 · 进程内的日志加游标，对应 Kafka 里的什么**｜架构

进程内的 pub-sub 主题是一条有界日志，每个订阅者一个游标，满了按策略丢最老的。放到 Kafka 这类系统里，日志、游标、丢最老分别对应什么？消费者处理完一条消息、还没提交位点就崩了，重启后会怎样？

## A
**要点。** 对应关系：有界日志 = 分区（partition），游标 = 消费组的位点（offset），丢最老 = 保留策略（retention，按时间或大小清理旧段）。变的是游标要持久化、要显式提交。崩溃发生在「处理」与「提交位点」之间，重启后就从上一个已提交的位点继续，那条消息被处理第二遍：这是至少一次（at-least-once）投递，处理逻辑必须幂等。

```python
log = ["m0", "m1", "m2", "m3"]                    # 一个分区：只追加的日志，进程内版就是 Topic 的 deque
committed = {"g1": 0}                             # 消费组的位点（offset）= 进程内版的游标
processed: list[str] = []

def consume(group: str, crash_after_processing: int | None = None) -> None:
    pos = committed[group]
    while pos < len(log):
        processed.append(log[pos])                # 1. 先处理
        if crash_after_processing == pos:
            raise RuntimeError("进程在提交位点之前崩了")
        pos += 1
        committed[group] = pos                    # 2. 再提交位点

try:
    consume("g1", crash_after_processing=2)
except RuntimeError as e:
    print(e, "| 已提交位点 =", committed["g1"])
consume("g1")                                     # 重启后从已提交位点继续
print("处理序列:", processed)
print("m2 被处理了", processed.count("m2"), "次 -> 至少一次投递，处理逻辑必须幂等")
```

日志 `m0..m3`，第一次在处理完 `m2` 后崩溃，重启再消费，实际输出：

```
进程在提交位点之前崩了 | 已提交位点 = 2
处理序列: ['m0', 'm1', 'm2', 'm2', 'm3']
m2 被处理了 2 次 -> 至少一次投递，处理逻辑必须幂等
```

**为什么。** 先提交再处理则相反：崩溃时消息丢了，叫至多一次。想要「恰好一次的效果」，只能是至少一次加幂等（见幂等键存结果），因为没有办法让「处理」与「提交位点」成为一个原子操作，除非它们落在同一个事务性存储里。

**代价。** 只保证分区内有序，跨分区没有全局顺序；进程内的单日志顺序到分布式要靠「同一个 key 落同一个分区」来保留。
