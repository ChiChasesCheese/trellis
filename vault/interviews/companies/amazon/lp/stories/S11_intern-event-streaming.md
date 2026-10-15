# S11 · 实习期：Kafka 事件流 · Spring · Spark（广度补充）

> 来源：`core/stories/S11 实习期事件流.md`（status: **partial**）。**证据偏薄：这是技术广度故事，不是 LP 主力。** 作为 Learn and Be Curious / Dive Deep 的侧证，或当 LP 追问技术背景时使用。
> 主 LP：无（P=0）；副：Learn and Be Curious · Dive Deep · Insist on the Highest Standards · Deliver Results。
> 简历对应：PayPal 实习（Chicago, May–Aug 2024）三条 bullet：Kotlin/Spring Boot B2B 费用服务；Kafka 事件处理（Kafka proxies in Kubernetes）；Airflow DAG + Spark 校验。

## 1. 数字

没有可口播的业务数字。可数的事实：
- Kafka Connect 部署形态：一 topic 一 Deployment，并行度 = replicas × `tasks.max`，上限 = partition 数。
- 三个交付物：CDC 摄取管线扩展；Kotlin/Spring Boot + JPA 合规审计日志模块；Spark + Airflow EOD 合规校验器。
- 【待 Chi 补：实习项目的量化结果（处理的事件量、校验器发现过几个问题、审计日志被谁用）；无就不要编】

## 2. 60–90 秒口播版（≈ 170 词）

> As an intern I worked on the event-streaming side of the fee platform. A settled transaction publishes a protobuf event to Kafka; the pricing service consumes it in batches, books it idempotently — dedup before insert, unique constraint as the backstop — computes the fee and publishes a fee event for payouts.
>
> My pieces: I extended the Kafka Connect sink into Snowflake — Snowpipe Streaming, a custom protobuf converter that returns a null record on a poison message instead of killing the task, and a CDC filter that whitelists tables and drops deletes. I wrote a Spring Boot and JPA audit-log module with dynamic criteria queries, and Spark validators scheduled by Airflow that check pricing-schedule provenance at end of day.
>
> What I took from it: at-least-once delivery plus an idempotent consumer is effectively once, and one bad message must never poison a pipeline. That's the same instinct as the "record, never drop" rule in the Amex pipeline I built later.

## 3. 2 分钟版

在 60–90 秒版基础上加 **Learn and Be Curious** 角度（≈ 260 词）：

> The task was to extend a live CDC path from Kafka into Snowflake. 【待 Chi 补：入职时你对 Kafka Connect / Snowpipe Streaming 的起点是什么、怎么学的——源笔记没写，不要编；这一句决定它能不能算 Learn and Be Curious】 The decision I'd highlight: a malformed protobuf message used to be able to kill a task; I made the converter return a null record and surface it, so one bad message can't block the stream. For the CDC filter, a JSONPath whitelist on kind keeps upserts and drops deletes, because the warehouse tables should only follow inserts and updates. Consumers and connectors run on Kubernetes, one deployment per topic; parallelism is replicas times tasks, capped by partitions, so if throughput is short the first thing I check is partition count.
>
> The consumer side: Kafka is at-least-once, so redelivery happens. The pricing service dedups a batch before insert, relies on a unique constraint for concurrent races, catches the integrity violation to skip duplicates, and uses a batch-listener failure to re-deliver exactly the failed record.
>
> 【待 Chi 补：你在这个实习里"主动学新东西然后用上"的一个具体瞬间（例如第一次读懂 Connect 配置后怎么验证）；用于 Learn and Be Curious 的 senior 版】

## 4. 适用 LP 与改角度

| LP | 开场一句 | 重点讲 | 避免 |
|---|---|---|---|
| **Learn and Be Curious** (S) | 【待 Chi 补：起点与学习路径后才能写开场句】 | 坏消息返回 NULL 的 converter；并行度模型 | 声称运维过 Kafka 集群/K8s（只有部署形态经验） |
| **Dive Deep** (S) | "Parallelism is replicas times tasks, capped by partitions." | 并行度的上限；幂等的三道防线 | — |
| **Insist on the Highest Standards** (S) | "One bad message must not poison the pipeline." | poison-message 处理 | — |
| **Deliver Results** (S) | "Three deliverables in one summer internship." | CDC 扩展、审计日志、Spark 校验 | 无数字，别编；实习期长度见简历 May–Aug 2024 |

## 5. 追问（≥5）

1. **How do you not double-charge / not miss fees?** → at-least-once + 消费侧幂等：落库前批量去重、唯一约束兜并发、catch `DataIntegrityViolationException` 跳过、`BatchListenerFailedException` 精确重投失败那条。
2. **How does Connect scale?** → replicas × `tasks.max`，上限被 partition 数卡住。
3. **What's the Kafka proxy?** → 放在 broker 前做 SASL SCRAM + 双向 TLS 的代理，凭据走 vault；不是出网代理。**broker / proxy 是平台团队的；我的地盘是消费/落库/校验侧。**
4. **Proto → table?** → 自定义 converter → JSON → Snowflake schematization 自动展开；坏消息返回 NULL。
5. **Real-time vs batch?** → 实时（Kafka + Connect，秒级）搬数据、算费用；批（Spark + Airflow，天级）事后校验。
6. **What if a consumer crashes?** → 自动提交 + 短间隔更偏 at-most-once；真正防丢靠上游重试 + 对账/健康检查。
7. **What did the Spark validators check?** → pricing schedule 创建来源、settlement 数据合规，结果推 Slack。

## 6. Senior 升级点（bar = senior）

当前档位：**intern-level 广度**——只作 **技术背景**。不要在 LP 轮次作为主故事讲。
- 若被问到 "tell me about your Kafka experience"，转到 **生产**：Gateway 事件 → Kafka → Snowpipe Streaming → Stream/Task，Funding → Snowflake 的 CDC（S11 笔记明确建议）。
- 【待 Chi 补：实习成果在转正后是否仍被使用（"my intern code is still running"是 Ownership/Deliver 的好句）】
