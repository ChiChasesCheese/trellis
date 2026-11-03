---
id: craft-in-process-to-distributed-5-ids-and-what-is-lost
node: craft.architecture.in-process-to-distributed
type: qa
step: 5
---
## Q
**从单进程到分布式 · 自增 ID 到多实例为什么撞车，以及每次迁移通常丢了什么**｜架构

单机里用一个自增计数器生成 ID，又快又有序。服务起了两个实例，各有各的计数器。会发生什么？更一般地，把一个进程内的原语换成分布式版本，通常会丢掉哪几种保证？

## A
**要点。** 两个实例的计数器都从 1 开始，ID 撞车。分布式 ID 的做法是把「全局协调」换成「分区编码」：时间戳 + 实例号 + 序号（雪花 ID 一类），每个实例只在自己的编号空间内自增，不用互相通信。通用规律：进程内原语迁移到分布式，丢掉的是原子性、顺序、统一的时钟和故障独立性，每次迁移都要问这四样是谁在补。

```python
class Counter:                                    # 对比：单机自增，每个实例各有一个
    """单机：自增计数器。每个实例各有自己的计数。"""
    def __init__(self) -> None:
        self._n = itertools.count(1)
    def next_id(self) -> int:
        return next(self._n)

a, b = Counter(), Counter()
print("两个实例的计数器:", [a.next_id(), a.next_id()], [b.next_id(), b.next_id()])

class Snowflake:
    """分布式：时间戳 + 实例号 + 序号。各实例不用协调，也不会撞。"""
    def __init__(self, worker: int, clock) -> None:
        self.worker, self.clock, self.last_ms, self.seq = worker, clock, -1, 0
    def next_id(self) -> int:
        ms = self.clock()
        if ms == self.last_ms:
            self.seq += 1                         # 同一毫秒内靠序号区分
        else:
            self.last_ms, self.seq = ms, 0
        return (ms << 14) | (self.worker << 10) | self.seq   # 低 14 位：4 位实例号 + 10 位序号

t = lambda: 1_000
s1, s2 = Snowflake(1, t), Snowflake(2, t)
ids = [s1.next_id(), s1.next_id(), s2.next_id(), s2.next_id()]
print("同一毫秒内 4 个 ID 是否唯一:", len(set(ids)) == 4)
```

两个计数器各取两个 ID；两个雪花实例在同一毫秒各取两个，实际输出：

```
两个实例的计数器: [1, 2] [1, 2]
同一毫秒内 4 个 ID 是否唯一: True
```

**为什么。** 原语与生产对应物：锁 → 数据库行锁或唯一约束；事务 → 单库事务（跨库要 2PC 或 saga）；内存日志加游标 → 分区加位点；到期堆 → 存储侧的过期；自增 ID → 分区编码的 ID。

**代价。** 雪花 ID 依赖时钟只增不减：时钟回拨会生出重复 ID，所以实现要检测回拨并拒绝或等待；同一毫秒序号用满也要等下一毫秒。
