---
id: craft-bounded-deque-2-count-what-you-drop
node: craft.idioms.bounded-deque
type: qa
step: 2
---
## Q
**有界 deque · 自动淘汰会静默丢数据，死信怎么补救**｜写法

死信队列用 `deque(maxlen=1000)`：满了自动丢最旧的。故障持续了一晚，运维早上来看，里面只有最后 1000 条，他不知道还有多少条已经被挤掉。这个写法缺了什么？

## A
**要点。** 有界容器必须说清楚满了怎么办。`deque(maxlen)` 的选择是丢最旧，且不告诉你。对于只供查看最近状况的日志，这没问题；对于死信，要同时记录丢了多少条，让运维知道记录是不完整的。检查发生在 `append` 之前，因为 `append` 之后已经看不出有没有东西被挤出。

```python
from collections import deque
from dataclasses import dataclass, field

@dataclass
class DeadLetters:
    limit: int
    items: deque[str] = field(init=False)
    dropped: int = 0                               # 被挤掉的条数：不能悄悄消失
    def __post_init__(self) -> None:
        self.items = deque(maxlen=self.limit)
    def add(self, x: str) -> None:
        if len(self.items) == self.items.maxlen:   # 这次 append 会挤掉最左一个
            self.dropped += 1
        self.items.append(x)

d = DeadLetters(3)
for i in range(5):
    d.add(f"m{i}")
print(list(d.items), "已丢弃", d.dropped)
```

实际输出：

```
['m2', 'm3', 'm4'] 已丢弃 2
```

**为什么。** 如果死信真的不能丢（支付失败），就不该用丢最旧的容器，而是持久化到磁盘或另一个队列，满了拒绝写入并告警（背压），而不是静默覆盖。选哪种出口取决于数据的价值：可丢的历史用 `maxlen`，不可丢的用持久化和背压。

**易错。** 同一个容器被多个线程追加时，`len(...) == maxlen` 和 `append` 之间不是原子的，计数可能偏差；要准确计数就把这两步放进同一把锁。
