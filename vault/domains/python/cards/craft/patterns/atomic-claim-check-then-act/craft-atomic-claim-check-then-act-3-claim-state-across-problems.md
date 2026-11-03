---
id: craft-atomic-claim-check-then-act-3-claim-state-across-problems
node: craft.patterns.atomic-claim-check-then-act
type: qa
step: 3
---
## Q
**原子占位 · 派单、去重、占座里的同一个「占」**｜模式

打车派单要保证两位乘客不会匹配到同一位司机；通知服务要保证同一封信不发两遍；订票要保证一批座位要么全占要么全不占。这三件事的代码长得很不一样，共同骨架是什么？为什么司机要多一个 OFFERED 状态？

## A
**要点。** 都是「在一把锁里：读状态 → 判断 → 写入我的名字」，并且写入后别人再读就会看到「已被占」。OFFERED 状态就是占位的痕迹：没有它，派单只能先查空闲、再另行写入，中间的窗口就是双重派单。

```python
# ride-sharing  DriverPool.hold
with self._lock:
    driver = self._drivers.get(driver_id)
    if driver is None or driver.status is not DriverStatus.AVAILABLE:
        return False
    self._drivers[driver_id] = replace(driver, status=OFFERED, held_by=offer_id)
    return True

# notification-service  IdempotencyStore.claim
with self._lock:
    entry = self._entries.get(key)
    if entry is not None and now - entry[0] <= self._ttl:
        return entry[1] if entry[1] is not None else _PENDING
    self._entries[key] = (now, None)       # 占坑
    return None

# movie-booking  Show.hold：先检查所有座位，再全部标成 HELD
with self._lock:
    taken = [l for l in labels if self._effective(self._slots[l], now) is not AVAILABLE]
    if taken:
        raise SeatNotAvailableError(...)
    for label in labels:
        self._slots[label] = _Slot(SeatStatus.HELD, hold_id=receipt.id, ...)
```

以上各题的代码是节选：省略了类型标注、文档字符串和 `...` 处的细节，个别行为讲解而合并成一行，不是逐字摘抄。

**不变。** 一把锁、判断与写入在同一块、写入的内容让别人能看出「已被占」。**变化。** 司机返回 `bool`（赢了没有）；去重返回上一次的结果；订票对一批对象全有或全无，失败时什么都没写，所以不需要清理。

**见于。** ride-sharing、idempotent-transfer、notification-service、movie-booking。

**信号。** 代码里出现「查询是否可用」和「标记为占用」是两次调用，或中间夹着别的语句。
