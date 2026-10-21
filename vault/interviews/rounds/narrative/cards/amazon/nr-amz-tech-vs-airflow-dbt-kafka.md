---
id: nr-amz-tech-vs-airflow-dbt-kafka
node: amazon.tech
type: qa
step: 3
---
## Q
<p class="title">技术深挖<span class="meta">05 Snowflake · 数据 · AWS</span></p>

Snowflake 和 Airflow、dbt、Kafka 分别是什么关系？

## A
<span class="label">分层</span> **Kafka 是搬运（事件总线），Airflow 是编排（谁先谁后、失败重试），dbt 是建模（SQL 转换的工程化：版本、测试、依赖），Snowflake 是引擎和存储。** 它们不是互相替代，而是叠在一起。

Streams + Tasks｜相当于把「轻量编排 + 增量处理」放进仓库内部：Stream 记住处理到哪，Task 按时间或上游完成来触发。好处是少一个系统、数据不出仓库；代价是编排能力弱于 Airflow（可视化、跨系统依赖、回填工具都更少）。

Kafka 在哪｜上游业务系统把事件写进 Kafka，再由 connector / Snowpipe Streaming 落进 Snowflake。**Kafka 管「实时、多消费者」，Snowflake 管「落地后的分析与对账」。**

<span class="label">说法</span> *"Streams and Tasks gave us orchestration inside the warehouse; the trade-off was weaker tooling than Airflow, which we covered with monitoring."*

<div class="sources"><b>表达 · business English</b><br>• <b><i>fewer moving parts</i></b> — 组件更少、出错点更少<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Keeping orchestration in the warehouse meant fewer moving parts to page someone at 3 a.m.”</span><br>• <b><i>orchestration layer</i></b> — 编排层<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Airflow is the orchestration layer; it shouldn&#x27;t hold business logic.”</span><br>• <b><i>event backbone</i></b> — 事件主干（总线）<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Kafka is the event backbone; Snowflake is where the events land for reconciliation.”</span></div>
