---
id: hi-pt-scheduler-system-design-8-fixed-rate-delay
node: qb.lld.scheduler-system-design.points
type: qa
step: 8
---
## Q
**任务调度器（定时、周期、带优先级） · 固定频率与固定延迟**｜出自：任务调度器（定时、周期、带优先级） › 深入 2

周期任务的"下一次"有固定频率、固定延迟、cron 三种算法，区别是什么？

## A
**固定频率。** 下一次 = 起点 + k × 间隔，不受执行耗时影响，长期不漂移。
**固定延迟。** 上一次结束后再等一个间隔，保证不重叠，但会逐渐漂移。
**cron。** 按日历字段找下一个匹配时刻，要处理时区和夏令时。
**封装。** 全部放在 `Trigger.after` 里，调度器不关心。
