---
id: hl-sd02-alternatives
node: system-design.sd02-job-scheduler
type: qa
step: 30
---
## Q
Redis ZSET、消息队列延迟投递、`ScheduledThreadPoolExecutor`、Quartz 为什么不适合做这个调度器的主方案？

## A
- **数据库轮询**（`SKIP LOCKED`）：适合 Δ 分钟级、规模小；
- **Redis ZSET**（score = fireAt，`ZRANGEBYSCORE` + 原子领取）：适合中等规模、可接受缓存级持久性；持久性 / 复制语义弱于 I1，要自己处理领取丢失；
- **消息队列延迟投递**（SQS delay、RabbitMQ 延迟插件）：适合延迟范围受限（如分钟级）的场景；许多实现有最大延迟上限，且不允许取消 / 查询；
- **`ScheduledThreadPoolExecutor`**：进程内、数量小；不持久、对象多；
- **Quartz / 工作流引擎**：业务级调度、较低速率；吞吐与延迟精度不够。
