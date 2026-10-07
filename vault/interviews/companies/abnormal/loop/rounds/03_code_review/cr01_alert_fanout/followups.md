# followups · 第二部分：扩展 + 规模

原话（#8496901）：要讨论 Concurrency · Parallelism · Worker scaling · Message queue scaling · Throughput · Bottlenecks · Failure scenarios，并且 "be prepared to go beyond 'add more workers' or 'use a queue.'" 下面每题：中文要点 + 英文口播。数字由 `python3 -c` 算过，换成你自己的假设也要现场算。

## F1 吞吐估算：现在的 worker 够吗？

- 假设：高危告警峰值 2,000 条/分钟 = 33.3/s；平均每租户 2.5 个渠道 → **83.3 次发送/s**。
- webhook 延迟：95% 为 300 ms，5% 慢到超时 5 s → 平均 0.535 s/次。
- Little 定律：并发 = 速率 × 延迟 = 83.3 × 0.535 ≈ **45 个并发发送**；默认 `concurrency=8` 只能撑 8/0.535 ≈ **15 次/s**，差 5.5 倍。
- 还有批次栅栏：`run_once` 等整批结束才再 `receive`，批里最慢的一条（5 s 超时）决定下一批何时开始，实际吞吐更低。
> "Back of the envelope: 2,000 alerts a minute is about 33 a second, times 2.5 channels is 83 sends a second. With a mean send time of half a second, Little's law says I need about 45 in flight, and the default of 8 threads gives me about 15 per second. So I'd raise concurrency and stop waiting on a whole batch before fetching the next."

## F2 worker 扩容的上限在哪

- 下游限流：客户 endpoint 和 Slack/SMTP 有各自限速；加 worker 只会更快触发 429。
- 连接数：每个 worker 进程占 DB 连接（配置查询）与出站连接；Postgres `max_connections` 是硬顶，要连接池/缓存。
- 队列并行度：SQS 标准队列无分区上限；Kafka 则是 **consumer 数 ≤ partition 数**。
- 单进程内 GIL：发送是 IO 密集，线程够用；CPU 密集（签名、渲染）才需要多进程。
> "Adding workers moves the bottleneck rather than removing it: the next limits are the customers' own rate limits, our database connections for config lookups, and, if this were Kafka, the partition count. So I'd size from the slowest dependency, not from the queue depth."

## F3 租户隔离：一个坏 endpoint 拖垮所有人（舱壁）

- 现状：所有租户共用 8 个线程。某租户 endpoint 黑洞，100 条/分钟 × 5 s 超时 = 8.3 次/s × 5 s ≈ **42 个线程被占住**，8 线程池瞬间耗尽。
- 对策：按租户（或按 endpoint 主机）限制并发的 **bulkhead**（信号量），超过就把消息 `change_visibility` 推后；对持续失败的 endpoint 做**熔断**（circuit breaker）暂停一段时间；按租户限速。
> "I'd put a per-tenant concurrency cap in front of the pool, so one dead endpoint can only ever hold its own few threads, and add a circuit breaker so we stop hammering an endpoint that has been failing for minutes."

## F4 队列扩容：分片、顺序、可见性超时

- 是否需要顺序？告警通知基本不需要全局顺序；需要的话只需"同一 alert 的更新"有序 → 按 `tenant_id:alert_id` 做分区键（Kafka）/ FIFO 的 MessageGroupId。
- 热点租户：按 tenant 分区会让大租户成为热分区；折中是 `hash(tenant, alert_id) mod N`。
- **visibility timeout 必须大于最坏处理时间**：本方案每渠道最坏 3 次 × 5 s 超时 + 退避 ≈ 15.6 s，3 个渠道串行 ≈ 47 s > 30 s，会在处理中途被重投 → 重复。解法：缩短单渠道时限 / 并行发送各渠道 / 长任务定期 `change_visibility`（心跳）。
> "Ordering only matters per alert, so I'd partition by tenant and alert id rather than globally. And the visibility timeout has to exceed the worst-case processing time, which here is about 47 seconds with three slow channels, so either I shorten the timeouts, send channels in parallel, or heartbeat the visibility."

## F5 DLQ 与毒消息

- 毒消息 = 反复失败的消息（畸形、永久 4xx、触发 bug）。`receive_count >= max_receives` 进 DLQ，保留原文 + 原因 + 次数。
- 区分**可重试**（超时、5xx、429）与**不可重试**（400/401/404、畸形）：后者直接 DLQ，不浪费重试。
- DLQ 要有告警（深度 > 0）与重放工具（redrive），否则只是换了个地方丢。
> "Poison messages go to a DLQ after a bounded number of receives, with the reason attached. I'd classify errors so a 400 or a malformed body goes straight there, and I'd alert on DLQ depth and ship a redrive tool, otherwise the DLQ is just a quieter way to lose alerts."

## F6 幂等键与"恰好一次"

- 队列是至少一次；"恰好一次"只能是**至少一次 + 幂等**。键 = `tenant : rule : alert_id : channel : target`。
- 进程内 `DedupCache` 在多实例/重启后失效 → 需要共享存储：Redis `SET key NX EX ttl`（claim 语义）或 Postgres 唯一约束；失败要释放 claim。
- 对 webhook：把幂等键放进请求头（`Idempotency-Key`），让客户端也能去重；这是我们能保证的上限。
> "Delivery is at least once, so the honest goal is idempotency. I'd claim a key per tenant, alert and channel with an atomic set-if-absent in Redis with a TTL, release it on failure, and send the same key to the customer as an Idempotency-Key header so they can dedupe too."

## F7 背压（backpressure）

- 症状：队列深度和最老消息年龄上升。不要无限接收：只在有空闲 worker 时才 `receive`（拉取式天然背压）；批大小与线程数匹配。
- 过载时的取舍：按严重度优先（critical 先发，info 延后）；对过期告警（>15 min）直接丢弃并计数，因为通知旧告警没有价值；对生产者端限流或合并（同一用户的 N 条告警合并成一条摘要）。
> "I'd keep it pull-based so we only take what we can process, prioritise by severity, drop or coalesce notifications that are already stale, and make the producer side aware via queue-age alerts rather than letting the queue grow unbounded."

## F8 失败场景清单

- 下游宕机：重试 + 退避 + 熔断；消息留在队列，visibility 退避，恢复后自然追平。
- 重复投递：dedup claim（F6）。
- 部分失败（email 成功、webhook 失败）：按渠道 claim，重投只补发失败的。
- worker 重启/崩溃：ack 在成功之后（CR-01）；可见性过期后重投。
- 配置库宕机：不要把"查不到配置"当成"没有渠道"而 ack；应当失败并重投。
- 时钟/时区、超大 payload、租户 id 异常：参数化 SQL、校验输入。
> "For each failure I try to answer two questions: what state is the message in afterwards, and who finds out. If the answer to the second is nobody, it needs a metric or an alert."

## F9 观测

- 指标：队列深度（visible / in-flight）、**最老消息年龄**（age of oldest message，比深度更接近用户感受）、发送成功率/延迟分渠道分租户、重试次数、DLQ 深度、去重命中率、线程池占用。
- SLO 例：99% 的 critical 告警在 60 s 内通知出去；告警：最老消息年龄 > 5 min、DLQ 深度 > 0、某租户失败率 > 50%。
- 日志：结构化，带 tenant / alert / channel / attempt；**绝不**打 secret（CR-07）。
> "I'd alert on the age of the oldest message rather than raw depth, because that's what the customer feels, plus DLQ depth and per-tenant failure rate, with an SLO like 99% of critical alerts notified within 60 seconds."

## F10（加分）不是"加 worker"也不是"上队列"

> "More workers and a queue are the obvious answers; the interesting levers are limiting blast radius per tenant, making delivery idempotent so retries are safe, and shaping the load: dropping stale alerts, coalescing noisy users and prioritising by severity. Those change the system's behaviour under stress, rather than just its capacity."
