---
id: nr-amz-tech-same-problems
node: amazon.tech
type: qa
step: 7
---
## Q
<p class="title">技术深挖<span class="meta">05 Snowflake · 数据 · AWS</span></p>

殊途同归：两边都必须解决哪些问题？各自怎么解决？

## A
<span class="label">共同问题</span> 幂等、顺序、重放 / 回填、可观测、模式演进、测试、发布回滚。

<span class="label">幂等</span> 服务：请求带幂等键、数据库唯一约束；仓库：复合键 `MERGE`、按批次 id 去重。

<span class="label">顺序与重放</span> 服务：分区内有序的消息队列、按 offset 重放；仓库：Stream 的 offset、Time Travel 回到某个时间点重跑。

<span class="label">可观测</span> 服务：指标、日志、链路追踪、告警；仓库：任务历史、行数 / 金额对账、新鲜度告警（我们用 Streamlit 看板 + Datadog）。

<span class="label">测试与发布</span> 服务：单元测试 + CI + 灰度；仓库：zero-copy clone 上跑集成测试、版本化迁移（Flyway / schemachange）、feature flag 一键停。

<span class="label">结论</span> **工具不同，工程纪律一样：可重放、可对账、可回滚。**

<div class="sources"><b>表达 · business English</b><br>• <b><i>replayable</i></b> — 可重放<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Because every stage was replayable, a bad file was a re-run, not an incident.”</span><br>• <b><i>reconcile against the source of truth</i></b> — 对照权威数据源对账<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“We reconciled fee totals against Amex&#x27;s summary records every run.”</span><br>• <b><i>roll back / roll forward</i></b> — 回滚 / 往前修<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“For money data we roll forward with correcting entries rather than roll back.”</span></div>
