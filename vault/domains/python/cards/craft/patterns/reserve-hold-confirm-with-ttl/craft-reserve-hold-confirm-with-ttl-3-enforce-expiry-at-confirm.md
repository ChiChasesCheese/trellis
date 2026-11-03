---
id: craft-reserve-hold-confirm-with-ttl-3-enforce-expiry-at-confirm
node: craft.patterns.reserve-hold-confirm-with-ttl
type: qa
step: 3
---
## Q
**预留—确认—过期 · 为什么确认时必须再检查一次预留有没有过期**｜写法

预留 A 迟迟没付款，到期后库存已放回，被另一位用户 B 买走了。这时 A 的付款回来，调用 `commit("A")`。如果确认时不检查预留是否仍然有效，会发生什么？

## A
**要点。** 超卖。预留有时限这件事，必须在确认的那一刻被强制：确认前先结清过期，预留已经失效就直接失败，而不是把它当作仍然有效。否则 TTL 只是个建议。

```python
def commit(self, rid):
    if self.enforce:
        n, exp = self.res.get(rid, (0, 0.0))
        if rid not in self.res or exp <= Clock.t:
            raise RuntimeError(f"预留已失效：{rid}")   # 过期的预留不能再确认
    n, _ = self.res.pop(rid)
    self.on_hand -= n
```

库存 1，A 预留后过期，B 买走，A 再确认：

```
不检查过期 -> A 也成交了，在架 -1 （超卖）
检查过期   -> A 被拒绝: 预留已失效：A | 在架 0
```

**为什么。** 过期本身是惰性的（见惰性过期），所以确认入口必须先结清，再判断；这就是把「结清」放进每个公开操作的装饰器里的原因。

**代价。** A 付了钱但预留已失效：款要退，用户要被告知。订座系统的做法是付款前先把持有期延长到付款窗口，并在超时时抛出带「需要退款」提示的错误，而不是覆盖别人的座位。

**信号。** 流程里「占用」与「最终成交」之间隔着一个人的操作（付款、填表）。
