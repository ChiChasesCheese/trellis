---
id: craft-time-types-2-aware-datetime
node: craft.idioms.time-types
type: qa
step: 2
---
## Q
**时间类型 · 默认时钟为什么是 `datetime.now(timezone.utc)`，naive 与 aware 比较会怎样**｜写法

调度器的默认时钟写成 `datetime.now`（没带参数），传入的到期时间是带时区的，两者一比较就抛 `TypeError`。naive 和 aware 的 `datetime` 差在哪？外卖结算的 `_at(day, seconds, like)` 为什么要把 `like.tzinfo` 带过去？

## A
**要点。** naive `datetime` 没有时区信息，只是一个「年月日时分秒」的标签，aware 的带有 `tzinfo`，能对应到唯一的时刻。两者混用没有意义，所以 Python 的 `<` 直接抛 `TypeError`（`==` 则静默返回 `False`，更隐蔽）。默认时钟用 `datetime.now(timezone.utc)`，所有时间都是 aware、都在 UTC：可以跨时区比较，静默时段这类要换算本地时间的逻辑才可能算对。

```python
def utc_now() -> datetime:
    return datetime.now(timezone.utc)      # 带时区的当前时间

def at(day, seconds: int, like: datetime) -> datetime:
    # 当天第 N 秒，时区沿用 like 的：不能凭空造一个 naive 的
    return datetime.combine(day, datetime.min.time(), tzinfo=like.tzinfo) + timedelta(seconds=seconds)

naive = datetime(2026, 1, 1, 12, 0)
aware = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)
try:
    naive < aware
except TypeError as e:
    print("比较 naive 与 aware:", e)
print("== 比较(不抛错, 但永远不等):", naive == aware)

now = utc_now()
print("utc_now 带时区:", now.tzinfo)
print("at(...) 沿用 like 的时区:", at(now.date(), 3600, now).tzinfo)
print("同一时刻不同时区相等:",
      datetime(2026, 1, 1, 12, tzinfo=timezone.utc) == datetime(2026, 1, 1, 20, tzinfo=timezone(timedelta(hours=8))))
```

实际输出：

```
比较 naive 与 aware: can't compare offset-naive and offset-aware datetimes
== 比较(不抛错, 但永远不等): False
utc_now 带时区: UTC
at(...) 沿用 like 的时区: UTC
同一时刻不同时区相等: True
```

**为什么沿用 `like.tzinfo`。** 外卖要合成「当天第 N 秒」的时刻，去和订单事件比较。凭空用 `datetime.combine(day, time(0))` 造出来的是 naive 的，一比较就崩；从样本值复制时区，造出的值天然与之可比。

**易错。** `datetime.utcnow()` 返回的是 **naive** 的 UTC 时间（且在 3.12 起被弃用），不是 aware；要 aware 的 UTC 用 `datetime.now(timezone.utc)`。
