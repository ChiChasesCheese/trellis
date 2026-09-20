---
id: problems-ride-sharing-offered-status-cas
node: problems.marketplaces.ride-sharing
type: qa
step: 2
tags: [grown]
---
## Q
网约车派单时，一张要约敞开的那十几秒里，这位司机算不算「空闲」？用一个 `is_available` 布尔字段会出什么事？

## A
不算。必须给他一个**第四个状态** `OFFERED`：被一张敞开的要约独占着——既不是空闲（不能再被派单），也不是在跑车（还没人接单）。

用布尔字段会踩**先检查后动作**（check-then-act）竞态：`if d.is_available` 和 `d.is_available = False` 是两段字节码，两个线程会同时挑中同一位司机，两位乘客匹配到同一辆车。Python 的 GIL 在这里什么也不保证——它只保证单条字节码不被打断。

正确形态是锁内的一次**比较并交换**（compare-and-swap）：

```python
def hold(self, driver_id: str, offer_id: str) -> bool:
    with self._lock:
        driver = self._drivers.get(driver_id)
        if driver is None or driver.status is not DriverStatus.AVAILABLE:
            return False
        self._drivers[driver_id] = replace(
            driver, status=DriverStatus.OFFERED, held_by=offer_id)
        return True
```

它返回 `bool` 而不是抛异常：抢不到司机是派单的正常路径（换下一个候选），不是错误。`held_by` 记的是「被哪张要约占着」，`release` / `commit` 都只认当前持有者，于是迟到的超时清扫不会把已经在跑下一单的司机打回空闲——这是 fencing token（护栏令牌）的最小形式。
