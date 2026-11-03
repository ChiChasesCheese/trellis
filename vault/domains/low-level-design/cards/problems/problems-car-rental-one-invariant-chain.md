---
id: problems-car-rental-one-invariant-chain
node: problems.booking.car-rental
type: qa
step: 2
tags: [grown]
---
## Q
租车系统（Car Rental）里，一辆车的排期用「按开始时间排好的行程链」表示后，判断「这辆车能不能接这一单」只需要一条不变量。这条不变量是什么？它一口气解决了哪三件事？

## A
不变量：**按时间排好之后，每一段的取车门店等于上一段的还车门店（第一段等于基地门店），且租约段与上一段之间留够周转时间。**

它一口气解决三件事：

1. **不重叠**——两段交叠时，后一段的开始时刻落在前一段结束之前，被周转条件挡住；
2. **接得上**——门店链首尾相接，异地还车带来的位置变化自动传播给后面每一段；
3. **周转缓冲**——清洁、加油、检查的时间写在同一个判断里。

于是「能不能接单」就是一句话：把候选段插进链里，再检查链是否仍然自洽。链本来就排好序且自洽，所以只需要用 `bisect` 找到插入点、复查左右邻居，不必每次把整条链重排重查。

```python
def accepts(self, leg: ScheduleLeg) -> bool:
    at = bisect_left(self._legs, _order_key(leg), key=_order_key)
    before = self._legs[at - 1] if at else None
    after = self._legs[at] if at < len(self._legs) else None
    window = [x for x in (before, leg, after) if x is not None]
    return self._consistent(window, before.origin if before else self._base)
```

这条不变量的含金量在于**复用**：可用性查询、迟还后的修复、维修封锁后的复核，全部调同一个 `_consistent`。
