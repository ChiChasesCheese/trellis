---
id: craft-time-types-3-calendar-vs-duration
node: craft.idioms.time-types
type: qa
step: 3
---
## Q
**时间类型 · 「每天 9 点」和「24 小时后」在夏令时当天差一小时，怎么表示才不出错**｜写法

系统有两种需求：每天早上 9 点发提醒；令牌 24 小时后过期。夏令时开始的那天只有 23 小时，两种需求如果都用「加 24 小时」或都用「加一天」，会各出什么错？跨午夜的静默时段（22:00 到 07:00）怎么写？

## A
**要点。** 两种需求是不同的东西。**日历时间**（每天 9 点）要在本地时区做钟面加法：同一时区内的 `datetime + timedelta(days=1)` 保持钟面时间不变，夏令时当天依然是 9:00。**时长**（24 小时后到期）要在 UTC 或单调时钟上做：绝对流逝的 86400 秒，本地钟面上可能显示 10:00。用错的后果：日历需求用 UTC 加 24 小时，提醒会在夏令时前后漂移一小时；时长需求用钟面加一天，令牌会少活或多活一小时。

```python
from datetime import datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

ny = ZoneInfo("America/New_York")

# 2026-03-08 美国东部时间凌晨 2 点跳到 3 点（夏令时开始），这一天只有 23 小时
t = datetime(2026, 3, 7, 9, 0, tzinfo=ny)
cal = t + timedelta(days=1)                      # 同一时区内：钟面加一天
utc = (t.astimezone(timezone.utc) + timedelta(hours=24)).astimezone(ny)
print("每天 9 点提醒 (钟面+1天):", cal.strftime("%m-%d %H:%M"))
print("24 小时后到期 (UTC+24h) :", utc.strftime("%m-%d %H:%M"))
print("两者相隔(小时):", (cal - utc).total_seconds() / 3600)

# 跨午夜的静默时段 22:00-07:00：start > end 表示跨天
def in_quiet(local: datetime, start: time = time(22), end: time = time(7)) -> bool:
    t = local.timetz().replace(tzinfo=None)
    return start <= t or t < end if start > end else start <= t < end

for h in (23, 3, 12):
    print(f"{h:02d}:00 在静默时段:", in_quiet(datetime(2026, 1, 1, h, tzinfo=ny)))
```

实际输出：

```
每天 9 点提醒 (钟面+1天): 03-08 09:00
24 小时后到期 (UTC+24h) : 03-08 10:00
两者相隔(小时): -1.0
23:00 在静默时段: True
03:00 在静默时段: True
12:00 在静默时段: False
```

**跨午夜的区间。** `start > end` 表示跨天：判断时用「不小于 start，或小于 end」，不能写成 `start <= t < end`。

**易错。** 一些钟面时间在夏令时当天不存在（春季跳过的 02:xx）或出现两次（秋季回拨）。重复发生的任务要在配置里记**时区名**（`America/New_York`），不要记固定偏移（`-05:00`），否则夏令时一过就错一小时。
