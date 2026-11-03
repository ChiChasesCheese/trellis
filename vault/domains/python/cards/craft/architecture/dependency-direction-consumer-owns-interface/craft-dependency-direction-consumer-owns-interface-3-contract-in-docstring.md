---
id: craft-dependency-direction-consumer-owns-interface-3-contract-in-docstring
node: craft.architecture.dependency-direction-consumer-owns-interface
type: qa
step: 3
---
## Q
**依赖方向 · 接口的语义契约写在哪里、怎么验证**｜架构

下单流程定义了 `PaymentGateway`，补偿动作（退款）可能在「不知道扣款到底成没成」时被调用：钱扣了，响应在网络上丢了。方法签名只写得出 `charge(key, amount)`，写不出「同一个键只扣一次」。这类语义要求放在哪里？怎样保证每个实现（真网关、测试替身）都遵守？

## A
**要点。** 签名之外的语义写在接口的 docstring 里，并且写成一组契约测试（contract test），对每个实现都跑一遍。幂等键让调用方可以放心重试和补偿：`charge` 重试不会重复扣，`refund` 对没扣过的键是无操作，所以补偿可以无条件调用。

```python
class PaymentGateway(Protocol):
    """契约：同一个键重复扣款只扣一次；对没扣过款的键退款是无操作。"""
    def charge(self, idempotency_key: str, amount: int) -> str: ...
    def refund(self, idempotency_key: str) -> None: ...

class GoodGateway:
    def __init__(self) -> None:
        self.held: dict[str, int] = {}
    def charge(self, idempotency_key: str, amount: int) -> str:
        self.held.setdefault(idempotency_key, amount)
        return f"ch_{idempotency_key}"
    def refund(self, idempotency_key: str) -> None:
        self.held.pop(idempotency_key, None)

class BadGateway(GoodGateway):                 # 违约：重复键累加
    def charge(self, idempotency_key: str, amount: int) -> str:
        self.held[idempotency_key] = self.held.get(idempotency_key, 0) + amount
        return f"ch_{idempotency_key}"

def contract_test(make: Callable[[], GoodGateway]) -> str:
    g = make()
    g.charge("order-1", 50); g.charge("order-1", 50)   # 重试
    g.refund("never-charged")                          # 退没扣过的键
    return "通过" if g.held == {"order-1": 50} else f"违约 held={g.held}"

for cls in (GoodGateway, BadGateway):
    print(cls.__name__, contract_test(cls))
```

对 `GoodGateway` 和 `BadGateway` 各跑一遍 `contract_test(cls)`，实际输出：

```
GoodGateway 通过
BadGateway 违约 held={'order-1': 100}
```

**为什么。** 下单流程里的补偿 `undo_pay` 无条件按订单号退款，不看有没有拿到回执，它的正确性完全建立在这条契约上；替身若不守契约，测试通过也说明不了什么。

**代价。** 契约测试要维护；真实供应商的契约只能靠沙箱或消费者驱动契约测试（consumer-driven contract test）去验证，不能只信文档。
