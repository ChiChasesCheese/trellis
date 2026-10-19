# 实习期：Kafka 事件流 · Spring · Spark（广度补充）

**As an intern I extended the Kafka-to-Snowflake event path, and I made sure one bad message could never poison the pipeline.**

## 适用 LP

- 主：无（技术广度故事，不作 LP 主力；被追问技术背景时用）
- 副：Learn and Be Curious、Dive Deep、Insist on the Highest Standards、Deliver Results
- 被问 "tell me about your Kafka experience" 时转到生产：Gateway 事件 → Kafka → Snowpipe Streaming → Stream/Task，Funding → Snowflake 的 CDC

## 数字

- 无业务数字，别编
- **三个交付物**：CDC 摄取管线扩展；Kotlin/Spring Boot + JPA 合规审计日志模块；Spark + Airflow EOD 合规校验器
- 实习：2024 年 5–8 月
- 并行度 = replicas × `tasks.max`，上限 = partition 数；一 topic 一 Deployment
- 【待补：实习项目的量化结果（处理的事件量、校验器发现过几个问题、审计日志被谁用）；无就不要编】

## S / T / A / R / L

### S
- **2024** 年夏天实习，费用平台团队的事件流一侧
- 结算交易发布 **protobuf 事件到 Kafka**；定价服务**幂等**入账并发布费用事件

### T
- 扩展线上 **Kafka → Snowflake 的 CDC 路径**
- 另有两个小件：**审计日志模块**和 **EOD 校验器**

### A
- 把 **Kafka Connect sink** 扩展到 Snowflake（**Snowpipe Streaming**）
- 写**自定义 protobuf converter**：遇到坏消息返回 **null 记录**，不让 task 死掉
- 加 **CDC 过滤**：表白名单，**丢弃 delete**
- 写 **Spring Boot + JPA 审计日志模块**，动态 criteria 查询
- 写 **Spark 校验器**，**Airflow** 调度，EOD 检查定价计划来源

### R
- 一个夏天**三个交付物**：CDC 扩展、审计日志、Spark 校验器
- 无业务数字

### L
- **At-least-once + 幂等消费者** = 实际上的恰好一次
- **一条坏消息不能毒死管线**；和后来 Amex 管线的 "record, never drop" 是同一直觉

## 追问与回答

- **How do you not double-charge / not miss fees?**
  - **At-least-once + 消费者幂等**；**批内先去重再插入**；**唯一约束**兜底竞态
  - 捕获 **`DataIntegrityViolationException`** 跳过；**`BatchListenerFailedException`** 精确重投失败那条
- **How does Connect scale?**
  - **replicas × `tasks.max`**，上限 **partition 数**；吞吐不够先看 partition 数
- **What's the Kafka proxy?**
  - broker 前面的代理：**SASL SCRAM + 双向 TLS**，凭据走 **vault**；不是 egress proxy
  - broker/proxy 归平台团队；我做的是**消费 / 落地 / 校验**
- **Proto → table?**
  - **自定义 converter → JSON → Snowflake schematization** 展开列；坏消息返回 **NULL**
- **Real-time vs batch?**
  - **实时**（Kafka + Connect，秒级）搬数据、算费用；**批**（Spark + Airflow，每日）事后校验
- **What if a consumer crashes?**
  - 短间隔 auto-commit 偏 **at-most-once**；真正的保护是**上游重试 + 对账 / 健康检查**
- **What did the Spark validators check?**
  - **定价计划创建来源**和**结算数据合规**；结果发 **Slack**

## 换个 LP 讲

- **Learn and Be Curious**：坏消息返回 NULL 的 converter、并行度模型；别声称运维过 Kafka 集群 / K8s，只有部署形态经验
- **Dive Deep**："Parallelism is replicas times tasks, capped by partitions."；幂等的三道防线
- **Insist on the Highest Standards**："One bad message must not poison the pipeline."：poison-message 处理
- **Deliver Results**："Three deliverables in one summer internship."：CDC 扩展、审计日志、Spark 校验；无数字别编

## 待补

- 【待补：入职时你对 Kafka Connect / Snowpipe Streaming 的起点是什么、怎么学的，决定它能不能算 Learn and Be Curious；不要编】
- 【待补：实习里「主动学新东西然后用上」的一个具体瞬间（比如第一次读懂 Connect 配置后怎么验证）】
- 【待补：实习成果在转正后是否仍被使用（"my intern code is still running"）】
- 【待补：What I'd do differently】

<details><summary>逐字稿</summary>

> As an intern I worked on the event-streaming side of the fee platform. A settled transaction publishes a protobuf event to Kafka; the pricing service consumes it in batches, books it idempotently — dedup before insert, unique constraint as the backstop — computes the fee and publishes a fee event for payouts.
>
> My pieces: I extended the Kafka Connect sink into Snowflake — Snowpipe Streaming, a custom protobuf converter that returns a null record on a poison message instead of killing the task, and a CDC filter that whitelists tables and drops deletes. I wrote a Spring Boot and JPA audit-log module with dynamic criteria queries, and Spark validators scheduled by Airflow that check pricing-schedule provenance at end of day.
>
> What I took from it: at-least-once delivery plus an idempotent consumer is effectively once, and one bad message must never poison a pipeline. That's the same instinct as the "record, never drop" rule in the Amex pipeline I built later.

</details>
