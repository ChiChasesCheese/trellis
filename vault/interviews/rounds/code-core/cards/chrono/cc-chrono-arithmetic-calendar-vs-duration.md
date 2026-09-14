---
id: cc-chrono-arithmetic-calendar-vs-duration
node: chrono.arithmetic
type: qa
---
## Q
A plan starts 2025-01-31 and renews "monthly". Two implementations: `start + timedelta(days=30)`, and "the same day of the next month". Give both answers and the rule that decides.

## A
**Calendar arithmetic is not duration arithmetic.** `timedelta` only knows fixed units — days, hours, seconds — so `+30 days` gives 2025-03-02 while "next month" gives 2025-02-28.

- Duration math (a TTL, an SLA, "within 60 minutes"): `timedelta` or integer seconds. Exact, monotone, no calendar involved.
- Calendar math (billing anchors, "the 1st of next month", "three months later"): compute the month as `y*12 + m` arithmetic, then clamp the day ([[cc-chrono-arithmetic-month-end-clamp]]).
- Never approximate a month as 30 days or a year as 365 in money math — the drift is a failed test, not a rounding error.
- Say which one the sentence means before coding; "every month" and "every 30 days" are different products.

## Q zh
一个套餐 2025-01-31 开始，按「月」续期。两种实现：`start + timedelta(days=30)`，以及「下个月的同一天」。给出两者的结果和判断规则。

## A zh
**日历算术不是时长算术。** `timedelta` 只认识固定单位 —— 天、小时、秒 —— 所以 `+30 天` 得到 2025-03-02，而「下个月」得到 2025-02-28。

- 时长运算（TTL、SLA、「60 分钟以内」）：用 `timedelta` 或整数秒。精确、单调，与日历无关。
- 日历运算（账单锚点、「下月 1 号」、「三个月后」）：用 `y*12 + m` 做月份算术，再对日做钳位（[[cc-chrono-arithmetic-month-end-clamp]]）。
- money 相关的计算里绝不要把一个月近似成 30 天、一年近似成 365 天 —— 漂移是测试失败，不是舍入误差。
- 写代码前先说清句子指的是哪一种；「每月」和「每 30 天」是两种产品。
