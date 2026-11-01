---
id: hi-x-injected-clock-testability-3-choose
node: lld.cross.injected-clock-testability
type: qa
step: 3
---
## Q
**时间注入与可测试性**｜跨题模式 · 怎么选

写一个依赖时间的类时，怎么决定用哪种时钟、怎么注入、怎么测？请按时间在逻辑里扮演的角色分情况说明，并各举一例。

## A
| 时间扮演的角色 | 做法 | 例子 |
|---|---|---|
| 度量“过了多久”（令牌补充、窗口、冷却） | 注入单调时钟；补充量用 max(0, …) 防回拨；假时钟拨动验证边界 | [[rate-limiter-system\|限流器（单机类设计）]]、[[tt-per-merchant-rate-limit\|按商户限流]] |
| 状态转换由时间触发（冷却到期转半开） | 时钟注入，测四条转换；并发测试另做，用多线程抢同一个探测名额 | [[api-circuit-breaker\|熔断器（Circuit Breaker）]] |
| 绝对时刻（某天几点触发） | 触发规则接收 now 参数，下一次由规则算出；计时线程另给同步推进入口 | [[scheduler-system-design\|设计任务调度器（定时、周期、带优先级）]] |
| 日历、时区、夏令时 | 时间点、墙上读数、时区规则、Duration 与 Period 分开，让调用方能明确给出输入 | [[date-time-management\|设计日期时间库（Date and Time Library）]] |
| 时序是产品行为（防抖、冷却） | 用事件序列回放，断言每个穿越最多通知一次 | [[stock-price-alerts\|股票价格提醒系统]] |
