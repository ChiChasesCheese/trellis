# sd01 · 追问（中文要点 + 英文口播）

1. **"Why not just shard Postgres?"** — 能撑写，但原始事件本质是 append-only、按时间查、量级 TB/天，是日志/分析型负载，OLTP 分片后仍要为每事件一次随机读付费。→ "Sharding buys write throughput, but we'd still be paying a random read per event and storing an append-only log in an OLTP database. The right fix is to stop asking the database per event."
2. **"How do you keep impossible-travel correct if events arrive out of order?"** — 按事件时间而非处理时间；每 key 小的乱序缓冲（watermark，如 2 min）；迟到事件重新评估并允许更新告警（幂等 upsert）。
3. **"What happens when the big tenant triples overnight?"** — 入口配额 + 独立 topic/consumer group；热 key 预聚合；扩分区需要新 topic 迁移，所以开始就多开。
4. **"How would you test this before cutover?"** — 影子管线 + 告警差异报告（按规则、按租户），回放一周的真实流量；"Make every PR prove itself"：附 lag 图与差异数字。
5. **"Exactly-once?"** — 不追求端到端 exactly-once；at-least-once + 幂等告警键。说清楚"重复事件只会增加 event_count，不会多一条告警"。
6. **"Where would you use DynamoDB instead of Redis for state?"** — 需要持久、按 key 读写、规模大且不想管快照时用 DynamoDB（按 (tenant,user) 分区键）；代价是每次网络往返——所以仍然在 consumer 内存做热缓存，DynamoDB 做持久层。注意热分区（同一 partition key 的吞吐上限）。
7. **"What metrics would you put on the dashboard?"** — 每 partition lag、最老未处理消息年龄、事件→告警 p99、每租户入口速率、告警速率与去重率、DLQ 深度、OpenSearch 索引延迟。
