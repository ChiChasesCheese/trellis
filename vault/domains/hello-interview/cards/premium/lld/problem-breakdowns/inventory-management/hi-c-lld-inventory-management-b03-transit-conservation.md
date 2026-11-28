---
id: hi-c-lld-inventory-management-b03-transit-conservation
node: lld.problem-breakdowns.inventory-management.beyond
type: qa
step: 4
---
## Q
**库存管理 · Python：在途库存与守恒不变量**｜拓展 · 加分

调拨对象作为持有库存的实体，怎么保证系统总量不变？怎么测？

## A
**模式。** 守恒不变量（类似会计的复式记账）：库存只能从一个"持有者"转移到另一个，不凭空产生或消失；用一个总量函数在测试里反复断言。

```python
import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class Transfer:                                  # 在途库存也是"持有库存的地方"，和仓库同级
    id: str
    pid: str
    qty: int
    src: str
    dst: str


class Network:
    def __init__(self, stock: dict[str, dict[str, int]]) -> None:
        self.stock = stock                       # 仓库 -> 商品 -> 数量
        self.transit: dict[str, Transfer] = {}

    def total(self, pid: str) -> int:            # 守恒不变量：仓库里的 + 在途的 = 系统总量
        return sum(w.get(pid, 0) for w in self.stock.values()) + \
               sum(t.qty for t in self.transit.values() if t.pid == pid)

    def ship(self, pid: str, src: str, dst: str, qty: int) -> str | None:
        if self.stock[src].get(pid, 0) < qty:
            return None
        self.stock[src][pid] -= qty              # 出库和登记在途是一个整体（真实系统里是同一事务）
        t = Transfer(uuid.uuid4().hex, pid, qty, src, dst)
        self.transit[t.id] = t
        return t.id

    def arrive(self, tid: str) -> bool:
        t = self.transit.pop(tid, None)          # pop：同一运单第二次到货返回 False，不会双倍入库
        if t is None:
            return False
        self.stock[t.dst][t.pid] = self.stock[t.dst].get(t.pid, 0) + t.qty
        return True

    def cancel(self, tid: str) -> bool:          # 取消 = 退回源仓库
        t = self.transit.pop(tid, None)
        if t is None:
            return False
        self.stock[t.src][t.pid] = self.stock[t.src].get(t.pid, 0) + t.qty
        return True


n = Network({"CA": {"w": 10}, "NY": {}})
tid = n.ship("w", "CA", "NY", 4)
assert n.total("w") == 10                        # 在途期间总量不变，只是哪边都不可售
assert n.stock["CA"]["w"] == 6 and n.stock["NY"].get("w", 0) == 0
assert n.arrive(tid) and not n.arrive(tid)       # 重复到货通知不会多出库存
assert n.total("w") == 10 and n.stock["NY"]["w"] == 4
```
- **总量函数：** `total(pid)` = 所有仓库 + 所有在途。任何操作前后它都应该相等，是最好用的属性测试（property-based test）断言：随机序列的发货、到货、取消，之后总量必须不变。
- **`pop` 做幂等：** 同一运单第二次到货通知返回假，不会双倍入库；外部系统重复推送是常态。
- **可售与总量的区别：** 在途库存计入总量但不可售，所以"哪些仓库能满足某个数量"的查询只看仓库库存，不看在途。
- **持久化后：** 出库与登记在途必须在同一个事务里，否则崩溃会让货"消失"。
- **何时不用：** 面试时间不够、需求没提到在途时，不要引入；先说原子调拨是简化，被追问再展开。
