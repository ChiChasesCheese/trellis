---
id: nr-amz-tech-data-platform-thinking
node: amazon.tech
type: qa
step: 12
---
## Q
<p class="title">技术深挖<span class="meta">05 Snowflake · 数据 · AWS</span></p>

senior 层面：做数据管线时，比「能跑起来」更深一层要想什么？

## A
<span class="label">数据契约</span> 上游字段改名或类型变化会悄悄毁掉下游：**用 schema 契约和兼容性检查，变更先通知、再发布。**

<span class="label">数据质量即代码</span> 行数、金额合计、空值率、唯一性写成检查，失败就停，不是靠人眼看报表。

新鲜度 SLA｜下游关心「数据最晚几点到」：给每张关键表定新鲜度目标并告警。

<span class="label">回填策略</span> 修了 bug 之后历史数据怎么办：可重放的阶段 + 按日期分区重跑，**金额类用更正分录而不是覆盖**。

<span class="label">血缘与审计</span> 一个数字能追溯到哪个文件、哪次运行；财务数据尤其需要。

<span class="label">成本</span> 按工作负载拆 warehouse、自动挂起、监控贵查询。

<div class="sources"><b>表达 · business English</b><br>• <b><i>data contract</i></b> — 数据契约<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“A data contract would have caught the upstream schema change before it reached fees.”</span><br>• <b><i>freshness SLA</i></b> — 数据新鲜度承诺<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Finance had a freshness SLA of 9 a.m., so we alarmed at 8.”</span><br>• <b><i>lineage</i></b> — 数据血缘<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“With lineage we could trace any fee back to the file and run that produced it.”</span></div>
