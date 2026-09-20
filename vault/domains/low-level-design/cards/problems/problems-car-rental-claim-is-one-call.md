---
id: problems-car-rental-claim-is-one-call
node: problems.booking.car-rental
type: qa
step: 7
tags: [grown]
---
## Q
租车系统（Car Rental）里两个客人同时抢同一门店最后一辆 SUV。为什么「先调 `is_available()` 再调 `make_reservation()`」一定会双开？Python 的 GIL 为什么救不了它？

## A
因为查和占之间有一条**没有锁的缝**：线程 A 查到「有车」还没写入时，线程 B 也查到「有车」，两个都写入，同一辆车被卖了两次。这是检查后行动（check-then-act）竞态的教科书形态。

GIL 救不了：它只保证**单条字节码**不被切开。`dict` 的一次 `get` 或 `set` 是原子的，但「遍历一遍车队 + 逐辆判定 + 写入一段行程」是几百条字节码，中间随时可能切换线程。**锁保护的是复合操作，不是某一次赋值。**

正确形状是把两步合成一个原子方法，返回已经占好的那辆车：

```python
def claim(self, category, branch, period, destination, ref) -> Vehicle:
    leg = ScheduleLeg(ref, period, branch, destination)
    with self._lock:
        for plate in sorted(self._schedules):
            schedule = self._schedules[plate]
            if schedule.vehicle.category is category and schedule.accepts(leg):
                schedule.add(leg)
                return schedule.vehicle
    raise NoVehicleAvailableError(...)
```

测试要用真线程 + `threading.Barrier` 对齐起跑，断言「恰好一个成功、排期上恰好一段」这样的不变量，而不是断言时序。
