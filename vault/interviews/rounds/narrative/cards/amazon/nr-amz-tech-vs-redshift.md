---
id: nr-amz-tech-vs-redshift
node: amazon.tech
type: qa
step: 5
---
## Q
<p class="title">技术深挖<span class="meta">05 Snowflake · 数据 · AWS</span></p>

Snowflake 和 Redshift 的关键差别是什么？面试官问「为什么不用 Redshift」怎么答？

## A
<span class="label">架构</span> Snowflake 从一开始就是存储计算分离、多个独立 warehouse 并发读同一份数据；**Redshift 传统上是集群（MPP），RA3 和 Serverless 之后才把存储托管出去**，并发靠 concurrency scaling。

Redshift 的优势｜和 AWS 原生集成：IAM、Glue Catalog、Spectrum 直接查 S3、Aurora / DynamoDB 的 zero-ETL、数据不出 AWS 账号。

Snowflake 的优势｜几乎零运维（没有 vacuum、sort key 调优的负担更小）、跨云、按秒启停、Time Travel 和 clone 开箱即用、数据共享（share）。

<span class="label">怎么答</span> **不评价谁更好，讲约束：数据在哪、团队已有什么、运维预算、跨云需求。** *"The data and the finance consumers were already on Snowflake, so the cheapest correct choice was to compute where the data lives."*

<div class="sources"><b>表达 · business English</b><br>• <b><i>data gravity</i></b> — 数据引力：数据在哪，计算就往哪去<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Data gravity decided it: the ledger was already in Snowflake.”</span><br>• <b><i>operational overhead</i></b> — 运维负担<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Snowflake had lower operational overhead for a team our size.”</span><br>• <b><i>it depends on the constraints</i></b> — 取决于约束（避免站队的说法）<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Which one is better depends on the constraints: where the data lives and who consumes it.”</span></div>
