---
id: hi-lld-oop-concepts-3-polymorphism
node: lld.in-a-hurry.oop-concepts
type: qa
step: 3
---
## Q
**多态（polymorphism）取代类型判断**｜低层设计 · 速览

多态在 LLD 里替代什么写法？用停车场的车辆类型说明做法，以及它的代价是什么？

## A
**要点。** 多态取代的是 `if type == "credit"` 或 `switch (vehicleType)` 这类类型判断：调用同一个方法，让每个对象用自己的方式响应，不检查类型。它自然来自抽象：先定义 `Vehicle` 这样的接口，每个实现提供自己的行为。

```python
from enum import Enum

class SpotSize(Enum):
    REGULAR = "regular"
    MOTORCYCLE = "motorcycle"
    LARGE = "large"

class Vehicle:
    def get_required_spot_size(self) -> SpotSize:
        raise NotImplementedError

class Truck(Vehicle):
    def get_required_spot_size(self) -> SpotSize:
        return SpotSize.LARGE             # 每种车自己说出需要的车位

class ParkingLot:
    def park(self, vehicle: Vehicle) -> bool:
        size = vehicle.get_required_spot_size()   # 没有 if/else，新增车型无需改这里
        return self._find_spot(size) is not None
```

新增车型只需新增一个实现 `Vehicle` 的类，`ParkingLot` 不变。信号：一旦发现自己在对枚举写 switch 或类型检查，就该考虑多态。

**取舍。** 高度多态的代码可能难跟踪和调试，实现一多更明显。有些公司偏爱清晰明确的分支，有些喜欢多态的扩展性，面试里要能解释这个取舍。
