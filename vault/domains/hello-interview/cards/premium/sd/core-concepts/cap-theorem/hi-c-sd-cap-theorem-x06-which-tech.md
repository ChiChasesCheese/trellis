---
id: hi-c-sd-cap-theorem-x06-which-tech
node: sd.core-concepts.cap-theorem.exam
type: qa
step: 6
---
## Q
**CAP 定理 · 说出技术选型的依据**｜考点 · 追问
面试官问："账户转账用 Cassandra 还是 PostgreSQL？"你怎么用 CAP 来论证？

## A
- **先问需求：** 转账不允许丢失或重复，要强一致。
- **PostgreSQL 更合适：** 单主的 ACID 事务天然满足；规模可通过读副本、分片（按账户）扩展，并通过避免跨分片事务来保持强一致。
- **Cassandra 的问题：** 默认偏可用性、最终一致，虽能配置法定人数读写提高一致性，但没有通用的跨分区事务（只有限于单个分区的轻量事务），跨账户转账需要自己做补偿，复杂且易错。
- **不要说：** "NoSQL 就是不一致"。Cassandra 和 DynamoDB 都有可调一致性。要说清楚默认行为和可配置的选项。
