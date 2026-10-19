---
id: nr-amz-s11-hook
node: amazon.outline
type: qa
step: 31
---
## Q
<p class="title">实习：Kafka 事件流<span class="meta">02 提纲</span></p>

开场第一句是什么？适用哪些 LP？要报哪些数字？

## A
<span class="label">开场</span>

**As an intern I extended the Kafka-to-Snowflake event path, and I made sure one bad message could never poison the pipeline.**

<span class="label">适用 LP</span>

- 主：无（技术广度故事，不作 LP 主力；被追问技术背景时用）
- 副：Learn and Be Curious、Dive Deep、Insist on the Highest Standards、Deliver Results
- 被问 "tell me about your Kafka experience" 时转到生产：Gateway 事件 → Kafka → Snowpipe Streaming → Stream/Task，Funding → Snowflake 的 CDC

<span class="label">数字</span>

- 无业务数字，别编
- **三个交付物**：CDC 摄取管线扩展；Kotlin/Spring Boot + JPA 合规审计日志模块；Spark + Airflow EOD 合规校验器
- 实习：2024 年 5–8 月
- 并行度 = replicas × `tasks.max`，上限 = partition 数；一 topic 一 Deployment
- 【待补：实习项目的量化结果（处理的事件量、校验器发现过几个问题、审计日志被谁用）；无就不要编】

<div class="sources"><b>表达 · business English</b><br>• <b><i>deliverable</i></b> — 交付物<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I shipped three deliverables in one summer.”</span><br>• <b><i>end to end</i></b> — 端到端<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I touched the path end to end, from the Kafka event to the Snowflake table.”</span><br>• <b><i>breadth</i></b> — 技术广度<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“This story is about breadth: streaming, a Spring service and batch validation.”</span></div>
