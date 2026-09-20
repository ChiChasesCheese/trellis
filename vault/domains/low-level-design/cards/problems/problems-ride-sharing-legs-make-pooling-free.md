---
id: problems-ride-sharing-legs-make-pooling-free
node: problems.marketplaces.ride-sharing
type: qa
step: 8
tags: [grown]
---
## Q
网约车第 4 关加「拼车」（第二位乘客上同一辆车）。如果第 1 关就把 `rider_id`、`pickup`、`dropoff` 直接放在 `Trip` 上，会发生什么？正确的建模是什么？

## A
会**推倒重来**：三个字段要变成列表，所有读它们的代码都要改，计价、上下车、座位校验全部重写。

正确建模是从一开始就让行程持有一串**腿**（`RideLeg`）：每条腿是一位乘客的那一段（上下车点、占几个座、何时上车、锁死的加价倍数、结束时回填的车费）。于是「独享」和「拼车」是同一种东西——一条腿 vs 两条腿。

加拼车只需要两道闸加一次追加：

```python
if trip.seats_taken + request.seats > driver.seats:
    raise SeatUnavailableError
detour = (a.distance_to(p) + p.distance_to(q) + q.distance_to(b)) - a.distance_to(b)
if detour > self._max_detour_km:
    raise SeatUnavailableError
trip.add_leg(RideLeg(...))
```

（绕路判据是一条朴素的椭圆式不等式：走 A→P→Q→B 比直接 A→B 多出来的公里数。）

关键在于加人这一步**一次都没有调用状态转移**——多一个人上车不是一次状态转移。这件事可以被直接断言：拼车前后行程的状态轨迹完全相同。「加需求没动老代码」是能被测出来的，不是嘴上说的。
