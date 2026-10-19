---
id: nr-amz-s2-full
node: amazon.full
type: qa
step: 2
---
## Q
<p class="title">Quality-check 框架<span class="meta">01 完整故事</span></p>

先在心里把前因后果过一遍，再用英文完整讲一遍。

## A
<span class="label">前因后果</span>

- 背景：团队有几十张对账表，每一张都有自己手写的校验 task，所以每加一张表就要写、评审、发布一个新 task，成本很高。
- 问题：我想让加检查变便宜，并且让 is this data safe to read 变成一个硬条件，而不是 Slack 里的约定。
- 我做了什么：我做了一张配置表，一行就说明哪个 subject area 跑哪个存储过程、SLA 是什么；一个通用 executor 用动态 SQL 调用并写入标准化的 PASS / FAIL / WARNING，exception handler 把崩溃变成 FAIL 行，所以一个坏检查不会拖垮其他检查；全部检查通过后状态行翻成 Completed 并复制到 share 层，下游 JOIN 它。我自己铺开了 8 个 subject area，加检查变成插入一行。
- 结果：之后我在生产规模下发现自己设计的缺陷：就绪判断按表，约 50 个持续失败的商户挡住了 35000 个商户。我没有悄悄修补，而是写了 ADR：四个方案加正确性论证和容量分析，否决 VARIANT（关闭谓词下推）、flatten（单元格大小上限）和新表（新基础设施），选了汇总行加每商户失败行，规则是 strictest wins。当前状态要说准：框架和 8 次铺开已在生产，商户级就绪已设计、评审，并在一个 subject area 验证过，全框架铺开排在 net settlement 之后。
- 为什么这样做 / 学到：粒度是随规模要重新审视的设计参数；修自己的缺陷也应走正式的 ADR；设计任何 gate 之前先问一个检查失败时的 blast radius 是谁。

<span class="label">英文口述（60–90 秒）</span>

Our team had dozens of reconciliation tables, and every new one got its own hand-written validation task. I replaced that with a config-driven quality-check framework. One row in a config table says which stored procedure to run for which subject area, with what SLA. A generic executor builds the call, captures the result, and writes a normalized pass, fail or warning row, and an exception handler means one broken check never takes down the others. When every enabled check passes, a status row flips to Completed and replicates to a share layer where downstream teams JOIN on it. So 'is this data safe to read' went from a Slack convention to a SQL condition. I rolled it out across eight subject areas myself, and adding a check became inserting a row. Then I saw a flaw in my own design: readiness was per table, so roughly fifty bad merchants out of thirty-five thousand blocked everybody. I didn't patch it quietly. I wrote an ADR with four alternatives, a correctness argument, and a volume analysis. The direction is reviewed and proven in one subject area; the broader rollout is sequenced behind the net-settlement work.

<div class="sources"><b>表达 · business English</b><br>• <b><i>config-driven</i></b> — 配置驱动<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I made validation config-driven, so adding a check is inserting a row instead of shipping a task.”</span><br>• <b><i>quality gate</i></b> — 质量gate<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“Downstream teams treat the status row as a quality gate and JOIN on it.”</span><br>• <b><i>own up to a flaw in my own design</i></b> — 主动承认自己设计里的缺陷<br>&nbsp;&nbsp;&nbsp;<span style="opacity:.85">“I owned up to a flaw in my own design and wrote an ADR instead of patching it quietly.”</span></div>
