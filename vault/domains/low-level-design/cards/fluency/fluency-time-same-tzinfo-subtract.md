---
id: fluency-time-same-tzinfo-subtract
node: fluency.time-numbers
type: qa
step: 2
---
## Q
两个都带 `America/New_York` 时区的时间，一个是 3 月 8 日 0 点，一个是 3 月 9 日 0 点，中间跨过夏令时开始。直接相减得到 1 天整，实际经过了多久？算有效期、年龄、耗时之前应该先做什么？

## A
**相减前先换成 UTC，别信同一 tzinfo**

- **规则**：两个 aware 值的 `tzinfo` 是同一个对象时，Python 相减按钟面（wall time）算，不考虑中间偏移变了；`tzinfo` 不同才先各自换算成 UTC 再相减；
- **后果**：夏令时切换那一天，`b - a` 显示 24 小时，真实只过了 23 小时；用它算令牌年龄、到期时间，会差一小时，只在每年两个日子出问题，很难复现；
- **做法**：所有“经过多久”的计算，两端都先 `astimezone(UTC)` 再相减；业务里干脆只存 UTC，就不存在这个坑；
- **日历运算是另一回事**：“明天同一时刻”要在本地时区上加 `timedelta(days=1)`（钟面前进一天），“24 小时后”要在 UTC 上加 `timedelta(hours=24)`，两者在夏令时当天不同，需求要说清楚是哪一个。

```python
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

ny = ZoneInfo("America/New_York")
a = datetime(2026, 3, 8, 0, 0, tzinfo=ny)    # 夏令时 3 月 8 日凌晨 2 点开始
b = datetime(2026, 3, 9, 0, 0, tzinfo=ny)
print(b - a)                                  # 1 day, 0:00:00：按钟面
print(b.astimezone(timezone.utc) - a.astimezone(timezone.utc))   # 23:00:00：真实经过
```

**知识点：**时间与数字（Time & Numbers）
