---
id: hi-x-timers-scheduling-time-3-choose
node: sd.cross.timers-scheduling-time
type: qa
step: 3
---
## Q
**定时触发、到期查找与时间语义**｜跨题模式 · 怎么选

新题里出现时间相关的需求，怎么判断该用哪种做法？请按需求特征分情况说明，并各举一例。

## A
| 判断信号 | 做法 | 例子 |
|---|---|---|
| 待定任务极多，只有一小撮到期 | 数据库按 (分片, 到期时间) 索引范围扫描，内存堆做精粒度；重试写成更晚的到期 | [[job-scheduler-cron-history\|分布式任务调度器（含 cron 与一年执行历史）]] |
| 单机进程内，要支持优先级 | 两级队列：定时堆只管何时到点，到点后进就绪队列再按优先级排 | [[scheduler-system-design\|设计任务调度器（定时、周期、带优先级）]] |
| 涉及时区、夏令时、日历加减 | 先分清时间点、墙上读数、时区规则、精确时长与日历时长，再选语义 | [[date-time-management\|设计日期时间库（Date and Time Library）]] |
| 周期事项，重跑不能重复产生副作用 | 幂等键包含期次，每个事项自带下一次时间 | [[grocery-subscription-orders\|生鲜订阅转订单服务]] |
| 一串固定周期的日期 | 每期都从起始日出发计算，月末截断 | [[tt-installment-plan\|分期计划生成器]] |
| 时间决定“是否还有意义” | 每条消息带过期时间，在每个环节出队和发送前都再检查 | [[notification-system-scale\|通知系统（支持单发与群发，百万级每秒）]] |
| 超时判负要公平 | 服务端单调时钟，计时器属于单局唯一写者 | [[online-chess-platform\|在线国际象棋平台]] |
