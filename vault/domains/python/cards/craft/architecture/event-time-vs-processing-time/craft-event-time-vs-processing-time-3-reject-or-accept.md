---
id: craft-event-time-vs-processing-time-3-reject-or-accept
node: craft.architecture.event-time-vs-processing-time
type: qa
step: 3
---
## Q
**事件时间 vs 处理时间 · 系统该接受乱序事件，还是明确拒绝**｜架构

人流统计（进出场事件）和配送员结算（取餐、到店、送达事件）都要处理事件时间。前者拒绝时间倒流的事件，后者接受乱序到达。两种选择各自换来了什么，什么时候该选哪一种？

## A
**要点。** 先问：这个系统接受乱序吗？不接受，就明确拒绝，并把它写进契约；数据结构因此可以简单得多：人流统计时间戳只增，可以用 append-only 的前缀和数组，二分查询任一时刻人数。接受，就把事实存下来，只检查时间线是否自洽（取餐不能晚于送达），之后的结果按事实重算。

```python
class OutOfOrder(Exception): ...

class Occupancy:                          # 拒绝倒流：时间戳只增
    """选择拒绝倒流：时间戳只增，前缀和数组就能 append，二分查任一时刻人数。"""
    def __init__(self) -> None:
        self.ts: list[int] = []
        self.prefix: list[int] = [0]          # prefix[i] = 前 i 个事件之后的在场人数
    def record(self, ts: int, delta: int) -> None:
        if self.ts and ts < self.ts[-1]:
            raise OutOfOrder(f"{ts} < {self.ts[-1]}")
        self.ts.append(ts)
        self.prefix.append(self.prefix[-1] + delta)
    def at(self, t: int) -> int:
        return self.prefix[bisect_right(self.ts, t)]

o = Occupancy()
o.record(10, +1); o.record(20, +1); o.record(30, -1)
print("t=25 在场:", o.at(25), "| t=35 在场:", o.at(35))
try:
    o.record(15, +1)
except OutOfOrder as e:
    print("倒流事件被拒绝:", e)

class Lifecycle:                          # 接受乱序：只检查时间线自洽
    """选择接受乱序：事实存起来，只检查时间线是否自洽。"""
    ORDER = ["PICKED_UP", "ARRIVED", "DELIVERED"]     # 生命周期的先后
    def __init__(self) -> None:
        self.events: dict[str, int] = {}
    def record(self, kind: str, at: int) -> None:
        i = self.ORDER.index(kind)
        for other, t in self.events.items():
            j = self.ORDER.index(other)
            if (j < i and t > at) or (j > i and t < at):
                raise ValueError(f"{kind}@{at} 与 {other}@{t} 矛盾")
        self.events[kind] = at

d = Lifecycle()
d.record("DELIVERED", 90)                     # 送达先到
d.record("PICKED_UP", 10)                     # 取餐后到，但时间合理
print("乱序接受:", d.events)
try:
    d.record("ARRIVED", 95)                   # 到店时间晚于送达：矛盾
except ValueError as e:
    print("矛盾被拒绝:", e)
```

人流依次记 (10,+1)、(20,+1)、(30,-1)，再记 15；配送先记送达 90，再记取餐 10，最后记到店 95。实际输出：

```
t=25 在场: 2 | t=35 在场: 1
倒流事件被拒绝: 15 < 30
乱序接受: {'DELIVERED': 90, 'PICKED_UP': 10}
矛盾被拒绝: ARRIVED@95 与 DELIVERED@90 矛盾
```

**为什么。** 取舍是复杂度与容错：接受乱序的系统不会因为网络延迟丢事实，但每次写入都要检查一致性，读取往往要重算；拒绝的系统简单，但要求上游保证顺序，否则调用方得有重试与排队。

**易错。** 「拒绝」不是静默丢弃：要抛明确的错误，让上游知道这条没进去。
