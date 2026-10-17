---
id: amz-parking-fees-stage1-bill-by-segments
node: amazon.amz-parking-fees
type: qa
step: 3
tags: [grown]
---
## Q
在 Amazon 停车场计费设计里，第 1 关「按车型的小时费率算出场费」的核心循环怎么写？

## A
从入场时刻起，每次走到「下一个变价时刻」或出场时刻，把这一段的「分/小时 × 秒数」累加到所在日历日；最后每个日历日除以 3600 向上取整到分。小时费率是 400 分的小汽车，周五 10:00 到 12:00：400×7200÷3600 = 800 分。
```python
at = entered
while at < exited:
    end = min(tariff.next_change(at), exited)
    span = int((end - at).total_seconds())
    rate = tariff.rate_at(vehicle, at).cents
    units[at.date()] = units.get(at.date(), 0) + rate * span
    at = end
raw = Money(-(-units[day] // 3600))  # 向上取整，每天一次
```
