---
id: nr-amz-tech-when-service-vs-warehouse
node: amazon.tech
type: qa
step: 8
---
## Q
<p class="title">技术深挖<span class="meta">05 Snowflake · 数据 · AWS</span></p>

什么时候逻辑该放在微服务里，什么时候该放进仓库？

## A
<span class="label">放服务</span> **用户在等结果（毫秒级）、一次处理一条、要调用外部 API、强事务的在线写入（OLTP）。** 例如下单、支付授权。

<span class="label">放仓库</span> **批量、按集合处理、数据已经在仓库、下游是财务 / 分析、可以容忍分钟级延迟。** 例如结算、手续费计算、对账。

<span class="label">判断方法</span> 问三个问题：谁在等结果？数据现在在哪？逻辑能不能写成集合运算？三个答案都指向仓库时，把逻辑留在服务里只是在来回搬数据。

<span class="label">说法</span> *"Latency-sensitive, single-record logic stays in services; set-based logic over data that already lives in the warehouse moves to the warehouse."*

<div class="sources"><b>表达 · business English</b><br>• <b><i>latency-sensitive</i></b> — 对延迟敏感<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Authorization is latency-sensitive, so it stays in the service.”</span><br>• <b><i>move compute to the data</i></b> — 把计算搬到数据旁边<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“We moved compute to the data instead of shipping millions of rows to a service.”</span><br>• <b><i>OLTP vs OLAP</i></b> — 在线事务 vs 分析处理<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Fee calculation looked like OLTP in Ruby but it was really an OLAP-shaped batch job.”</span></div>
