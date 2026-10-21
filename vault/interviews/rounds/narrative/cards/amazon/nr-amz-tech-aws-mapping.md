---
id: nr-amz-tech-aws-mapping
node: amazon.tech
type: qa
step: 4
---
## Q
<p class="title">技术深挖<span class="meta">05 Snowflake · 数据 · AWS</span></p>

如果在 AWS 上做同样的事：Snowflake 的各个能力分别对应 AWS 的什么服务？

## A
<span class="label">对照表</span> 

| Snowflake | AWS |
|---|---|
| 仓库（存储 + SQL 计算） | **Redshift**（RA3 托管存储 / Serverless），或 S3 + **Athena**（Iceberg 表） |
| Snowpipe / Snowpipe Streaming | **Kinesis Data Firehose**、S3 事件 + **Lambda**、**MSK**（托管 Kafka） |
| Streams（变更追踪） | **DynamoDB Streams**、**DMS** 的 CDC、Aurora 到 Redshift 的 **zero-ETL** |
| Tasks（定时 / 依赖触发） | **EventBridge Scheduler**、**Step Functions**（多步骤带重试） |
| 存储过程 / UDF | **Lambda**、Redshift 存储过程、**Glue**（Spark ETL） |
| Time Travel / clone | S3 版本控制、Aurora Backtrack、快照 |
| 治理 / 权限 | **Lake Formation**、IAM、Glue Data Catalog |

<span class="label">要点</span> **AWS 是一组可组合的积木，Snowflake 是一个把这些积木集成好的产品。** 积木更灵活、可以按成本细调；集成产品更少胶水代码、更少运维。

<span class="label">说法</span> *"On AWS I'd land files in S3, trigger a Step Functions workflow, do the idempotent upsert in Redshift or DynamoDB with a conditional write, and alarm in CloudWatch."*

<div class="sources"><b>表达 · business English</b><br>• <b><i>undifferentiated heavy lifting</i></b> — 没有差异化价值的重复苦活（Amazon 常用语）<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Running our own scheduler was undifferentiated heavy lifting; a managed service removes it.”</span><br>• <b><i>building blocks</i></b> — 可组合的基础组件<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“AWS gives you building blocks; the trade-off is the glue code you own.”</span><br>• <b><i>glue code</i></b> — 把组件粘起来的胶水代码<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Most of the bugs lived in the glue code between services, not in the services.”</span></div>
