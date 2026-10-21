---
id: amz-train-fare-edge-per-trip-vs-per-day-cap
node: amazon.amz-train-fare
type: qa
step: 7
tags: [grown]
---
## Q
在 Amazon 火车票价设计里，「总票价封顶」若指一个人一天累计不超过封顶，怎样记账才对？一个具体例子是什么？

## A
`DailyCapLedger` 记 `(日期 → 乘客 → 已付)`，本次实付 = min(本次票价, max(封顶 − 已付, 0))。例：封顶 6.00，乘客 ann 周一 G→I（4.00）实付 4.00，I→G（4.00）实付 2.00，再 G→U 实付 0。关键细节：整个 `charge` 只取一次时间，避免 23:59 算价、00:01 记账落到两天；封顶已满时剩余额度取 0 而不是负数；字典按天增长，要清理旧日期。
