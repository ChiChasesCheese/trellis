---
id: craft-thin-service-fat-domain-5-orchestrator-at-scale
node: craft.architecture.thin-service-fat-domain
type: qa
step: 5
---
## Q
**服务层薄、领域对象厚 · 微服务里的协调器应该保存什么**｜架构

下单要跨库存服务和支付服务。API 网关或 Saga 协调器负责串起这两步。协调器自己应该保存哪些状态？它崩溃重启后，怎么保证不会重复预留库存？

## A
**要点。** 同样的规则放大到服务之间：协调器（API 网关、BFF、Saga 协调器）只编排，不持有业务状态；库存、金额这些带不变量的数据由各自的领域服务拥有。协调器唯一需要持久化的是进度：每个订单走到了哪一步。重启后恢复进度表，已经完成的步骤跳过，不会重复预留。

```python
# 领域服务：各自拥有数据和不变量
class Inventory:
    def __init__(self) -> None:
        self.stock = {"sku": 1}
    def reserve(self, sku: str) -> None:
        if self.stock[sku] <= 0:
            raise RuntimeError("缺货")              # 不变量由库存服务自己守
        self.stock[sku] -= 1
    def release(self, sku: str) -> None:
        self.stock[sku] += 1

class Payments:
    def __init__(self) -> None:
        self.charged: set[str] = set()
    def charge(self, order: str) -> None:
        self.charged.add(order)

# 编排者：只记「走到哪一步了」，不持有库存、金额
class Orchestrator:
    def __init__(self, inv: Inventory, pay: Payments) -> None:
        self.inv, self.pay = inv, pay
        self.progress: dict[str, list[str]] = {}    # 订单 -> 已完成的步骤（真正需要持久化的唯一状态）
    def place(self, order: str, sku: str) -> str:
        done = self.progress.setdefault(order, [])
        try:
            if "reserve" not in done:
                self.inv.reserve(sku); done.append("reserve")
            if "charge" not in done:
                self.pay.charge(order); done.append("charge")
        except RuntimeError as e:
            for step in reversed(done):
                if step == "reserve":
                    self.inv.release(sku)
            self.progress[order] = []
            return f"失败并补偿: {e}"
        return f"成功 {done}"

inv, pay = Inventory(), Payments()
inv.stock["sku"] = 2
orch = Orchestrator(inv, pay)
print(orch.place("o1", "sku"), "| 库存", inv.stock)
inv.reserve("sku"); orch.progress["o2"] = ["reserve"]   # o2 预留后，编排者在扣款前崩了
orch2 = Orchestrator(inv, pay)                            # 重启，只恢复进度表
orch2.progress = dict(orch.progress)
print(orch2.place("o2", "sku"), "| 不会重复预留，库存", inv.stock)
print(orch2.place("o3", "sku"), "| 库存", inv.stock)
```

库存 2；o1 正常；o2 在预留之后、扣款之前协调器崩溃，重启后只恢复进度表再执行；o3 在缺货时执行，实际输出：

```
成功 ['reserve', 'charge'] | 库存 {'sku': 1}
成功 ['reserve', 'charge'] | 不会重复预留，库存 {'sku': 0}
失败并补偿: 缺货 | 库存 {'sku': 0}
```

**为什么。** 缺货的判断在库存服务里（`reserve` 抛 `RuntimeError`），协调器不知道库存有多少，只知道这一步失败了该补偿哪几步。业务规则变了只改领域服务，协调器不动。

**代价。** 协调器的进度表本身要持久化，且「执行步骤」与「记录进度」之间有崩溃窗口，所以每个领域服务的操作也要幂等；否则重启后重做的那一步会生效两次。
