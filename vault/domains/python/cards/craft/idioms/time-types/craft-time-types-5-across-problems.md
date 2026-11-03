---
id: craft-time-types-5-across-problems
node: craft.idioms.time-types
type: qa
step: 5
---
## Q
**时间类型 · 限流、通知、结算、键值存储、调度器各自用的时间**｜写法

五个系统里的时间有的是 `float`，有的是带时区的 `datetime`，有的是整数参数。每一种为什么这样选？

## A
**要点。** 同一个判据：这个时间用来**量时长**、**对应日历**，还是只是**排序的数据**。时长用单调秒数，日历用带时区的 `datetime`，排序数据用整数。时钟都不在类里硬编码，永远从外部给。

```python
# rate-limiter：单调秒数，永远从外部注入
Clock = Callable[[], float]

# notification-service：默认时钟带时区，静默时段才可能跨时区算对
def utc_now() -> datetime:
    return datetime.now(timezone.utc)

# dasher-payout：合成「当天第 N 秒」时沿用样本的时区
def _at(day: date, seconds: int, like: datetime) -> datetime:
    return datetime.combine(day, time(0), tzinfo=like.tzinfo) + timedelta(seconds=seconds)

# kv-store：整数时间戳是每个方法的第一个参数
def set(self, timestamp: int, key: str, field: str, value: str, ttl: int | None = None) -> None:
```

调度器和取款机的默认时钟同样是 `utc_now()`，到期时间可与带时区的 `due` 直接比较。

**见于。** rate-limiter、notification-service、dasher-payout、kv-store、task-scheduler、atm。

**信号。** 代码里直接出现 `time.time()`、`datetime.now()`、`time.sleep(...)` 之后做算术比较；或者测试里需要真的等几秒。
