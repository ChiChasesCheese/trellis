---
id: craft-backpressure-overflow-policy-4-what-to-drop
node: craft.patterns.backpressure-overflow-policy
type: qa
step: 4
---
## Q
**反压与溢出策略 · 丢哪一条：按到达顺序，还是按重要程度**｜架构

紧急事件广播里，每个订阅者有一个容量有限的信箱，事件带严重度（severity）。信箱满了，是和普通队列一样丢最老的，还是挤掉最不重要的？被丢的那条该去哪儿？

## A
**要点。** 丢哪一条是业务决定。队列没有优先级：丢最老是对的，因为新的更有价值。事件有严重度时：丢最不重要的，严重度相同才比先后。新来的如果本身就是最不重要的，丢的就是它自己。无论丢哪条，都要留下一条死信（dead letter）记录，写明事件和原因，不能凭空消失。

```python
import heapq
from dataclasses import dataclass

@dataclass(frozen=True)
class Event: seq: int; severity: int; text: str
@dataclass(frozen=True)
class DeadLetter: event: Event; reason: str

class Mailbox:
    """容量有限；满了就挤掉最不重要的一条（严重度低的先走，同级里更老的先走），并留下死信。"""
    def __init__(self, cap): self.cap, self.heap, self.dead = cap, [], []

    def offer(self, e):
        key = lambda it: (it[0], -it[1])               # (−严重度, −seq)：越大越该被挤掉
        if len(self.heap) >= self.cap:
            worst = max(self.heap, key=key)
            if key(worst) < (-e.severity, -e.seq):     # 新来的就是最不重要的：丢它
                self.dead.append(DeadLetter(e, "mailbox full")); return
            self.heap.remove(worst); heapq.heapify(self.heap)
            self.dead.append(DeadLetter(worst[2], "evicted by more severe event"))
        heapq.heappush(self.heap, (-e.severity, e.seq, e))

    def take(self): return heapq.heappop(self.heap)[2]

m = Mailbox(2)
for i, sev in enumerate([1, 5, 1, 9, 1]):
    m.offer(Event(i, sev, f"e{i}(sev{sev})"))
print("留下:", [m.take().text for _ in range(2)])
print("死信:", [(d.event.text, d.reason) for d in m.dead])
```

容量 2，依次到达严重度 1、5、1、9、1 的事件：

```
留下: ['e3(sev9)', 'e1(sev5)']
死信: [('e0(sev1)', 'evicted by more severe event'), ('e2(sev1)', 'evicted by more severe event'), ('e4(sev1)', 'mailbox full')]
```

**为什么。** 紧急事件里，一个严重度 9 的事件被一串严重度 1 的事件挤掉，比丢一条旧的糟糕得多。把「谁更不重要」写进排序键，淘汰规则和消费顺序用同一个键，不会前后矛盾。死信让每一次丢弃可以事后查：丢了什么，为什么。

**代价。** 堆只能高效取最小，不能高效取最大，这里用 `max(...)` 加 `remove` 加 `heapify`，每次满溢是 O(n)。信箱很小（几十条）时无所谓；大了就换成双端结构（例如同时维护最大堆），或者分级队列（每个严重度一个队列）。
