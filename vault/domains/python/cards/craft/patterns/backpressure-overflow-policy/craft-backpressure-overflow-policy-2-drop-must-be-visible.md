---
id: craft-backpressure-overflow-policy-2-drop-must-be-visible
node: craft.patterns.backpressure-overflow-policy
type: qa
step: 2
---
## Q
**反压与溢出策略 · 丢消息时，怎么让「丢了多少」可查**｜写法

消息主题用 DROP_OLDEST：容量满了，发布者直接淘汰队头，从不阻塞。慢订阅者回来读的时候，它的游标指向的消息已经被淘汰了。如果读取接口悄悄从最老的现存消息开始返回，会出什么问题？

## A
**要点。** 丢弃本身是策略允许的，**悄悄**丢弃不允许。每条消息有一个单调递增的序号（seq）；订阅者的游标是它下一条要读的序号；日志只保留 `[start, next)` 窗口。读取时，若游标小于 `start`，说明落后了 `start - cursor` 条：把这个数字随结果一起返回，并把游标拉到窗口头。调用方立刻知道自己漏了数据，可以决定重新同步、告警或接受。

```python
from collections import deque

class Topic:
    """有界保留日志 + 每个订阅者一个游标。DROP_OLDEST：发布者永不阻塞，落后的订阅者丢旧消息。"""
    def __init__(self, cap):
        self.cap, self.log, self.start, self.next = cap, deque(), 0, 0
        self.cursors, self.evicted = {}, 0
    def publish(self, payload):
        if len(self.log) >= self.cap:
            self.log.popleft(); self.start += 1; self.evicted += 1   # 淘汰队头，计数可查
        self.log.append((self.next, payload)); self.next += 1
    def read(self, sub, n=100):
        cur = self.cursors[sub]
        lost = max(0, self.start - cur)                # 游标落到了窗口之外：丢了多少条
        cur = max(cur, self.start)
        out = [p for s, p in self.log if s >= cur][:n]
        self.cursors[sub] = cur + len(out)
        return out, lost

t = Topic(cap=3); t.cursors["fast"] = t.cursors["slow"] = 0
for i in range(5):
    t.publish(f"m{i}")
    if i < 2: t.read("fast")                           # fast 一直在读
print("fast:", t.read("fast"))
print("slow:", t.read("slow"), "<- 返回丢失条数，而不是悄悄少几条")
print("总共淘汰:", t.evicted)
```

容量 3，发布 5 条（m0 到 m4），快订阅者一直在读，慢订阅者从没读过：

```
fast: (['m2', 'm3', 'm4'], 0)
slow: (['m2', 'm3', 'm4'], 2) <- 返回丢失条数，而不是悄悄少几条
总共淘汰: 2
```

**为什么。** 序号是让丢弃可检测的关键：没有序号，消费者只看到消息序列，看不出中间缺了什么。主题自己再维护一个累计淘汰数（`evicted_count`），运维能看到趋势：持续增长说明订阅者长期处理不过来，该扩容。

**代价。** 每条消息要带序号，游标要持久；消息可以重放（从某个序号读）也是同一个机制，所以序号的投入一举两得。

**易错。** 返回丢失数，而不是抛异常：丢弃是该策略下的正常结果，不是调用方的 bug。
