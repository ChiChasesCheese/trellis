# sd02 · 追问

1. **"Why not just autoscale on CPU?"** — worker 是 I/O-bound，CPU 低但在途满；按队列积压/最老消息年龄扩缩，并受下游限流封顶。
2. **"Kafka or SQS?"** — SQS：每条消息独立可见性、DLQ 原生、无分区上限的运维，适合每租户队列（但每租户一个队列管理成本高 → 用 FIFO 的 message group id 按 tenant 隔离）；Kafka：按 key 有序、可重放，但一个慢 key 会阻塞其分区（需要把慢 key 移到重试 topic）。
3. **"How do you stop one customer's outage from paging us?"** — 熔断 + 按租户告警阈值；对客户发"endpoint failing"通知，不是我们 on-call。
4. **"Exactly once?"** — 跨 HTTP 不可能；at-least-once + 幂等键，文档化给客户。
5. **"What's the next bottleneck after you fix the downstream?"** — 出口连接数/NAT 端口、TLS 握手（连接复用）、序列化与签名 CPU、状态存储（去重表）的写入。
