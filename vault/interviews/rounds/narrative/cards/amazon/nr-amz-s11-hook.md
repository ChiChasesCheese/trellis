---
id: nr-amz-s11-hook
node: amazon.s11
type: qa
step: 1
---
## Q
【实习期：Kafka 事件流 · Spring · Spark（广度补充）】开场第一句是什么？适用哪些 LP？要报哪些数字？

## A
**As an intern I extended the Kafka-to-Snowflake event path, and I made sure one bad message could never poison the pipeline.**

**适用 LP**

- 主：无（技术广度故事，不作 LP 主力；被追问技术背景时用）
- 副：Learn and Be Curious、Dive Deep、Insist on the Highest Standards、Deliver Results
- 被问 "tell me about your Kafka experience" 时转到生产：Gateway 事件 → Kafka → Snowpipe Streaming → Stream/Task，Funding → Snowflake 的 CDC

**数字**

- 无业务数字，别编
- **三个交付物**：CDC 摄取管线扩展；Kotlin/Spring Boot + JPA 合规审计日志模块；Spark + Airflow EOD 合规校验器
- 实习：2024 年 5–8 月
- 并行度 = replicas × `tasks.max`，上限 = partition 数；一 topic 一 Deployment
- 【待补：实习项目的量化结果（处理的事件量、校验器发现过几个问题、审计日志被谁用）；无就不要编】
