---
id: nr-amz-tech-migration-costs
node: amazon.tech
type: qa
step: 10
---
## Q
<p class="title">技术深挖<span class="meta">05 Snowflake · 数据 · AWS</span></p>

迁到 Snowflake 的代价是什么？你怎么补？

## A
<span class="label">代价</span> **编排工具弱**（没有 Airflow 那样的回填和可视化）；**可观测性要自己补**；SQL 逻辑的单元测试和代码复用比 Kotlin 难；存储过程的版本管理和发布要额外纪律；**厂商锁定**；查询写得差会在账单上直接体现。

你的补法（管线里真做过的）｜Streamlit 监控看板 + Datadog 告警；每个阶段复合键 `MERGE` 保证可重放；校验函数把不一致写进错误日志而不是丢掉；一个 feature flag 同时当 kill switch，一条 `UPDATE` 就能停，不用发版；费用总额对 Amex 汇总记录对账，不一致就停 task 并呼叫值班。

<span class="label">说法</span> *"The cost was weaker orchestration and observability, so we bought them back with dashboards, alerts, and a one-line kill switch."*

<div class="sources"><b>表达 · business English</b><br>• <b><i>kill switch</i></b> — 一键停止开关<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“A feature flag doubled as a kill switch, so stopping it was one UPDATE, not a deploy.”</span><br>• <b><i>buy back (observability)</i></b> — 把丢掉的能力补回来<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“We bought back observability with Streamlit dashboards and Datadog alerts.”</span><br>• <b><i>blast radius</i></b> — 出问题时的影响范围<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Per-record-type streams kept the blast radius of a bad file to one stage.”</span></div>
