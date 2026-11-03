---
id: craft-half-open-intervals-2-instant-boundaries
node: craft.patterns.half-open-intervals
type: qa
step: 2
---
## Q
**半开区间 · 额度包、高峰窗口、预留的「恰好那一刻」算在里面还是外面**｜写法

额度包有效期从 12:00 到 13:00。在 12:00:00 整，它能用吗？在 13:00:00 整呢？每天 18:00 到 19:00 是高峰，19:00:00 整算不算高峰？预留有效期到某个时刻，"到点"那一刻已经过期还是还没过期？

## A
**要点。** 统一规则：**起点那一刻属于区间，终点那一刻不属于**。时刻上同样是半开区间 `[at, expires_at)`。判断可用写 `at <= now < expires`；判断过期写 `expires_at <= now`（恰好到点就算过期）。窗口 `start <= t < end`。这样，紧接着的下一个区间 `[expires_at, ...)` 从同一个瞬间开始，任何一刻恰好属于一个区间，没有重叠也没有缝。

```python
from datetime import datetime, time, timedelta

# ① 额度包有效期 [at, expires_at)——到点那一刻已经失效
at, expires = datetime(2026, 11, 3, 12, 0, 0), datetime(2026, 11, 3, 13, 0, 0)
usable = lambda now: at <= now < expires         # 起点含，终点不含
for label, now in [("开始前 1 秒", at - timedelta(seconds=1)), ("恰好开始", at),
                   ("结束前 1 秒", expires - timedelta(seconds=1)), ("恰好到期", expires)]:
    print(f"{label:8} 可用={usable(now)}")

# ② 高峰窗口 [start, end)；end == 00:00 表示"到当天午夜"，换算成 24:00 = 86400 秒
secs = lambda t: t.hour * 3600 + t.minute * 60 + t.second
def covers(start, end, t):
    end_s = 86400 if end == time(0) else secs(end)
    return secs(start) <= secs(t) < end_s
print("22:00-24:00 覆盖 23:59:59?", covers(time(22), time(0), time(23, 59, 59)), " 覆盖 00:00?", covers(time(22), time(0), time(0)))
print("18:00-19:00 覆盖 19:00?", covers(time(18), time(19), time(19)), " 覆盖 18:00?", covers(time(18), time(19), time(18)))
```

```
开始前 1 秒  可用=False
恰好开始     可用=True
结束前 1 秒  可用=True
恰好到期     可用=False
22:00-24:00 覆盖 23:59:59? True  覆盖 00:00? False
18:00-19:00 覆盖 19:00? False  覆盖 18:00? True
```

**为什么。** "恰好那一刻"是最容易出现分歧的地方，也是测试最常断言的地方，所以必须有唯一的约定，而不是各函数各写各的。到期用 `<=` 而不是 `<`：到期时刻本身已经失效；堆里 `expires_at <= now` 的条目被弹出结算，和 `usable` 的 `now < expires` 恰好互补，不会出现某一刻既"可用"又"已过期"。

**易错。** 午夜是 `time(0)`，用 `end > start` 比较会把"22:00 到午夜"当成空区间；换算成当天第 86400 秒才能继续用 `<`。跨午夜的窗口拆成两个窗口（22:00-24:00 和 00:00-06:00），每个都是普通的半开窗口。
