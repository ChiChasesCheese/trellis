# sd02 · 参考答案（数字由 `python3 -c` 计算）

## 1. 先算

| 量 | 值 |
|---|---|
| 在途请求（Little：λ × W = 5,000/s × 0.2 s） | **1,000** |
| 每 worker 20 个线程在途 → worker 数 | **50**（或 asyncio：单进程上千在途，CPU 很少） |
| 大租户流量（40%） | **2,000/s**，而它的端点限流 **50/s** |
| 该租户积压增长 | **1,950/s** → 10 分钟 ≈ **117 万**条 |

> "Adding workers doesn't help the biggest customer at all — their endpoint accepts 50 a second and we're producing 2,000. More workers just means more 429s, faster. The bottleneck is the downstream, so the design has to be about isolation and shaping, not raw parallelism."

## 2. 改什么

1. **隔离**：按 (tenant, endpoint) 分子队列（或 Kafka 按该键分区 + 每 key 的令牌桶）；每个端点一个限流器（读取并尊重 `Retry-After`），一个慢/宕机的端点只堆积它自己的队列，不占全局 worker（消除 head-of-line blocking）。
2. **整形**：大租户超限时**合并**——同一 alert 的多次更新只发最新；低严重度批量成摘要（每分钟一条）。和客户约定批量 webhook 格式。
3. **I/O 模型**：线程池 → asyncio/httpx 连接池（每主机连接上限），1,000 在途只需几个进程；worker 数按"在途需求 / 每进程在途上限"扩，不按 CPU。
4. **优先级**：high severity 单独队列与预留并发，保证 p99 < 1 min；low 可延迟。
5. **可靠性**：at-least-once + 幂等键（`alert_id:version`，放在 header，客户据此去重）；可见性超时 > p99 处理时间；指数退避 + 抖动，上限后入 DLQ（按租户），可重放；熔断：连续失败 N 次 → 打开，定期探测。
6. **顺序**：同一 alert 的更新进同一 key、串行发送；或带单调 `version`，客户丢弃旧版本（更简单、可并行）。

## 3. 失败场景演练

- 端点宕机 3 小时：熔断打开 → 该租户队列积压（有上限，超出后只保留每个 alert 的最新版本）→ 恢复后按限流速率回放，先 high 后 low。
- worker 崩溃中途：消息可见性超时后重投；幂等键避免客户侧重复。
- 毒消息（payload 让序列化崩溃）：重试 N 次 → DLQ + 告警，不阻塞队列。
- 队列本身成瓶颈（SQS 每队列吞吐、Kafka 分区数）：分区数 ≥ 峰值并行 key 数的需要；提前多开分区。

## 4. 观测

每 (tenant, endpoint) 积压深度与最老消息年龄 · 429 / 5xx 率 · 熔断状态 · 端到端延迟（alert 创建 → 投递成功）p99 按严重度 · DLQ 深度。
