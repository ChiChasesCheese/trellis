---
id: craft-injected-clock-three-forms-3-monotonic-contract
node: craft.patterns.injected-clock-three-forms
type: qa
step: 3
---
## Q
**注入时钟 · 方法收时间戳时隐含了什么约定**｜模式

返现系统里每个写操作都带一个时间戳，类自己没有时钟，到期的返现在下一次写操作时才结清。这种设计没有后台线程，很简单，但调用方传一个比上次更小的时间戳会怎样？

## A
**要点。** 隐含约定：时间只能前进。惰性结清（见到期后在访问时结清）依赖「当前时间单调不减」：时间倒退，已经结清的状态没法撤销，同一个时刻可能算出两种结果。所以第一步要校验，倒退就拒绝。

```python
def _advance(self, ts: int) -> None:
    if ts < self.last:
        raise NonMonotonic(f"时间戳不能倒退：{ts} < {self.last}")
    self.last = ts
    due = [p for p in self.pending if p[0] <= ts]    # 到期的在写操作时结清
    self.pending = [p for p in self.pending if p[0] > ts]
    self.balance += sum(a for _, a in due)
```

先在 0 时刻支付 1000，再在 150 时刻写操作，再用 120 写操作：

```
t=150 余额 20
拒绝: 时间戳不能倒退：120 < 150
```

**为什么。** 只读的 `get_balance` 不走 `_advance`，它可以查询任意历史时刻：读不改变状态，所以不受单调约束。

**代价。** 乱序到达的事件（网络延迟）会被拒绝，调用方要先排序；真实系统里这需要水位线（watermark）或允许一段延迟。
