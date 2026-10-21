---
id: nr-amz-s11-full
node: amazon.full
type: qa
step: 11
---
## Q
<p class="title">实习：Kafka 事件流<span class="meta">01 完整故事</span></p>

先在心里把前因后果过一遍，再用英文完整讲一遍。

## A
<span class="label">前因后果</span>

- 背景：2024 年夏天我在费用平台团队实习，负责事件流这一侧。结算交易会把 protobuf 事件发到 Kafka，定价服务批量消费、幂等入账、算出费用，再发费用事件给出款。
- 任务：扩展线上 Kafka 到 Snowflake 的 CDC 路径，另外有两个小件：一个审计日志模块和一个 EOD 校验器。
- 我做了什么（摄取）：把 Kafka Connect sink 扩展到 Snowflake（Snowpipe Streaming）；写了自定义 protobuf converter，遇到坏消息返回 null 记录，这样一条坏消息不会让整个 task 死掉；加了 CDC 过滤，只放行白名单表并丢弃 delete。
- 我做了什么（另两件）：写了 Spring Boot + JPA 的审计日志模块，用动态 criteria 查询；写了 Spark 校验器，用 Airflow 调度，在每天结束时检查定价计划的创建来源。
- 结果与学到：一个夏天交付三件东西。学到两点：at-least-once 加幂等消费者就等于实际上的恰好一次；一条坏消息不能毒死管线，这和我后来在 Amex 管线里用的 record, never drop 是同一个直觉。没有业务数字可报。

<span class="label">英文口述（60–90 秒）</span>

As an intern I worked on the event-streaming side of the fee platform. A settled transaction publishes a protobuf event to Kafka; the pricing service consumes it in batches, books it idempotently, with dedup before insert and a unique constraint as the backstop, computes the fee and publishes a fee event for payouts. My pieces: I extended the Kafka Connect sink into Snowflake with Snowpipe Streaming, a custom protobuf converter that returns a null record on a poison message instead of killing the task, and a CDC filter that whitelists tables and drops deletes. I wrote a Spring Boot and JPA audit-log module with dynamic criteria queries, and Spark validators scheduled by Airflow that check pricing-schedule provenance at end of day. What I took from it: at-least-once delivery plus an idempotent consumer is effectively once, and one bad message must never poison a pipeline.

<div class="sources"><b>表达 · business English</b><br>• <b><i>effectively once</i></b> — 实际效果上的恰好一次<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“At-least-once delivery plus an idempotent consumer gives you effectively once.”</span><br>• <b><i>poison message</i></b> — 毒消息（会反复卡死消费的坏消息）<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“My converter returns a null record on a poison message instead of killing the task.”</span><br>• <b><i>backstop</i></b> — 兜底机制<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The unique constraint is the backstop for concurrent inserts.”</span></div>
