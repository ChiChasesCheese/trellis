---
id: craft-policy-seam-1-inject-what-changes
node: craft.patterns.policy-seam
type: qa
step: 1
---
## Q
**策略接缝 · 会变的规则为什么要在构造时注入**｜模式

航班订座：每个舱位的座位数固定，但航司会按舱位超售（overbooking，卖得比座位多一点，因为总有人不来）。比例今天 10%，下周经济舱 15%、头等舱 0。把「超售多少」写成订座函数里的一个 `if`，和把它做成注入的函数，后来会差在哪？

## A
**要点。** 订座流程（查余量、占座、记账）是稳定的，「超售多少」是会变的政策。把后者做成一个函数参数在构造时传入：流程只认一个数 `authorized = 座位数 + 政策(舱位, 航班)`，不知道这个数怎么来的。换政策就是换一个参数，不碰库存和状态机。默认值取政策的下界（不超售），测试不必先配置政策。

```python
from collections.abc import Callable, Mapping
from dataclasses import dataclass

OverbookingPolicy = Callable[[str, "Flight"], int]    # (舱位, 航班) -> 额外可售张数

def no_overbooking(cabin, flight) -> int:
    return 0                                          # 下界，也是测试里最省心的基线

def percent_overbooking(by_cabin: Mapping[str, int]) -> OverbookingPolicy:
    def extra(cabin, flight):
        return flight.capacity(cabin) * by_cabin.get(cabin, 0) // 100
    return extra                                      # 闭包带着配置

@dataclass
class Flight:
    seats: dict[str, int]
    overbooking: OverbookingPolicy = no_overbooking   # 构造时注入，默认 = 下界
    def __post_init__(self): self.sold: dict[str, int] = {}
    def capacity(self, cabin): return self.seats[cabin]
    def authorized(self, cabin):                      # 流程只认这一个数
        return self.capacity(cabin) + self.overbooking(cabin, self)
    def sell(self, cabin) -> bool:
        if self.sold.get(cabin, 0) >= self.authorized(cabin): return False
        self.sold[cabin] = self.sold.get(cabin, 0) + 1; return True

for name, policy in [("默认", no_overbooking), ("经济舱 10%", percent_overbooking({"Y": 10}))]:
    f = Flight({"Y": 20, "F": 8}, policy)             # 经济舱 Y 20 座，头等舱 F 8 座
    ok = sum(f.sell("Y") for _ in range(30)); okF = sum(f.sell("F") for _ in range(30))
    print(f"{name}: 经济舱卖出 {ok}，头等舱卖出 {okF}")
```

经济舱 20 座、头等舱 8 座，各尝试卖 30 张：

```
默认: 经济舱卖出 20，头等舱卖出 8
经济舱 10%: 经济舱卖出 22，头等舱卖出 8
```

**为什么。** 硬编码的 `if` 会把「政策变了」变成「改订座核心」，核心每改一次，库存的一致性就要重新验证一遍。注入以后，政策可以单独测试（给一个舱位和座位数，看返回值），流程的测试用 `no_overbooking` 跑，互不干扰。

**代价。** 多一个间接层：读代码的人要多跳一步才知道上限是怎么来的。所以只在「真的会变」的地方加（判据见第 3 张卡）。
