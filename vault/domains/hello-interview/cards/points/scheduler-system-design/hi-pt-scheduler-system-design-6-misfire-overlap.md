---
id: hi-pt-scheduler-system-design-6-misfire-overlap
node: qb.lld.scheduler-system-design.points
type: qa
step: 6
---
## Q
**任务调度器（定时、周期、带优先级） · 错过触发与重叠策略**｜出自：任务调度器（定时、周期、带优先级） › 整体设计

进程卡了好几个周期，`FixedRate` 怎么处理错过的触发？上一轮没跑完下一轮又到点怎么办？

## A
**错过。** 落后时直接跳到下一个网格点，只补跑一次而不是连跑好几次，叫错过触发的合并（misfire 策略）；不想合并可让 `after` 返回每一个错过的时间点。
**重叠。** 默认不允许同一任务重叠：上一轮没跑完就跳过本轮，防止慢任务把线程池堆满；需要的任务设 `allow_overlap`。
**测试。** `run_pending(now)` 配假时钟同步推进，不依赖睡眠和线程调度。
