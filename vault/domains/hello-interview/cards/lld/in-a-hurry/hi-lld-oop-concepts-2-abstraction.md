---
id: hi-lld-oop-concepts-2-abstraction
node: qb.lld.kv-store-eviction.pre-lld-in-a-hurry-oop-concepts
type: qa
step: 2
---
## Q
**抽象（abstraction）：何时引入接口**｜低层设计 · 速览

抽象在 LLD 里解决什么问题？什么时候该引入接口，抽象层级怎么拿捏？用支付方式举例。

## A
**要点。** 抽象是只暴露必要的东西，把实现细节藏在清晰的接口后面：定义“能做什么”而不透露“怎么做”。支付处理依赖 `PaymentMethod` 接口，而不是具体的 `CreditCardProcessor` 或 `PayPalProcessor`，就能随时替换实现而不改调用方；调用方只管 `process()` 拿结果，不关心背后是调 Stripe 还是存令牌。

**何时用。** 抽象出现在系统有复杂性的地方：逻辑纠缠、变化多、规则杂，或需求暗示有多种做法时。

```python
from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def process(self, amount: float) -> bool: ...   # 接口只定契约

class OrderService:
    def __init__(self, payment_method: PaymentMethod) -> None:
        self.payment_method = payment_method        # 依赖抽象，不依赖 StripeAPI 之类的具体类

    def checkout(self, total: float) -> bool:
        return self.payment_method.process(total)
```

**易错。** 难在选对层级：太抽象，接口毫无意义（`doWork()`、`handleRequest()`）；太具体，等于没抽象。从调用方需要执行什么操作出发，而不是操作内部怎么实现。
