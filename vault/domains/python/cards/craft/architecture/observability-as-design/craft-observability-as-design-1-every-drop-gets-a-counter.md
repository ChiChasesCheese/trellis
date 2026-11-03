---
id: craft-observability-as-design-1-every-drop-gets-a-counter
node: craft.architecture.observability-as-design
type: qa
step: 1
---
## Q
**可观测性即设计 · 缓冲区满了丢最老的，为什么必须同时加一个计数器**｜架构

有界缓冲区满了以后有三种选择：阻塞生产者、拒绝新数据、丢弃最老的。「丢最老的」最省事，Python 的 `deque(maxlen=n)` 一行就有。可是丢掉的数据去了哪里，上线以后谁来告诉你？

## A
**要点。** 凡是会**丢、拒、重试、降级**的地方，都要在做这个动作的同一处加一个计数。丢弃本身可以是正确的设计，但静默丢弃不是：没有计数，线上出现「少了几条数据」时，你无法区分是 bug、是流量涨了，还是策略在正常工作。

```python
buf = deque(maxlen=3)                      # 满了自动挤掉最老的，没有任何信号
for i in range(5):
    buf.append(i)
print("只剩", list(buf), "- 丢了 2 条，没人知道")

class CountingBuffer:
    """同样的丢弃策略，但每次丢弃都计数。"""
    def __init__(self, cap: int) -> None:
        self._buf: deque[int] = deque()
        self._cap = cap
        self.dropped = 0                   # 丢弃必须可观测
    def append(self, x: int) -> None:
        if len(self._buf) >= self._cap:
            self._buf.popleft()
            self.dropped += 1
        self._buf.append(x)

b = CountingBuffer(3)
for i in range(5):
    b.append(i)
print("只剩", list(b._buf), "- dropped =", b.dropped)
```

实际输出：

```
只剩 [2, 3, 4] - 丢了 2 条，没人知道
只剩 [2, 3, 4] - dropped = 2
```

**为什么。** 发布订阅的订阅者有 `lagged_count`（因日志被淘汰而没看到的消息条数），注释写得直白：「丢弃必须可观测，否则 DROP_OLDEST 就是静默丢数据」。日志框架的异步 handler 也一样：队列满了丢弃、已关闭后到达的记录，都累加 `dropped_count`。

**易错。** 计数和丢弃要在同一把锁、同一个分支里更新，否则会出现「丢了但没计」的窗口。`deque(maxlen=n)` 做不到这点，因为丢弃发生在 C 层，你拿不到钩子；需要观测就得自己写出 `popleft`。
