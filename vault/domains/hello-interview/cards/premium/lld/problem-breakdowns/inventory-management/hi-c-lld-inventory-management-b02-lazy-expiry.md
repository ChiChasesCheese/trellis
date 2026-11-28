---
id: hi-c-lld-inventory-management-b02-lazy-expiry
node: lld.problem-breakdowns.inventory-management.beyond
type: qa
step: 3
---
## Q
**库存管理 · Python：用惰性过期代替后台清理线程**｜拓展 · 加分

预留需要超时释放。除了周期扫描的后台线程，还有更简单的写法吗？

## A
**模式。** 惰性过期（lazy expiry）加注入时钟：过期不是由某个线程"执行"的，而是每次读状态时顺手清掉已过期的项。

```python
from dataclasses import dataclass
from typing import Callable


@dataclass
class Reservation:
    pid: str
    qty: int
    expires_at: float


class ReservingStock:
    """一个仓库的库存加预留。过期不靠后台线程，而是在每次访问时顺手清理（惰性过期）。"""

    def __init__(self, clock: Callable[[], float]) -> None:
        self._clock = clock
        self._stock: dict[str, int] = {}
        self._res: dict[str, Reservation] = {}   # 预留号 -> 预留；调用方生成，重试同一个号是幂等的

    def _expire(self) -> None:                   # 调用方须已持有锁（此处省略锁以突出逻辑）
        now = self._clock()
        for rid in [r for r, v in self._res.items() if v.expires_at <= now]:
            del self._res[rid]                   # 预留消失 = 额度自动回到可售池

    def available(self, pid: str) -> int:
        self._expire()
        held = sum(r.qty for r in self._res.values() if r.pid == pid)
        return self._stock.get(pid, 0) - held    # 可售 = 实物库存 - 已被预留

    def reserve(self, rid: str, pid: str, qty: int, ttl: float) -> bool:
        if rid in self._res:                     # 同一预留号重试：幂等，不重复占用
            return True
        if self.available(pid) < qty:
            return False
        self._res[rid] = Reservation(pid, qty, self._clock() + ttl)
        return True

    def confirm(self, rid: str) -> bool:
        self._expire()
        r = self._res.pop(rid, None)             # 已过期的在上一行就被清掉了
        if r is None:
            return False
        self._stock[r.pid] -= r.qty              # 此刻才真正扣实物库存
        return True


t = [0.0]
s = ReservingStock(lambda: t[0])
s._stock["w"] = 1
assert s.reserve("o1", "w", 1, ttl=600) and not s.reserve("o2", "w", 1, ttl=600)   # 第二个人立即知道没货
t[0] = 601                                       # 10 分钟没付款
assert s.available("w") == 1 and s.reserve("o2", "w", 1, ttl=600)   # 额度自动释放
assert not s.confirm("o1")                       # 迟到的付款确认失败
assert s.confirm("o2") and s._stock["w"] == 0
```
- **为什么不需要线程：** 预留只在被查询（`available`、`reserve`、`confirm`）时才会影响别人，所以只要在这些入口先清理，对外效果与"准时释放"完全一致；没有后台线程的启动、停止和与业务锁的竞争。
- **代价：** 每次访问有一次清理扫描，预留很多时要换成按过期时间排序的堆或分桶；内存里留着过期但没人访问的项，直到下一次访问。
- **幂等的预留号：** 调用方生成预留号，网络重试同一个号不会重复占用。
- **迟到的确认：** 过期的预留在 `confirm` 之前就被清掉，确认返回假，调用方需要走"重新预留或退款"的路径。
- **何时仍用后台任务：** 需要在过期时主动做事（发通知、释放外部资源）、或者必须限制内存时。
