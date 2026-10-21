---
id: nr-amz-tech-all-sde-data
node: amazon.tech
type: qa
step: 6
---
## Q
<p class="title">技术深挖<span class="meta">05 Snowflake · 数据 · AWS</span></p>

为什么说「所有 SDE 都在玩数据」？Snowflake 的 Stream / Task / 存储过程和 Spring Boot 微服务怎么一一对应？

## A
<span class="label">领悟</span> **后端服务本质上是「读状态 → 按规则改状态 → 写回」的状态机；数据管线也是。** 区别只在状态放在哪、触发方式是什么。

<span class="label">对应</span> 

| Snowflake | Spring Boot 微服务 |
|---|---|
| Stream（记住处理到哪个变更） | Kafka consumer offset、outbox 表 + CDC |
| Task（定时 / 上游完成触发） | `@Scheduled` / Quartz、消息驱动的 worker |
| 存储过程 | service 方法（transaction script） |
| `MERGE` 用复合键 | 幂等 upsert、去重键 |
| 事务里消费 Stream | `@Transactional` + 提交 offset |
| 错误日志表 | 死信队列（DLQ） |
| feature flag 表当 kill switch | 配置中心 + 功能开关 |

<span class="label">说法</span> *"Whether it's a Spring service or a Snowflake task, I'm solving the same problems: idempotency, ordering, replay and observability."*

<div class="sources"><b>表达 · business English</b><br>• <b><i>state machine</i></b> — 状态机<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Every service I&#x27;ve built is a state machine over data; only the runtime changes.”</span><br>• <b><i>idempotent by construction</i></b> — 从设计上就幂等<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The composite-key MERGE made every stage idempotent by construction.”</span><br>• <b><i>dead-letter queue</i></b> — 死信队列<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Our error-log table played the role of a dead-letter queue.”</span></div>
