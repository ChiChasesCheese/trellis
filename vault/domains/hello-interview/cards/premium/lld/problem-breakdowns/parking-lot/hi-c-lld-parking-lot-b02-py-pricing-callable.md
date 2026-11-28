---
id: hi-c-lld-parking-lot-b02-py-pricing-callable
node: lld.problem-breakdowns.parking-lot.beyond
type: qa
step: 3
---
## Q
**停车场 · Python：用函数做定价策略**｜拓展 · 加分

定价策略需要建一个抽象基类加多个子类吗？Python 里有更轻的写法吗？

## A
**模式。** 策略（Strategy）：同一个"票 + 出场时间 → 费用"的约定，可替换的实现。

```python
from dataclasses import dataclass
from functools import partial
from typing import Callable

HOUR = 3_600_000


@dataclass(frozen=True)
class Ticket:
    vehicle: str
    entered_ms: int


Pricing = Callable[[Ticket, int], int]          # 策略的全部"接口"：一个签名


def hourly(rate_cents: int, ticket: Ticket, exit_ms: int) -> int:
    hours = -(-(exit_ms - ticket.entered_ms) // HOUR)
    return max(hours, 1) * rate_cents


def per_vehicle(rates: dict[str, int], ticket: Ticket, exit_ms: int) -> int:
    return hourly(rates[ticket.vehicle], ticket, exit_ms)


flat: Pricing = partial(hourly, 500)            # partial 固定前面的参数，得到只剩 (ticket, exit_ms) 的函数
typed: Pricing = partial(per_vehicle, {"car": 500, "moto": 300})

t = Ticket("moto", 0)
assert flat(t, 90 * 60_000) == 1000             # 90 分钟 -> 2 小时 x 500
assert typed(t, 90 * 60_000) == 600             # 摩托车 2 小时 x 300
```
- **为什么更轻：** 策略只有一个方法时，函数就是策略；`partial` 把配置（费率）绑进去，不需要类和 `self`。
- **什么时候要类：** 策略有多个相关方法、要保存状态，或者要用类型检查强制实现完整接口（可用 `typing.Protocol` 描述接口，无需继承）。
- **代价：** 函数策略没有名字和文档的天然位置，靠类型别名和注释补；配置多了不如一个配置对象清楚。
- **何时不用：** 只有一个固定费率时直接写 `compute_fee`，别提前抽象。
