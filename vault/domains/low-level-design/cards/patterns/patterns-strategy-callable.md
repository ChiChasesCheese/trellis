---
id: patterns-strategy-callable
node: patterns.strategy
type: qa
step: 1
---
## Q
停车场对不同车型按不同规则计算每小时停车费，如果用 Strategy 模式来做，Python 里最朴素的写法是什么？

## A
不需要专门定义一个 `PricingStrategy` 接口——把"会变的算法"直接当参数传，类型是一个 `Callable[[float], float]`。调用方可以在运行时换成任何符合签名的函数，比为每种定价方式建一个类要轻。

```python
from typing import Callable

PricingFn = Callable[[float], float]  # hours -> fee

def hourly_rate(hours: float) -> float:
    return hours * 2.5

def charge(hours: float, pricing: PricingFn) -> float:
    return pricing(hours)
```
