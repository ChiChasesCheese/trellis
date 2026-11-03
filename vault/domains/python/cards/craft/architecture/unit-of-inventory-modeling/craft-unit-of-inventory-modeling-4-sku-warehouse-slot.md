---
id: craft-unit-of-inventory-modeling-4-sku-warehouse-slot
node: craft.architecture.unit-of-inventory-modeling
type: qa
step: 4
---
## Q
**库存的单位怎么选 · 多仓库存的预留，怎么做到全有或全无**｜架构

电商库存按 (商品, 仓库) 记。下单要 6 件，上海仓有 5 件、北京仓有 3 件，一个预留可能跨仓。如果边遍历边扣，最后发现总量不够时，已经扣掉的怎么办？可售数量和实际在架数量又怎么区分？

## A
**要点。** 单位是 (商品, 仓库) 的格子，每个格子两个数：在架（`on_hand`）和已预留（`reserved`），可售 = 在架 − 已预留。预留分两步：先只读地算出分配计划（从可售最多的仓库开始拿，并列取仓库名小的，保证确定），不够就抛 `OutOfStock`，什么也没动；再提交计划，只做加法，不会失败。确认发货时同时减在架和已预留。

```python
class OutOfStock(Exception): ...

@dataclass
class Slot:
    on_hand: int = 0
    reserved: int = 0
    @property
    def free(self) -> int:
        return self.on_hand - self.reserved

class Inventory:
    def __init__(self):
        self.slots: dict[str, dict[str, Slot]] = defaultdict(dict)    # 商品 → 仓库 → 格子
    def add(self, wh: str, sku: str, n: int):
        self.slots[sku].setdefault(wh, Slot()).on_hand += n
    def available(self, sku: str) -> int:
        return sum(s.free for s in self.slots[sku].values())
    def plan(self, sku: str, n: int) -> list[tuple[str, int]]:       # 只读
        plan, left = [], n
        for wh, slot in sorted(self.slots[sku].items(), key=lambda it: (-it[1].free, it[0])):
            take = min(slot.free, left)
            if take > 0:
                plan.append((wh, take)); left -= take
        if left:
            raise OutOfStock(f"缺 {left}")
        return plan
    def reserve(self, sku: str, n: int) -> list[tuple[str, int]]:
        plan = self.plan(sku, n)                             # 先算好，再提交
        for wh, take in plan:
            self.slots[sku][wh].reserved += take
        return plan
    def confirm(self, sku, plan):
        for wh, take in plan:
            s = self.slots[sku][wh]
            s.on_hand -= take; s.reserved -= take

inv = Inventory()
inv.add("上海", "sku", 5); inv.add("北京", "sku", 3)
plan = inv.reserve("sku", 6)
print("预留 6 件的计划:", plan, "| 可售:", inv.available("sku"))
try:
    inv.reserve("sku", 3)
except OutOfStock as e:
    print("超量全有或全无:", e, "| 可售仍是", inv.available("sku"))
inv.confirm("sku", plan)
print("确认发货后在架:", {w: (s.on_hand, s.reserved) for w, s in inv.slots["sku"].items()})
```

上海 5 件、北京 3 件；预留 6 件，再预留 3 件，最后确认第一个预留，实际输出：

```
预留 6 件的计划: [('上海', 5), ('北京', 1)] | 可售: 2
超量全有或全无: 缺 1 | 可售仍是 2
确认发货后在架: {'上海': (0, 0), '北京': (2, 0)}
```

**为什么。** 预留占着库存但不减在架，所以取消、过期时只需要把 `reserved` 减回去；确认发货才真正减在架。分成「算计划」和「提交」两步，是把会失败的部分放在前面（见副作用排序）。

**代价。** 按可售最多的仓库先拿，会让一个订单拆成多个仓的包裹，物流成本变高；这种策略取舍应该做成可替换的函数，而不是写死在预留里。
