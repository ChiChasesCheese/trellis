---
id: mlp-hm-learn-intern
node: hm.learning
type: qa
step: 2
---
## Q
**一个暑假学会三样新东西**｜经理面与行为面

“What did you do as an intern? How quickly can you pick up a stack you haven't used?”

## A
实习期（2024 年夏天，同一个团队）是你快速上手新技术栈的证据：Kafka、Spring Boot、Spark、Airflow 都是在这个暑假里用上的。

- **事件流：** 已结算交易以 protobuf（一种二进制消息格式）事件发到 Kafka（消息队列）；定价服务用 Spring Kafka 批量消费，幂等入账，算出 Braintree 手续费，再发一个费用事件给出款。
- **你做的：** 扩展了 Kafka 到 Snowflake 的摄取路径：自定义 protobuf 转换器，遇到坏消息返回空记录而不是让任务崩；CDC 过滤器只放行白名单表、丢掉删除事件。写了 Kotlin/Spring Boot 加 JPA 的审计日志模块；写了 Spark 校验器，由 Airflow 排程，每天结束后检查定价计划的来源。
- **并行度：** Kubernetes 上一个 topic 一个 Deployment，并行度是副本数乘以连接器任务数，上限是分区数。
- **边界：** broker 和代理是平台团队的；你的地盘是消费、落库和校验侧；Kubernetes 只有部署形态经验，没有运维过集群。

**英文答法。**
- As an intern on the same team I worked on the **event-streaming side** of the fee platform: a settled transaction publishes a **protobuf event** to Kafka, and the pricing service books it **idempotently**.
- My pieces: a **Kafka Connect** path into Snowflake with a custom converter that returns a **null record on a poison message** instead of killing the task.
- I wrote a **Spring Boot / JPA** audit-log module and **Spark validators scheduled by Airflow**.
- It ran on Kubernetes, one Deployment per topic; parallelism is replicas times connector tasks, **capped by partition count**.

**追问。**
- **Won't a consumer redelivery double-charge?** Kafka is at-least-once, so the consumer dedups before insert, a unique constraint backstops races, and a duplicate-key error is skipped.
- **Did you run Kafka or Kubernetes?** The broker side belonged to the platform team; I owned consume, land and validate, and I know Kubernetes as a deployment shape, not as a cluster operator.
- **Real-time versus batch?** Kafka and Connect move data and compute fees in seconds; Spark and Airflow validate afterwards, daily.
