---
id: nr-amz-tech-snowflake-what
node: amazon.tech
type: qa
step: 1
---
## Q
<p class="title">技术深挖<span class="meta">05 Snowflake · 数据 · AWS</span></p>

一句话：Snowflake 是什么、在数据平台里处在哪一层？

## A
<span class="label">要点</span> **云上数据仓库：存储和计算分开。** 数据以列存的 micro-partition 放在对象存储上；计算是按需启停、按秒计费的 virtual warehouse，多个 warehouse 可以读同一份数据而互不抢资源。

<span class="label">位置</span> 在一个数据平台里，它同时占了「存储层 + SQL 计算层」，再往上是建模（dbt）和消费（BI、应用）；往下接摄取（Snowpipe、Kafka connector、批量 COPY）。

<span class="label">能力</span> Time Travel（查历史版本、误删恢复）、zero-copy clone（秒级复制一个库给测试用）、Streams（表的变更追踪）、Tasks（定时或依赖触发的 SQL）、存储过程与 UDF。

<span class="label">说法</span> *"Snowflake is a cloud warehouse that separates storage from compute, so each workload gets its own warehouse over the same data."*

<div class="sources"><b>表达 · business English</b><br>• <b><i>separation of storage and compute</i></b> — 存储与计算分离<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Separation of storage and compute meant our pipeline never fought the analysts for resources.”</span><br>• <b><i>spin up / spin down</i></b> — 按需启停（计算资源）<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“The warehouse only spins up when there is new data to process.”</span><br>• <b><i>zero-copy clone</i></b> — 零拷贝克隆<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Each test run got a zero-copy clone, so integration tests never touched shared data.”</span></div>
