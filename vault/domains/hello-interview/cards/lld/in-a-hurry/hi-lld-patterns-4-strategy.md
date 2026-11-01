---
id: hi-lld-patterns-4-strategy
node: lld.in-a-hurry.patterns
type: qa
step: 4
---
## Q
**策略：用多态替换条件分支**｜低层设计 · 速览

为什么策略模式（Strategy）是低层设计面试里最常被问的模式？请以支付方式为例写出结构，并说明它与工厂的区别。

## A
**为什么常考。** 它直接检验你是否理解多态和“组合优于继承”。看到按类型分支的一长串 if/else，就是一个等待被改成策略的地方。

```python
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> bool: ...

class ShoppingCart:
    def set_strategy(self, s: PaymentStrategy) -> None:
        self.strategy = s
    def checkout(self, amount: float) -> None:
        self.strategy.pay(amount)  # 委托，不判断类型
```

信用卡和 PayPal 各自实现 `pay`。购物车只持有一个策略引用并委托给它，运行时可以随时更换。

**区别。** 策略是在对象已存在后，决定用哪种行为；工厂是决定创建哪个类型的对象。

**要点。** 常见例子还有停车场的车辆类型、计费规则、匹配算法。
