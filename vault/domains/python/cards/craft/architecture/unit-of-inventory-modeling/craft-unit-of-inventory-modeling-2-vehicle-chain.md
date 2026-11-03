---
id: craft-unit-of-inventory-modeling-2-vehicle-chain
node: craft.architecture.unit-of-inventory-modeling
type: qa
step: 2
---
## Q
**库存的单位怎么选 · 租车为什么不能只问「这辆车这段时间空不空」**｜架构

租车允许异地还车。车 7 号从 A 店开到 B 店、9 号还车。有人想 10 号在 A 店取这辆车，时间上与已有行程没有任何重叠。系统能接受吗？可用性应该怎样建模？

## A
**要点。** 单位是「一辆具体的车在时间轴上的一段行程」，不变量是整条行程链自洽：每一段的取车门店等于上一段的还车门店，且段与段之间不重叠。可用性不是「空不空」，而是「把这一段插进去之后整条链还自洽不自洽」。车的位置是算出来的（最后一段在此之前结束的还车门店），不存成字段：存一个当前位置就多了一个真相，也没法表示未来的预约。

```python
@dataclass(frozen=True)
class Leg:
    start: int
    end: int
    origin: str
    dest: str
    @property
    def key(self): return (self.start, self.end)

class VehicleSchedule:
    def __init__(self, base: str) -> None:
        self.base, self.legs = base, []
    def _consistent(self, legs, where) -> bool:    
        prev_end = None
        for leg in legs:
            if leg.origin != where:
                return False
            if prev_end is not None and leg.start < prev_end:
                return False
            where, prev_end = leg.dest, leg.end
        return True
    def accepts(self, leg: Leg) -> bool:
        at = bisect_left(self.legs, leg.key, key=lambda x: x.key)
        before = self.legs[at - 1] if at else None
        after = self.legs[at] if at < len(self.legs) else None
        window = [x for x in (before, leg, after) if x]
        return self._consistent(window, before.origin if before else self.base)
    def add(self, leg: Leg) -> None:
        if not self.accepts(leg):
            raise ValueError("排不下")
        insort(self.legs, leg, key=lambda x: x.key)

car = VehicleSchedule(base="A")
car.add(Leg(7, 9, "A", "B"))
print("10 号在 A 取车（时间上不重叠）:", car.accepts(Leg(10, 11, "A", "A")))
print("10 号在 B 取车:", car.accepts(Leg(10, 11, "B", "B")))
print("3 号在 A 取车 5 号还回 A（赶在 7 号之前）:", car.accepts(Leg(3, 5, "A", "A")))
print("3 号在 A 取车 5 号还到 C（接不上 7 号的出发点）:", car.accepts(Leg(3, 5, "A", "C")))
```

基地 A；已有 7 号到 9 号从 A 到 B 的一段，询问四种新行程，实际输出：

```
10 号在 A 取车（时间上不重叠）: False
10 号在 B 取车: True
3 号在 A 取车 5 号还回 A（赶在 7 号之前）: True
3 号在 A 取车 5 号还到 C（接不上 7 号的出发点）: False
```

**为什么。** 链原本就排好序且自洽，所以插入只会影响左右邻居：用 `bisect` 找插入点，只复查「前一段 → 这一段 → 后一段」，不用重排整条链。

**易错。** 「邻居自洽就等于整链自洽」依赖链本身一直自洽；强行写入的情形（迟还、事故封车）会暂时破坏它，需要退回整链重查的慢路径。
