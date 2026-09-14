---
id: reliability-red-vs-use
node: reliability.observability
type: qa
---
## Q
RED method vs USE method: what does each one measure, and which do you apply to a payment service vs a database host?

## A
- **RED** — for every *request-driven service*: **R**ate (req/s), **E**rrors (failed req/s), **D**uration (latency distribution). This is the user's view; the payment service gets RED dashboards, and RED metrics feed SLIs.
- **USE** — for every *resource* (CPU, memory, disk I/O, connection pool, GPU): **U**tilization (% busy), **S**aturation (queue depth / wait), **E**rrors. This is the capacity view; the database host gets USE.

Key discrimination: **saturation, not utilization, predicts trouble** — a resource can be 70% utilized with a growing queue. Standard practice: RED to detect user impact, USE to explain it.

## Q zh
RED 方法 vs USE 方法：每个测量什么，对支付服务 vs 数据库主机应用哪个？

## A zh
- **RED** ——对于每个*请求驱动服务*：**R**ate（req/s）、**E**rrors（failed req/s）、**D**uration（延迟分布）。这是用户的视图；支付服务获得 RED 仪表盘，RED 指标馈送 SLI。
- **USE** ——对于每个*资源*（CPU、内存、磁盘 I/O、连接池、GPU）：**U**tilization（% busy）、**S**aturation（队列深度 / 等待）、**E**rrors。这是容量视图；数据库主机获得 USE。

关键区别：**饱和，不是使用，预测问题** ——资源可以 70% 使用且队列增长。标准做法：RED 检测用户影响，USE 解释它。
