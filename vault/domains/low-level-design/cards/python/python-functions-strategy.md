---
id: python-functions-strategy
node: python.first-class-functions
type: qa
step: 2
tags: [grown]
---
## Q
用函数替代“策略模式（Strategy）”的类层级，给一个定价策略的例子。

## A
```python
def regular_price(base: float) -> float:
    return base

def member_discount(base: float) -> float:
    return base * 0.9

def price(base: float, strategy) -> float:
    return strategy(base)

price(100, member_discount)  # 90.0
```
`strategy` 只是一个 `Callable[[float], float]`；换策略就是传一个不同的函数，不需要 `PricingStrategy` 抽象基类和一堆只有一个方法的子类。
